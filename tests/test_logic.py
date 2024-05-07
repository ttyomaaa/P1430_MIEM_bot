import pytest
from aiogram.methods import SendMessage, EditMessageText, EditMessageReplyMarkup, AnswerCallbackQuery, DeleteMessage
from aiogram.methods.base import TelegramType
from aiogram.types import Message, Update, User, Chat, CallbackQuery
from aiogram.enums import ChatType
from datetime import datetime
from aiogram.fsm.context import FSMContext
from aiogram.dispatcher.event.bases import UNHANDLED
from treelib import Node, Tree

TEMPLATE_USER = User(first_name="test", id=123, is_bot=False)
TEMPLATE_CHAT = Chat(id=1234, type=ChatType.PRIVATE)
TEMPLATE_BOT = User(first_name="bot", id=321, is_bot=True)


tree = Tree()


@pytest.mark.skip(reason="not ready")
@pytest.mark.asyncio
async def test_logic(bot, dispatcher):

    fsm_context: FSMContext = dispatcher.fsm.get_context(bot=bot, user_id=TEMPLATE_USER.id, chat_id=TEMPLATE_CHAT.id)
    await fsm_context.set_state(None)

    message = make_message("/chapters", sender=TEMPLATE_USER)
    bot.add_result_for(SendMessage, ok=True)
    await dispatcher.feed_update(bot, Update(message=message, update_id=1))
    outgoing_message: TelegramType = bot.get_request()

    tree.create_node("/chapters", "root")

    await map_maker(outgoing_message, bot, dispatcher, "root")


def make_message(text: str, sender: User) -> Message:

    message = Message(
        message_id=sender.id,
        from_user=sender,
        chat=TEMPLATE_CHAT,
        date=datetime.now(),
        text=text
    )
    return message


async def map_maker(seed_message, bot, dispatcher, parent: str):
    print(tree)
    try:
        seed_message.reply_markup.inline_keyboard
    except AttributeError:
        bot.add_result_for(SendMessage, ok=True, result=make_message(text="test", sender=TEMPLATE_BOT))
        await dispatcher.feed_update(bot, Update(message=make_message(text="Назад", sender=TEMPLATE_USER), update_id=1))
        outgoing_message: TelegramType = bot.get_request()
        print(outgoing_message)
        return

    for i in seed_message.reply_markup.inline_keyboard:
        key = i[0].callback_data
        if str(key) == "back" or key is None:
            continue

        tree.create_node(key, parent+key, parent=parent)

        callback = CallbackQuery(message=make_message(text="test", sender=TEMPLATE_BOT), data=key, id="test", from_user=TEMPLATE_USER, chat_instance="test")

        try:
            bot.add_result_for(EditMessageText, ok=True)
            await dispatcher.feed_update(bot, Update(callback_query=callback, update_id=1))
            outgoing_message: TelegramType = bot.get_request()
            await map_maker(outgoing_message, bot, dispatcher, parent + key)
        except IndexError:
            bot.add_result_for(DeleteMessage, ok=True)
            bot.add_result_for(SendMessage, ok=True)
            await dispatcher.feed_update(bot, Update(callback_query=callback, update_id=1))
            await dispatcher.feed_update(bot, Update(callback_query=callback, update_id=1))
            outgoing_message: TelegramType = bot.get_request()
            await map_maker(outgoing_message, bot, dispatcher, parent + key)


