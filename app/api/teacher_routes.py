from flask import render_template, request, redirect, url_for, flash
from app.config.database import db
from app.models import Teacher, Log
from app.auth.auth import login_required

def register_teacher_routes(app):
    @app.route("/teachers")
    @login_required
    def teachers():
        teachers = Teacher.query.all()
        return render_template("teachers.html", teachers=teachers)

    @app.route("/add_teacher", methods=["GET", "POST"])
    @login_required
    def add_teacher():
        if request.method == "POST":
            new_teacher = Teacher(
                first_name=request.form["first_name"],
                last_name=request.form["last_name"],
                email=request.form["email"],
                phone=request.form.get("phone"),
                subject=request.form["subject"],
                secondary_subjects=request.form.get("secondary_subjects"),
                notes=request.form.get("notes")
            )
            db.session.add(new_teacher)
            db.session.commit()
            Log.log_action("create", f"Added teacher: {new_teacher.full_name}", "teacher")
            flash("Teacher added successfully!", "success")
            return redirect(url_for("teachers"))

        return render_template("add_teacher.html")

    @app.route("/edit_teacher/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_teacher(id):
        teacher = Teacher.query.get_or_404(id)
        if request.method == "POST":
            old_name = teacher.full_name
            teacher.first_name = request.form["first_name"]
            teacher.last_name = request.form["last_name"]
            teacher.email = request.form["email"]
            teacher.phone = request.form.get("phone")
            teacher.subject = request.form["subject"]
            teacher.secondary_subjects = request.form.get("secondary_subjects")
            teacher.notes = request.form.get("notes")

            db.session.commit()
            Log.log_action("update", f"Modified teacher: {old_name} → {teacher.full_name}", "teacher")
            flash("Teacher updated successfully!", "success")
            return redirect(url_for("teachers"))

        return render_template("edit_teacher.html", teacher=teacher)

    @app.route("/delete_teacher/<int:id>")
    @login_required
    def delete_teacher(id):
        teacher = Teacher.query.get_or_404(id)
        name = teacher.full_name
        db.session.delete(teacher)
        db.session.commit()
        Log.log_action("delete", f"Deleted teacher: {name}", "teacher")
        flash("Teacher deleted successfully!", "success")
        return redirect(url_for("teachers"))
