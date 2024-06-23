import bcrypt
from sqlalchemy import Column, String, Integer

from Reflex_fastapi_with_admin.databases.database import Base
from Reflex_fastapi_with_admin.utils.Decoders import JsonEncodedDict


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False)
    name = Column(String(100), nullable=False)
    avatar = Column(String(100))
    company_logo_url = Column(String(100))
    password = Column(String(100), nullable=False)
    roles = Column(JsonEncodedDict)

    def __init__(self, **kwargs):
        if 'password' in kwargs:
            password = kwargs.pop('password')
            kwargs['password'] = self.hash_password(password)
        super().__init__(**kwargs)

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))