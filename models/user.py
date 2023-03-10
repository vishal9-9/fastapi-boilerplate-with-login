from sqlalchemy import Column, Integer, String
from database.config import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(250))
