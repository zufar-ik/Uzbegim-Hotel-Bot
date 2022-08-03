import datetime
import os
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.deep_linking import get_start_link
from aiogram.utils.exceptions import MessageToDeleteNotFound
from data.config import PAYMENTS_PROVIDER_TOKEN_CLICK, PAYMENTS_PROVIDER_TOKEN_Unlimited, \
    PAYMENTS_PROVIDER_TOKEN_YuKassa, ADMINS

from keyboards.inline.calendar import create_calendar, separate_callback_data
from keyboards.inline.menu import First_menu_ru, First_menu_en, First_menu_uz, lang1, cash_ru, cash_en, cash_uz, \
    back6_ru, back6_uz, back6_en, back_ru, back_en, back_uz
from loader import db, bot
from loader import dp
from states.state import Send, Payments, Admin
import qrcode


@dp.callback_query_handler(text='settings')
async def set1(call: types.CallbackQuery):
    lang = await db.select_user(tg_id=call.from_user.id)
    if lang['lang'] == 'ru':
        await call.message.edit_text('Выберите язык интерфейса', reply_markup=lang1)
    elif lang['lang'] == 'en':
        await call.message.edit_text('Select interface language', reply_markup=lang1)
    elif lang['lang'] == 'uz':
        await call.message.edit_text('Interfeys tilini tanlang', reply_markup=lang1)


@dp.callback_query_handler(text='ru')
async def langru(call: types.CallbackQuery):
    await db.update_user_langcode(langcode='ru', telegram_id=call.from_user.id)
    await call.answer('Ваш язык был успешно изменен на Русский')
    await call.message.edit_text('Выберите интересующий вас раздел', reply_markup=First_menu_ru)


@dp.callback_query_handler(text='en')
async def langen(call: types.CallbackQuery):
    await db.update_user_langcode(langcode='en', telegram_id=call.from_user.id)
    await call.answer(f'Your language has been successfully changed to English')
    await call.message.edit_text(f'Select the section you are interested in', reply_markup=First_menu_en)


@dp.callback_query_handler(text='uz')
async def langen(call: types.CallbackQuery):
    await db.update_user_langcode(langcode='uz', telegram_id=call.from_user.id)
    await call.answer(f'Tilingiz Oʻzbek tiliga muvaffaqiyatli oʻzgartirildi')
    await call.message.edit_text(f'Sizni qiziqtirgan boʻlimni tanlang', reply_markup=First_menu_uz)


@dp.callback_query_handler(text='back')
async def back1(call: types.CallbackQuery):
    lang = await db.select_user(tg_id=call.from_user.id)
    if lang['lang'] == 'ru':
        await call.message.edit_text('Выберите интересующий вас раздел', reply_markup=First_menu_ru)
    elif lang['lang'] == 'en':
        await call.message.edit_text('Select the section you are interested in', reply_markup=First_menu_en)
    elif lang['lang'] == 'uz':
        await call.message.edit_text('Sizni qiziqtirgan boʻlimni tanlang', reply_markup=First_menu_uz)


@dp.callback_query_handler(text='sos')
async def sos(call: types.CallbackQuery):
    lang = await db.select_user(tg_id=call.from_user.id)
    if lang['lang'] == 'ru':
        await call.message.edit_text('Наши контакты:\n\n'
                                     'Ресепшен: +998 62 212 34 56\n\n'
                                     'Сайт: www.uzbegim-hotel.uz\n\n'
                                     'Адрес: A.Баходирхон 182/1\n\n', reply_markup=back_ru)
    elif lang['lang'] == 'en':
        await call.message.edit_text('Our contacts:\n\n'
                                     'Reception: +998 62 212 34 56\n\n'
                                     'Website: www.uzbegim-hotel.uz\n\n'
                                     'Address: A.Bahodirkhon 182/1\n\n', reply_markup=back_en)
    elif lang['lang'] == 'uz':
        await call.message.edit_text("Bizning kontaktlarimiz:\n\n"
                                     'Qabul: +998 62 212 34 56\n\n'
                                     'Veb-sayt: www.uzbegim-hotel.uz\n\n'
                                     'Manzil: A.Bahodirxon 182/1\n\n', reply_markup=back_uz)


