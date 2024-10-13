from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import database.requests as rq

router = Router()


class Add(StatesGroup):
    title = State()
    answer = State()
    number = State()


class Find(StatesGroup):
    title = State()


class UpdateItem(StatesGroup):
    title = State()
    change = State()
    number = State()


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


@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('это команда /help', reply_markup=kb.main)


@router.message(F.text == 'Изменить кол-во')
async def update_first(message: Message):
    await message.reply('⬇️Выберите название для изменения⬇️', reply_markup=await kb.reply_nums())


@router.callback_query(F.data.startswith('изменить:'))
async def update_second(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UpdateItem.title)
    res = callback.data.split(':')[1]
    await state.update_data(title=res)
    await state.set_state(UpdateItem.change)
    await callback.message.edit_text('⬇️Выберете действие⬇️', reply_markup=await kb.choice())


@router.callback_query(F.data.startswith('выбор:'))
async def update_third(callback: CallbackQuery, state: FSMContext):
    res = callback.data.split(':')[1]
    await state.update_data(change=res)
    await state.set_state(UpdateItem.number)
    await callback.message.edit_text('⬇️Выберите количество⬇️', reply_markup=await kb.add_nums_two())


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
    await callback.message.edit_text(f'{num_data}ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ᅠ ', reply_markup=await kb.add_nums_two())


@router.callback_query(F.data.endswith('ввод2'))
async def update_fourth(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(f'Число {data["number"]} принято📝')
    if data['change'] == '-':
        try:
            await rq.upgrade_item_count(data["title"], data["number"], data["change"])
            item = (await rq.show_item(data["title"])).fetchone()
            await callback.message.answer(f'Товар уменьшен🗂\nНазвание:{item[0]} - {data["number"]}={item[1]}',
                                          reply_markup=kb.main)
        except ValueError as err:
            await callback.message.answer(f'⛔️{err}⛔️', reply_markup=kb.main)
    elif data['change'] == '+':
        await rq.upgrade_item_count(data["title"], data["number"], data["change"])
        item = (await rq.show_item(data["title"])).fetchone()
        await callback.message.answer(f'Товар добавлен🗂\nНазвание:{item[0]} + {data["number"]}={item[1]}',
                                      reply_markup=kb.main)
    await rq.del_calculate(callback.message.chat.id)
    await state.clear()


@router.callback_query(F.data.startswith('Показать'))
async def show_sort_alphabet(callback: CallbackQuery):
    await callback.answer('Показать наименования')
    await callback.message.edit_text(
        '⬇️Наименования на складе⬇️',
        reply_markup=await kb.inline_nums('alphabet', 'остаток'))


@router.callback_query(F.data.startswith('поиск'))
async def item_find(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Find.title)
    await callback.message.edit_text('⬇️Введите название для поиска⬇️')


@router.message(Find.title)
async def add_third(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    data = await state.get_data()
    await message.reply('⬇️Результаты поиска⬇️', reply_markup=await kb.find_items(data["title"]))


@router.callback_query(F.data.endswith('остаток'))
async def show_sort(callback: CallbackQuery):
    await callback.answer('Сортировка')
    type_sort = callback.data.split(':')[0]
    await callback.message.edit_text(
        '⬇️Наименования на складе⬇️',
        reply_markup=await kb.inline_nums(type_sort, 'остаток'))


@router.callback_query(F.data.startswith('остаток'))
async def number(callback: CallbackQuery):
    await callback.answer('Выбор')
    res = callback.data.split(':')[1]
    item = (await rq.show_item(res)).fetchone()
    await callback.message.edit_text(
        f'Товар: {item[0]}\nКол-во: {item[1]}\nДата изменения: {item[2]}',
        reply_markup=await kb.item_change(item[0]))


@router.callback_query(F.data.startswith('Добавить'))
async def add_first(callback: CallbackQuery, state: FSMContext):
    await callback.answer('Добавление нового наименования')
    await state.set_state(Add.title)
    await callback.message.edit_text('⬇️Введите название для добавления⬇️')


@router.message(Add.title)
async def add_third(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(Add.number)
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
        await rq.add_item(data["title"], data["number"], 1)
        await callback.message.answer(
            f'Товар добавлен🗂\nНазвание: {data["title"]}\nКоличество: {data["number"]}',
            reply_markup=kb.main)
    except Exception as err:
        await callback.message.answer(f'⛔️{err}⛔️', reply_markup=kb.main)
    await rq.del_calculate(callback.message.chat.id)
    await state.clear()


@router.message(F.text == 'Удалить')
async def item_del(message: Message):
    await message.answer(
        '⬇️Выберите название для удаления⬇️',
        reply_markup=await kb.inline_nums('alphabet', 'подтверждение'))


@router.callback_query(F.data.endswith('подтверждение'))
async def show_item_del(callback: CallbackQuery):
    await callback.answer('Сортировка')
    type_sort = callback.data.split(':')[0]
    await callback.message.edit_text(
        '⬇️Выберите название для удаления⬇️',
        reply_markup=await kb.inline_nums(type_sort, 'подтверждение'))


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
