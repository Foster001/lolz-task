from create_bot import dp, db
from aiogram import types

from functions.funcs import is_int
from handlers.settings.settings import settings_show
from other.states import Settings


@dp.message_handler(state=Settings.update)
async def update_(message:types.Message, state=Settings.update):
	data = await state.get_data()
	if data['column'] in ['cabinets']:
		if not await is_int(message.text):
			await message.answer("❌ Значение должно быть числом!")
			return

	await db.execute(f"UPDATE settings SET `{data['column']}` = ?", (message.text,))
	await db.commit()

	await message.answer("✅ Успешно!")
	await settings_show(message)