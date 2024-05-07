from inspect import signature
import ciphers.cipher
import filters.validators
from aiogram import Router, F
from aiogram.filters import StateFilter, or_f, ExceptionMessageFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.types.error_event import ErrorEvent
from enums.texts import *
from fsm.states import ButtonsStates
from handlers.structure import go_back
from keyboards.keyboard_builders import reply_keyboard_maker, inline_keyboard_maker, matrix_maker, generate_maker
from storage.custom_storage import msg_storage

router = Router()


@router.error(ExceptionMessageFilter(ERROR_MSG), F.update.message.as_("message"))
async def handle_msg_too_long(event: ErrorEvent, message: Message, state: FSMContext):
    data = await state.get_data()
    current_state = await state.get_state()

    cipher_n = data['cipher_n']
    chapter_n = data['chapter_n']
    cipher_code = str(chapter_n) + str(cipher_n)

    if current_state == ButtonsStates.button1:
        mode = 0
    else:
        mode = 1

    await message.answer(
        text=ERROR_RESPONSE,
        reply_markup=reply_keyboard_maker(KEYBOARD_BACK, cipher_code=cipher_code, mode=mode)
    )


async def reset_flag(state, current_state, cipher_n, chapter_n):
    await state.clear()
    await state.set_state(current_state)
    await state.update_data(cipher_n=cipher_n)
    await state.update_data(chapter_n=chapter_n)


