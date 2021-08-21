"""SQLAlchemy model"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as pg

from basic_app.models import base

class User(base.Base):
    """Defines user table"""
    __tablename__ = 'user'

    id = sa.Column('id', pg.UUID(as_uuid=True), primary_key=True)

    email = sa.Column('email', sa.String(128), unique=True, nullable=False)

    username = sa.Column('username', sa.String(128), nullable=False)

    password = sa.Column('password', sa.String(), nullable=False)

    create_time = sa.Column('create_time',
        sa.TIMESTAMP(timezone=True), nullable=False)

    update_time = sa.Column('update_time',
        sa.TIMESTAMP(timezone=True), nullable=False)

    def __repr__(self):
        return '<User(id={},email={})>'.format(self.id, self.email)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
