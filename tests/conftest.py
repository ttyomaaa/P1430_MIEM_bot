import pytest
import pytest_asyncio

from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from tests.mocked_bot import MockedBot

from handlers.coder import router as r1
from handlers.structure import router as r2
from handlers.commands import router as r3


@pytest_asyncio.fixture(scope="session")
async def memory_storage():
    storage = MemoryStorage()
    try:
        yield storage
    finally:
        await storage.close()


@pytest.fixture(scope="session")
def bot():
    return MockedBot()


@pytest_asyncio.fixture(scope="session")
async def dispatcher():
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(r1, r2, r3)
    await dp.emit_startup()
    try:
        yield dp
    finally:
        await dp.emit_shutdown()


