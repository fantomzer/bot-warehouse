from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.requests import show_item, show_items_type, find_item, show_stickers_type, find_sticker


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Наклейки', callback_data='Наклейки')],
    [InlineKeyboardButton(text='Покраска', callback_data='Покраска')]])


painting = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить предмет', callback_data='add_item')],
    [InlineKeyboardButton(text='Показать остатки', callback_data='items')],
    [InlineKeyboardButton(text='Главное меню', callback_data='Назад:')]])


stickers = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить наклейку', callback_data='add_sticker')],
    [InlineKeyboardButton(text='Показать остатки', callback_data='sticker_')],
    [InlineKeyboardButton(text='Главное меню', callback_data='Назад:')]])


add_nums = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1', callback_data='1'), InlineKeyboardButton(text='2', callback_data='2'),
     InlineKeyboardButton(text='3', callback_data='3')],
    [InlineKeyboardButton(text='4', callback_data='4'), InlineKeyboardButton(text='5', callback_data='5'),
     InlineKeyboardButton(text='6', callback_data='6')],
    [InlineKeyboardButton(text='7', callback_data='7'), InlineKeyboardButton(text='8', callback_data='8'),
     InlineKeyboardButton(text='9', callback_data='9')],
    [InlineKeyboardButton(text='0', callback_data='0'), InlineKeyboardButton(text='.', callback_data='.'),
     InlineKeyboardButton(text='<-', callback_data='-')],
    [InlineKeyboardButton(text='ввод', callback_data='ввод')]])


async def reply_nums():
    all_items = await show_item(1)
    keyboard = InlineKeyboardBuilder()
    for item in all_items:
        keyboard.add(InlineKeyboardButton(
            text=f'{item[0]} - {item[1]}',
            callback_data=f'изменить:{item[0]}'))
    return keyboard.adjust(1).as_markup()


async def find_items(name):
    items = await find_item(name)
    keyboard = InlineKeyboardBuilder()
    button = InlineKeyboardButton(text='Главное меню', callback_data='Назад:')
    for item in items:
        keyboard.add(InlineKeyboardButton(
            text=f'{item[0]} - {item[1]}',
            callback_data=f'остаток:{item[0]}'))
    keyboard.add(button)
    return keyboard.adjust(1).as_markup()


async def find_stickers(name):
    items = await find_sticker(name)
    keyboard = InlineKeyboardBuilder()
    button = InlineKeyboardButton(text='Главное меню', callback_data='Назад:')
    for item in items:
        keyboard.add(InlineKeyboardButton(
            text=f'{item[0]}-{item[1]}: {item[2]}',
            callback_data=f'остатокНак:{item[0]}:{item[1]}:{item[2]}'))
    keyboard.add(button)
    return keyboard.adjust(1).as_markup()


async def items_view(type_sort, type_keyboard):
    all_items = await show_items_type(type_sort)
    button1 = InlineKeyboardButton(text='Поиск', callback_data='поиск')
    button2 = InlineKeyboardButton(text='По алфавиту', callback_data=f'alphabet:{type_keyboard}')
    button3 = InlineKeyboardButton(text='По возрастанию', callback_data=f'count:{type_keyboard}')
    button4 = InlineKeyboardButton(text='По убыванию', callback_data=f'count_desc:{type_keyboard}')
    button5 = InlineKeyboardButton(text='Главное меню', callback_data='Назад:')
    if type_sort == 'alphabet':
        button2 = InlineKeyboardButton(text='✅По алфавиту', callback_data=f'alphabet:{type_keyboard}')
    elif type_sort == 'count':
        button3 = InlineKeyboardButton(text='✅По возрастанию', callback_data=f'count:{type_keyboard}')
    elif type_sort == 'count_desc':
        button4 = InlineKeyboardButton(text='✅По убыванию', callback_data=f'count_desc:{type_keyboard}')

    keyboard = InlineKeyboardBuilder()
    keyboard.add(button1, button2, button3, button4)
    for item in all_items:
        keyboard.add(InlineKeyboardButton(
            text=f'{item[0]} - {item[1]}',
            callback_data=f'{type_keyboard}:{item[0]}'))
    keyboard.add(button5)
    return keyboard.adjust(1, 3, 1).as_markup()


