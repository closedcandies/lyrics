import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .sessions import SqlAlchemyBase


class Track(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'Track'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    artist_id = sqlalchemy.Column(sqlalchemy.Integer)
