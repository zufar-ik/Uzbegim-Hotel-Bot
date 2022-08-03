import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data.config import ADMINS
from keyboards.inline.menu import lang1, First_menu_uz, First_menu_en, First_menu_ru
from loader import db, bot
from loader import dp


@dp.message_handler(CommandStart(), state='*', user_id=ADMINS)
async def bot_start(message: types.Message, state: FSMContext):
    args = message.get_args()
    name = message.from_user.full_name
    id = message.from_user.id
    user = await db.select_user(tg_id=message.from_user.id)
    try:
        if args.split('-')[1] == 'code':
            id = (args.split('-')[2])
            lanq = await db.select_user(tg_id=int(id))
            pay_id = (args.split('-')[3])
            dd = await db.where_all(tg_id=int(id), provider_payment_charge_id=pay_id)
            if dd['active'] == True:
                await message.answer('Вы уже ранее активировали эту комнату!')
            else:
                await db.update_active(tg_id=int(id), tg_payment=pay_id, active=True)
                data1 = await db.where_all(tg_id=int(id), provider_payment_charge_id=pay_id)
                await message.answer(f'<b>Вы успешно активировали комнату!</b>\n'
                                     f'1.Категория номера: {data1["room_category"]}\n'
                                     f'Дата прибытия ⬇️\n\n'
                                     f'{data1["visit_date"]}\n\n'
                                     f'Дата отбытия ⬆️\n\n'
                                     f'{data1["leav_date"]}\n\n'
                                     f'Дней {data1["day_count"]}\n'
                                     f'<b>Цена: {data1["price"]} \n'
                                     f'Валюта: {data1["currency"]}\n</b>'
                                     f'Имя: {data1["name"]}\n'
                                     f'Email: {data1["email"]}\n'
                                     f'Номер: +{data1["tel_num"]}\n'
                                     f'ID подтверждения: <code>{data1["provider_payment_charge_id"]}</code>',
                                     reply_markup=First_menu_ru)
                await state.finish()
                if lanq['lang'] == 'ru':
                    await message.bot.send_message(chat_id=id, text='Комната была активирована\n\n'
                                                                    f'1.Категория номера: {data1["room_category"]}\n'
                                                                    f'Дата прибытия ⬇️\n\n'
                                                                    f'{data1["visit_date"]}\n\n'
                                                                    f'Дата отбытия ⬆️\n\n'
                                                                    f'{data1["leav_date"]}\n\n'
                                                                    f'Дней {data1["day_count"]}\n'
                                                                    f'<b>Цена: {data1["price"]} \n'
                                                                    f'Валюта: {data1["currency"]}\n</b>'
                                                                    f'Имя: {data1["name"]}\n'
                                                                    f'Email: {data1["email"]}\n'
                                                                    f'Номер: +{data1["tel_num"]}\n'
                                                                    f'ID подтверждения: <code>{data1["provider_payment_charge_id"]}</code>\n\n'
                                                                    'Добро пожаловать!')
                elif lanq['lang'] == 'en':
                    await message.bot.send_message(chat_id=id, text='The room has been activated\n\n'
                                                                    f'1.Room category: {data1["room_category"]}\n'
                                                                    f'Date of arrival ⬇️\n\n'
                                                                    f'{data1["visit_date"]}\n\n'
                                                                    f'Departure date ⬆️\n\n'
                                                                    f'{data1["leav_date"]}\n\n'
                                                                    f'Days {data1["day_count"]}\n'
                                                                    f'<b>Price: {data1["price"]} \n'
                                                                    f'Currency: {data1["currency"]}\n</b>'
                                                                    f'Name: {data1["name"]}\n'
                                                                    f'Email: {data1["email"]}\n'
                                                                    f'Tel Number: +{data1["tel_num"]}\n'
                                                                    f'Confirmation ID: <code>{data1["provider_payment_charge_id"]}</code>\n\n'
                                                                    'Welcome!')
                elif lanq['lang'] == 'uz':
                    await message.bot.send_message(chat_id=id,text='Xona faollashtirildi\n\n'
                                                                    f'1.Xona toifasi: {data1["room_category"]}\n'
                                                                    f'Kelish sanasi ⬇️\n\n'
                                                                    f'{data1["visit_date"]}\n\n'
                                                                    f'Ketish sanasi ⬆️\n\n'
                                                                    f'{data1["leav_date"]}\n\n'
                                                                    f'Kunlar {data1["day_count"]}\n'
                                                                    f'<b>Narxi: {data1["price"]} \n'
                                                                    f'Valyuta: {data1["currency"]}\n</b>'
                                                                    f'Ism: {data1["name"]}\n'
                                                                    f'E-pochta: {data1["email"]}\n'
                                                                    f'Tel raqam: +{data1["tel_num"]}\n'
                                                                    f'Tasdiqlash identifikatori: <code>{data1["provider_payment_charge_id"]}</code>\n\n'
                                                                    'Xush kelibsiz!')
                await state.finish()
    except IndexError:
        await message.answer(f'Вход выполнен от имени Администратора\n\n'
                             f'Привет {name}', reply_markup=First_menu_ru)
        await state.finish()


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext):
    lanq = await db.select_user(tg_id=message.from_user.id)
    if len(message.text) > 6:
        if lanq['lang'] == 'ru':
            await message.answer('У вас недостаточно прав для активации комнаты!')
        elif lanq['lang'] == 'en':
            await message.answer('You do not have enough rights to activate the room!')
        elif lanq['lang'] == 'uz':
            await message.answer('Siz xonani faollashtirish uchun yetarli huquqlarga ega emassiz!')
    name = message.from_user.full_name
    # Добавляем пользователей в базу
    try:
        user = await db.add_user(
            tg_id=message.from_user.id,
            nickname=message.from_user.first_name,
            username=message.from_user.username,
        )

        await message.answer('Welcome!\n'
                             'Choose language!', reply_markup=lang1)

        # Оповещаем админа
        count = await db.count_users()
        msg = f"{message.from_user.full_name} добавлен в базу пользователей.\nВ базе есть {count} людей."
        await bot.send_message(chat_id=ADMINS[0], text=msg)
        await state.finish()


    except asyncpg.exceptions.UniqueViolationError:
        await bot.send_message(chat_id=ADMINS[0], text=f"{name} в базе имелся раньше")
        lanq = await db.select_user(tg_id=message.from_user.id)
        if lanq['lang'] == 'ru':
            await message.answer((f"Добро пожаловать! {name}\n\n"
                                  f"🤖 Я бот который поможет ознакомится и забронировать номер в <b>Hotel Uzbegim</b>\n\n"
                                  f"🤝 Заказать похожего или совсем иного бота? Свяжитесь с разработчиком <a href='https://t.me/zufar_ik'>Zufar</a>"),
                                 reply_markup=First_menu_ru, disable_web_page_preview=True)
            await state.finish()
        elif lanq['lang'] == 'en':
            await message.answer(f"Welcome! {name}\n\n"
                                 f"🤖 I am a bot that will help you get acquainted and book a room at <b>Hotel Uzbegim</b>\n\n"
                                 f"🤝 Order a similar or completely different bot? Contact the developer <a href='https://t.me/zufar_ik'>Zufar</a>",
                                 reply_markup=First_menu_en, disable_web_page_preview=True)
            await state.finish()
        elif lanq['lang'] == 'uz':
            await message.answer(f"Xush kelibsiz! {name}\n\n"
                                 f"🤖 Men <b>Uzbegim mehmonxonasi</b>da tanishish va xona band qilishda yordam beradigan botman\n\n"
                                 f"🤝 Shu kabi yoki butunlay boshqa botga buyurtma berishni xohlaysizmi? Dasturchi bilan bog'laning <a href='https://t.me/zufar_ik'>Zufar</a>",
                                 reply_markup=First_menu_uz, disable_web_page_preview=True)
            await state.finish()