@dp.callback_query_handler(text='nomer')
async def get_nomer(call: types.CallbackQuery):
    category_db = await db.get_all_category()
    lang = await db.select_user(tg_id=call.from_user.id)
    category = InlineKeyboardMarkup(row_width=1)
    for i in category_db:
        category.insert(InlineKeyboardButton(text=f'{i[1]}', callback_data=f'{i[2]}'))
    if lang['lang'] == 'ru':

        category.insert(InlineKeyboardButton(text='Назад 🔙', callback_data='back'))
        await call.message.edit_text('Выберите категорию номеров!', reply_markup=category)
    elif lang['lang'] == 'en':
        category.insert(InlineKeyboardButton(text='Back 🔙', callback_data='back'))
        await call.message.edit_text('Choose a room category!', reply_markup=category)
    elif lang['lang'] == 'uz':

        category.insert(InlineKeyboardButton(text='Orqaga 🔙', callback_data='back'))
        await call.message.edit_text('Xona toifasini tanlang!', reply_markup=category)

    for i in category_db:
        @dp.callback_query_handler(text=f'{i[2]}')
        async def get_nomer(call: types.CallbackQuery, state: FSMContext):
            lang = await db.select_user(tg_id=call.from_user.id)
            call_1 = call.data
            await state.update_data(
                {"wh_cat": call_1}
            )
            where_cat = await db.where_category(slug=f'{call_1}')
            a = where_cat['id']
            IMG = []
            for h in await db.where_pic(name_id=a):
                IMG.append(h['img'])
            media = types.MediaGroup()
            for q in IMG:
                if lang['lang'] == 'ru':
                    media.attach_photo(q, (f"<b>Категория</b>: {where_cat['name']}\n\n"
                                           f"<b>Номера в категории</b>: {where_cat['room_num']}\n\n"
                                           f"<b>Подробнее о номерах</b>: {where_cat['about_ru']}\n\n"
                                           f"<b>Цена</b>: {where_cat['price_ru']} ₽\n\t\t\t\t\t\t\t\t\t\t\t{where_cat['price_uz']} so'm"))
                elif lang['lang'] == 'en':
                    media.attach_photo(q, (f"<b>Category</b>: {where_cat['name']}\n\n"
                                           f"<b>Rooms in category</b>: {where_cat['room_num']}\n\n"
                                           f"<b>More about room</b>: {where_cat['about_en']}\n\n"
                                           f"<b>Price</b>: {where_cat['price_en']} $ \n\n"))

                elif lang['lang'] == 'uz':
                    media.attach_photo(q, (f"<b>Kategoriya</b>: {where_cat['name']}\n\n"
                                           f"<b>Xona raqamlari</b>: {where_cat['room_num']}\n\n"
                                           f"<b>Xonalar haq0ida batafsil</b>: {where_cat['about_uz']}\n\n"
                                           f"<b>Narx</b>: {where_cat['price_uz']} so'm"))
            await call.message.delete()
            await bot.send_media_group(call.message.chat.id, media=media)
            a = call.message.message_id
            await state.update_data(
                {"a": a}
            )

            backru = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text='Забронировать 🔑', callback_data=f'{where_cat["bron_slug"]}')],
                    [InlineKeyboardButton(text='Назад 🔙', callback_data='back2')]
                ]
            )

            backen = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text='Book 🔑', callback_data=f'{where_cat["bron_slug"]}')],
                    [InlineKeyboardButton(text='Back 🔙', callback_data='back2')]
                ]
            )

            backuz = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text='Bron qilish 🔑', callback_data=f'{where_cat["bron_slug"]}')],
                    [InlineKeyboardButton(text='Orqaga 🔙', callback_data='back2')]
                ]
            )
            if lang['lang'] == 'ru':
                await call.message.answer(f"<b>Категория</b>: {where_cat['name']}\n\n"
                                          f"<b>Номера в категории</b>: {where_cat['room_num']}\n\n"
                                          f"<b>Подробнее о номерах</b>: {where_cat['about_ru']}\n\n"
                                          f"<b>Цена</b>: {where_cat['price_ru']} ₽\n\t\t\t\t\t\t\t\t\t\t\t{where_cat['price_uz']} so'm",
                                          reply_markup=backru)
                await Send.up.set()

            elif lang['lang'] == 'en':
                await call.message.answer(f"<b>Category</b>: {where_cat['name']}\n\n"
                                          f"<b>Rooms in category</b>: {where_cat['room_num']}\n\n"
                                          f"<b>More about room</b>: {where_cat['about_en']}\n\n"
                                          f"<b>Price</b>: {where_cat['price_en']} $\n\n", reply_markup=backen)
                await Send.up.set()

            elif lang['lang'] == 'uz':
                await call.message.answer(f"<b>Kategoriya</b>: {where_cat['name']}\n\n"
                                          f"<b>Xona raqamlari</b>: {where_cat['room_num']}\n\n"
                                          f"<b>Xonalar haqida batafsil</b>: {where_cat['about_uz']}\n\n"
                                          f"<b>Narx</b>: {where_cat['price_uz']} so'm\n\n", reply_markup=backuz)
                await Send.up.set()

            @dp.callback_query_handler(text='back4', state=Payments.peyments)
            async def back99(call: types.CallbackQuery):
                lang = await db.select_user(tg_id=call.from_user.id)
                data = await state.get_data()
                here_cat = data.get("wh_cat")
                where_cat = await db.where_category(slug=f'{here_cat}')
                a = where_cat['id']
                IMG = []
                for h in await db.where_pic(name_id=a):
                    IMG.append(h['img'])
                media = types.MediaGroup()
                for q in IMG:
                    if lang['lang'] == 'ru':
                        media.attach_photo(q, (f"<b>Категория</b>: {where_cat['name']}\n\n"
                                               f"<b>Номера в категории</b>: {where_cat['room_num']}\n\n"
                                               f"<b>Подробнее о номерах</b>: {where_cat['about_ru']}\n\n"
                                               f"<b>Цена за один день</b>: {where_cat['price_ru']} ₽\n\t\t\t\t\t\t\t\t\t\t\t{where_cat['price_uz']} so'm"))
                    elif lang['lang'] == 'en':
                        media.attach_photo(q, (f"<b>Category</b>: {where_cat['name']}\n\n"
                                               f"<b>Rooms in category</b>: {where_cat['room_num']}\n\n"
                                               f"<b>More about room</b>: {where_cat['about_en']}\n\n"
                                               f"<b>Price for one day</b>: {where_cat['price_en']} $ \n\n"))

                    elif lang['lang'] == 'uz':
                        media.attach_photo(q, (f"<b>Kategoriya</b>: {where_cat['name']}\n\n"
                                               f"<b>Xona raqamlari</b>: {where_cat['room_num']}\n\n"
                                               f"<b>Xonalar haqida batafsil</b>: {where_cat['about_uz']}\n\n"
                                               f"<b>Narx bir kun uchun</b>: {where_cat['price_uz']} so'm"))
                await call.message.delete()
                await bot.send_media_group(call.message.chat.id, media=media)
                if lang['lang'] == 'ru':
                    await call.message.answer(f"<b>Категория</b>: {where_cat['name']}\n\n"
                                              f"<b>Номера в категории</b>: {where_cat['room_num']}\n\n"
                                              f"<b>Подробнее о номерах</b>: {where_cat['about_ru']}\n\n"
                                              f"<b>Цена за один день</b>: {where_cat['price_ru']} ₽\n\t\t\t\t\t\t\t\t\t\t\t{where_cat['price_uz']} so'm",
                                              reply_markup=backru)
                    await Send.up.set()

                elif lang['lang'] == 'en':
                    await call.message.answer(f"<b>Category</b>: {where_cat['name']}\n\n"
                                              f"<b>Rooms in category</b>: {where_cat['room_num']}\n\n"
                                              f"<b>More about room</b>: {where_cat['about_en']}\n\n"
                                              f"<b>Price for one day</b>: {where_cat['price_en']} $\n\n",
                                              reply_markup=backen)
                    await Send.up.set()

                elif lang['lang'] == 'uz':
                    await call.message.answer(f"<b>Kategoriya</b>: {where_cat['name']}\n\n"
                                              f"<b>Xona raqamlari</b>: {where_cat['room_num']}\n\n"
                                              f"<b>Xonalar haqida batafsil</b>: {where_cat['about_uz']}\n\n"
                                              f"<b>Narx bir kun uchun</b>: {where_cat['price_uz']} so'm\n\n",
                                              reply_markup=backuz)
                    await Send.up.set()

            @dp.callback_query_handler(text='back2', state=Send.up)
            async def back2(call: types.CallbackQuery, state: FSMContext):
                lang = await db.select_user(tg_id=call.from_user.id)
                data = await state.get_data()
                a = data.get("a")
                try:
                    for i in range(1, 100):
                        a = call.message.message_id - i
                        await bot.delete_message(chat_id=call.message.chat.id, message_id=a)
                except MessageToDeleteNotFound:
                    if lang['lang'] == 'ru':
                        await call.message.edit_text('Выберите раздел который вас интересует',
                                                     reply_markup=category)
                        await state.finish()
                    elif lang['lang'] == 'en':
                        await call.message.edit_text('Choose the section you are interested in',
                                                     reply_markup=category)
                        await state.finish()
                    elif lang['lang'] == 'uz':
                        await call.message.edit_text('Sizni qiziqtirgan boʻlimni tanlang', reply_markup=category)
                        await state.finish()

            @dp.callback_query_handler(text=f'{where_cat["bron_slug"]}', state=Send.up)
            async def bron(call: types.CallbackQuery):
                lang = await db.select_user(tg_id=call.from_user.id)
                data = await state.get_data()
                a = data.get("a")
                try:
                    for i in range(1, 100):
                        a = call.message.message_id - i
                        await bot.delete_message(chat_id=call.message.chat.id, message_id=a)
                except MessageToDeleteNotFound:
                    await call.message.delete()
                    now = datetime.datetime.now()
                    markup = create_calendar(now.year, now.month)
                    if lang['lang'] == 'ru':
                        await call.message.answer("Пожалуйста, выберите дату прибытия в отель\n\n"
                                                  f"Сегодня: {now.year}", reply_markup=markup)
                        await Admin.first.set()
                    elif lang['lang'] == 'en':
                        await call.message.answer("Please, choose the date of arrival at the hotel\n\n"
                                                  f"Today: {now.year}", reply_markup=markup)
                        await Admin.first.set()
                    elif lang['lang'] == 'uz':
                        await call.message.answer("Iltimos, mehmonxonaga kelish sanansini tanlang\n\n"
                                                  f"Bugun: {now.year}", reply_markup=markup)
                        await Admin.first.set()


