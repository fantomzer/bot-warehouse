from sqlalchemy import String, Integer
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
    tg_id: Mapped[str] = mapped_column(String(100))
    user_name: Mapped[Optional[str]] = mapped_column(default=None)
    first_name: Mapped[Optional[str]] = mapped_column(default=None)
    calculate_str: Mapped[str] = mapped_column(String(100))


class Warehouse(Base):
    __tablename__: str = 'warehouses'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))


class Item(Base):
    __tablename__: str = 'items'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product_name: Mapped[str] = mapped_column(String(50), unique=True)
    product_number: Mapped[int] = mapped_column(Integer, default=1)
    product_count: Mapped[int] = mapped_column(Integer, default=1)


class Sticker(Base):
    __tablename__: str = 'stickers'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    sticker_name: Mapped[str] = mapped_column(String(50))
    sticker_volume: Mapped[str] = mapped_column(String(50))
    sticker_ahead: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    sticker_behind: Mapped[Optional[int]] = mapped_column(Integer, default=0)


class BottlingOil(Base):
    __tablename__: str = 'bottling_oil'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bottling_name: Mapped[str] = mapped_column(String(50))
    bottling_number: Mapped[int] = mapped_column(Integer)
    bottling_count: Mapped[int] = mapped_column(Integer, default=1)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
