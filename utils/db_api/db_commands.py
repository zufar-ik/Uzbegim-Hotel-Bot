from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
        )

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, nickname, username, tg_id):
        sql = "INSERT INTO reg_bot_user (nickname, username, tg_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, nickname, username, tg_id, fetchrow=True)

    async def add_successful_pay(self, tg_id, price, currency, tg_payment, qr_link, tel_num, email,
                                 name, active, room, vis_date, leav_date, day_count):
        sql = 'INSERT INTO reg_bot_successful_pay (tg_id,price,currency,provider_payment_charge_id,qr_link,tel_num,email,name,active,room_category,visit_date,leav_date,day_count) VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13) returning *'
        return await self.execute(sql, tg_id, price, currency, tg_payment, qr_link, tel_num, email, name, active, room,
                                  vis_date, leav_date, day_count,
                                  fetchrow=True)

    async def where_all(self, **kwargs):
        sql = "SELECT * FROM reg_bot_successful_pay WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def update_active(self, active, tg_id, tg_payment):
        sql = "UPDATE reg_bot_successful_pay SET active=$1 WHERE tg_id=$2 AND provider_payment_charge_id=$3"
        return await self.execute(sql, active, tg_id, tg_payment, execute=True)

    async def get_all_category(self):
        sql = 'SELECT * FROM reg_bot_category'
        return await self.execute(sql, fetch=True)

    async def where_category(self, **kwargs):
        sql = "SELECT * FROM reg_bot_category WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def where_pic(self, **kwargs):
        sql = "SELECT * FROM reg_bot_image WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetch=True)

    async def select_all_users(self):
        sql = "SELECT * FROM reg_bot_user"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM reg_bot_user WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM reg_bot_user"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE reg_bot_user SET username=$1 WHERE tg_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def update_user_langcode(self, langcode, telegram_id):
        sql = "UPDATE reg_bot_user SET lang=$1 WHERE tg_id=$2"
        return await self.execute(sql, langcode, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM reg_bot_user WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE reg_bot_user", execute=True)