@dp.callback_query_handler(state=Admin.first)
async def inline11(call: types.CallbackQuery, state: FSMContext):
    now = datetime.datetime.now()
    lang = await db.select_user(tg_id=call.from_user.id)
    a = separate_callback_data(call.data)
    (_, action, year, month, day) = a
    curr = datetime.datetime(int(year), int(month), 1)
    if action == 'IGNORE':
        pass
    elif action == "DAY":
        ret_data = True, datetime.datetime(int(year), int(month), int(day))
        a = []
        if lang['lang'] == 'ru':
            a = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
                 'Ноябрь', 'Декабрь']
        elif lang['lang'] == 'en':
            a = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                 'November December']
        elif lang['lang'] == 'uz':
            a = ['', 'yanvar', 'fevral', 'mart', 'aprel', 'may', 'iyun', 'iyul', 'avgust', 'sentyabr', 'oktyabr',
                 "Noyabr dekabr"]
        mon = (ret_data[1].strftime("%m"))
        month = (a[int(mon) % 12])
        day = (ret_data[1].strftime("%d"))
        await state.update_data(
            {'chekday1': ret_data[1]}
        )
        await state.update_data(
            {'vis_year': year}
        )
        await state.update_data(
            {"vis_month": month}
        )
        await state.update_data(
            {"vis_day": day}
        )
        await Admin.second.set()
    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        await call.message.edit_text("Пожалуйста, выберите дату прибытия в отель\n\n"
                                     f"Сегодня: {now.year}",
                                     reply_markup=create_calendar(int(pre.year), int(pre.month)))

    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        await call.message.edit_text("Пожалуйста, выберите дату прибытия в отель\n\n"
                                     f"Сегодня: {now.year}", reply_markup=create_calendar(int(ne.year), int(ne.month)))
    else:
        await call.message.edit_text(text="Что-то пошло не так!", reply_markup=create_calendar(now.year, now.month))
        await Send.up.set()


