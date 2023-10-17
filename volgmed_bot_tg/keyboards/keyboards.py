from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

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
