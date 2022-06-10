from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from src.singleton import Singleton
import db.tables

class Manager(metaclass=Singleton):

    def __init__(self, parser):
        self.parser = parser
        self.engine = create_engine(
            "sqlite:///{db_name}.db".format(db_name=parser.get("database", "name"))
        )
        db.tables.base.metadata.create_all(self.engine)
        self.session = Session(self.engine)