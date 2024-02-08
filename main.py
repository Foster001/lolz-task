from aiogram import executor
from handlers import dp

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=print(f"Бот был успешно запущен."))