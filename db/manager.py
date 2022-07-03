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

def get_app_links(db: Manager):
    return db.session.query(Link).filter(Link.group == "app_links").all()

def get_app_link(db: Manager, name):
    return db.session.query(Link).filter(Link.name == name, Link.group == "app_links").first()

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

def get_handled_class(db: Manager, handledclass_id: int):
    return db.session.query(HandledClass).filter(HandledClass.handledclass_id==handledclass_id).first()

def get_session_attendance_in_class(db: Manager, handledclass_id: int, session: int):
    return db.session.query(ClassAttendance).filter(ClassAttendance.handledclass_id==handledclass_id, ClassAttendance.session==session).all()

def get_course_in_handledclass(db: Manager, handledclass_id: int):
    return db.session.query(HandledClass).filter(HandledClass.handledclass_id==handledclass_id).first().course

def add_new_link(db: Manager, name, group, url):
    link = Link(name=name, group=group, url=url)
    db.session.add(link)
    db.session.commit()
    db.session.close()

def add_new_course(db: Manager, **kwargs):
    name = kwargs["name"]
    part = kwargs["part"]
    desc= kwargs["desc"]
    assignments = kwargs["assignments"]
    activities = kwargs["activities"]
    quizzes = kwargs["quizzes"]
    course = Course(
        name=name, 
        part=part, 
        desc=desc, 
        assignments=assignments, 
        activities=activities, 
        quizzes=quizzes
    )
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
        for session_number in range(sessions):
            classattendance = ClassAttendance(session=session_number+1)
            student.classattendances.append(classattendance)
            handledclass.classattendances.append(classattendance)
        handledclass.students.append(student)
    course = db.session.query(Course).filter(Course.name==course_name).first()
    course.handledclasses.append(handledclass)
    db.session.add(course)
    db.session.add(handledclass)
    db.session.commit()
    db.session.close()

def update_app_link(db: Manager, name, url):
    link = db.session.query(Link).filter(Link.name == name, Link.group == "app_links").first()
    link.url = url
    db.session.add(link)
    db.session.commit()
    db.session.close()

def update_handledclass_current_session(db: Manager, handledclass_id: int, current_session: int):
    handledclass = db.session.query(HandledClass).filter(HandledClass.handledclass_id==handledclass_id).first()
    handledclass.current_session = current_session
    db.session.add(handledclass)
    db.session.commit()
    db.session.close()

def update_class_attendance_status(db: Manager, classattendance_id: int, status: str):
    classattendance = db.session.query(ClassAttendance).filter(ClassAttendance.classattendance_id==classattendance_id).first()
    classattendance.status = status
    db.session.add(classattendance)
    db.session.commit()
    db.session.close()

def delete_app_link(db: Manager, name):
    link = db.session.query(Link).filter(Link.name == name, Link.group == "app_links").first()
    db.session.delete(link)
    db.session.commit()
    db.session.close()

def delete_handledclass(db: Manager, handledclass_id: int):
    handledclass = db.session.query(HandledClass).filter(HandledClass.handledclass_id==handledclass_id)
    db.session.delete(handledclass)
    db.session.commit()
    db.session.close()

def delete_student(db: Manager, student_id: int):
    student = db.session.query(Student).filter(Student.student_id==student_id).first()
    db.session.delete(student)
    db.session.commit()
    db.session.close()

def delete_course(db: Manager, course_id: int):
    course = db.session.query(Course).filter(Course.course_id==course_id).first()
    db.session.delete(course)
    db.session.commit()
    db.session.close()

def get_all_links(db: Manager):
    return db.session.query(Link).all()