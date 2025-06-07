from app.config.database import db
from datetime import datetime

# many-to-many relationship Group <--> Teacher
group_teacher = db.Table(
    "group_teacher",
    db.Column("group_id", db.Integer, db.ForeignKey("group.id", ondelete="CASCADE"), primary_key=True),
    db.Column("teacher_id", db.Integer, db.ForeignKey("teacher.id", ondelete="CASCADE"), primary_key=True),
)

class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    details = db.Column(db.String(500), nullable=True)
    entity_type = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, nullable=True)

    @staticmethod
    def log_action(action, details, entity_type, user_id=None):
        log = Log(action=action, details=details, entity_type=entity_type, user_id=user_id)
        db.session.add(log)
        db.session.commit()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(1), nullable=False)  # 'M' or 'F'
    address = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    
    parent_name = db.Column(db.String(100), nullable=True)
    parent_email = db.Column(db.String(120), nullable=True)
    parent_phone = db.Column(db.String(20), nullable=True)
    
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    group_id = db.Column(db.Integer, db.ForeignKey("group.id", ondelete="SET NULL"), nullable=True)
    
    notes = db.Column(db.Text, nullable=True)
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        today = datetime.now().date()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    
    subject = db.Column(db.String(80), nullable=False)
    secondary_subjects = db.Column(db.String(200), nullable=True)
    
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    notes = db.Column(db.Text, nullable=True)
    
    groups = db.relationship(
        "Group",
        secondary=group_teacher,
        lazy="subquery",
        backref=db.backref("teachers", lazy=True),
        cascade="all, delete"
    )

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    code = db.Column(db.String(20), unique=True, nullable=True)
    
    academic_year = db.Column(db.String(9), nullable=False)
    
    capacity = db.Column(db.Integer, nullable=False, default=30)
    min_students = db.Column(db.Integer, nullable=True)
    max_students = db.Column(db.Integer, nullable=True)
    
    description = db.Column(db.String(200), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    
    students = db.relationship("Student", backref="group", lazy=True, cascade="all, delete-orphan")

    @property
    def student_count(self):
        return len(self.students)

    @property
    def has_capacity(self):
        return self.student_count < self.capacity
