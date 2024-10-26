from database.models import async_session
from database.models import User, Item, Sticker
from sqlalchemy import select, update, delete


async def set_user(tg_id, user_name, first_name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, user_name=user_name, first_name=first_name, calculate_str='_'))
            await session.commit()


async def find_item(name):
    list_name = name.split(' ')
    if len(list_name) == 1:
        async with async_session() as session:
            return await session.execute(
                select(Item.product_name, Item.product_number)
                .where(Item.product_name.like(f'{list_name[0].lower()}%')))
    elif len(list_name) == 2:
        async with async_session() as session:
            return await session.execute(
                select(Item.product_name, Item.product_number)
                .where(Item.product_name.like(f'{list_name[0].lower()}%'))
                .where(Item.product_name.like(f'% {list_name[1].lower()}%')))
    elif len(list_name) >= 3:
        async with async_session() as session:
            return await session.execute(
                select(Item.product_name, Item.product_number)
                .where(Item.product_name.like(f'{list_name[0].lower()}%'))
                .where(Item.product_name.like(f'% {list_name[1].lower()}%'))
                .where(Item.product_name.like(f'% {list_name[2].lower()}%')))


async def find_sticker(name):
    list_name = name.split(' ')
    if len(list_name) == 1:
        async with async_session() as session:
            return await session.execute(
                select(Sticker.sticker_name, Sticker.sticker_volume, Sticker.sticker_ahead)
                .where(Sticker.sticker_name.like(f'{list_name[0].upper()}%')))
    elif len(list_name) == 2:
        async with async_session() as session:
            return await session.execute(
                select(Sticker.sticker_name, Sticker.sticker_volume, Sticker.sticker_ahead)
                .where(Sticker.sticker_name.like(f'{list_name[0].upper()}%'))
                .where(Sticker.sticker_name.like(f'% {list_name[1].upper()}%')))
    elif len(list_name) >= 3:
        async with async_session() as session:
            return await session.execute(
                select(Sticker.sticker_name, Sticker.sticker_volume, Sticker.sticker_ahead)
                .where(Sticker.sticker_name.like(f'{list_name[0].upper()}%'))
                .where(Sticker.sticker_name.like(f'% {list_name[1].upper()}%'))
                .where(Sticker.sticker_name.like(f'% {list_name[2].upper()}%')))


async def add_item(title, number):
    async with async_session() as session:
        item = await session.scalar(select(Item).where(Item.product_name == title.lower()))

        if not item:
            session.add(Item(
                product_name=title.lower(),
                product_number=number
            ))
            await session.commit()
        elif item:
            raise KeyError(f'Наименование {title} уже есть в базе данных')


async def show_items_type(type_sort):
    if type_sort == 'alphabet':
        async with async_session() as session:
            return await session.execute(
                select(Item.product_name, Item.product_number)
                .order_by(Item.product_name))
    elif type_sort == 'count':
        async with async_session() as session:
            return await session.execute(
                select(Item.product_name, Item.product_number)
                .order_by(Item.product_number))
    elif type_sort == 'count_desc':
        async with async_session() as session:
            return await session.execute(
                select(Item.product_name, Item.product_number)
                .order_by(Item.product_number.desc()))


async def show_item(prod_name):
    async with async_session() as session:
        return await session.execute(
            select(Item.product_name, Item.product_number)
            .where(Item.product_name == prod_name)
        )


async def show_sticker(title, volume):
    async with async_session() as session:
        return await session.execute(
            select(Sticker.sticker_name, Sticker.sticker_volume, Sticker.sticker_ahead)
            .where(Sticker.sticker_name == title)
            .where(Sticker.sticker_volume == volume)
        )


async def show_all_sticker():
    async with async_session() as session:
        return await session.execute(
            select(Sticker.sticker_name, Sticker.sticker_volume, Sticker.sticker_ahead)
            .order_by(Sticker.sticker_ahead.desc())
        )


async def show_stickers_type(type_sort):
    if type_sort == 'alphabet':
        async with async_session() as session:
            return await session.execute(
                select(Sticker.sticker_name, Sticker.sticker_volume, Sticker.sticker_ahead, Sticker.sticker_behind)
                .order_by(Sticker.sticker_name))
    elif type_sort == 'count':
        async with async_session() as session:
            return await session.execute(
                select(Sticker.sticker_name, Sticker.sticker_volume, Sticker.sticker_ahead, Sticker.sticker_behind)
                .order_by(Sticker.sticker_ahead))
    elif type_sort == 'count_desc':
        async with async_session() as session:
            return await session.execute(
                select(Sticker.sticker_name, Sticker.sticker_volume, Sticker.sticker_ahead, Sticker.sticker_behind)
                .order_by(Sticker.sticker_ahead.desc()))


