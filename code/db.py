'''
Author: flwfdd
Date: 2022-03-09 13:37:03
LastEditTime: 2022-08-28 21:33:05
Description: 数据库
_(:з」∠)_
'''
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import class_mapper
import datetime

db = SQLAlchemy()

def add(x):
    db.session.add(x)


def add_all(x):
    db.session.add_all(x)


def flush():
    db.session.flush()


def commit():
    db.session.commit()


def to_dict(model):
    if type(model) == list:
        return [to_dict(i) for i in model]
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c, getattr(model, c)) for c in columns)


class Exam(db.Model):
    __tablename__ = 'exam'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title= db.Column(db.Text, default="考试名称")
    intro= db.Column(db.Text, default="考试介绍")
    limit_time=db.Column(db.Integer, default=42)
    random=db.Column(db.Integer, default=0)
    active=db.Column(db.Boolean, default=True)

class Problem(db.Model):
    __tablename__ = 'problem'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type=db.Column(db.String(24), nullable=False)
    text=db.Column(db.Text, nullable=False)
    data=db.Column(db.Text)
    answer=db.Column(db.Text, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    exam = db.Column(db.Integer, nullable=False)
    active=db.Column(db.Boolean, default=True)
    
class ExamLog(db.Model):
    __tablename__ = 'exam_log'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    exam = db.Column(db.Integer, nullable=False)
    name=db.Column(db.String(42), nullable=False)
    problems=db.Column(db.Text, nullable=False)
    answers=db.Column(db.Text, nullable=False)
    scores=db.Column(db.Text, nullable=False)
    submit_answers=db.Column(db.Text)
    full_score=db.Column(db.Integer, nullable=False)
    score=db.Column(db.Integer)
    start_time=db.Column(db.DateTime, default=datetime.datetime.now)
    end_time= db.Column(db.DateTime)

