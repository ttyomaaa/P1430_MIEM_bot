from inspect import signature
import ciphers.cipher
from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from enums.texts import *
from fsm.states import ButtonsStates, PreButtonStates
from keyboards.keyboard_builders import (inline_keyboard_maker, reply_keyboard_maker, inline_keyboard_maker_webapp,
                                         matrix_maker, generate_maker)
from storage.custom_storage import msg_storage

router = Router()


@router.callback_query(F.data == 'back')
async def go_back(callback: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state in ButtonsStates:
        data = await state.get_data()
        chapter_n = data['chapter_n']
        cipher_n = data['cipher_n']

        cipher_code = str(chapter_n) + str(cipher_n)

        await callback.message.delete()

        if cipher_code == CipherData.keccak.number:
            msg = await callback.message.answer(
                text=SCENARIO_POST.format(KEYBOARD_CIPHERS[chapter_n-1][cipher_n-1]),
                reply_markup=inline_keyboard_maker_webapp(KEYBOARD_BUTTONS_keccak, identity="buttons", mode=1,
                                                          cipher_code=cipher_code),
            )
        else:
            msg = await callback.message.answer(
                text=SCENARIO_POST.format(KEYBOARD_CIPHERS[chapter_n-1][cipher_n-1]),
                reply_markup=inline_keyboard_maker_webapp(KEYBOARD_BUTTONS, identity="buttons", mode=1,
                                                          cipher_code=cipher_code),
            )

        msg_storage.append(msg)

        await state.set_state(PreButtonStates.cipher_selected)
    elif current_state in PreButtonStates:
        if current_state == PreButtonStates.chapter_selected:
            if callback.message.text != CHAPTERS_POST:
                await callback.message.edit_text(
                    text=CHAPTERS_POST,
                    reply_markup=inline_keyboard_maker(keyboard_pool=KEYBOARD_CHAPTERS, identity="chapters", mode=1)
                )
            await state.set_state(None)
        elif current_state == PreButtonStates.cipher_selected:
            data = await state.get_data()
            chapter_n = data['chapter_n']
            # await callback.message.delete()
            await msg_storage.remove(callback.message.chat.id)

            msg = await callback.message.answer(
                text=CHAPTER_WELCOME["msg_chapter"].format(str(chapter_n), KEYBOARD_CHAPTERS[chapter_n-1]),
                reply_markup=inline_keyboard_maker(keyboard_pool=KEYBOARD_CIPHERS[chapter_n-1], identity="ciphers", mode=1)
            )

            msg_storage.append(msg)
            await state.set_state(PreButtonStates.chapter_selected)
    else:
        if current_state is not None:
            await state.clear()
        if callback.message.text != START_POST:
            await callback.message.edit_text(
                text=START_POST,
                reply_markup=None
            )


@router.callback_query(F.data.startswith('chapters'))
async def process_chapters(callback: CallbackQuery, state: FSMContext):
    chapter_n = int(callback.data[8:])+1
    if callback.message.text != CHAPTER_WELCOME["msg_chapter"].format(str(chapter_n), KEYBOARD_CHAPTERS[chapter_n-1]):
        await callback.message.edit_text(
            text=CHAPTER_WELCOME["msg_chapter"].format(str(chapter_n), KEYBOARD_CHAPTERS[chapter_n-1]),
            reply_markup=inline_keyboard_maker(keyboard_pool=KEYBOARD_CIPHERS[chapter_n-1], identity="ciphers", mode=1)
        )

    await state.set_state(PreButtonStates.chapter_selected)
    await state.update_data(chapter_n=chapter_n)


@router.callback_query(F.data.startswith('ciphers'), StateFilter(PreButtonStates.chapter_selected))
async def process_ciphers(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chapter_n = data['chapter_n']
    cipher_n = int(callback.data[7:])+1

    cipher_code = str(chapter_n) + str(cipher_n)

    # await callback.message.delete()
    await msg_storage.remove(callback.message.chat.id)

    if cipher_code == CipherData.keccak.number:
        msg = await callback.message.answer(
            text=SCENARIO_POST.format(KEYBOARD_CIPHERS[chapter_n-1][cipher_n-1]),
            reply_markup=inline_keyboard_maker_webapp(KEYBOARD_BUTTONS_keccak, identity="buttons", mode=1,
                                                      cipher_code=cipher_code),
        )
    else:
        msg = await callback.message.answer(
            text=SCENARIO_POST.format(KEYBOARD_CIPHERS[chapter_n-1][cipher_n-1]),
            reply_markup=inline_keyboard_maker_webapp(KEYBOARD_BUTTONS, identity="buttons", mode=1,
                                                      cipher_code=cipher_code),
        )

    msg_storage.append(msg)

    await state.set_state(PreButtonStates.cipher_selected)
    await state.update_data(cipher_n=cipher_n)


@router.callback_query(F.data.startswith('buttons'), StateFilter(PreButtonStates.cipher_selected))
async def process_buttons(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chapter_n = data['chapter_n']
    cipher_n = data['cipher_n']

    button_n = int(callback.data[7:]) + 1
    await state.set_state(getattr(ButtonsStates, "button" + str(button_n)))

    cipher = getattr(ciphers.cipher, "cipher" + str(chapter_n) + str(cipher_n))
    sig = signature(cipher)
    params = len(sig.parameters) - 1
    cipher_code = str(chapter_n) + str(cipher_n)

    await msg_storage.remove(callback.message.chat.id)

    if button_n == ButtonsData.encode:
        # await callback.message.delete()
        await callback.message.answer(
            text=POST_2,
            reply_markup=None
        )

        await callback.message.answer(
            text=ENCODE_POST["msg_encode"].format(text_by_number(cipher_number=cipher_code, text_type='encode_text')),
            reply_markup=reply_keyboard_maker(keyboard_pool=KEYBOARD_BACK,
                                              cipher_code=cipher_code,
                                              mode=ButtonsData.encode - 1)
        )

        if params > 1:
            if cipher_code == CipherData.vizhener.number:
                await callback.message.answer_photo(
                    caption=None,
                    photo=FSInputFile('resourcesdb/media/vizhener_encode.png'),
                    reply_markup=None
                )
            elif cipher_code == CipherData.gronsfeld.number:
                await callback.message.answer_photo(
                    caption=None,
                    photo=FSInputFile('resourcesdb/media/gronsfeld_encode.png'),
                    reply_markup=None
                )
            elif cipher_code == CipherData.vernam.number:
                await callback.message.answer_photo(
                    caption=None,
                    photo=FSInputFile('resourcesdb/media/vernam_encode.png'),
                    reply_markup=None
                )
            elif cipher_code == CipherData.enigma.number:
                await callback.message.answer_photo(
                    caption=None,
                    photo=FSInputFile('resourcesdb/media/enigma_encode.png'),
                    reply_markup=None
                )
            if (cipher_code == CipherData.alberti.number or
                    cipher_code == CipherData.squares.number or
                    cipher_code == CipherData.adfgx.number):
                msg = await callback.message.answer(
                    text=text_by_number(cipher_number=cipher_code, text_type='key_request_encode'),
                    reply_markup=generate_maker()
                )
                await state.update_data(msg=msg)
            else:
                await callback.message.answer(
                    text=text_by_number(cipher_number=cipher_code, text_type='key_request_encode'),
                    reply_markup=None
                )
        else:
            if cipher_code == CipherData.polibiy.number:
                await callback.message.answer_photo(
                    caption=None,
                    photo=FSInputFile('resourcesdb/media/polibiy_encode.png'),
                    reply_markup=None
                )
            elif cipher_code == CipherData.tritemiy.number:
                await callback.message.answer_photo(
                    caption=None,
                    photo=FSInputFile('resourcesdb/media/tritemiy_encode.png'),
                    reply_markup=None
                )
            await callback.message.answer(
                text=text_by_number(cipher_number=cipher_code, text_type='msg_request_encode'),
                reply_markup=None
            )

    elif button_n == ButtonsData.decode:
        # await callback.message.delete()
        await callback.message.answer(
            text=POST_2,
            reply_markup=None
        )

        await callback.message.answer(
            text=DECODE_POST["msg_decode"].format(text_by_number(cipher_number=cipher_code, text_type='decode_text')),
            reply_markup=reply_keyboard_maker(keyboard_pool=KEYBOARD_BACK,
                                              cipher_code=cipher_code,
                                              mode=ButtonsData.decode - 1)
        )

        if params > 1:
            if cipher_code == CipherData.vizhener.number:
                await callback.message.answer_photo(
                    caption=None,
                    photo=FSInputFile('resourcesdb/media/vizhener_encode.png'),
                    reply_markup=None
                )
            elif cipher_code == CipherData.gronsfeld.number:
                await callback.message.answer_photo(
                    caption=None,
                    photo=FSInputFile('resourcesdb/media/gronsfeld_encode.png'),
                    reply_markup=None
                )
            elif cipher_code == CipherData.vernam.number:
                await callback.message.answer_photo(
                    caption=None,
                    photo=FSInputFile('resourcesdb/media/vernam_encode.png'),
                    reply_markup=None
                )
            elif cipher_code == CipherData.enigma.number:
                await callback.message.answer_photo(
                    caption=None,
                    photo=FSInputFile('resourcesdb/media/enigma_decode.png'),
                    reply_markup=None
                )
            if (cipher_code == CipherData.alberti.number or
                    cipher_code == CipherData.squares.number or
                    cipher_code == CipherData.adfgx.number):
                msg = await callback.message.answer(
                    text=text_by_number(cipher_number=cipher_code, text_type='key_request_decode'),
                    reply_markup=generate_maker()
                )
                await state.update_data(msg=msg)
            else:
                await callback.message.answer(
                    text=text_by_number(cipher_number=cipher_code, text_type='key_request_decode'),
                    reply_markup=None
                )
        else:
            if cipher_code == CipherData.polibiy.number:
                msg = await callback.message.answer(
                    text=text_by_number(cipher_number=cipher_code, text_type='msg_request_decode'),
                    reply_markup=matrix_maker()
                )
                await state.update_data(msg=msg)
            else:
                await callback.message.answer(
                    text=text_by_number(cipher_number=cipher_code, text_type='msg_request_decode'),
                    reply_markup=None
                )