async def calculate_str(user_id, number):
    async with async_session() as session:
        res = await session.scalar(select(User.calculate_str).where(User.tg_id == str(user_id)))
        if res == '_':
            await session.execute(
                update(User)
                .where(User.tg_id == str(user_id))
                .values(calculate_str=number))
            await session.commit()
        elif number == '-':
            if len(res) != 0:
                result = res[:-1]
                await session.execute(
                    update(User)
                    .where(User.tg_id == str(user_id))
                    .values(calculate_str=result))
                await session.commit()
            else:
                raise Exception(f'Строка полностью очищена')
        else:
            result = res + str(number)
            await session.execute(
                update(User)
                .where(User.tg_id == str(user_id))
                .values(calculate_str=result))
            await session.commit()


async def get_calculate(user_id):
    async with async_session() as session:
        res = await session.scalar(select(User.calculate_str).where(User.tg_id == str(user_id)))
    return res


async def del_calculate(user_id):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == str(user_id)).values(calculate_str='_'))
        await session.commit()


async def volume_selection(user_id, volume):
    async with async_session() as session:
        res = await session.scalar(select(User.calculate_str).where(User.tg_id == str(user_id)))
        if res == '_':
            await session.execute(
                update(User)
                .where(User.tg_id == str(user_id))
                .values(calculate_str=str(volume)))
            await session.commit()
        elif volume == '-':
            if len(res) != 0:
                result_list = res.split('|')[:-1]
                result_str = '|'.join(result_list)
                await session.execute(
                    update(User)
                    .where(User.tg_id == str(user_id))
                    .values(calculate_str=result_str))
                await session.commit()
            else:
                raise Exception(f'Строка полностью очищена')
        else:
            result = res + '|' + str(volume)
            await session.execute(
                update(User)
                .where(User.tg_id == str(user_id))
                .values(calculate_str=result))
            await session.commit()


async def upgrade_item_count(product_name, number, symbol):
    async with async_session() as session:
        res = await session.scalar(select(Item.product_number).where(Item.product_name == product_name))

        if symbol == '-':
            if float(number) > float(res):
                raise ValueError(f'Число {number} не может быть больше остатка')

            result = float(res) - float(number)
            await session.execute(
                update(Item)
                .where(Item.product_name == product_name)
                .values(count_product=result))
            await session.commit()
        elif symbol == '+':
            result = float(res) + float(number)
            await session.execute(
                update(Item)
                .where(Item.product_name == product_name)
                .values(count_product=result))
            await session.commit()


async def del_item(product_name):
    async with async_session() as session:
        await session.execute(delete(Item).where(Item.product_name == product_name))
        await session.commit()


async def add_sticker(title, volume):
    async with async_session() as session:
        volume_list = volume.split('|')
        for vol in volume_list:
            sticker = await session.scalar(
                select(Sticker)
                .where(Sticker.sticker_name == title.upper())
                .where(Sticker.sticker_volume == vol))

            if not sticker:
                session.add(Sticker(
                    sticker_name=title.upper(),
                    sticker_volume=vol
                ))
                await session.commit()

            elif sticker:
                raise KeyError(f'Наименование {title} {volume} уже есть в базе данных')


async def upgrade_sticker_count(title, volume, number, symbol):
    async with async_session() as session:
        res = await session.scalar(
            select(Sticker.sticker_ahead)
            .where(Sticker.sticker_name == title)
            .where(Sticker.sticker_volume == volume))

        if symbol == '-':
            if int(number) > int(res):
                raise ValueError(f'Число {number} не может быть больше остатка')

            result = int(res) - int(number)
            await session.execute(
                update(Sticker)
                .where(Sticker.sticker_name == title)
                .where(Sticker.sticker_volume == volume)
                .values(sticker_ahead=result))
            await session.commit()
        elif symbol == '+':
            result = int(res) + int(number)
            await session.execute(
                update(Sticker)
                .where(Sticker.sticker_name == title)
                .where(Sticker.sticker_volume == volume)
                .values(sticker_ahead=result))
            await session.commit()
