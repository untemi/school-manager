from app.config.database import db
from datetime import datetime

# Association table for many-to-many relationship between Group and Teacher
group_teacher = db.Table(
    "group_teacher",
    db.Column("group_id", db.Integer, db.ForeignKey("group.id"), primary_key=True),
    db.Column("teacher_id", db.Integer, db.ForeignKey("teacher.id"), primary_key=True),
)

class Log(db.Model):
    ACTION_CREATE = "create"
    ACTION_UPDATE = "update"
    ACTION_DELETE = "delete"
    
    ENTITY_STUDENT = "student"
    ENTITY_TEACHER = "teacher"
    ENTITY_GROUP = "group"
    
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    details = db.Column(db.String(500), nullable=True)
    entity_type = db.Column(db.String(50), nullable=False)

    @staticmethod
    def log_action(action, details, entity_type):
        log = Log(action=action, details=details, entity_type=entity_type)
        db.session.add(log)
        db.session.commit()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id"), nullable=False)

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    subject = db.Column(db.String(80), nullable=False)
    groups = db.relationship(
        "Group",
        secondary=group_teacher,
        lazy="subquery",
        backref=db.backref("teachers", lazy=True),
    )

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    students = db.relationship("Student", backref="group", lazy=True)