@router.message(or_f(StateFilter(ButtonsStates.button1), StateFilter(ButtonsStates.button2)))
async def process_encode_decode(message: Message, state: FSMContext):
    data = await state.get_data()
    current_state = await state.get_state()
    cipher_n = data['cipher_n']
    chapter_n = data['chapter_n']
    cipher_code = str(chapter_n) + str(cipher_n)
    cipher_obj = object_by_number(cipher_code)

    if current_state == ButtonsStates.button1:
        mode = 0
    else:
        mode = 1
    if message.text == "Назад":
        if (cipher_code == CipherData.alberti.number or
                cipher_code == CipherData.squares.number or
                cipher_code == CipherData.adfgx.number):
            await data["msg"].delete()
        if cipher_code == CipherData.polibiy.number and current_state == ButtonsStates.button2:
            await data["msg"].delete()

        await message.delete()

        await reset_flag(state, current_state, cipher_n, chapter_n)

        msg = await message.answer(
            text=GOING_BACK,
            reply_markup=ReplyKeyboardRemove()
        )
        await msg.delete()
        msg = await message.answer(
            text=GOING_BACK,
            reply_markup=None
        )
        await go_back(CallbackQuery(id="back", message=msg, from_user=message.from_user, chat_instance="None"), state)
    elif message.text == "Выбор раздела":
        if (cipher_code == CipherData.alberti.number or
            cipher_code == CipherData.squares.number or
                cipher_code == CipherData.adfgx.number):
            await data["msg"].delete()

        if cipher_code == CipherData.polibiy.number and current_state == ButtonsStates.button2:
            await data["msg"].delete()
        await message.delete()

        await state.clear()

        msg = await message.answer(
            text=GOING_BACK,
            reply_markup=ReplyKeyboardRemove()
        )
        await msg.delete()
        msg = await message.answer(
            text=CHAPTERS_POST,
            reply_markup=inline_keyboard_maker(keyboard_pool=KEYBOARD_CHAPTERS, identity="chapters", mode=1)
        )
        msg_storage.append(msg)
    else:
        cipher = getattr(ciphers.cipher, "cipher"+str(chapter_n)+str(cipher_n))

        sig = signature(cipher)
        params = len(sig.parameters) - 1
        if params > 1:
            valid = getattr(filters.validators, "key_validation" + str(chapter_n) + str(cipher_n))
        if params > 2:
            valid2 = getattr(filters.validators, "key_validation" + str(chapter_n) + str(cipher_n) + "_2")

        try:
            int(data["flag"])
        except KeyError:
            try:
                key = data["key"]
            except KeyError:
                key = 0
        else:
            key = data["key"]

        try:
            int(data["flag2"])
        except KeyError:
            try:
                key2 = data["key2"]
            except KeyError:
                key2 = 0
        else:
            key2 = data["key2"]

        if (params > 1) & (key == 0):
            if ((cipher_code == CipherData.alberti.number or
                 cipher_code == CipherData.squares.number or
                 cipher_code == CipherData.adfgx.number) and
                    message.from_user.is_bot):
                if data['input_seq'] == WarningsData.no_text_and_callback:
                    returned_text = WarningsData.no_text_and_callback
                    await message.answer(
                        text=returned_text,
                        reply_markup=reply_keyboard_maker(KEYBOARD_BACK, cipher_code=cipher_code, mode=mode)
                    )
                    msg = await message.answer(
                        text=message.text,
                        reply_markup=message.reply_markup
                    )
                    await state.update_data(msg=msg)
                    await message.delete()
                    return
                else:
                    key_text = data['input_seq']
            else:
                key_text = message.text
            try:
                if cipher_code == CipherData.enigma.number:
                    valid(key_text, mode)
                else:
                    valid(key_text)
            except ValueError:
                returned_text = cipher_obj.key_error_encode
                await message.answer(
                    text=returned_text,
                    reply_markup=reply_keyboard_maker(KEYBOARD_BACK, cipher_code=cipher_code, mode=mode)
                )
                if (cipher_code == CipherData.alberti.number or
                    cipher_code == CipherData.squares.number or
                        cipher_code == CipherData.adfgx.number):
                    await data["msg"].delete()
                    msg = await message.answer(
                        text=data["msg"].text,
                        reply_markup=data["msg"].reply_markup
                    )
                    await state.update_data(msg=msg)
                return
            else:
                if (cipher_code == CipherData.alberti.number or
                    cipher_code == CipherData.squares.number or
                        cipher_code == CipherData.adfgx.number):
                    if not message.from_user.is_bot:
                        await data["msg"].delete_reply_markup()
            if current_state == ButtonsStates.button1:
                if params > 2:
                    if cipher_code == CipherData.squares.number:
                        msg = await message.answer(
                            text=cipher_obj.key2_request_encode,
                            reply_markup=generate_maker()
                        )
                        await state.update_data(msg=msg)
                        await state.update_data(input_seq=WarningsData.no_text_and_callback)
                    else:
                        await message.answer(
                            text=cipher_obj.key2_request_encode,
                            reply_markup=reply_keyboard_maker(KEYBOARD_BACK, cipher_code=cipher_code, mode=mode)
                        )
                else:
                    await message.answer(
                        text=cipher_obj.msg_request_encode,
                        reply_markup=reply_keyboard_maker(KEYBOARD_BACK, cipher_code=cipher_code, mode=mode)
                    )
            else:
                if params > 2 and cipher_code != CipherData.alberti.number:
                    if cipher_code == CipherData.squares.number:
                        msg = await message.answer(
                            text=cipher_obj.key2_request_decode,
                            reply_markup=generate_maker()
                        )
                        await state.update_data(msg=msg)
                        await state.update_data(input_seq=WarningsData.no_text_and_callback)
                    else:
                        await message.answer(
                            text=cipher_obj.key2_request_decode,
                            reply_markup=reply_keyboard_maker(KEYBOARD_BACK, cipher_code=cipher_code, mode=mode)
                        )
                else:
                    await message.answer(
                        text=cipher_obj.msg_request_decode,
                        reply_markup=reply_keyboard_maker(KEYBOARD_BACK, cipher_code=cipher_code, mode=mode)
                    )
            if cipher_obj.key_type == "int":
                await state.update_data(key=int(key_text))
            else:
                await state.update_data(key=key_text)
            return
        if (params > 2) & (key != 0) & (key2 == 0):
            if not (current_state == ButtonsStates.button2 and
                    cipher_code == CipherData.alberti.number):
                await state.update_data(flag="1")
                await state.update_data(key=key)

                if cipher_code == CipherData.squares.number and message.from_user.is_bot:
                    if data['input_seq'] == WarningsData.no_text_and_callback:
                        returned_text = WarningsData.no_text_and_callback
                        await message.answer(
                            text=returned_text,
                            reply_markup=reply_keyboard_maker(KEYBOARD_BACK, cipher_code=cipher_code, mode=mode)
                        )
                        msg = await message.answer(
                            text=message.text,
                            reply_markup=message.reply_markup
                        )
                        await state.update_data(msg=msg)
                        await message.delete()
                        return
                    else:
                        key2_text = data['input_seq']
                else:
                    key2_text = message.text
                try:
                    valid2(key2_text)
                except ValueError:
                    returned_text = cipher_obj.key2_error_encode
                    await message.answer(
                        text=returned_text,
                        reply_markup=reply_keyboard_maker(KEYBOARD_BACK, cipher_code=cipher_code, mode=mode)
                    )
                    if cipher_code == CipherData.squares.number:
                        await data["msg"].delete()
                        msg = await message.answer(
                            text=data["msg"].text,
                            reply_markup=data["msg"].reply_markup
                        )
                        await state.update_data(msg=msg)
                    return
                else:
                    if cipher_code == CipherData.squares.number:
                        if not message.from_user.is_bot:
                            await data["msg"].delete_reply_markup()
                if current_state == ButtonsStates.button1:
                    await message.answer(
                        text=cipher_obj.msg_request_encode,
                        reply_markup=reply_keyboard_maker(KEYBOARD_BACK, cipher_code=cipher_code, mode=mode)
                    )
                elif current_state == ButtonsStates.button2:
                    await message.answer(
                        text=cipher_obj.msg_request_decode,
                        reply_markup=reply_keyboard_maker(KEYBOARD_BACK, cipher_code=cipher_code, mode=mode)
                    )
                await state.update_data(key2=key2_text)
                return
        if current_state == ButtonsStates.button1:  # encode
            if params <= 1:
                try:
                    returned_text = cipher(message.text, 0)
                except ValueError:
                    returned_text = cipher_obj.msg_error_encode
                    await message.answer(
                        text=returned_text,
                        reply_markup=reply_keyboard_maker(KEYBOARD_BACK, cipher_code=cipher_code, mode=mode)
                    )
                    return
            elif params > 2:
                try:
                    returned_text = cipher(message.text, key, 0, key2)
                except ValueError:
                    returned_text = cipher_obj.msg_error_encode
                    await state.update_data(flag2="1")
                    await state.update_data(key=key)
                    await state.update_data(key2=key2)
                else:
                    await reset_flag(state, current_state, cipher_n, chapter_n)
            elif params == 2:
                try:
                    returned_text = cipher(message.text, key, 0)
                except ValueError:
                    returned_text = cipher_obj.msg_error_encode
                    await state.update_data(flag="1")
                    await state.update_data(key=key)
                except KeyError:
                    returned_text = cipher_obj.msg_error_encode_2
                    await state.update_data(flag="1")
                    await state.update_data(key=key)
                else:
                    await reset_flag(state, current_state, cipher_n, chapter_n)
            else:
                returned_text = cipher(message.text, 0)
        else:  # decode
            if params <= 1:
                if cipher_code == CipherData.polibiy.number:
                    await message.delete()
                    if not message.from_user.is_bot:
                        return
                    try:
                        data['input_seq']
                    except KeyError:
                        returned_text = WarningsData.no_text
                    else:
                        if data['input_seq'] == WarningsData.no_text:
                            returned_text = WarningsData.no_text
                        else:
                            returned_text = cipher(data['input_seq'], 1)
                else:
                    try:
                        returned_text = cipher(message.text, 1)
                    except ValueError:
                        returned_text = cipher_obj.msg_error_decode
                        await message.answer(
                            text=returned_text,
                            reply_markup=reply_keyboard_maker(KEYBOARD_BACK, cipher_code=cipher_code, mode=mode)
                        )
                        return
            elif params > 2 and cipher_code != CipherData.alberti.number:
                try:
                    returned_text = cipher(message.text, key, 1, key2)
                except ValueError:
                    returned_text = WarningsData.try_again
                    await state.update_data(flag2="1")
                    await state.update_data(key=key)
                    await state.update_data(key2=key2)
                else:
                    await reset_flag(state, current_state, cipher_n, chapter_n)
            elif params == 2 or cipher_code == CipherData.alberti.number:
                try:
                    returned_text = cipher(message.text, key, 1)
                except ValueError:
                    returned_text = cipher_obj.msg_error_decode
                    await state.update_data(flag="1")
                    await state.update_data(key=key)
                except KeyError:
                    if (cipher_code == CipherData.column.number or
                            cipher_code == CipherData.des.number):
                        returned_text = cipher_obj.msg_error_decode_2
                    await state.update_data(flag="1")
                    await state.update_data(key=key)
                else:
                    await reset_flag(state, current_state, cipher_n, chapter_n)
            else:
                returned_text = cipher(message.text, 1)
        if returned_text.isspace():
            returned_text = WarningsData.no_text
        await message.answer(
            text=returned_text,
            reply_markup=reply_keyboard_maker(KEYBOARD_BACK, cipher_code=cipher_code, mode=mode)
        )
        if current_state == ButtonsStates.button1:
            if (cipher_code == CipherData.atbash.number or
                cipher_code == CipherData.polibiy.number or
                cipher_code == CipherData.tritemiy.number or
                    cipher_code == CipherData.keccak.number):
                await message.answer(
                    text=cipher_obj.msg_request_encode,
                    reply_markup=reply_keyboard_maker(KEYBOARD_BACK, cipher_code=cipher_code, mode=mode)
                )
            else:
                data = await state.get_data()
                try:
                    int(data["flag"])
                except KeyError:
                    if (cipher_code == CipherData.alberti.number or
                            cipher_code == CipherData.squares.number or
                            cipher_code == CipherData.adfgx.number):
                        msg = await message.answer(
                            text=cipher_obj.key_request_encode,
                            reply_markup=generate_maker()
                        )
                        await state.update_data(msg=msg)
                    else:
                        await message.answer(
                            text=cipher_obj.key_request_encode,
                            reply_markup=reply_keyboard_maker(KEYBOARD_BACK, cipher_code=cipher_code, mode=mode)
                        )
        elif current_state == ButtonsStates.button2:
            if cipher_code == CipherData.atbash.number or cipher_code == CipherData.tritemiy.number:
                await message.answer(
                    text=cipher_obj.msg_request_decode,
                    reply_markup=reply_keyboard_maker(KEYBOARD_BACK, cipher_code=cipher_code, mode=mode)
                )
            elif cipher_code == CipherData.polibiy.number:
                await reset_flag(state, current_state, cipher_n, chapter_n)
                msg = await message.answer(
                    text=cipher_obj.msg_request_decode,
                    reply_markup=matrix_maker()
                )
                await state.update_data(msg=msg)
            else:
                data = await state.get_data()
                try:
                    int(data["flag"])
                except KeyError:
                    if (cipher_code == CipherData.alberti.number or
                            cipher_code == CipherData.squares.number or
                            cipher_code == CipherData.adfgx.number):
                        msg = await message.answer(
                            text=cipher_obj.key_request_decode,
                            reply_markup=generate_maker()
                        )
                        await state.update_data(msg=msg)
                    else:
                        await message.answer(
                            text=cipher_obj.key_request_decode,
                            reply_markup=reply_keyboard_maker(KEYBOARD_BACK, cipher_code=cipher_code, mode=mode)
                        )


