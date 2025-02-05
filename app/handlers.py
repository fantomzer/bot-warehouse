from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import database.requests as rq

router = Router()


class AddItem(StatesGroup):
    title = State()
    answer = State()
    number = State()


class AddSticker(StatesGroup):
    title = State()
    volume = State()


class UpdateSticker(StatesGroup):
    title = State()
    volume = State()
    change = State()
    sticker_count = State()


class UpdateItem(StatesGroup):
    title = State()
    change = State()
    number = State()


class FindItem(StatesGroup):
    title = State()


class FindSticker(StatesGroup):
    title = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await rq.set_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name
    )
    await rq.del_calculate(message.from_user.id)
    await message.answer(f'Бот-склад📦\nГлавное меню📜', reply_markup=kb.main)


@router.callback_query(F.data.startswith('Назад:'))
async def cmd_start(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await rq.del_calculate(call.message.chat.id)
    await call.answer('Главное меню')
    await call.message.edit_text(f'Бот-склад📦\nГлавное меню📜', reply_markup=kb.main)


@router.callback_query(F.data.startswith('Наклейки'))
async def cmd_start(call: CallbackQuery):
    await call.answer('Наклейки')
    await call.message.edit_text('Склад: наклейки', reply_markup=kb.stickers)


@router.callback_query(F.data.startswith('sticker_'))
async def show_sort_alphabet(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Показать наклейки')
    await callback.message.edit_text(
        '⬇️Наклейки на складе⬇️',
        reply_markup=await kb.stickers_view('alphabet', 'остатокНак'))


@router.callback_query(F.data.endswith('поискНак'))
async def item_find(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FindSticker.title)
    await callback.message.answer('⬇️Введите название для поиска⬇️')


@router.message(FindSticker.title)
async def add_third(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    data = await state.get_data()
    await message.answer('⬇️Результаты поиска⬇️', reply_markup=await kb.find_stickers(data["title"]))


@router.callback_query(F.data.startswith('остатокНак'))
async def number(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Выбор')
    title, volume = callback.data.split(':')[1], callback.data.split(':')[2]
    item = (await rq.show_sticker(title=title, volume=volume)).fetchone()
    await state.set_state(UpdateSticker.title)
    await state.update_data(title=title)
    await state.set_state(UpdateSticker.volume)
    await state.update_data(volume=volume)
    await state.set_state(UpdateSticker.change)
    await callback.message.edit_text(
        f'Наклейка: <b>{item[0]}</b>\nОбъём: <b>{item[1]}</b>\nКоличество: <b>{item[2]}</b>',
        reply_markup=await kb.choice_three())


@router.callback_query(F.data.endswith('остатокНак'))
async def update_second(callback: CallbackQuery):
    await callback.answer('Сортировка')
    type_sort = callback.data.split(':')[0]
    await callback.message.edit_text(
        '⬇️Наклейки на складе⬇️',
        reply_markup=await kb.stickers_view(type_sort, 'остатокНак'))


@router.callback_query(F.data.startswith('enter:'))
async def update_third(callback: CallbackQuery, state: FSMContext):
    res = callback.data.split(':')[1]
    await state.update_data(change=res)
    await state.set_state(UpdateSticker.sticker_count)
    await callback.message.edit_text('⬇️Выберите количество⬇️',
                                     reply_markup=await kb.add_nums_two('кл_3', 'sticker'))


@router.callback_query(F.data.in_(['кл_3:1', 'кл_3:2', 'кл_3:3', 'кл_3:4', 'кл_3:5', 'кл_3:6', 'кл_3:7', 'кл_3:8',
                                   'кл_3:9', 'кл_3:0', 'кл_3:.', 'кл_3:-']))
async def callback_func_two(callback: CallbackQuery, state: FSMContext):
    user_id, data = callback.message.chat.id, callback.data.split(':')[1]
    try:
        await rq.calculate_str(user_id, data)
    except Exception as exp:
        await callback.answer(f'{exp}')
    num_data = await rq.get_calculate(user_id)
    await state.update_data(number=num_data)
    await callback.message.edit_text(f'{num_data}ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ',
                                     reply_markup=await kb.add_nums_two('кл_3', '|sticker'))


@router.callback_query(F.data.endswith('|sticker'))
async def update_fourth(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(f'Число {data["number"]} принято📝')
    if data['change'] == '-':
        try:
            await rq.upgrade_sticker_count(data["title"], data["volume"], data["number"], data["change"])
            item = (await rq.show_sticker(data["title"], data["volume"])).fetchone()
            await callback.message.answer(f'<b>{item[0]}</b> - <b>{item[1]}</b> : <b>{item[2]}</b>')
            await callback.message.answer('Бот-склад📦\nГлавное меню📜', reply_markup=kb.main)
        except ValueError as err:
            await callback.message.answer(f'⛔️{err}⛔️', reply_markup=kb.main)
    elif data['change'] == '+':
        await rq.upgrade_sticker_count(data["title"], data["volume"], data["number"], data["change"])
        item = (await rq.show_sticker(data["title"], data["volume"])).fetchone()
        await callback.message.answer(f'<b>{item[0]}</b> + <b>{item[1]}</b> : <b>{item[2]}</b>')
        await callback.message.answer('Бот-склад📦\nГлавное меню📜', reply_markup=kb.main)
    await rq.del_calculate(callback.message.chat.id)
    await state.clear()


@router.callback_query(F.data.startswith('Покраска'))
async def cmd_start(call: CallbackQuery):
    await call.answer('Покраска')
    await call.message.edit_text('Склад: материалы', reply_markup=kb.painting)


@router.callback_query(F.data.startswith('изменить:'))
async def update_second(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UpdateItem.title)
    res = callback.data.split(':')[1]
    await state.update_data(title=res)
    await state.set_state(UpdateItem.change)
    await callback.message.edit_text('⬇️Выберете действие⬇️', reply_markup=await kb.choice('выборкол'))


@router.callback_query(F.data.startswith('выборкол:'))
async def update_third(callback: CallbackQuery, state: FSMContext):
    res = callback.data.split(':')[1]
    await state.update_data(change=res)
    await state.set_state(UpdateItem.number)
    await callback.message.edit_text('⬇️Выберите количество⬇️',
                                     reply_markup=await kb.add_nums_two('кл_2', 'ввод2'))


@router.callback_query(F.data.in_(['кл_2:1', 'кл_2:2', 'кл_2:3', 'кл_2:4', 'кл_2:5', 'кл_2:6', 'кл_2:7', 'кл_2:8',
                                   'кл_2:9', 'кл_2:0', 'кл_2:.', 'кл_2:-']))
async def callback_func_two(callback: CallbackQuery, state: FSMContext):
    user_id, data = callback.message.chat.id, callback.data.split(':')[1]
    try:
        await rq.calculate_str(user_id, data)
    except Exception as exp:
        await callback.answer(f'{exp}')
    num_data = await rq.get_calculate(user_id)
    await state.update_data(number=num_data)
    await callback.message.edit_text(f'{num_data}ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ',
                                     reply_markup=await kb.add_nums_two('кл_2', 'ввод2'))


@router.callback_query(F.data.endswith('ввод2'))
async def update_fourth(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(f'Число {data["number"]} принято📝')
    if data['change'] == '-':
        try:
            await rq.upgrade_item_count(data["title"], data["number"], data["change"])
            item = (await rq.show_item(data["title"])).fetchone()
            await callback.message.answer(f'Товар уменьшен🗂\nНазвание:<b>{item[0]}</b>\nКоличество: <b>{item[1]}</b>')
            await callback.message.answer('Бот-склад📦\nГлавное меню📜', reply_markup=kb.main)
        except ValueError as err:
            await callback.message.answer(f'⛔️{err}⛔️', reply_markup=kb.main)
    elif data['change'] == '+':
        await rq.upgrade_item_count(data["title"], data["number"], data["change"])
        item = (await rq.show_item(data["title"])).fetchone()
        await callback.message.answer(f'Товар добавлен🗂\nНазвание:<b>{item[0]}</b>\nКоличество: <b>{item[1]}</b>')
        await callback.message.answer('Бот-склад📦\nГлавное меню📜', reply_markup=kb.main)
    await rq.del_calculate(callback.message.chat.id)
    await state.clear()


@router.callback_query(F.data.startswith('изменитьшт:'))
async def update_second(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UpdateItem.title)
    res = callback.data.split(':')[1]
    await state.update_data(title=res)
    await state.set_state(UpdateItem.change)
    await callback.message.edit_text('⬇️Выберете действие⬇️', reply_markup=await kb.choice('выборшт'))


@router.callback_query(F.data.startswith('выборшт:'))
async def update_third(callback: CallbackQuery, state: FSMContext):
    res = callback.data.split(':')[1]
    await state.update_data(change=res)
    await state.set_state(UpdateItem.number)
    await callback.message.edit_text('⬇️Выберите количество⬇️',
                                     reply_markup=await kb.add_nums_two('кл_3', 'ввод4'))


@router.callback_query(F.data.in_(['кл_3:1', 'кл_3:2', 'кл_3:3', 'кл_3:4', 'кл_3:5', 'кл_3:6', 'кл_3:7', 'кл_3:8',
                                   'кл_3:9', 'кл_3:0', 'кл_3:.', 'кл_3:-']))
async def callback_func_two(callback: CallbackQuery, state: FSMContext):
    user_id, data = callback.message.chat.id, callback.data.split(':')[1]
    try:
        await rq.calculate_str(user_id, data)
    except Exception as exp:
        await callback.answer(f'{exp}')
    num_data = await rq.get_calculate(user_id)
    await state.update_data(number=num_data)
    await callback.message.edit_text(f'{num_data}ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ',
                                     reply_markup=await kb.add_nums_two('кл_3', 'ввод4'))


@router.callback_query(F.data.endswith('ввод4'))
async def update_fourth(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(f'Число {data["number"]} принято📝')
    if data['change'] == '-':
        try:
            await rq.upgrade_item_number(data["title"], data["number"], data["change"])
            item = (await rq.show_item(data["title"])).fetchone()
            await callback.message.answer(f'Товар уменьшен🗂\nНазвание:<b>{item[0]}</b>\nШтуки: <b>{item[2]}</b>')
            await callback.message.answer('Бот-склад📦\nГлавное меню📜', reply_markup=kb.main)
        except ValueError as err:
            await callback.message.answer(f'⛔️{err}⛔️', reply_markup=kb.main)
    elif data['change'] == '+':
        await rq.upgrade_item_number(data["title"], data["number"], data["change"])
        item = (await rq.show_item(data["title"])).fetchone()
        await callback.message.answer(f'Товар добавлен🗂\nНазвание:<b>{item[0]}</b>\nШтуки: <b>{item[2]}</b>')
        await callback.message.answer('Бот-склад📦\nГлавное меню📜', reply_markup=kb.main)
    await rq.del_calculate(callback.message.chat.id)
    await state.clear()


@router.callback_query(F.data.startswith('items'))
async def show_sort_alphabet(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer('Показать наименования')
    await callback.message.edit_text(
        '⬇️Наименования на складе⬇️',
        reply_markup=await kb.items_view('alphabet', 'остаток'))


@router.callback_query(F.data.startswith('поиск'))
async def item_find(callback: CallbackQuery, state: FSMContext):
    await state.set_state(FindItem.title)
    await callback.message.edit_text('⬇️Введите название для поиска⬇️')


@router.message(FindItem.title)
async def add_third(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    data = await state.get_data()
    await message.answer('⬇️Результаты поиска⬇️', reply_markup=await kb.find_items(data["title"]))


@router.callback_query(F.data.endswith('остаток'))
async def show_sort(callback: CallbackQuery):
    await callback.answer('Сортировка')
    type_sort = callback.data.split(':')[0]
    await callback.message.edit_text(
        '⬇️Наименования на складе⬇️',
        reply_markup=await kb.items_view(type_sort, 'остаток'))


@router.callback_query(F.data.startswith('остаток'))
async def number(callback: CallbackQuery):
    await callback.answer('Выбор')
    res = callback.data.split(':')[1]
    item = (await rq.show_item(res)).fetchone()
    await callback.message.edit_text(
        f'Товар: <b>{item[0]}</b>\nКол-во: <b>{item[1]}</b>',
        reply_markup=await kb.item_change(item[0]))


@router.callback_query(F.data.startswith('add_item'))
async def add_first(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Добавление нового наименования')
    await state.set_state(AddItem.title)
    await callback.message.edit_text('⬇️Введите название для добавления⬇️')


@router.message(AddItem.title)
async def add_second(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddItem.number)
    await message.reply('⬇️Выберите количество⬇️', reply_markup=kb.add_nums)


@router.callback_query(F.data.in_(['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '.', '-']))
async def callback_func(callback: CallbackQuery, state: FSMContext):
    user_id, data = callback.message.chat.id, callback.data
    try:
        await rq.calculate_str(user_id, data)
    except Exception as exp:
        await callback.answer(f'{exp}')
    num_data = await rq.get_calculate(user_id)
    await state.update_data(number=num_data)
    await callback.message.edit_text(f'{num_data}ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ', reply_markup=kb.add_nums)


@router.callback_query(F.data.endswith('ввод'))
async def add_fourth(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(f'Число {data["number"]} принято📝')
    try:
        await rq.add_item(data["title"], data["number"])
        await callback.message.answer(
            f'Товар добавлен🗂\nНазвание: <b>{data["title"]}</b>\nКоличество: <b>{data["number"]}</b>')
        await callback.message.answer('Бот-склад📦\nГлавное меню📜', reply_markup=kb.main)
    except Exception as err:
        await callback.message.answer(f'⛔️{err}⛔️', reply_markup=kb.main)
    await rq.del_calculate(callback.message.chat.id)
    await state.clear()


@router.callback_query(F.data.startswith('add_sticker'))
async def add_first(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Добавление наклейки')
    await state.set_state(AddSticker.title)
    await callback.message.edit_text('⬇️Введите название наклейки для добавления⬇️')


@router.message(AddSticker.title)
async def add_second(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AddSticker.volume)
    await message.reply('⬇️Выберите объём⬇️', reply_markup=await kb.add_volume())


@router.callback_query(F.data.in_(['кл_стикер:0,2', 'кл_стикер:0,45', 'кл_стикер:0,9', 'кл_стикер:1',
                                   'кл_стикер:2,7', 'кл_стикер:4,5', 'кл_стикер:5', 'кл_стикер:9',
                                   'кл_стикер:18', 'кл_стикер:kg 1', 'кл_стикер:kg 3', 'кл_стикер:kg 10',
                                   'кл_стикер:-']))
async def callback_func(callback: CallbackQuery, state: FSMContext):
    user_id, data = callback.message.chat.id, callback.data.split(':')[1]
    try:
        await rq.volume_selection(user_id, data)
    except Exception as exp:
        await callback.answer(f'{exp}')
    volume_data = await rq.get_calculate(user_id)
    await state.update_data(volume=volume_data)
    await callback.message.edit_text(f'{volume_data}ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ', reply_markup=await kb.add_volume())


@router.callback_query(F.data.endswith('ввод3'))
async def add_fifth(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(f'Наклейка {data["title"]} принята📝')
    try:
        await rq.add_sticker(data["title"], data["volume"])
        await callback.message.answer(
            f'Наклейка добавлена🗂\nНазвание: <b>{data["title"]}</b>\nОбъемы: <b>{data["volume"]}</b>')
        await callback.message.answer('Бот-склад📦\nГлавное меню📜', reply_markup=kb.main)
    except Exception as err:
        await callback.message.answer(f'⛔️{err}⛔️', reply_markup=kb.main)
    await rq.del_calculate(callback.message.chat.id)
    await state.clear()


@router.message(F.text == 'Удалить')
async def item_del(message: Message):
    await message.answer(
        '⬇️Выберите название для удаления⬇️',
        reply_markup=await kb.items_view('alphabet', 'подтверждение'))


@router.callback_query(F.data.endswith('подтверждение'))
async def show_item_del(callback: CallbackQuery):
    await callback.answer('Сортировка')
    type_sort = callback.data.split(':')[0]
    await callback.message.edit_text(
        '⬇️Выберите название для удаления⬇️',
        reply_markup=await kb.items_view(type_sort, 'подтверждение'))


@router.callback_query(F.data.startswith('подтверждение'))
async def item_del_choice(callback: CallbackQuery):
    res = callback.data.split(':')[1]
    await callback.answer(f'Вы точно хотите удалить {res} ❓', show_alert=True)
    await callback.message.edit_text('Выбор', reply_markup=await kb.choice_two(res))


@router.callback_query(F.data.startswith('отмена_удаления:'))
async def item_del_cancel(callback: CallbackQuery):
    res = callback.data.split(':')[1]
    await callback.message.edit_text('Отмена')
    await callback.message.answer(f'Удаление {res} отменено❗️', reply_markup=kb.main)


@router.callback_query(F.data.startswith('удаление:'))
async def item_del_confirm(callback: CallbackQuery):
    res = callback.data.split(':')[1]
    await callback.message.edit_text(f'Удаление {res}')
    await rq.del_item(res)
    await callback.message.answer(f'❌Товар: {res} удалён❌', reply_markup=kb.main)
