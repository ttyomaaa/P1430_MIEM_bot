from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from enums.texts import *
from keyboards.keyboard_builders import inline_keyboard_maker
from storage.custom_storage import msg_storage


router = Router()


@router.message(Command('chapters'))
async def command_chapters(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()

    await msg_storage.remove(message.chat.id)

    msg = await message.answer(
        text=CHAPTERS_POST,
        reply_markup=inline_keyboard_maker(keyboard_pool=KEYBOARD_CHAPTERS, identity="chapters", mode=1)
    )

    msg_storage.append(msg)


@router.message(Command('start'))
async def command_start(message: Message, state: FSMContext):
    curr_state = await state.get_state()
    if curr_state is not None:
        await state.clear()

    await message.answer(
        text=START_POST,
        reply_markup=None
    )


@router.message(Command('help'))
async def command_help(message: Message):
    await message.answer(
        text=HELP_POST,
        reply_markup=None
    )


@router.message()
async def command_unknown(message: Message):
    await message.answer(
        text=UNKNOWN_COMMAND_POST,
        reply_markup=None
    )