@router.callback_query(StateFilter(ButtonsStates.button2), F.data.startswith('bn'))
async def process_matrix(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chapter_n = data['chapter_n']
    cipher_n = data['cipher_n']
    cipher_code = str(chapter_n) + str(cipher_n)

    if cipher_code == CipherData.polibiy.number:
        try:
            input_seq = data["input_seq"]
        except KeyError:
            input_seq = ''
        input_seq_upd = input_seq+callback.data[2:]
        await state.update_data(input_seq=input_seq_upd)
        await data["msg"].edit_text(
            text=USE_KEYBOARD+f"\n{input_seq_upd}|",
            reply_markup=matrix_maker()
        )


@router.callback_query(StateFilter(ButtonsStates.button2), F.data.startswith('end'))
async def process_end(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chapter_n = data['chapter_n']
    cipher_n = data['cipher_n']
    cipher_code = str(chapter_n) + str(cipher_n)

    if cipher_code == CipherData.polibiy.number:
        try:
            input_seq = data["input_seq"]
        except KeyError:
            input_seq = WarningsData.no_text
        else:
            if input_seq.isspace():
                input_seq = WarningsData.no_text
        await state.update_data(input_seq=input_seq)
        msg = data["msg"]
        await process_encode_decode(message=msg, state=state)


@router.callback_query(or_f(StateFilter(ButtonsStates.button1), StateFilter(ButtonsStates.button2)), or_f(F.data.startswith('gen'), F.data.startswith('yes')))
async def process_generate(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chapter_n = data['chapter_n']
    cipher_n = data['cipher_n']
    cipher_code = str(chapter_n) + str(cipher_n)
    if (cipher_code == CipherData.alberti.number or
            cipher_code == CipherData.squares.number or
            cipher_code == CipherData.adfgx.number):
        current_state = await state.get_state()

        try:
            int(data["flag"])
        except KeyError:
            is_key_2 = False
        else:
            is_key_2 = True

        if current_state == ButtonsStates.button1:
            if is_key_2:
                text_type = 'key2_request_encode'
            else:
                text_type = 'key_request_encode'
        else:
            if is_key_2:
                text_type = 'key2_request_decode'
            else:
                text_type = 'key_request_decode'

        if callback.data == "gen":
            input_seq = generator(cipher_code)
            await state.update_data(input_seq=input_seq)
            msg = await data["msg"].edit_text(
                text=text_by_number(cipher_number=cipher_code, text_type=text_type)+"\n"+input_seq,
                reply_markup=generate_maker()
            )
            await state.update_data(msg=msg)
        elif callback.data == "yes":
            try:
                input_seq = data["input_seq"]
            except KeyError:
                input_seq = WarningsData.no_text_and_callback
            await state.update_data(input_seq=input_seq)
            msg = data["msg"]
            await msg.delete_reply_markup()
            await process_encode_decode(message=msg, state=state)


def generator(cipher_code: str) -> str:
    import random
    if cipher_code == "23":
        alpha = list("абвгдеёжзийклмнопрстуфхцчшщъыьэюя")
    elif cipher_code == "24":
        alpha = list("абвгдезжиклмнопрстуфхцчшщъыьэяю.,:_")
    elif cipher_code == "41":
        alpha = list("abcdefghijklmnopqrstuvwxyz0123456789")
    random.shuffle(alpha)
    res = ''.join(alpha)
    return res
