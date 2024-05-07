import pytest
from unittest.mock import AsyncMock, ANY
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.types import CallbackQuery, User
from app.handlers.coder import process_encode_decode, process_matrix, process_end
import re

TEMPLATE_USER = User(first_name="test", id=123, is_bot=False)


def create_test_state(memory_storage, bot, cipher_number):
    key = StorageKey(bot_id=bot.id, chat_id=42, user_id=42)
    storage = memory_storage
    state = FSMContext(storage=storage, key=key)
    ctx = storage.storage[key]
    if ctx.state != "ButtonsStates:button1":
        data = {'chapter_n': int(cipher_number[0]), 'cipher_n': int(cipher_number[1])}
        ctx.data = data
        ctx.state = "ButtonsStates:button1"
    elif ctx.state != "ButtonsStates:button2":
        ctx.state = "ButtonsStates:button2"

    return state


@pytest.mark.asyncio
async def test_handlers_14(memory_storage, bot):
    cipher_number = "14"

    init_text = "аляля всем привет"

    state = create_test_state(memory_storage, bot, cipher_number)

    message = AsyncMock(text=init_text)
    await process_encode_decode(message=message, state=state)
    new_text = message.mock_calls[0][2]['text']

    result = []
    for i in new_text.split(' '):
        result.extend(re.findall('\(\d+,\d+\)', i))
        result.append(' ')
    result.pop()

    result = ['bn' + i for i in result]
    state = create_test_state(memory_storage, bot, cipher_number)

    message = AsyncMock(text=new_text)
    await state.update_data(msg=message)
    for i in result:
        await process_matrix(callback=CallbackQuery(data=i, id="test", from_user=TEMPLATE_USER, chat_instance="test"), state=state)
    await process_end(callback=CallbackQuery(data="end", id="test", from_user=TEMPLATE_USER, chat_instance="test"), state=state)

    message.answer.assert_any_call(text=init_text, reply_markup=ANY)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "cipher_number, key_text, key2_text, init_text, special_case",
    [
        ["11", None, None, "аляля всем привет", None],
        ["12", "9", None, "аляля всем привет", None],
        ["13", "14", None, "аляля всем привет", None],
        ["21", "1 4 2 3", None, "Привет всем", None],
        ["22", "Один за всех", None, "Привет всем", None],
        ["23", "абвгдеёжзийклмнопрстуфхцчшщъыьэюя", "И Б Г 5", "Коллаборация", getattr(str, "lower")],
        ["24", "а.бвгдезжиклмн,опрстуф:хцчшщъы_ьэяю", "ьэюяшщъ,ыфхцч_рст.умнопи:клежзабвгд", "Надо подумать ля ля", getattr(str, "upper")],
        ["31", None, None, "А что у нас на обед??", getattr(str, "lower")],
        ["32", "Колбаса", None, "Бутерброд с колбасой", getattr(str, "lower")],
        ["33", "1864", None, "Блинчик с бананом", getattr(str, "lower")],
        ["34", "Ваза с цветами", None, "крестики-нолики", None],
        ["41", "abcdefghijklmnopqrstuvwxyz0123456789", "weekend", "We need 1 year", getattr(str, "lower")],
        ["43", "Патроонаж", None, "Беспредел", getattr(str, "lower")],
        ["51", "лох", None, "Смешарики", None],
        ["52", "abdedf", None, "nanana", None],
    ]
)
async def test_handlers_uni(memory_storage, bot, cipher_number, key_text, key2_text, init_text, special_case):
    state = create_test_state(memory_storage, bot, cipher_number)

    if key_text:
        message = AsyncMock(text=key_text)
        await process_encode_decode(message=message, state=state)
        if key2_text:
            message = AsyncMock(text=key2_text)
            await process_encode_decode(message=message, state=state)
    message = AsyncMock(text=init_text)
    await process_encode_decode(message=message, state=state)

    new_text = message.mock_calls[0][2]['text']
    state = create_test_state(memory_storage, bot, cipher_number)

    if key_text:
        message = AsyncMock(text=key_text)
        await process_encode_decode(message=message, state=state)
        if key2_text and cipher_number != "23":
            message = AsyncMock(text=key2_text)
            await process_encode_decode(message=message, state=state)

    message = AsyncMock(text=new_text)
    await process_encode_decode(message=message, state=state)

    if special_case:
        if cipher_number == "41":
            message.answer.assert_any_call(text=special_case(init_text).replace(" ", ""), reply_markup=ANY)
        else:
            message.answer.assert_any_call(text=special_case(init_text), reply_markup=ANY)
    else:
        message.answer.assert_any_call(text=init_text, reply_markup=ANY)
