from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from src.singleton import Singleton
from db.tables import *

class Manager(metaclass=Singleton):

    def __init__(self, parser):
        self.parser = parser
        self.engine = create_engine(
            "sqlite:///{db_name}.db".format(db_name=parser.get("database", "name"))
        )
        base.metadata.create_all(self.engine)
        self.session = Session(self.engine)

def get_student(db: Manager, student_id: int):
    return db.session.query(Student).filter(Student.student_id==student_id).first()

def get_students(db: Manager):
    return db.session.query(Student).all()

def get_students_in_class(db: Manager, handledclass_id: int):
    return db.session.query(Student).filter(HandledClass.handledclass_id==handledclass_id).join(HandledClass).all()

def get_courses(db: Manager):
    return db.session.query(Course).all()