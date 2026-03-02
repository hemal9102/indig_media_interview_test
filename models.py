from fastapi import FastAPI
from sqlalchemy.orm import relationship
from database import base
from sqlalchemy import Column, Integer, String, ForeignKey
# making a subject class to add subjects and connect with question and question can be add or delete
class Subject(base):
    __tablename__ = "subjects"
    id = Column(Integer,primary_key = True ,  index = True)
    name = Column(String , unique = True , index = True)
    questions = relationship("question" , cascade = "all, delete-orphan")

    # child class question
class Question(Subject):
    __tablename__ = "quesions"
    id = Column(Integer,primary_key = True ,  index = True)
    quesion_text = Column(String, index=True)
    option_a = Column(String)
    option_b = Column(String)
    option_c = Column(String)
    option_d = Column(String)

    correct_option = Column(String)
    # can be chosen from a,b,c,d
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    subject = relationship("Subject", back_populates="questions")
