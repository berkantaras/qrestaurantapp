# coding: utf-8
from sqlalchemy import Column, DateTime, Float, Integer, String, Table, Text, text
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    email = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    password_hash = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    api_key = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    status = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)


class DeliveryOrder(Base):
    __tablename__ = 'delivery_orders'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, nullable=False)
    menu_id = Column(Integer, nullable=False)
    qty = Column(Integer, nullable=False)
    address = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    phone = Column(String(255, 'utf8mb4_unicode_ci'))
    notes = Column(String(255, 'utf8mb4_unicode_ci'))
    price_total = Column(Float(asdecimal=True), nullable=False)
    status = Column(Integer, nullable=False, server_default=text("0"))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Desk(Base):
    __tablename__ = 'desks'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    capacity = Column(Integer, nullable=False)
    available = Column(Integer, nullable=False, server_default=text("1"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Menu(Base):
    __tablename__ = 'menus'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    description = Column(Text(collation='utf8mb4_unicode_ci'), nullable=False)
    category_id = Column(Integer, nullable=False)
    price = Column(Float(asdecimal=True), nullable=False)
    image = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class Migration(Base):
    __tablename__ = 'migrations'

    id = Column(Integer, primary_key=True)
    migration = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    batch = Column(Integer, nullable=False)


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, nullable=False)
    status = Column(Integer, nullable=False, server_default=text("0"))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


t_password_resets = Table(
    'password_resets', metadata,
    Column('email', String(255, 'utf8mb4_unicode_ci'), nullable=False, index=True),
    Column('token', String(255, 'utf8mb4_unicode_ci'), nullable=False),
    Column('created_at', DateTime)
)


class PlaceOrder(Base):
    __tablename__ = 'place_orders'

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, nullable=False)
    desk_id = Column(Integer, nullable=False)
    menu_id = Column(Integer, nullable=False)
    qty = Column(Integer, nullable=False)
    price_total = Column(Float(asdecimal=True), nullable=False)
    status = Column(Integer, nullable=False, server_default=text("0"))
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Promotion(Base):
    __tablename__ = 'promotions'

    id = Column(Integer, primary_key=True)
    menu_id = Column(Integer, nullable=False)
    image = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    email = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False, unique=True)
    password = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False)
    remember_token = Column(String(100, 'utf8mb4_unicode_ci'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
