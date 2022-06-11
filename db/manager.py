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

def get_handled_classes(db: Manager):
    return db.session.query(HandledClass).all()

def add_new_course(db: Manager, **kwargs):
    name = kwargs["name"]
    part = kwargs["part"]
    desc= kwargs["desc"]
    course = Course(name=name, part=part, desc=desc)
    db.session.add(course)
    db.session.commit()
    db.session.close()

def add_handled_class(db: Manager, **kwargs):
    course_name = kwargs["course"]
    student_ids = kwargs["student_ids"]
    sessions = kwargs["sessions"]
    schedule = kwargs["schedule"]
    time = kwargs["time"]
    handledclass = HandledClass()
    handledclass.sessions = sessions
    handledclass.schedule = schedule
    handledclass.time = time
    for student_id in student_ids:
        student = db.session.query(Student).filter(Student.student_id==student_id).first()
        handledclass.students.append(student)
    course = db.session.query(Course).filter(Course.name==course_name).first()
    course.handledclasses.append(handledclass)
    db.session.add(course)
    db.session.add(handledclass)
    db.session.commit()
    db.session.close()


