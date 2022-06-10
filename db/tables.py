from sqlalchemy import VARCHAR, Column, ForeignKey, Integer
from sqlalchemy.orm import declarative_base, relationship

base = declarative_base()

class Student(base):

    __tablename__ = "student"
    student_id = Column(Integer, primary_key=True)
    fname = Column(VARCHAR(200))
    mname = Column(VARCHAR(200))
    lname = Column(VARCHAR(200))
    age = Column(Integer)

    def __repr__(self):
        return f"Student(student_id={self.student_id}, fname='{self.fname}', mname='{self.mname}', lname='{self.lname}')"

class Course(base):

    __tablename__ = "course"
    course_id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(200))
    handledclass = relationship("HandledClass", backref="course", cascade="all, delete-orphan")

    def __repr__(self):
        return f"Course(course_id={self.course_id}, name='{self.name}')"

class HandledClass(base):

    __tablename__ = "handledclass"
    class_id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("course.course_id"))