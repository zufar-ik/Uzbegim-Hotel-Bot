from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from utils.db_api.db_commands import Database
from data import config

from typing import Tuple, Any, Optional
from aiogram import types
from aiogram.contrib.middlewares.i18n import I18nMiddleware
bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()

