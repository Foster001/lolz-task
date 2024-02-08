from aiogram.dispatcher import FSMContext

from create_bot import dp, db
from aiogram import types

from other.states import Settings


@dp.callback_query_handler(text=['Settings_Show'], state='*')
async def settings_show(callback: types.CallbackQuery | types.Message):
	settings = await db.fetchone("SELECT cabinets FROM settings")

	reply_markup = types.InlineKeyboardMarkup(row_width=2).add(
		types.InlineKeyboardButton(f"{int(settings[0])} кабинетов", callback_data=f"Settings_Update_cabinets")).row(
		types.InlineKeyboardButton(f"🔙 Вернуться назад", callback_data=f"Menu_Show")
	)

	if type(callback) is types.CallbackQuery:
		await callback.message.edit_text("⚙️ Настройки", reply_markup=reply_markup)
	elif type(callback) is types.Message:
		await callback.answer("⚙️ Настройки", reply_markup=reply_markup)

texts = {
	'cabinets': f"<em>Введите новое кол-во кабинетов</em>",
}

@dp.callback_query_handler(text_startswith=['Settings_Update'], state='*')
async def settings_update(callback:types.CallbackQuery, state=FSMContext):
	split = callback.data.split("_")
	column = split[2]
	await state.update_data(column=column)
	await Settings.update.set()

	reply_markup = types.InlineKeyboardMarkup(row_width=2).add(
		types.InlineKeyboardButton(f"🔙 Вернуться назад", callback_data=f"Settings_Show")
	)
	await callback.message.edit_text(texts[column], reply_markup=reply_markup)