async def stickers_view(type_sort, type_keyboard):
    all_items = await show_stickers_type(type_sort)
    button1 = InlineKeyboardButton(text='Поиск', callback_data='поискНак')
    button2 = InlineKeyboardButton(text='По алфавиту', callback_data=f'alphabet:{type_keyboard}')
    button3 = InlineKeyboardButton(text='По возрастанию', callback_data=f'count:{type_keyboard}')
    button4 = InlineKeyboardButton(text='По убыванию', callback_data=f'count_desc:{type_keyboard}')
    button5 = InlineKeyboardButton(text='Главное меню', callback_data='Назад:')
    if type_sort == 'alphabet':
        button2 = InlineKeyboardButton(text='✅По алфавиту', callback_data=f'alphabet:{type_keyboard}')
    elif type_sort == 'count':
        button3 = InlineKeyboardButton(text='✅По возрастанию', callback_data=f'count:{type_keyboard}')
    elif type_sort == 'count_desc':
        button4 = InlineKeyboardButton(text='✅По убыванию', callback_data=f'count_desc:{type_keyboard}')

    keyboard = InlineKeyboardBuilder()
    keyboard.add(button1, button2, button3, button4)
    for item in all_items:
        keyboard.add(InlineKeyboardButton(
            text=f'{item[0]}-{item[1]}: {item[2]}|{item[3]}',
            callback_data=f'{type_keyboard}:{item[0]}:{item[1]}:{item[2]}:{item[3]}'))
    keyboard.add(button1, button2, button3, button4, button5)
    return keyboard.adjust(1, 3, 1).as_markup()


async def choice(type_choice):
    choices = [('➕', '+'), ('➖', '-')]
    keyboard = InlineKeyboardBuilder()
    for choice_ in choices:
        keyboard.add(InlineKeyboardButton(
            text=f'{choice_[0]}',
            callback_data=f'{type_choice}:{choice_[1]}'))
    keyboard.add(InlineKeyboardButton(text='Назад', callback_data='items'))
    return keyboard.adjust(1).as_markup()


async def choice_two(product_name):
    button_one = InlineKeyboardButton(text='✅Да', callback_data=f'удаление:{product_name}')
    button_two = InlineKeyboardButton(text='❌Нет', callback_data=f'отмена_удаления:{product_name}')
    keyboard = InlineKeyboardBuilder()
    keyboard.add(button_one, button_two)
    return keyboard.adjust(1).as_markup()


async def choice_three():
    choices = [('➕', '+'), ('➖', '-')]
    keyboard = InlineKeyboardBuilder()
    button = InlineKeyboardButton(text='Назад', callback_data='sticker_')
    for choice_ in choices:
        keyboard.add(InlineKeyboardButton(
            text=f'{choice_[0]}',
            callback_data=f'enter:{choice_[1]}'))
    keyboard.add(button)
    return keyboard.adjust(1).as_markup()


async def add_nums_two(keyb, enter):
    nums_two = [
        ('1', '1'), ('2', '2'), ('3', '3'),
        ('4', '4'), ('5', '5'), ('6', '6'),
        ('7', '7'), ('8', '8'), ('9', '9'),
        ('0', '0'), ('.', '.'), ('<-', '-'),
        ('ввод', f'{enter}')]
    keyboard = InlineKeyboardBuilder()
    for button in nums_two:
        keyboard.add(InlineKeyboardButton(
            text=f'{button[0]}',
            callback_data=f'{keyb}:{button[1]}'))
    return keyboard.adjust(3).as_markup()


set_type_sticker = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='одна', callback_data='одна'),
     InlineKeyboardButton(text='комплект', callback_data='комплект')]])


async def add_volume():
    nums_two = [
        ('0,2', '0,2'), ('0,45', '0,45'), ('0,9', '0,9'),
        ('1', '1'), ('2,7', '2,7'), ('4,5', '4,5'),
        ('5', '5'), ('9', '9'), ('18', '18'),
        ('1 кг', 'kg 1'), ('3 кг', 'kg 3'), ('10 кг', 'kg 10'),
        ('<-', '-'), ('ввод', 'ввод3')]
    keyboard = InlineKeyboardBuilder()
    for button in nums_two:
        keyboard.add(InlineKeyboardButton(
            text=f'{button[0]}',
            callback_data=f'кл_стикер:{button[1]}'))
    return keyboard.adjust(3).as_markup()


async def item_change(item):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=f'Изменить количество {item}', callback_data=f'изменить:{item}'),
                 InlineKeyboardButton(text=f'Удалить {item}', callback_data=f'подтверждение:{item}'),
                 InlineKeyboardButton(text='Назад', callback_data=f'items:{item}')
                 )
    return keyboard.adjust(1).as_markup()


async def sticker_change():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Изменить', callback_data=f'изменение_н'),
                 InlineKeyboardButton(text='Удалить', callback_data='н')
                 )
    return keyboard.adjust(1).as_markup()
