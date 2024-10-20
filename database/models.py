from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from typing import Optional

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__: str = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    user_name: Mapped[str] = mapped_column()
    first_name: Mapped[str] = mapped_column()
    calculate_str: Mapped[str]


class Warehouse(Base):
    __tablename__: str = 'warehouses'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))


class Item(Base):
    __tablename__: str = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    product_name: Mapped[str] = mapped_column(String(25), unique=True)
    count_product: Mapped[float] = mapped_column()
    count_max: Mapped[float] = mapped_column()
    data_add: Mapped[str] = mapped_column()
    warehouse: Mapped[int] = mapped_column(ForeignKey('warehouses.id'))


class Sticker(Base):
    __tablename__: str = 'stickers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sticker_name: Mapped[str] = mapped_column(String(50))
    sticker_volume: Mapped[str] = mapped_column(String(50))
    sticker_count: Mapped[Optional[int]] = mapped_column(default=0)
    sticker_type: Mapped[Optional[str]] = mapped_column(String(25), default=None)
    type: Mapped[Optional[str]] = mapped_column(String(50))


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
