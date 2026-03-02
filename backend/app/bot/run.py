"""
Minimal Telegram bot entrypoint.
- /start: send WebApp button "Open Seafarer App".
- URL from env MINI_APP_URL.

Run from backend dir:
  python -m app.bot.run
"""
import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, WebAppInfo, KeyboardButton, ReplyKeyboardMarkup
from aiogram.enums import ParseMode

from app.core.settings import settings

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger("seafarer.bot")

bot = Bot(token=settings.BOT_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()


def get_webapp_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="Open Seafarer App",
                    web_app=WebAppInfo(url=settings.MINI_APP_URL),
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False,
    )


@dp.message(F.text == "/start")
async def cmd_start(message: Message) -> None:
    try:
        await message.answer(
            "Welcome to Seafarer App. Tap the button below to open the app.",
            reply_markup=get_webapp_keyboard(),
        )
        logger.info("start from user_id=%s", message.from_user and message.from_user.id)
    except Exception as e:
        logger.exception("start failed: %s", e)
        await message.answer("Something went wrong. Try again later.")


async def main() -> None:
    try:
        logger.info("Bot starting...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception("Bot error: %s", e)
        raise
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
