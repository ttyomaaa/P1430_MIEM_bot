import pytest
from aiogram.methods import (
    SendMessage
)
from app.handlers.coder import reset_flag
from aiogram.types import Message, Update, User, Chat
from aiogram.enums import ChatType
from datetime import datetime
from aiogram.fsm.context import FSMContext
from aiogram.dispatcher.event.bases import UNHANDLED
from fsm.states import ButtonsStates
from random import randrange, choice
import string

TEMPLATE_USER = User(first_name="test", id=123, is_bot=False)
TEMPLATE_CHAT = Chat(id=1234, type=ChatType.PRIVATE)
TEMPLATE_BOT = User(first_name="bot", id=321, is_bot=True)


def make_random_messages(length: int, sender: User) -> list[list[Message]]:
    cyrillic = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
    configs = [
        string.ascii_letters,
        string.ascii_letters + string.digits,
        string.ascii_letters + " ",
        string.ascii_letters + string.digits + string.punctuation + " ",
        cyrillic,
        cyrillic + string.digits,
        cyrillic + " ",
        cyrillic + string.punctuation,
        cyrillic + string.punctuation + " " + string.digits,
        string.digits,
        string.digits + " ",
        string.digits + string.punctuation,
        string.punctuation,
        string.punctuation + " ",
        cyrillic + string.ascii_letters,
        cyrillic + string.ascii_letters + string.punctuation + " " + string.digits

    ]
    message_array = [[] for _ in range(len(configs))]
    for idx, config in enumerate(configs):
        for offset in range(32):
            text = ''.join(choice(config) for _ in range(randrange(start=1, stop=length)))
            message = Message(
                message_id=sender.id+offset,
                from_user=sender,
                chat=TEMPLATE_CHAT,
                date=datetime.now(),
                text=text
            )
            message_array[idx].append(message)

    return message_array


@pytest.mark.parametrize(
    "cipher_number",
    [
        "11",
        "12",
        "13",
        "21",
        "22",
        "23",
        "24",
        "31",
        "32",
        "33",
        "34",
        "41",
        "43",
        "51",
        "52",
    ]
)
@pytest.mark.asyncio
async def test_errors(bot, dispatcher, cipher_number):
    cipher_n = int(cipher_number[1])
    chapter_n = int(cipher_number[0])
    states = ButtonsStates
    for state in states:
        fsm_context: FSMContext = dispatcher.fsm.get_context(bot=bot, user_id=TEMPLATE_USER.id, chat_id=TEMPLATE_CHAT.id)
        await fsm_context.set_state(state)
        await fsm_context.update_data(chapter_n=chapter_n, cipher_n=cipher_n)

        messages = make_random_messages(length=128, sender=TEMPLATE_USER)

        for message_block in messages:
            for message in message_block:
                bot.add_result_for(SendMessage, ok=True)
                bot.add_result_for(SendMessage, ok=True)
                result = await dispatcher.feed_update(bot, Update(message=message, update_id=1))
                assert result is not UNHANDLED
                bot.get_request()
            await reset_flag(fsm_context, state, cipher_n, chapter_n)
