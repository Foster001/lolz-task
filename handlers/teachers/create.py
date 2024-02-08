from aiogram.dispatcher import FSMContext

from create_bot import dp, db
from aiogram import types

from functions.btns import create_btns
from other.states import Teachers


@dp.callback_query_handler(text_startswith=['Teachers_Create_Show'], state='*')
async def teacher_create(callback:types.CallbackQuery):
	subjects = await db.fetchall("SELECT key,name FROM subjects WHERE view = 1", is_dict=True)
	btns = []
	for subject in subjects:
		btns.append(
			types.InlineKeyboardButton(f"{subject['name']}", callback_data=f"Teachers_Create_SelectSubject_{subject['key']}")
		)
	reply_markup = await create_btns(btns, 2)
	reply_markup.add(
		types.InlineKeyboardButton(f"🔙 Вернуться назад", callback_data=f"Teachers_Show"),
	)

	await callback.message.edit_text("👨‍🏫 Создание преподавателя\n\n"
									 "<em>Выберите предмет для преподавателя</em>", reply_markup=reply_markup)

@dp.callback_query_handler(text_startswith=['Teachers_Create_SelectSubject'], state='*')
async def select_subject(callback:types.CallbackQuery, state=FSMContext):
	split = callback.data.split('_')
	key = split[3]

	await state.update_data(subject=key)
	await Teachers.Create.name.set()

	reply_markup = types.InlineKeyboardMarkup(row_width=2).add(
		types.InlineKeyboardButton(f"🔙 Вернуться назад", callback_data=f"Teachers_Create_Show"),
	)

	await callback.message.edit_text("👨‍🏫 Создание преподавателя\n\n"
									 "<em>Напишите имя преподавателя</em>",
									 reply_markup=reply_markup)