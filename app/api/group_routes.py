from flask import render_template, request, redirect, url_for, flash
from app.config.database import db
from app.models import Group, Teacher, Log
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
            new_group = Group(
                name=request.form["name"],
                code=request.form.get("code"),
                academic_year=request.form["academic_year"],
                capacity=request.form.get("capacity", type=int),
                min_students=request.form.get("min_students", type=int),
                max_students=request.form.get("max_students", type=int),
                description=request.form.get("description"),
                notes=request.form.get("notes")
            )

            # Handle teacher assignments
            teacher_ids = request.form.getlist("teacher_ids")
            for teacher_id in teacher_ids:
                if teacher_id:
                    teacher = Teacher.query.get(int(teacher_id))
                    if teacher:
                        new_group.teachers.append(teacher)

            db.session.add(new_group)
            db.session.commit()
            flash("Group added successfully!", "success")
            Log.log_action("create", f"Added group {new_group.name} with {len(teacher_ids)} teacher(s)", "group")
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
            group.code = request.form.get("code")
            group.academic_year = request.form["academic_year"]
            group.capacity = request.form.get("capacity", type=int)
            group.min_students = request.form.get("min_students", type=int)
            group.max_students = request.form.get("max_students", type=int)
            group.description = request.form.get("description")
            group.notes = request.form.get("notes")

            # Handle teacher assignments
            group.teachers.clear()
            teacher_ids = request.form.getlist("teacher_ids")
            for teacher_id in teacher_ids:
                if teacher_id:
                    teacher = Teacher.query.get(int(teacher_id))
                    if teacher:
                        group.teachers.append(teacher)

            db.session.commit()
            flash("Group updated successfully!", "success")
            Log.log_action("update", f"Modified group: {old_name} → {group.name}", "group")
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
        flash("Group deleted successfully!", "success")
        Log.log_action("delete", f"Deleted group: {name}", "group")
        return redirect(url_for("groups"))
