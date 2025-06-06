from flask import render_template, request, redirect, url_for, flash
from app.config.database import db
from app.models.models import Student, Group, Log
from app.auth.auth import login_required
from datetime import datetime

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
            new_student = Student(
                first_name=request.form["first_name"],
                last_name=request.form["last_name"],
                email=request.form["email"],
                date_of_birth=datetime.strptime(request.form["date_of_birth"], "%Y-%m-%d"),
                gender=request.form["gender"],
                address=request.form.get("address"),
                phone=request.form.get("phone"),
                parent_name=request.form.get("parent_name"),
                parent_email=request.form.get("parent_email"),
                parent_phone=request.form.get("parent_phone"),
                notes=request.form.get("notes"),
                group_id=request.form.get("group_id")
            )
            db.session.add(new_student)
            db.session.commit()
            Log.log_action("create", f"Added student: {new_student.full_name}", "student")
            flash("Student added successfully!", "success")
            return redirect(url_for("students"))
            
        groups = Group.query.all()
        return render_template("add_student.html", groups=groups)

    @app.route("/edit_student/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_student(id):
        student = Student.query.get_or_404(id)
        if request.method == "POST":
            old_name = student.full_name
            student.first_name = request.form["first_name"]
            student.last_name = request.form["last_name"]
            student.email = request.form["email"]
            student.date_of_birth = datetime.strptime(request.form["date_of_birth"], "%Y-%m-%d")
            student.gender = request.form["gender"]
            student.address = request.form.get("address")
            student.phone = request.form.get("phone")
            student.parent_name = request.form.get("parent_name")
            student.parent_email = request.form.get("parent_email")
            student.parent_phone = request.form.get("parent_phone")
            student.notes = request.form.get("notes")
            student.group_id = request.form.get("group_id")
            
            db.session.commit()
            Log.log_action("update", f"Modified student: {old_name} → {student.full_name}", "student")
            flash("Student updated successfully!", "success")
            return redirect(url_for("students"))

        groups = Group.query.all()
        return render_template("edit_student.html", student=student, groups=groups)

    @app.route("/delete_student/<int:id>")
    @login_required
    def delete_student(id):
        student = Student.query.get_or_404(id)
        name = student.full_name
        db.session.delete(student)
        db.session.commit()
        Log.log_action("delete", f"Deleted student: {name}", "student")
        flash("Student deleted successfully!", "success")
        return redirect(url_for("students"))
