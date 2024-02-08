import datetime

from create_bot import dp, db
from aiogram import types

from handlers.subjects.subjects import subjects_show
from other.states import Subjects


@dp.message_handler(state=Subjects.Create.name)
async def create_name(message:types.Message, state=Subjects.Create.name):
	await db.execute("INSERT INTO subjects(name,date) VALUES(?,?)", (
		message.text, int(datetime.datetime.now().timestamp()),
	))
	await db.commit()

	await message.answer("✅ Успешно!")
	await subjects_show(message)