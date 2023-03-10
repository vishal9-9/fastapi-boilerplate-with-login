from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from base.base_config import setting


engine = create_engine(url=setting.sql_url)
Session = sessionmaker(bind=engine, expire_on_commit=True)
Base = declarative_base()


def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()
