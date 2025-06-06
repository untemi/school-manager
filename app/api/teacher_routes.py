from flask import render_template, request, redirect, url_for
from app.config.database import db
from app.models.models import Teacher, Log
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
            name = request.form["name"]
            email = request.form["email"]
            subject = request.form["subject"]
            new_teacher = Teacher(name=name, email=email, subject=subject)
            db.session.add(new_teacher)
            db.session.commit()
            Log.log_action("create", f"Ajout du professeur {name} ({subject})", "teacher")
            return redirect(url_for("teachers"))
        return render_template("add_teacher.html")

    @app.route("/edit_teacher/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_teacher(id):
        teacher = Teacher.query.get_or_404(id)
        if request.method == "POST":
            old_name = teacher.name
            teacher.name = request.form["name"]
            teacher.email = request.form["email"]
            teacher.subject = request.form["subject"]
            db.session.commit()
            Log.log_action("update", f"Modification du professeur : {old_name} → {teacher.name}", "teacher")
            return redirect(url_for("teachers"))
        return render_template("edit_teacher.html", teacher=teacher)

    @app.route("/delete_teacher/<int:id>")
    @login_required
    def delete_teacher(id):
        teacher = Teacher.query.get_or_404(id)
        name = teacher.name
        db.session.delete(teacher)
        db.session.commit()
        Log.log_action("delete", f"Suppression du professeur : {name}", "teacher")
        return redirect(url_for("teachers"))
