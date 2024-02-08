from create_bot import dp, db
from aiogram import types

from functions.btns import create_btns


@dp.callback_query_handler(text=['Subjects_Show'], state='*')
async def subjects_show(callback: types.CallbackQuery | types.Message):
	subjects = await db.fetchall("SELECT key,name FROM subjects WHERE view = 1", is_dict=True)
	btns = []
	for subject in subjects:
		btns.append(
			types.InlineKeyboardButton(f"{subject['name']}", callback_data=f"Teachers_Select_{subject['key']}")
		)
	reply_markup = await create_btns(btns, 2)
	reply_markup.add(
		types.InlineKeyboardButton(f"➕ Создать", callback_data=f"Subjects_Create_Show"),
		types.InlineKeyboardButton(f"➖ Удалить", callback_data=f"Subjects_Delete_Show"),).row(
		types.InlineKeyboardButton(f"🔙 Вернуться назад", callback_data=f"Menu_Show")
	)
	if type(callback) is types.CallbackQuery:
		await callback.message.edit_text(f"📚 Предметы", reply_markup=reply_markup)
	elif type(callback) is types.Message:
		await callback.answer(f"📚 Предметы", reply_markup=reply_markup)

@dp.callback_query_handler(text_startswith=['Subjects_Delete'], state='*')
async def subjects_delete(callback:types.CallbackQuery):
	split = callback.data.split('_')
	key = split[2].lower()

	if key != 'show':
		await db.execute("UPDATE subjects SET view = 0 WHERE key = ?", (key,))
		await db.commit()

	subjects = await db.fetchall("SELECT key,name FROM subjects WHERE view = 1", is_dict=True)
	btns = []
	for subject in subjects:
		btns.append(
			types.InlineKeyboardButton(f"{subject['name']}", callback_data=f"Subjects_Delete_{subject['key']}")
		)
	reply_markup = await create_btns(btns, 2)
	reply_markup.add(
		types.InlineKeyboardButton(f"🔙 Вернуться назад", callback_data=f"Subjects_Show"),
	)

	await callback.message.edit_text("📚 Предметы\n\n"
									 "<em>Выберите предмет для удаления</em>",
									 reply_markup=reply_markup)

@dp.callback_query_handler(text_startswith=['Subjects_Select'], state='*')
async def subject_select(callback:types.CallbackQuery): await callback.answer()