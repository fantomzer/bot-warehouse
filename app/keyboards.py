from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.requests import show_item, show_items_type, find_item, show_sticker_line


main = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Наклейки', callback_data='Наклейки')],
    [InlineKeyboardButton(text='Покраска', callback_data='Покраска')]])


painting = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить', callback_data='add_warehouse')],
    [InlineKeyboardButton(text='Показать остатки', callback_data='warehouse')],
    [InlineKeyboardButton(text='Главное меню', callback_data='Назад:')]])


stickers = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='SILVER', callback_data='silver')],
    [InlineKeyboardButton(text='ECO', callback_data='eco')],
    [InlineKeyboardButton(text='EXPERT', callback_data='expert')],
    [InlineKeyboardButton(text='Показать остатки', callback_data='stickers')],
    [InlineKeyboardButton(text='Добавить наклейку', callback_data='sticker_add')],
    [InlineKeyboardButton(text='Главное меню', callback_data='Назад:')]])

silver = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Краска для дерева', callback_data='краска для дерева:silver')],
    [InlineKeyboardButton(text='Масла', callback_data='масла:silver')],
    [InlineKeyboardButton(text='Пропитка и антисептик', callback_data='пропитка и антисептик:silver')],
    [InlineKeyboardButton(text='Интерьерные краски', callback_data='интерьерные краски:silver')],
    [InlineKeyboardButton(text='Гидроизоляционная система', callback_data='гидроизоляционная система:silver')],
    [InlineKeyboardButton(text='Грунт', callback_data='грунт:silver')],
    [InlineKeyboardButton(text='Назад', callback_data='Наклейки')]])

eco = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Краска для дерева', callback_data='краска для дерева:eco')],
    [InlineKeyboardButton(text='Масла', callback_data='масла:eco')],
    [InlineKeyboardButton(text='Пропитка', callback_data='пропитка')],
    [InlineKeyboardButton(text='Интерьерные краски', callback_data='интерьерные краски:eco')],
    [InlineKeyboardButton(text='Фасадные краски', callback_data='фасадные краски:eco')],
    [InlineKeyboardButton(text='Назад', callback_data='Наклейки')]])

expert = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='WF EXPERT база А', callback_data='wfa:expert')],
    [InlineKeyboardButton(text='WF EXPERT база C', callback_data='wfc:expert')],
    [InlineKeyboardButton(text='WP EXPERT грунт для дерева', callback_data='wp exp:expert')],
    [InlineKeyboardButton(text='WO EXPERT масло для н. р.', callback_data='wo exp:expert')],
    [InlineKeyboardButton(text='Назад', callback_data='Наклейки')]])

main2 = InlineKeyboardMarkup(inline_keyboard=[
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


async def show_stickers_line(prod_line):
    items = await show_sticker_line(prod_line)
    keyboard = InlineKeyboardBuilder()
    button = InlineKeyboardButton(text='Главное меню', callback_data='Назад:')
    for item in items:
        keyboard.add(InlineKeyboardButton(
            text=f'{item[0]} - {item[1]}: {item[2]}',
            callback_data=f'изменение_н:{item[0]}:{item[1]}'))
    keyboard.add(button)
    return keyboard.adjust(1).as_markup()


async def inline_nums(type_sort, type_keyboard):
    all_items = await show_items_type(type_sort, 1)
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


async def choice():
    choices = [('➕', '+'), ('➖', '-')]
    keyboard = InlineKeyboardBuilder()
    for choice_ in choices:
        keyboard.add(InlineKeyboardButton(
            text=f'{choice_[0]}',
            callback_data=f'выбор:{choice_[1]}'))
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
    for choice_ in choices:
        keyboard.add(InlineKeyboardButton(
            text=f'{choice_[0]}',
            callback_data=f'enter:{choice_[1]}'))
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
    keyboard.add(InlineKeyboardButton(text=f'Изменить {item}', callback_data=f'изменить:{item}'),
                 InlineKeyboardButton(text=f'Удалить {item}', callback_data=f'подтверждение:{item}')
                 )
    return keyboard.adjust(1).as_markup()


async def sticker_change():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Изменить', callback_data=f'изменение_н'),
                 InlineKeyboardButton(text='Удалить', callback_data='н')
                 )
    return keyboard.adjust(1).as_markup()
