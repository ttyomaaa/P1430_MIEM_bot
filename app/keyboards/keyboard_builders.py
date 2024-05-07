from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from enums.texts import CipherData, text_by_number


def inline_keyboard_maker(keyboard_pool: list, identity: str, mode: int) -> InlineKeyboardMarkup:

    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    for i in range(len(keyboard_pool)):
        kb_builder.row(InlineKeyboardButton(
            text=keyboard_pool[i],
            callback_data="%s%s" % (identity, i))
        )
    if mode != 0:
        kb_builder.row(InlineKeyboardButton(text="Назад", callback_data="back"))

    return kb_builder.as_markup()


def inline_keyboard_maker_webapp(keyboard_pool: list, identity: str, mode: int, cipher_code: str) \
        -> InlineKeyboardMarkup:

    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    cipher_name = text_by_number(cipher_number=cipher_code, text_type="en_name")
    url_link = 'https://ttyomaaa.github.io/p1430webapp/' + cipher_name + '/history/'

    if not CipherData.is_available(getattr(CipherData, cipher_name)):
        url_link = 'https://ttyomaaa.github.io/p1430webapp/none/'

    kb_builder.row(InlineKeyboardButton(text="Историческая справка", web_app=WebAppInfo(url=url_link)))

    for i in range(len(keyboard_pool)):
        kb_builder.row(InlineKeyboardButton(
            text=keyboard_pool[i],
            callback_data="%s%s" % (identity, i))
        )
    if mode != 0:
        kb_builder.row(InlineKeyboardButton(text="Назад", callback_data="back"))

    return kb_builder.as_markup()


def reply_keyboard_maker(keyboard_pool: list, cipher_code: str, mode: int) -> ReplyKeyboardMarkup:

    kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

    cipher_name = text_by_number(cipher_number=cipher_code, text_type="en_name")
    if mode == 0:
        url_link = 'https://ttyomaaa.github.io/p1430webapp/' + cipher_name + '/examples/encode/'
    else:
        url_link = 'https://ttyomaaa.github.io/p1430webapp/' + cipher_name + '/examples/decode/'
    if not CipherData.is_available(getattr(CipherData, cipher_name)):
        url_link = 'https://ttyomaaa.github.io/p1430webapp/none/'

    if cipher_code == CipherData.enigma.number:
        if mode == 0:
            example_text = "Процедура шифрования"
        else:
            example_text = "Процедура расшифрования"
    elif cipher_code == CipherData.des.number or cipher_code == CipherData.threefish.number:
        if mode == 0:
            example_text = "Алгоритм шифрования"
        else:
            example_text = "Алгоритм расшифрования"
    elif cipher_code == CipherData.keccak.number:
        example_text = "Алгоритм хеширования"
    else:
        example_text = "Показать пример"
    kb_builder.row(KeyboardButton(text=example_text, web_app=WebAppInfo(url=url_link)))
    for i in range(len(keyboard_pool)):
        kb_builder.row(KeyboardButton(text=keyboard_pool[i]))

    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def matrix_maker() -> InlineKeyboardMarkup:

    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    for i in range(0, 36):
        kb_builder.add(InlineKeyboardButton(
            text='('+','.join([str(nums+1) for nums in divmod(i, 6)])+')',
            callback_data="bn"+'('+','.join([str(nums+1) for nums in divmod(i, 6)])+')')
        )
    kb_builder.adjust(6)
    kb_builder.row(InlineKeyboardButton(text="Пробел", callback_data="bn "))
    kb_builder.row(InlineKeyboardButton(text="Расшифровать сообщение", callback_data="end"))

    return kb_builder.as_markup()


def generate_maker() -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    kb_builder.row(InlineKeyboardButton(text="Сгенерировать случайный", callback_data="gen"))
    kb_builder.row(InlineKeyboardButton(text="Подтвердить", callback_data="yes"))
    return kb_builder.as_markup()
