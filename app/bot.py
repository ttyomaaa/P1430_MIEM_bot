import asyncio
import logging

import handlers.coder
import handlers.commands
import handlers.structure
from config.bot_startup import on_startup, on_shutdown
from config.settings import bot, dp


async def main():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] -  %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_routers(handlers.coder.router, handlers.structure.router, handlers.commands.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
