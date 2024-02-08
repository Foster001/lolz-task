from aiogram import types
from aiogram.types import InlineKeyboardMarkup


# Личная функция создающая из списка кнопок объект клавиатуры с определенным порядком кнопок в строку
# Если будете ей пользоваться, то прошу уведомить меня об этом
async def create_btns(btns: list, type: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=type)
    for j in btns:
        while len(btns) != 0:
            if len(btns) >= type: rang = type
            else: rang = len(btns)
            keyboard.add(*[btns[q] for q in range(rang)])
            [btns.pop(0) for q in range(rang)]
    return keyboard