import datetime

from create_bot import dp, db
from aiogram import types

from handlers.teachers.teachers import teachers_show
from other.states import Teachers


@dp.message_handler(state=Teachers.Create.name)
async def create_name(message:types.Message, state=Teachers.Create.name):
	data = await state.get_data()
	await db.execute("INSERT INTO teachers(name,subject,date) VALUES(?,?,?)", (
		message.text, data['subject'], int(datetime.datetime.now().timestamp()),
	))
	await db.commit()

	await message.answer("✅ Успешно!")
	await teachers_show(message)