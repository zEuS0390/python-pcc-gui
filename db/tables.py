from sqlalchemy import VARCHAR, Column, ForeignKey, Integer
from sqlalchemy.orm import declarative_base, relationship

base = declarative_base()

class Link(base):

    __tablename__="link"
    link_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(200))
    group = Column(VARCHAR(200))
    url = Column(VARCHAR(8000))
    def __repr__(self):
        return f"Link(link_id={self.link_id}, group='{self.group}', url='{self.url}')"

class Student(base):

    __tablename__ = "student"
    student_id = Column(Integer, primary_key=True)
    handledclass_id = Column(Integer, ForeignKey("handledclass.handledclass_id"))
    fname = Column(VARCHAR(200))
    mname = Column(VARCHAR(200))
    lname = Column(VARCHAR(200))
    gender = Column(VARCHAR(200))
    age = Column(Integer)
    email = Column(VARCHAR(200))
    classattendances = relationship("ClassAttendance", backref="student", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Student(student_id={self.student_id}, fname='{self.fname}', mname='{self.mname}', lname='{self.lname}', gender='{self.gender}', age={self.age})"

class Course(base):

    __tablename__ = "course"
    course_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(200))
    part = Column(VARCHAR(200))
    desc = Column(VARCHAR(200))
    assignments = Column(VARCHAR(200))
    activities = Column(VARCHAR(200))
    quizzes = Column(VARCHAR(200))
    handledclasses = relationship("HandledClass", backref="course", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Course(course_id={self.course_id}, name='{self.name}')"

class HandledClass(base):

    __tablename__ = "handledclass"
    handledclass_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("course.course_id", ondelete="CASCADE"))
    schedule = Column(VARCHAR(200))
    time = Column(VARCHAR(200))
    sessions = Column(Integer, default=10)
    current_session = Column(Integer, default=0)
    students = relationship("Student", backref="handledclass")
    classattendances = relationship("ClassAttendance", backref="handledclass", cascade="all, delete-orphan")

class ClassAttendance(base):

    __tablename__ = "classattendance"
    classattendance_id = Column(Integer, primary_key=True)
    handledclass_id = Column(Integer, ForeignKey("handledclass.handledclass_id"))
    student_id = Column(Integer, ForeignKey("student.student_id"))
    session = Column(Integer)
    status = Column(VARCHAR(200))

    def __repr__(self):
        return f"ClassAttendance(classattendance_id={self.classattendance_id}, handledclass_id={self.handledclass.handledclass_id}, student_id={self.student.student_id}, session={self.session}, status='{self.status}')"