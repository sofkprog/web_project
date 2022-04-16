import datetime
import sqlalchemy

from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin

class Corzina(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'corzina'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    content = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    image = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='/static/img/anon.jpg')