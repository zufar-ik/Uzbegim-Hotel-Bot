from pathlib import Path

from environs import Env

# Используем библиотеку environs
env = Env()
env.read_env()

# Считываем данные из .env

BOT_TOKEN = env.str('BOT_TOKEN')  # Токен бота
PAYMENTS_PROVIDER_TOKEN_CLICK = env.str('PAYMENTS_PROVIDER_TOKEN_CLICK')
PAYMENTS_PROVIDER_TOKEN_Unlimited = env.str('PAYMENTS_PROVIDER_TOKEN_Unlimited')
PAYMENTS_PROVIDER_TOKEN_YuKassa = env.str('PAYMENTS_PROVIDER_TOKEN_YuKassa')
ADMINS = (env.list('ADMIN_BOT'))  # Список админов
DB_USER = env.str("POSTGRES_USER")
DB_PASS = env.str("POSTGRES_PASSWORD")
DB_NAME = env.str("POSTGRES_DB")
DB_HOST = env.str("POSTGRES_HOST")
ADMINS_us = ['zufar_ik','None']
ADMINS_name = ['zufar_ik','None']