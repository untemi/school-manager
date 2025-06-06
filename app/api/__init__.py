from flask import render_template
from .student_routes import register_student_routes
from .teacher_routes import register_teacher_routes
from .group_routes import register_group_routes
from app.models.models import Log, Student, Teacher, Group
from app.auth.auth import login_required

def register_routes(app):
    @app.route("/")
    @login_required
    def home():
        logs = Log.query.order_by(Log.timestamp.desc()).limit(50).all()
        stats = {
            'student_count': Student.query.count(),
            'teacher_count': Teacher.query.count(),
            'group_count': Group.query.count()
        }
        return render_template("home.html", logs=logs, stats=stats)

    # Register all route modules
    register_student_routes(app)
    register_teacher_routes(app)
    register_group_routes(app)