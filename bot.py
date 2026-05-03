from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup, WebAppInfo

from app.config import get_settings


settings = get_settings()


def build_main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="Открыть reader",
                    web_app=WebAppInfo(url=settings.telegram_webapp_url),
                )
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Открой мини-приложение и продолжи чтение",
    )


async def handle_start(message: Message) -> None:
    await message.answer(
        "Привет. Я помогу возвращаться к книге маленькими спокойными сессиями.",
        reply_markup=build_main_keyboard(),
    )


async def handle_web_app_data(message: Message) -> None:
    await message.answer("Данные из Mini App получены. Можно продолжать чтение.")


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
