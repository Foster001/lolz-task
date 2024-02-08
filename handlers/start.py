from create_bot import dp, db
from aiogram import types

@dp.callback_query_handler(text=['Menu_Show'], state='*')
@dp.message_handler(commands=['start'], state='*')
async def start_message(message: types.Message | types.CallbackQuery):
	reply_markup = types.InlineKeyboardMarkup(row_width=2).add(
		types.InlineKeyboardButton(f"⚙️ Настройки", callback_data=f"Settings_Show"),).row(
		types.InlineKeyboardButton(f"👨‍🏫 Преподаватели", callback_data=f"Teachers_Show"),
		types.InlineKeyboardButton(f"📚 Предметы", callback_data=f"Subjects_Show"),).row(
		types.InlineKeyboardButton(f"📄 Расписание", callback_data=f"Lessons_Show"),).row(
	)

	if type(message) is types.Message:
		await message.answer("Главное меню бота", reply_markup=reply_markup)
	elif type(message) is types.CallbackQuery:
		await message.message.edit_text("Главное меню бота", reply_markup=reply_markup)