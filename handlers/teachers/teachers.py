from create_bot import dp, db
from aiogram import types

from functions.btns import create_btns


@dp.callback_query_handler(text=['Teachers_Show'], state='*')
async def teachers_show(callback: types.CallbackQuery | types.Message):
	teachers = await db.fetchall("SELECT key,name FROM teachers WHERE view = 1", is_dict=True)
	btns = []
	for teacher in teachers:
		btns.append(
			types.InlineKeyboardButton(f"{teacher['name']}", callback_data=f"Teachers_Select_{teacher['key']}")
		)
	reply_markup = await create_btns(btns, 2)
	reply_markup.add(
		types.InlineKeyboardButton(f"➕ Создать", callback_data=f"Teachers_Create_Show"),
		types.InlineKeyboardButton(f"➖ Удалить", callback_data=f"Teachers_Delete_Show"),).row(
		types.InlineKeyboardButton(f"🔙 Вернуться назад", callback_data=f"Menu_Show")
	)
	if type(callback) is types.CallbackQuery:
		await callback.message.edit_text(f"👨‍🏫 Преподаватели", reply_markup=reply_markup)
	elif type(callback) is types.Message:
		await callback.answer(f"👨‍🏫 Преподаватели", reply_markup=reply_markup)

@dp.callback_query_handler(text_startswith=['Teachers_Delete'], state='*')
async def teachers_delete(callback:types.CallbackQuery):
	split = callback.data.split('_')
	key = split[2].lower()

	if key != 'show':
		await db.execute("UPDATE teachers SET view = 0 WHERE key = ?", (key,))
		await db.commit()

	teachers = await db.fetchall("SELECT key,name FROM teachers WHERE view = 1", is_dict=True)
	btns = []
	for teacher in teachers:
		btns.append(
			types.InlineKeyboardButton(f"{teacher['name']}", callback_data=f"Teachers_Delete_{teacher['key']}")
		)
	reply_markup = await create_btns(btns, 2)
	reply_markup.add(
		types.InlineKeyboardButton(f"🔙 Вернуться назад", callback_data=f"Teachers_Show"),
	)

	await callback.message.edit_text("👨‍🏫 Преподаватели\n\n"
									 "<em>Выберите преподователя для удаления</em>",
									 reply_markup=reply_markup)

@dp.callback_query_handler(text_startswith=['Teachers_Select'], state='*')
async def teacher_select(callback:types.CallbackQuery): await callback.answer()