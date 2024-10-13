import datetime

from database.models import async_session
from database.models import User, Warehouse, Item
from sqlalchemy import select, update, delete


async def set_user(tg_id, user_name, first_name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, user_name=user_name, first_name=first_name, calculate_str='_'))
            await session.commit()


async def find_item(name):
    async with async_session() as session:
        return await session.execute(
            select(Item.product_name, Item.count_product)
            .where(Item.product_name.like(f'%{name.lower()}%')))


async def add_item(title, number, warehouse):
    async with async_session() as session:
        item = await session.scalar(select(Item).where(Item.product_name == title.lower()))

        if not item:
            session.add(Item(
                product_name=title.lower(),
                count_product=number,
                count_max=number,
                data_add=datetime.datetime.now().strftime('%Y-%m-%d'),
                warehouse=warehouse
            ))
            await session.commit()
        elif item:
            raise KeyError(f'Наименование {title} уже есть в базе данных')


async def show_items_type(type_sort, warehouse):
    if type_sort == 'alphabet':
        async with async_session() as session:
            return await session.execute(
                select(Item.product_name, Item.count_product)
                .where(Item.warehouse == warehouse)
                .order_by(Item.product_name))
    elif type_sort == 'count':
        async with async_session() as session:
            return await session.execute(
                select(Item.product_name, Item.count_product)
                .where(Item.warehouse == warehouse)
                .order_by(Item.count_product))
    elif type_sort == 'count_desc':
        async with async_session() as session:
            return await session.execute(
                select(Item.product_name, Item.count_product)
                .where(Item.warehouse == warehouse)
                .order_by(Item.count_product.desc()))


async def calculate_str(user_id, number):
    async with async_session() as session:
        res = await session.scalar(select(User.calculate_str).where(User.tg_id == user_id))
        if res == '_':
            await session.execute(
                update(User)
                .where(User.tg_id == user_id)
                .values(calculate_str=number))
            await session.commit()
        elif number == '-':
            if len(res) != 0:
                result = res[:-1]
                await session.execute(
                    update(User)
                    .where(User.tg_id == user_id)
                    .values(calculate_str=result))
                await session.commit()
            else:
                raise Exception(f'Строка полностью очищена')
        else:
            result = res + str(number)
            await session.execute(
                update(User)
                .where(User.tg_id == user_id)
                .values(calculate_str=result))
            await session.commit()


async def get_calculate(user_id):
    async with async_session() as session:
        res = await session.scalar(select(User.calculate_str).where(User.tg_id == user_id))
    return res


async def del_calculate(user_id):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == user_id).values(calculate_str='_'))
        await session.commit()


async def upgrade_item_count(product_name, number, symbol):
    async with async_session() as session:
        res = await session.scalar(select(Item.count_product).where(Item.product_name == product_name))
        if float(number) > float(res):
            raise ValueError(f'Число {number} не может быть больше остатка')
        elif symbol == '-':
            result = float(res) - float(number)
            await session.execute(
                update(Item)
                .where(Item.product_name == product_name)
                .values(count_product=result, data_add=datetime.datetime.now().strftime('%Y-%m-%d')))
            await session.commit()
        elif symbol == '+':
            result = float(res) + float(number)
            await session.execute(
                update(Item)
                .where(Item.product_name == product_name)
                .values(count_product=result, data_add=datetime.datetime.now().strftime('%Y-%m-%d')))
            await session.commit()


async def del_item(product_name):
    async with async_session() as session:
        await session.execute(delete(Item).where(Item.product_name == product_name))
        await session.commit()
