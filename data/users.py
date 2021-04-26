import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from flask_login import UserMixin
from .sessions import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'User'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    email = sqlalchemy.Column(sqlalchemy.String)
    hashed_password = sqlalchemy.Column(sqlalchemy.String)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def create_password(self, password):
        self.hashed_password = generate_password_hash(password)