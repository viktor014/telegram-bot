from aiogram import Router, F, Bot
from config_reader import config
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.keyboards import base_kb, conf_kb
from bot3 import Form
from typing import Any, Dict
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
import sqlite3

router = Router()
bot = Bot(token=config.bot_token.get_secret_value(), parse_mode=ParseMode.HTML)


@router.message(F.text == "🧬 Конференции")
@router.message(F.text.casefold() == "конференции")
async def process_conference(message: Message, state: FSMContext) -> None:
    # await state.set_state(Form.confST)
    await message.answer(
        "Выберите действие:",
        reply_markup=conf_kb()
    )


@router.message(F.text.casefold() == "просмотр конференций")
async def read_conference(message: Message, state: FSMContext) -> None:
    await state.clear()
    conn = sqlite3.connect('new.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM conference')
    a = cur.fetchall()
    info = ''
    for i in a:
        info += f'\nНазвание конференции: {i[2]}\n' \
                f'Даты конференции: {i[3]}\n' \
                f'Место проведения конференции: {i[4]}\n' \
                f'Стоимость участия в конференции: {i[5]}\n' \
                f'Описание конференции: {i[6]}\n' \
                f'Изображение конференции: {i[7]}\n\n'
    cur.close()
    conn.close()
    await message.answer(info, reply_markup=base_kb())


@router.message(F.text.casefold() == "добавить конференцию")
async def add_conference(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.name_confST)
    await message.answer(
        "Укажите название конференции",
        reply_markup=ReplyKeyboardRemove(),
    )


@router.message(Form.name_confST)
async def process_conf_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name_conf=message.text)
    await state.set_state(Form.date_confST)
    await message.answer('Укажите даты проведения конференции: ',
                         reply_markup=ReplyKeyboardRemove(),
                         )


@router.message(Form.date_confST)
async def process_conf_date(message: Message, state: FSMContext) -> None:
    await state.update_data(date_conf=message.text)
    await state.set_state(Form.location_confST)
    await message.answer('Укажите место проведения конференции: ',
                         reply_markup=ReplyKeyboardRemove(),
                         )


@router.message(Form.location_confST)
async def process_conf_location(message: Message, state: FSMContext) -> None:
    await state.update_data(location_conf=message.text)
    await state.set_state(Form.price_confST)
    await message.answer('Укажите стоимость участия в конференции: ',
                         reply_markup=ReplyKeyboardRemove(),
                         )


@router.message(Form.price_confST)
async def process_conf_price(message: Message, state: FSMContext) -> None:
    await state.update_data(price_conf=message.text)
    await state.set_state(Form.description_confST)
    await message.answer('Добавьте краткое описание конференции: ',
                         reply_markup=ReplyKeyboardRemove(),
                         )


@router.message(Form.description_confST)
async def process_conf_descriprion(message: Message, state: FSMContext) -> None:
    await state.update_data(description_conf=message.text)
    await state.update_data(id_user=message.from_user.id)
    await state.set_state(Form.pic_confST)
    await message.answer('Загрузите изображение для конференции( пока что только ссылкой): ',
                         reply_markup=ReplyKeyboardRemove(),
                         )


@router.message(Form.pic_confST)
async def process_conf_pic(message: Message, state: FSMContext) -> None:
    data = await state.update_data(pic_conf=message.text)
    await process_publ(message=message, data=data)


async def process_publ(message: Message, data: Dict[str, Any]) -> None:
    builder = InlineKeyboardBuilder()
    builder.button(text='Отправить', callback_data='send_conf')
    await message.answer(f'\nНазвание конференции: {data["name_conf"]}\n' \
                         f'Даты конференции: {data["date_conf"]}\n' \
                         f'Место проведения конференции: {data["location_conf"]}\n' \
                         f'Стоимость участия в конференции: {data["price_conf"]}\n' \
                         f'Описание конференции: {data["description_conf"]}\n' \
                         f'Изображение конференции: {data["pic_conf"]}\n\n',
                         reply_markup=builder.as_markup()
                         )


@router.callback_query(F.data == "send_conf")
async def send_conf(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await add_bd_conf(data=data)
    await bot.send_message(-1001910687841, f'\nНазвание конференции: {data["name_conf"]}\n' \
                                           f'Даты конференции: {data["date_conf"]}\n' \
                                           f'Место проведения конференции: {data["location_conf"]}\n' \
                                           f'Стоимость участия в конференции: {data["price_conf"]}\n' \
                                           f'Описание конференции: {data["description_conf"]}\n' \
                                           f'Изображение конференции: {data["pic_conf"]}\n\n')
    await state.clear()
    await callback.answer(
        text='Конференция успешно добавлена!',
        show_alert=True
    )

    await callback.message.answer('Главное меню: ',
                                  reply_markup=base_kb())


async def add_bd_conf(data: Dict[str, Any]) -> None:
    id_user = data["id_user"]
    name_conf = data["name_conf"]
    date_conf = data["date_conf"]
    location_conf = data["location_conf"]
    price_conf = data["price_conf"]
    description_conf = data["description_conf"]
    pic_conf = data["pic_conf"]
    conn = sqlite3.connect('new.db')
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO conference (id_user_conf, name_conf, date_conf,location_conf, price_conf, description_conf, pic_conf)"
        "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
            id_user, name_conf, date_conf, location_conf, price_conf,
            description_conf, pic_conf))
    conn.commit()
    cur.close()
    conn.close()
