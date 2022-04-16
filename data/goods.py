import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin

class Goods(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'goods'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='/static/img/anon.jpg')
    user = orm.relation('User')
