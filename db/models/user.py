from sqlalchemy import Column, String, Integer, Boolean

from .base import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    user_id = Column(String)
    total_warns = Column(Integer)
    is_adm = Boolean()

    def __init__(self, name, id, warns=0, is_adm=False):
        self.user_name = name
        self.user_id = id
        self.total_warns = warns
        self.is_adm = is_adm
