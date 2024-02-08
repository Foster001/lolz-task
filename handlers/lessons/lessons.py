import datetime

from create_bot import dp, db
from aiogram import types

from functions.btns import create_btns


@dp.callback_query_handler(text=['Lessons_Show'], state='*')
async def lessons_show(callback: types.CallbackQuery | types.Message):
	# Запрос на получение урока, имени учителя, названии урока
	lessons = await db.fetchall("SELECT lessons.key,teachers.name,subjects.name,lessons.cabinet FROM lessons "
								"LEFT JOIN teachers ON teachers.key = lessons.teacher "
								"LEFT JOIN subjects ON subjects.key = teachers.subject "
								"WHERE lessons.date_lesson = ? "
								"AND teachers.view = 1 AND subjects.view = 1 AND lessons.view = 1",
								(datetime.date.today(),),
								is_dict=True)


	text = f"\nКабинет | Предмет | Учитель"
	text += ''.join(
		[f"\n<b>№{lesson['lessons_cabinet']}</b>. <b>{lesson['subjects_name']}</b>. <b>{lesson['teachers_name']}.</b>" for lesson in lessons]
	)

	reply_markup = types.InlineKeyboardMarkup(row_width=2).add(
		types.InlineKeyboardButton(f"➕ Создать", callback_data=f"Lessons_Create_Show"),
		types.InlineKeyboardButton(f"➖ Удалить", callback_data=f"Lessons_Delete_Show"),).row(
		types.InlineKeyboardButton(f"🔙 Вернуться назад", callback_data=f"Menu_Show")
	)
	if type(callback) is types.CallbackQuery:
		await callback.message.edit_text(f"📄 Расписание\n"
										 f"{text}", reply_markup=reply_markup)
	elif type(callback) is types.Message:
		await callback.answer(f"📄 Расписание\n"
							  f"{text}", reply_markup=reply_markup)

@dp.callback_query_handler(text_startswith=['Lessons_Delete'], state='*')
async def lessons_delete(callback:types.CallbackQuery):
	split = callback.data.split('_')
	key = split[2].lower()

	if key != 'show':
		await db.execute("UPDATE lessons SET view = 0 WHERE key = ?", (key,))
		await db.commit()

	lessons = await db.fetchall("SELECT lessons.key,subjects.name FROM lessons "
								"LEFT JOIN teachers ON lessons.teacher = teachers.key "
								"LEFT JOIN subjects ON subjects.key = teachers.subject "
								"WHERE lessons.view = 1 AND subjects.view = 1 AND teachers.view = 1", is_dict=True)
	btns = []
	for lesson in lessons:
		btns.append(
			types.InlineKeyboardButton(f"{lesson['subjects_name']}", callback_data=f"Lessons_Delete_{lesson['lessons_key']}")
		)
	reply_markup = await create_btns(btns, 2)
	reply_markup.add(
		types.InlineKeyboardButton(f"🔙 Вернуться назад", callback_data=f"Lessons_Show"),
	)

	await callback.message.edit_text("📄 Расписание\n\n"
									 "<em>Выберите урок для удаления</em>",
									 reply_markup=reply_markup)