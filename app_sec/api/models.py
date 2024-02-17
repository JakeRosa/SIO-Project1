from typing import Any

from flask_login import UserMixin
from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        String)
from sqlalchemy.orm import (as_declarative, declarative_base, declared_attr,
                            relationship)
from sqlalchemy.sql import func


base = declarative_base()


class User(UserMixin, base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(120), unique=True)
    role = Column(String(50))
    profile_picture = Column(String(500), nullable=False, default='profile-picture-not-found.png')
    password = Column(String(128))
    # user has many reviews
    reviews = relationship("Review", backref="user", lazy=True)
    # user has many orders
    orders = relationship("Order", backref="user", lazy=True)
    # user has one wishlist
    wishlist = relationship("Wishlist", backref="user", lazy=True)

    def __repr__(self):
        return "<User %r>" % self.email

class Review(base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    rating = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    comment = Column(String(500))

    def __repr__(self):
        return "<reviews %r>" % self.id


class Product(base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String(500))
    price = Column(Float)
    image = Column(
        String(500),
        nullable=False,
        default='image-not-found.png')
    # adicionei esta linha para o stock
    stock_quantity = Column(Integer, default=0)
    if stock_quantity == "0":
        in_stock = Column(Boolean, default=False)
    else:
        in_stock = Column(Boolean, default=True)
    # product has many orders
    order_items = relationship("OrderItem", backref="product", lazy=True)
    # product has many reviews
    reviews = relationship("Review", backref="product", lazy=True)
    # product has many wishlists
    wishlist_product = relationship("WishlistProduct", backref="product", lazy=True)

    def __repr__(self):
        return "<Product %r>" % self.name


class OrderItem(base):
    __tablename__ = "order_items"
    order_id = Column(
        Integer,
        ForeignKey("orders.id"),
        primary_key=True,
    )
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    quantity = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())

    def __repr__(self):
        return "<OrderItem %r>" % self.id


class Order(base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    # adicionei esta linha para o relacionamento com a tabela de associação
    order_items = relationship("OrderItem", backref="order", lazy=True)
    created_at = Column(DateTime, server_default=func.now())
    is_finished = Column(Boolean, default=False)
    total_price = Column(Float)

    def __repr__(self):
        return "<Order %r>" % self.id

class Wishlist(base):
    __tablename__ = "wishlists"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    wishlist_product = relationship('WishlistProduct', backref='wishlist', lazy=True)

    def __repr__(self):
        return "<WishList %r>" % self.id

class WishlistProduct(base):
    __tablename__ = "wishlist_products"
    wishlist_id = Column(
        Integer,
        ForeignKey("wishlists.id"),
        primary_key=True,
    )
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)

    def __repr__(self):
        return "<WishlistProduct %r>" % self.id
