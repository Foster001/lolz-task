import configparser

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from moduls.database import Base

config = configparser.ConfigParser()
config.read('config.ini')
bot_token = config.get('BOT', 'token')
admins = config.get('BOT', 'admins').split(',')

start_sql_request = """
CREATE TABLE IF NOT EXISTS subjects ( -- Таблица с предметами
    key  INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    date INTEGER);
CREATE TABLE IF NOT EXISTS lessons ( -- Таблица с уроками
    key         INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT,
    teacher     INTEGER,
    date_lesson TEXT,
    date_add    INTEGER
);
CREATE TABLE IF NOT EXISTS teachers ( -- Таблица с учителями
    key     INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT,
    subject INTEGER,
    date    INTEGER
);

CREATE TABLE IF NOT EXISTS settings ( -- Таблица с настройками
    cabinets INTEGER DEFAULT (0) 
);

-- Запрос на запись в таблицу settings если она полностью пустая
INSERT INTO settings SELECT 0 WHERE (SELECT COUNT(*) FROM settings) = 0;
"""		# Запросы на создание пустых таблиц в базе данных

db = Base('base.db', start_sql_request)

bot = Bot(bot_token, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())