@dp.callback_query_handler(state=Admin.second)
async def get_leave(call: types.CallbackQuery):
    await call.message.delete()
    lang = await db.select_user(tg_id=call.from_user.id)
    now = datetime.datetime.now()  # Текущая дата
    markup = create_calendar(now.year, now.month)
    if lang['lang'] == 'ru':
        await call.message.answer("Пожалуйста, выберите дату отбытия из отеля\n\n"
                                  f"Сегодня: {now.year}", reply_markup=markup)
        await Admin.third.set()
    elif lang['lang'] == 'en':
        await call.message.answer("Please select a leave date from our hotel\n\n"
                                  f"Today: {now.year}", reply_markup=markup)
        await Admin.third.set()
    elif lang['lang'] == 'uz':
        await call.message.answer("Iltimos, mehmonxonadan jo‘nash sanasini tanlang\n\n"
                                  f"Bugun: {now.year}", reply_markup=markup)
        await Admin.third.set()


@dp.callback_query_handler(state=Admin.third)
async def get_pay(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    lang = await db.select_user(tg_id=call.from_user.id)
    call_data = call.data
    now = datetime.datetime.now()
    a = call_data.split(';')
    (_, action, year, month, day) = a
    curr = datetime.datetime(int(year), int(month), 1)
    if action == "IGNORE":
        pass
    elif action == "DAY":
        ret_data = True, datetime.datetime(int(year), int(month), int(day))
        year = (ret_data[1].strftime('%Y'))
        a = []
        if lang['lang'] == 'ru':
            a = ['', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь',
                 'Ноябрь', 'Декабрь']
        elif lang['lang'] == 'en':
            a = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                 'November December']
        elif lang['lang'] == 'uz':
            a = ['', 'yanvar', 'fevral', 'mart', 'aprel', 'may', 'iyun', 'iyul', 'avgust', 'sentyabr', 'oktyabr',
                 "Noyabr dekabr"]
        mon = (ret_data[1].strftime("%m"))
        month = (a[int(mon) % 12])
        day = (ret_data[1].strftime("%d"))
        await state.update_data(
            {'chekday2': ret_data[1]}
        )
        await state.update_data(
            {'leav_year': year}
        )
        await state.update_data(
            {"leav_month": mon}
        )
        await state.update_data(
            {"leav_day": day}
        )
        data = await state.get_data()
        vis_year = data.get("vis_year")
        vis_month = data.get("vis_month")
        vis_day = data.get("vis_day")
        if lang['lang'] == 'ru':
            await call.message.answer(f'Дата прибытия ⬇️\n\n'
                                      f'Год: {vis_year}\n'
                                      f'Месяц: {vis_month}\n'
                                      f'День: {vis_day}\n\n'
                                      f'Дата отбытия ⬆️\n\n'
                                      f'Год: {year}\n'
                                      f'Месяц: {month}\n'
                                      f'День: {day}\n\n'
                                      'Выберите удобный способ оплаты!', reply_markup=cash_ru)
            await Payments.peyments.set()
        if lang['lang'] == 'en':
            await call.message.answer(f'Date of arrival ⬇️\n\n'
                                      f'Year: {vis_year}\n'
                                      f'Month: {vis_month}\n'
                                      f'Day: {vis_day}\n\n'
                                      f'Departure date ⬆️\n\n'
                                      f'Year: {year}\n'
                                      f'Month: {month}\n'
                                      f'Day: {day}\n\n'
                                      'Choose a convenient payment method!', reply_markup=cash_en)
            await Payments.peyments.set()
        if lang['lang'] == 'uz':
            await call.message.answer(f'Kelish sanasi ⬇️\n\n'
                                      f'Yil: {vis_year}\n'
                                      f'Oy: {vis_month}\n'
                                      f'Kun: {vis_day}\n\n'
                                      f'Ketish sanasi ⬆️\n\n'
                                      f'Yil: {year}\n'
                                      f'Oy: {month}\n'
                                      f'Kun: {day}\n\n'
                                      "Qulay to'lov usulini tanlang!", reply_markup=cash_uz)
            await Payments.peyments.set()

    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        await call.message.answer("Пожалуйста, выберите дату прибытия в отель\n\n"
                                  f"Сегодня: {now.year}",
                                  reply_markup=create_calendar(int(pre.year), int(pre.month)))

    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        await call.message.answer("Пожалуйста, выберите дату прибытия в отель\n\n"
                                  f"Сегодня: {now.year}", reply_markup=create_calendar(int(ne.year), int(ne.month)))
    else:
        await call.message.edit_text(text="Что-то пошло не так!", reply_markup=create_calendar(now.year, now.month))
        await Send.up.set()


