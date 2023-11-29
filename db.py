from typing import Annotated

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,Session
from fastapi import Depends
Base = declarative_base()


class SQLAlchemy:
    pass

class DB:
    def __init__(self):
        database_url = "postgresql://admin:admin@db:5432/book_service"

        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.metadata = MetaData(bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def get_db_dependency(self):
        return Annotated[Session, Depends(self.get_db)]
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()