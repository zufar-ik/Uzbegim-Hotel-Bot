from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
First_menu_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Номера 🏨', callback_data='nomer')],
        [InlineKeyboardButton(text='Сайт 🌐', url='https://www.youtube.com/')],
        [InlineKeyboardButton(text='Связаться с нами! 📫', callback_data='sos')],
        [InlineKeyboardButton(text='Настройки ⚙️', callback_data='settings')]
    ],

)

First_menu_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=('Rooms 🏨'), callback_data='nomer')],
        [InlineKeyboardButton(text=('Website 🌐'), url='https://www.youtube.com/')],
        [InlineKeyboardButton(text=('Connect with us! 📫'), callback_data='sos')],
        [InlineKeyboardButton(text=('Settings ⚙️'), callback_data='settings')]
    ],

)

First_menu_uz = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=('Xonalar 🏨'), callback_data='nomer')],
        [InlineKeyboardButton(text=('Veb-sayt 🌐'), url='https://www.youtube.com/')],
        [InlineKeyboardButton(text=('Biz bilan bogʻlaning! 📫'), callback_data='sos')],
        [InlineKeyboardButton(text='Sozlamalar ⚙️', callback_data='settings')]
    ],

)

lang1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=('Русский 🇷🇺'), callback_data='ru')],
        [InlineKeyboardButton(text=('English 🇬🇧'), callback_data='en')],
        [InlineKeyboardButton(text=("O'zbek 🇺🇿"), callback_data='uz')],
    ]
)


cash_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Ю Kassa 🇷🇺', callback_data='yukassa'),InlineKeyboardButton(text='Click 🇺🇿', callback_data='click')],
        [InlineKeyboardButton(text='Unlimint 🇺🇸', callback_data='unlimint')],
        [InlineKeyboardButton(text='Back 🔙', callback_data='back4')]
    ]
)


cash_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Ю Kassa 🇷🇺', callback_data='yukassa'),InlineKeyboardButton(text='Click 🇺🇿', callback_data='click')],
        [InlineKeyboardButton(text='Unlimint 🇺🇸', callback_data='unlimint')],
        [InlineKeyboardButton(text='Назад 🔙', callback_data='back4')]
    ]
)

cash_uz = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Ю Kassa 🇷🇺', callback_data='yukassa'),InlineKeyboardButton(text='Click 🇺🇿', callback_data='click')],
        [InlineKeyboardButton(text='Unlimint 🇺🇸', callback_data='unlimint')],
        [InlineKeyboardButton(text='Orqaga 🔙', callback_data='back4')]
    ]
)

back6_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Оплатить 💳", pay=True)],
        [InlineKeyboardButton(text='Назад 🔙', callback_data='back6')]
    ]
)
back6_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Pay 💳", pay=True)],
        [InlineKeyboardButton(text='Back 🔙', callback_data='back6')]
    ]
)
back6_uz = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="To'lash 💳", pay=True)],
        [InlineKeyboardButton(text='Orqaga 🔙', callback_data='back6')]
    ]
)

back_uz = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Orqaga 🔙',callback_data='back')]
    ]
)

back_ru = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Назад 🔙',callback_data='back')]
    ]
)

back_en = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Back 🔙',callback_data='back')]
    ]
)