@dp.callback_query_handler(text=['click', 'yukassa', 'unlimint', 'back6'], state=Payments.peyments)
async def paymets_ru(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    chek1 = data.get('chekday1')
    chek2 = data.get('chekday2')
    now = datetime.datetime.now()

    if chek1 > chek2:
        await call.message.edit_text('Вы ввели некорректное значение дат',
                                     reply_markup=create_calendar(now.year, now.month))
        await Admin.first.set()
    elif chek1 <= chek2:
        day1 = (chek2 - chek1)
        print(day1)
        day = (str(day1).split(' '))
        day = day[0]
        day = str(day)
        if day == '0:00:00':
            day = int(1)
        await state.update_data(
            {"day": day}
        )
        here_cat = data.get("wh_cat")
        lang = await db.select_user(tg_id=call.from_user.id)
        where_cat = await db.where_category(slug=f'{here_cat}')
        await state.update_data(
            {'name': where_cat['name']}
        )
        if lang['lang'] == 'uz':
            if call.data == 'click':
                if PAYMENTS_PROVIDER_TOKEN_CLICK.split(':')[1] == 'TEST':
                    await call.message.delete()
                    await bot.send_invoice(
                        call.message.chat.id,
                        title=where_cat['name'],
                        description=where_cat['about_payments_uz'],
                        provider_token=PAYMENTS_PROVIDER_TOKEN_CLICK,
                        currency='uzs',
                        photo_url=where_cat['logo'],
                        photo_height=512,  # !=0/None, иначе изображение не покажется
                        photo_width=512,
                        photo_size=512,
                        need_email=True,
                        need_name=True,
                        need_phone_number=True,
                        is_flexible=False,  # True если конечная цена зависит от способа доставки
                        prices=([
                            {
                                "label": "Narx",
                                "amount": where_cat['price_payments_uzs'] * int(day)
                            }
                        ]),
                        start_parameter='time-machine-example',
                        payload='some-invoice-payload-for-our-internal-use',
                        reply_markup=back6_uz
                    )
                    await Payments.back.set()
            elif call.data == 'yukassa':
                if PAYMENTS_PROVIDER_TOKEN_YuKassa.split(':')[1] == 'TEST':
                    await call.message.delete()
                    await bot.send_invoice(
                        call.message.chat.id,
                        title=where_cat['name'],
                        description=where_cat['about_payments_uz'],
                        provider_token=PAYMENTS_PROVIDER_TOKEN_YuKassa,
                        currency='rub',
                        photo_url=where_cat['logo'],
                        photo_height=512,  # !=0/None, иначе изображение не покажется
                        photo_width=512,
                        photo_size=512,
                        need_email=True,
                        need_name=True,
                        need_phone_number=True,
                        is_flexible=False,  # True если конечная цена зависит от способа доставки
                        prices=([
                            {
                                "label": "Narx",
                                "amount": where_cat['price_payments_rub'] * int(day)
                            }
                        ]),
                        start_parameter='time-machine-example',
                        payload='some-invoice-payload-for-our-internal-use',
                        reply_markup=back6_uz
                    )
                    await Payments.back.set()
            elif call.data == 'unlimint':
                if PAYMENTS_PROVIDER_TOKEN_Unlimited.split(':')[1] == 'TEST':
                    await call.message.delete()
                    await bot.send_invoice(
                        call.message.chat.id,
                        title=where_cat['name'],
                        description=where_cat['about_payments_uz'],
                        provider_token=PAYMENTS_PROVIDER_TOKEN_Unlimited,
                        currency='usd',
                        photo_url=where_cat['logo'],
                        photo_height=512,  # !=0/None, иначе изображение не покажется
                        photo_width=512,
                        photo_size=512,
                        need_name=True,
                        need_email=True,
                        need_phone_number=True,
                        is_flexible=False,  # True если конечная цена зависит от способа доставки
                        prices=([
                            {
                                "label": "Narx",
                                "amount": where_cat['price_payments_usd'] * int(day)
                            }
                        ]),
                        start_parameter='time-machine-example',
                        payload='some-invoice-payload-for-our-internal-use',
                        reply_markup=back6_uz
                    )

                    await Payments.back.set()
        elif lang['lang'] == 'ru':
            if call.data == 'click':
                if PAYMENTS_PROVIDER_TOKEN_CLICK.split(':')[1] == 'TEST':
                    await call.message.delete()
                    await bot.send_invoice(
                        call.message.chat.id,
                        title=where_cat['name'],
                        description=where_cat['about_payments_ru'],
                        provider_token=PAYMENTS_PROVIDER_TOKEN_CLICK,
                        currency='uzs',
                        photo_url=where_cat['logo'],
                        photo_height=512,  # !=0/None, иначе изображение не покажется
                        photo_width=512,
                        photo_size=512,
                        need_email=True,
                        need_name=True,
                        need_phone_number=True,
                        is_flexible=False,  # True если конечная цена зависит от способа доставки
                        prices=([
                            {
                                "label": "Цена",
                                "amount": where_cat['price_payments_uzs'] * int(day)
                            }
                        ]),
                        start_parameter='time-machine-example',
                        payload='some-invoice-payload-for-our-internal-use',
                        reply_markup=back6_ru
                    )
                    await Payments.back.set()
            elif call.data == 'yukassa':
                if PAYMENTS_PROVIDER_TOKEN_YuKassa.split(':')[1] == 'TEST':
                    await call.message.delete()
                    await bot.send_invoice(
                        call.message.chat.id,
                        title=where_cat['name'],
                        description=where_cat['about_payments_ru'],
                        provider_token=PAYMENTS_PROVIDER_TOKEN_YuKassa,
                        currency='rub',
                        photo_url=where_cat['logo'],
                        photo_height=512,  # !=0/None, иначе изображение не покажется
                        photo_width=512,
                        photo_size=512,
                        need_email=True,
                        need_name=True,
                        need_phone_number=True,
                        is_flexible=False,  # True если конечная цена зависит от способа доставки
                        prices=([
                            {
                                "label": "Цена",
                                "amount": where_cat['price_payments_rub'] * int(day)
                            }
                        ]),
                        start_parameter='time-machine-example',
                        payload='some-invoice-payload-for-our-internal-use',
                        reply_markup=back6_ru
                    )
                    await Payments.back.set()
            elif call.data == 'unlimint':
                if PAYMENTS_PROVIDER_TOKEN_Unlimited.split(':')[1] == 'TEST':
                    await call.message.delete()
                    await bot.send_invoice(
                        call.message.chat.id,
                        title=where_cat['name'],
                        description=where_cat['about_payments_ru'],
                        provider_token=PAYMENTS_PROVIDER_TOKEN_Unlimited,
                        currency='usd',
                        photo_url=where_cat['logo'],
                        photo_height=512,  # !=0/None, иначе изображение не покажется
                        photo_width=512,
                        photo_size=512,
                        need_name=True,
                        need_email=True,
                        need_phone_number=True,
                        is_flexible=False,  # True если конечная цена зависит от способа доставки
                        prices=([
                            {
                                "label": "Цена",
                                "amount": where_cat['price_payments_usd'] * int(day)
                            }
                        ]),
                        start_parameter='time-machine-example',
                        payload='some-invoice-payload-for-our-internal-use',
                        reply_markup=back6_ru
                    )

                    await Payments.back.set()
        elif lang['lang'] == 'en':
            if call.data == 'click':
                if PAYMENTS_PROVIDER_TOKEN_CLICK.split(':')[1] == 'TEST':
                    await call.message.delete()
                    await bot.send_invoice(
                        call.message.chat.id,
                        title=where_cat['name'],
                        description=where_cat['about_payments_en'],
                        provider_token=PAYMENTS_PROVIDER_TOKEN_CLICK,
                        currency='uzs',
                        photo_url=where_cat['logo'],
                        photo_height=512,  # !=0/None, иначе изображение не покажется
                        photo_width=512,
                        photo_size=512,
                        need_email=True,
                        need_name=True,
                        need_phone_number=True,
                        is_flexible=False,  # True если конечная цена зависит от способа доставки
                        prices=([
                            {
                                "label": "Price",
                                "amount": where_cat['price_payments_uzs'] * int(day)
                            }
                        ]),
                        start_parameter='time-machine-example',
                        payload='some-invoice-payload-for-our-internal-use',
                        reply_markup=back6_en
                    )
                    await Payments.back.set()
            elif call.data == 'yukassa':
                if PAYMENTS_PROVIDER_TOKEN_YuKassa.split(':')[1] == 'TEST':
                    await call.message.delete()
                    await bot.send_invoice(
                        call.message.chat.id,
                        title=where_cat['name'],
                        description=where_cat['about_payments_en'],
                        provider_token=PAYMENTS_PROVIDER_TOKEN_YuKassa,
                        currency='rub',
                        photo_url=where_cat['logo'],
                        photo_height=512,  # !=0/None, иначе изображение не покажется
                        photo_width=512,
                        photo_size=512,
                        need_email=True,
                        need_name=True,
                        need_phone_number=True,
                        is_flexible=False,  # True если конечная цена зависит от способа доставки
                        prices=([
                            {
                                "label": "Price",
                                "amount": where_cat['price_payments_rub'] * int(day)
                            }
                        ]),
                        start_parameter='time-machine-example',
                        payload='some-invoice-payload-for-our-internal-use',
                        reply_markup=back6_en
                    )
                    await Payments.back.set()
            elif call.data == 'unlimint':
                if PAYMENTS_PROVIDER_TOKEN_Unlimited.split(':')[1] == 'TEST':
                    await call.message.delete()
                    await bot.send_invoice(
                        call.message.chat.id,
                        title=where_cat['name'],
                        description=where_cat['about_payments_en'],
                        provider_token=PAYMENTS_PROVIDER_TOKEN_Unlimited,
                        currency='usd',
                        photo_url=where_cat['logo'],
                        photo_height=512,  # !=0/None, иначе изображение не покажется
                        photo_width=512,
                        photo_size=512,
                        need_name=True,
                        need_email=True,
                        need_phone_number=True,
                        is_flexible=False,  # True если конечная цена зависит от способа доставки
                        prices=([
                            {
                                "label": "Price",
                                "amount": where_cat['price_payments_usd'] * int(day)
                            }
                        ]),
                        start_parameter='time-machine-example',
                        payload='some-invoice-payload-for-our-internal-use',
                        reply_markup=back6_en
                    )

                    await Payments.back.set()


@dp.callback_query_handler(text='back6', state=Payments.back)
async def back36(call: types.CallbackQuery, state: FSMContext):
    lang = await db.select_user(tg_id=call.from_user.id)
    await call.message.delete()
    if lang['lang'] == 'ru':
        await call.message.answer('Выберите удобный способ оплаты!', reply_markup=cash_ru)
        await Payments.peyments.set()
    if lang['lang'] == 'en':
        await call.message.answer('Choose a convenient payment method!', reply_markup=cash_en)
        await Payments.peyments.set()
    if lang['lang'] == 'uz':
        await call.message.answer("Qulay to'lov usulini tanlang!", reply_markup=cash_uz)
        await Payments.peyments.set()


@dp.pre_checkout_query_handler(lambda query: True, state='*')
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message="Ошибка")


