"""Provide SQLAlchemy Base class for models to inherit."""
from sqlalchemy import orm

Base = orm.declarative_base()
