from sqlalchemy import Column, String, Integer, ForeignKey, Table, Text
from sqlalchemy.orm import relationship, backref

from .base import Base


groups_user_association = Table(
    'groups_users', Base.metadata,
    Column('group_id', Integer, ForeignKey('group.id')),
    Column('user_id', Integer, ForeignKey('user.id'))
)


class Group(Base):
    __tablename__ = 'group'

    id = Column(Integer, primary_key=True)
    group_name = Column(String)
    group_id = Column(String)
    users = relationship("User", secondary=groups_user_association,
                         backref=backref('groups',
                                         uselist=True, cascade='delete,all'))
    max_warns = Column(Integer)
    welcome_msg = Column(Text)
    rules = Column(Text)
    link = Column(Text)

    def __init__(self, group_name='', group_id=None, max_warns=0):
        self.group_name = group_name
        self.group_id = group_id
        self.max_warns = max_warns
