from create_bot import dp
from aiogram import types

from other.states import Subjects

@dp.callback_query_handler(text_startswith=['Subjects_Create_Show'], state='*')
async def subject_create(callback:types.CallbackQuery):
	await Subjects.Create.name.set()

	reply_markup = types.InlineKeyboardMarkup(row_width=2).add(
		types.InlineKeyboardButton(f"🔙 Вернуться назад", callback_data=f"Subjects_Show"),
	)

	await callback.message.edit_text("📚 Создание предмета\n\n"
									 "<em>Напишите название предмета</em>",
									 reply_markup=reply_markup)