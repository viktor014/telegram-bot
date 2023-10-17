from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    InlineKeyboardMarkup
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, ReplyKeyboardBuilder

def base_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
                             keyboard=[
                                 [
                                     KeyboardButton(text="🧬 Конференции"),
                                     KeyboardButton(text="🤵 Мероприятия")
                                 ]
                             ],
        resize_keyboard=True,
        input_field_placeholder="Выберите категорию",
                         )
    return kb


def conf_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Добавить конференцию"),
                KeyboardButton(text="Просмотр конференций"),
                KeyboardButton(text="Меню")
            ]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие",
        )
    return kb


def modify_kb() -> ReplyKeyboardBuilder:
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text="Добавить конференцию"))
    builder.add(KeyboardButton(text="Удалить конференцию"))
    builder.add(KeyboardButton(text="Изменить конференцию"))
    builder.add(KeyboardButton(text="Меню"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, input_field_placeholder="Выберите действие")


