from aiogram.dispatcher.filters.state import StatesGroup, State

class Settings(StatesGroup):
	update = State()

class Teachers(StatesGroup):
	class Create(StatesGroup):
		name = State()

class Subjects(StatesGroup):
	class Create(StatesGroup):
		name = State()