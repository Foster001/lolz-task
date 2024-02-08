import datetime

from create_bot import dp, db
from aiogram import types

from functions.btns import create_btns
from handlers.lessons.lessons import lessons_show


@dp.callback_query_handler(text_startswith=['Lessons_Create_Show'], state='*')
async def lessons_create(callback:types.CallbackQuery):

	btns = []
	for j in range(7):
		date = datetime.date.today() + datetime.timedelta(days=j)
		btns.append(
			types.InlineKeyboardButton(f"{date}", callback_data=f"Lessons_Create_SelectDate_{date}")
		)

	reply_markup = await create_btns(btns, 2)
	reply_markup.add(
		types.InlineKeyboardButton(f"🔙 Вернуться назад", callback_data=f"Lessons_Show"),
	)

	await callback.message.edit_text("📄 Создание урока\n\n"
									 "<em>Выберите дату на которую хотите поставить урок</em>",
									 reply_markup=reply_markup)

@dp.callback_query_handler(text_startswith=['Lessons_Create_SelectDate'], state='*')
async def select_date(callback:types.CallbackQuery):
	split = callback.data.split('_')
	date = split[3]

	subjects = await db.fetchall("SELECT key,name FROM subjects", is_dict=True)
	btns = [
		types.InlineKeyboardButton(subject['name'],
								 callback_data=f"Lessons_Create_SelectSubject_{date}_{subject['key']}")
		for subject in subjects
	]
	reply_markup = await create_btns(btns, 2)
	reply_markup.add(
		types.InlineKeyboardButton(f"🔙 Вернуться назад", callback_data=f"Lessons_Create_Show"),
	)

	await callback.message.edit_text(f"📄 Создание урока\n"
									 f"<em>Выберите предмет</em>",
									 reply_markup=reply_markup)

@dp.callback_query_handler(text_startswith=['Lessons_Create_SelectSubject'], state='*')
async def select_subject(callback:types.CallbackQuery):
	split = callback.data.split('_')
	date = split[3]
	subject = split[4]

	# Запрос на поиск всех учителей с таким предметом, и что бы за эту дату у них было меньше 5 уроков

	teachers = await db.fetchall("SELECT teachers.name,teachers.key FROM teachers "
						  		 "WHERE (SELECT count(*) FROM lessons WHERE lessons.date_lesson = ? "
								 "AND lessons.teacher = teachers.key) < 5 "
						  	     "AND teachers.subject = ?", (date, subject,), is_dict=True)
	btns = [
		types.InlineKeyboardButton(teacher['teachers_name'],
								 callback_data=f"Lessons_Create_SelectTeacher_{date}_{subject}_{teacher['teachers_key']}")
		for teacher in teachers
	]
	reply_markup = await create_btns(btns, 2)
	reply_markup.add(
		types.InlineKeyboardButton(f"🔙 Вернуться назад", callback_data=f"Lessons_Create_SelectDate_{date}"),
	)

	await callback.message.edit_text(f"📄 Создание урока\n"
									 f"<em>Выберите учителя который будет проводить урок</em>",
									 reply_markup=reply_markup)

@dp.callback_query_handler(text_startswith=['Lessons_Create_SelectTeacher'], state='*')
async def select_teacher(callback:types.CallbackQuery):
	split = callback.data.split('_')
	date = split[3]
	subject = split[4]
	teacher = split[5]

	cabinets = await db.fetchone("SELECT cabinets FROM settings")
	btns = [
		types.InlineKeyboardButton(f"Кабинет №{q+1}", callback_data=f"Lessons_Create_SelectCabinet_{date}_{teacher}_{q+1}")
		for q in range(int(cabinets[0]))
	]
	reply_markup = await create_btns(btns, 2)
	reply_markup.add(
		types.InlineKeyboardButton(f"🔙 Вернуться назад", callback_data=f"Lessons_Create_SelectSubject_{date}_{subject}"),
	)

	await callback.message.edit_text(f"📄 Создание урока\n"
									 f"<em>Выберите кабинет в котором будет проводиться урок</em>",
									 reply_markup=reply_markup)

@dp.callback_query_handler(text_startswith=['Lessons_Create_SelectCabinet'], state='*')
async def select_teacher(callback:types.CallbackQuery):
	split = callback.data.split('_')
	date = split[3]
	teacher = split[4]
	cabinet = split[5]

	await db.execute("INSERT INTO lessons(teacher,date_lesson,date_add,cabinet) VALUES(?,?,?,?)", (
		teacher, date, int(datetime.datetime.now().timestamp()), cabinet,
	))
	await db.commit()

	await callback.answer("✅ Успешно!")
	await lessons_show(callback)

# Абуталабашунеба