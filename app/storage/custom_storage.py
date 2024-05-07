from collections import UserList
from aiogram.types.message import Message


class MessageStorage(UserList):
    def __init__(self, iterable):
        super().__init__(item for item in iterable if type(item) in [Message])

    def __setitem__(self, index, item):
        if type(item) in [Message]:
            self.data[index] = item
        else:
            raise TypeError('Item is not an aiogram message')

    def append(self, item):
        if type(item) in [Message]:
            self.data.append(item)
        else:
            raise TypeError('Item is not an aiogram message')

    # def append(self, item):
    #     pass

    async def remove(self, chat_id):
        for item in self:
            if item.chat.id == chat_id:
                self.data.remove(item)
                await item.delete()

    # async def remove(self, chat_id):
    #     pass


msg_storage = MessageStorage([])
