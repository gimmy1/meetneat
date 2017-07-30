# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

Base = declarative_base()


class User(Base):
    """docstring for User."""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(32), index=True)
    password_hash = Column(String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)


class Restaurant(Base):
    """docstring for Restaurant.Base"""
    __tablename__ = 'restaurant'
    id = Column(Integer, primary_key=True)
    restaurant_name = Column(String)
    restaurant_address = Column(String)
    restaurant_image = Column(String)

    # add a property decorator to serialize information from this dataset
    @property
    def serialize(self):
        return {
            'restaurant_name': self.restaurant_name,
            'restaurant_address': self.restaurant_address,
            'restaurant_image': self.restaurant_image,
            'id': self.id
        }

engine = create_engine('sqlite:///restaruants.db')
Base.metadata.create_all(engine)
