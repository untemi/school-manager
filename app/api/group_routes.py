from flask import render_template, request, redirect, url_for
from app.config.database import db
from app.models.models import Group, Teacher, Log
from app.auth.auth import login_required

def register_group_routes(app):
    @app.route("/groups")
    @login_required
    def groups():
        groups = Group.query.all()
        return render_template("groups.html", groups=groups)

    @app.route("/add_group", methods=["GET", "POST"])
    @login_required
    def add_group():
        if request.method == "POST":
            name = request.form["name"]
            teacher_ids = request.form.get("teacher_ids", "").split(",")
            new_group = Group(name=name)
            db.session.add(new_group)
            db.session.commit()
            for teacher_id in teacher_ids:
                if teacher_id:
                    teacher = Teacher.query.get(int(teacher_id))
                    new_group.teachers.append(teacher)
            db.session.commit()
            teacher_count = len([tid for tid in teacher_ids if tid])
            Log.log_action("create", f"Ajout du groupe {name} avec {teacher_count} professeur(s)", "group")
            return redirect(url_for("groups"))
        teachers = Teacher.query.all()
        return render_template("add_group.html", teachers=teachers)

    @app.route("/edit_group/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_group(id):
        group = Group.query.get_or_404(id)
        if request.method == "POST":
            old_name = group.name
            group.name = request.form["name"]
            teacher_ids = request.form.get("teacher_ids", "").split(",")
            group.teachers.clear()
            for teacher_id in teacher_ids:
                if teacher_id:
                    teacher = Teacher.query.get(int(teacher_id))
                    group.teachers.append(teacher)
            db.session.commit()
            Log.log_action("update", f"Modification du groupe : {old_name} → {group.name}", "group")
            return redirect(url_for("groups"))
        teachers = Teacher.query.all()
        return render_template("edit_group.html", group=group, teachers=teachers)

    @app.route("/delete_group/<int:id>")
    @login_required
    def delete_group(id):
        group = Group.query.get_or_404(id)
        name = group.name
        db.session.delete(group)
        db.session.commit()
        Log.log_action("delete", f"Suppression du groupe : {name}", "group")
        return redirect(url_for("groups"))
