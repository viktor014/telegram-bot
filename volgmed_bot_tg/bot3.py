import asyncio
import logging
import sys
import sqlite3
from os import getenv
from typing import Any, Dict

from config_reader import config

from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.enums import ParseMode
from aiogram.methods import DeleteWebhook
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

from keyboards.keyboards import base_kb
from handlers import conference

TOKEN = getenv("BOT_TOKEN")

form_router = Router()


# Список состояний,которые будем обрабатывать. Ожидание ввода имени, ожидание ввода языка программирования и тд
class Form(StatesGroup):
    menuST = State()
    changeST = State()
    changeST2 = State()
    changeST3 = State()
    # Состояния заполнения конференции
    confST = State()
    name_confST = State()
    date_confST = State()
    location_confST = State()
    price_confST = State()
    description_confST = State()
    pic_confST = State()

@form_router.message(Command("start"))
@form_router.message(CommandStart())
@form_router.message(F.text.casefold() == "меню")
async def command_start(message: Message, state: FSMContext) -> None:
    # await state.set_state(Form.menuST) # Устанавливается состояние меню
    # Подключение к бд и создание таблиц
    conn = sqlite3.connect('new.db')
    cur = conn.cursor()
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Conference (
    id INTEGER PRIMARY KEY,
    id_user_conf INTEGER,
    id_publ_msg INTEGER, 
    name_conf TEXT NOT NULL, 
    date_conf TEXT NOT NULL,
    location_conf TEXT,
    price_conf TEXT,
    description_conf TEXT,
    pic_conf TEXT 
    )
                ''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INTEGER
    )
    ''')
    conn.commit()
    cur.close()
    conn.close()

    await state.clear()
    await message.answer(
        "Выберите действие:",
        reply_markup=base_kb()
    )


# Разрешить подьзователю отменить любое действие
@form_router.message(Command("cancel"))
@form_router.message(F.text.casefold() == "отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Действие отменено. Возврат в главное меню.",
        reply_markup=base_kb(),
    )


async def main():
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)

    dp = Dispatcher()
    dp.include_router(form_router)
    dp.include_router(conference.router)
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
