from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardRemove, WebAppInfo

from app.config import get_settings
from app.services.books import UNCAT_TELEGRAM_ID


settings = get_settings()


def build_main_keyboard(is_admin: bool = False) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text="Магія ТГШ",
                web_app=WebAppInfo(url=settings.telegram_webapp_url),
            )
        ]
    ]
    if is_admin:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text="Uncat dashboard",
                    web_app=WebAppInfo(url=_admin_webapp_url()),
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


async def handle_start(message: Message) -> None:
    is_admin = str(message.from_user.id) == UNCAT_TELEGRAM_ID if message.from_user else False
    await message.answer("Оновлюю кнопки Mini App.", reply_markup=ReplyKeyboardRemove())
    await message.answer(
        "Привіт. Я допоможу повернутися до книги маленькими спокіними сесіями.",
        reply_markup=build_main_keyboard(is_admin=is_admin),
    )


async def handle_web_app_data(message: Message) -> None:
    await message.answer("Дані з Mini App отримано. Можна продовжувати читання.")


def _admin_webapp_url() -> str:
    return settings.telegram_webapp_url.rstrip("/") + "/admin/"


async def main() -> None:
    if not settings.telegram_bot_token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is required to run the bot")

    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=settings.telegram_bot_token)
    dispatcher = Dispatcher()
    dispatcher.message.register(handle_start, CommandStart())
    dispatcher.message.register(handle_web_app_data, F.web_app_data)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
