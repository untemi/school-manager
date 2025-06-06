from flask import render_template, request, redirect, url_for
from app.config.database import db
from app.models.models import Student, Group, Log
from app.auth.auth import login_required

def register_student_routes(app):
    @app.route("/students")
    @login_required
    def students():
        students = Student.query.all()
        return render_template("students.html", students=students)

    @app.route("/add_student", methods=["GET", "POST"])
    @login_required
    def add_student():
        if request.method == "POST":
            name = request.form["name"]
            email = request.form["email"]
            age = request.form["age"]
            group_id = request.form["group_id"]
            new_student = Student(name=name, email=email, age=age, group_id=group_id)
            db.session.add(new_student)
            db.session.commit()
            Log.log_action("create", f"Ajout de l'élève: {name}", "student")
            return redirect(url_for("students"))
        groups = Group.query.all()
        return render_template("add_student.html", groups=groups)

    @app.route("/edit_student/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_student(id):
        student = Student.query.get_or_404(id)
        if request.method == "POST":
            old_name = student.name
            student.name = request.form["name"]
            student.email = request.form["email"]
            student.age = request.form["age"]
            student.group_id = request.form["group_id"]
            db.session.commit()
            Log.log_action("update", f"Modification de l'élève: {old_name} → {student.name}", "student")
            return redirect(url_for("students"))
        groups = Group.query.all()
        return render_template("edit_student.html", student=student, groups=groups)

    @app.route("/delete_student/<int:id>")
    @login_required
    def delete_student(id):
        student = Student.query.get_or_404(id)
        name = student.name
        db.session.delete(student)
        db.session.commit()
        Log.log_action("delete", f"Suppression de l'élève: {name}", "student")
        return redirect(url_for("students"))
