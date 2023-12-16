from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton


def apply_keyboard(builder:ReplyKeyboardBuilder, buttons: list[KeyboardButton] = None):
    for button in buttons:
        builder.add(button)
    builder.adjust(1)
    markup = builder.as_markup()
    builder = None
    return markup

def apply_inline_keyboard(builder: InlineKeyboardBuilder, buttons: list[InlineKeyboardButton] = None):
    for button in buttons:
        builder.add(button)
    builder.adjust(1)
    markup = builder.as_markup()
    builder = None
    return markup   


def start_keyboard():
    start_builder = ReplyKeyboardBuilder()
    buttons = [
        KeyboardButton(text="➖Добавить расход"),
        KeyboardButton(text="➕Добавить доход"),
        KeyboardButton(text="📊Посмотреть расходы за временной период"),
    ]
    return apply_keyboard(builder=start_builder, buttons=buttons)


def categories_keyboard():
    """Кейборд для группы вопросов"""
    categories_builder = ReplyKeyboardBuilder()
    buttons = [
            KeyboardButton(text='Продукты питания'),
            KeyboardButton(text='Жилье'),
            KeyboardButton(text='Транспорт'),
            KeyboardButton(text='Медицинские расходы'),
            KeyboardButton(text='Одежда и обувь'),
            KeyboardButton(text='Развлечения'),
            KeyboardButton(text='Образование'),
            KeyboardButton(text='Сотовая связь и интернет'),
            KeyboardButton(text='Домашние животные'),
            KeyboardButton(text='Спорт и фитнес'),
            KeyboardButton(text='Страхование'),
            KeyboardButton(text='Интернет-шопинг и покупка товаров для дома'),
            KeyboardButton(text='Семейные мероприятия'),
            KeyboardButton(text='Электроэнергия и коммунальные услуги'),
            KeyboardButton(text='Долги и кредитные обязательства'),
            KeyboardButton(text='Налоги'),
            KeyboardButton(text='Оплата услуг'),
            KeyboardButton(text='Бытовая техника и электроника'),
            KeyboardButton(text='Проездной билет'),
            KeyboardButton(text='Инвестиции и сбережения'),
            KeyboardButton(text='↩️Отмена'),
    ]
    return apply_keyboard(builder=categories_builder, buttons=buttons)

def cancel_keyboard():
    """Кейборд для группы вопросов"""
    cancel_builder = ReplyKeyboardBuilder()
    buttons = [
            KeyboardButton(text='↩️Отмена'),
    ]
    return apply_keyboard(builder=cancel_builder, buttons=buttons)

def remove_expense_keyboard():
    remove_builder = InlineKeyboardBuilder()
    buttons = [
            InlineKeyboardButton(text='❌', callback_data="delete_expense_btn"),
    ]
    return apply_inline_keyboard(builder=remove_builder, buttons=buttons)