@dp.message_handler(content_types=['successful_payment'], state='*')
async def process_successful_payment(message: types.Message, state: FSMContext):
    lang = await db.select_user(tg_id=message.from_user.id)
    id = message.from_user.id
    alls = message.successful_payment
    data = await state.get_data()
    name2 = data.get("name")
    tel_num = alls['order_info']['phone_number']
    email = alls['order_info']['email']
    telegram_payment_charge_id = alls['telegram_payment_charge_id']
    id2 = (tel_num) + '-' + 'code' + '-' + str(id) + '-' + (telegram_payment_charge_id)
    link = await get_start_link(str(id2), encode=False)
    img = qrcode.make(link)
    name = alls['order_info']['name']
    chek1 = data.get('chekday1')
    chek2 = data.get('chekday2')
    price = alls['total_amount'] // 100
    currency = alls['currency']
    day = data.get('day')
    await db.add_successful_pay(tg_id=id, price=price, currency=currency, tg_payment=telegram_payment_charge_id,
                                qr_link=link, tel_num=tel_num, email=email, name=name, active=False, room=name2,
                                vis_date=chek1, leav_date=chek2, day_count=int(day))
    img.save(f'qr {message.from_user.id}.jpg')
    await message.answer_photo(photo=open(f'qr {message.from_user.id}.jpg', 'rb'))
    os.remove(os.path.join(f"qr {message.from_user.id}.jpg"))
    if lang['lang'] == 'ru':
        await bot.send_message(
            message.chat.id,
            ('Ура!!\nВаш платеж прошел успешно.\n\n'
             '1.Сохраните вышестоящий QR-CODE для подтверждения личности в ресепшене\n\n'
             '2.В случае если вы потеряете QR-CODE обратитесь к администраторам <b>Uzbegim</b>\n\n'
             f'3.Категория номера: {name2}\n'
             f'Дата прибытия ⬇️\n\n'
             f'{chek1}\n\n'
             f'Дата отбытия ⬆️\n\n'
             f'{chek2}\n\n'
             '<b>Цена: {total_amount} \n'
             'Валюта: {currency}\n</b>'
             f'Имя: {name}\n'
             f'Email: {email}\n'
             f'Номер: +{tel_num}').format(
                total_amount=message.successful_payment.total_amount // 100,
                currency=message.successful_payment.currency
            )
        )
        await state.finish()
    elif lang['lang'] == 'en':
        await bot.send_message(
            message.chat.id,
            ('Hooray!!\nYour payment was successful.\n\n'
             '1.Save the upstream QR-CODE to verify your identity at the reception\n\n'
             '2.If you lose the QR-CODE, contact the administrators of <b>Uzbegim</b>\n\n'
             f'3.Room category: {name2}\n'
             f'Date of arrival ⬇️\n\n'
             f'{chek1}\n\n'
             f'Departure date ⬆️\n\n'
             f'{chek2}\n\n'
             '<b>Price: {total_amount} \n'
             'Currency: {currency}\n</b>'
             f'Name: {name}\n'
             f'Email: {email}\n'
             f'Tel number: +{tel_num}').format(
                total_amount=message.successful_payment.total_amount // 100,
                currency=message.successful_payment.currency
            )
        )
        await state.finish()
    elif lang['lang'] == 'uz':
        await bot.send_message(message.chat.id,
                               ('Ura!\nToʻlovingiz muvaffaqiyatli boʻldi.\n\n'
                                '1. Qabulxonada shaxsingizni tasdiqlash uchun yuqori oqim QR-KODni saqlang\n\n'
                                '2. QR-KODni yo\'qotib qo\'ysangiz, <b>Uzbegim</b> administratorlariga murojaat qiling\n\n'
                                f'3.Xona toifasi: {name2}\n'
                                f'Kelish sanasi ⬇️\n\n'
                                f'{chek1}\n\n'
                                f'Ketish sanasi ⬆️\n\n'
                                f'{chek2}\n\n'
                                '<b>Narxi: {total_amount} \n'
                                'Valyuta: {currency}\n</b>'
                                f'Ism: {name}\n'
                                f'Email: {email}\n'
                                f'Tel raqam: +{tel_num}').format(
                                   total_amount=message.successful_payment.total_amount // 100,
                                   currency=message.successful_payment.currency
                               )
                               )
        await state.finish()
    await bot.send_message(ADMINS[0],
                           ('Номер забронирован!!!\n\n'
                            f'1.Категория номера: {name2}\n'
                            f'Дата прибытия ⬇️\n\n'
                            f'{chek1}\n\n'
                            f'Дата отбытия ⬆️\n\n'
                            f'{chek2}\n\n'
                            '<b>Цена: {total_amount} \n'
                            'Валюта: {currency}\n</b>'
                            f'Имя: {name}\n'
                            f'Email: {email}\n'
                            f'Номер: +{tel_num}\n'
                            f'Username: @{message.from_user.username}\n'
                            f'ID подтверждения: <code>{id2}</code>').format(
                               total_amount=message.successful_payment.total_amount // 100,
                               currency=message.successful_payment.currency
                           )
                           )
    await state.finish()

