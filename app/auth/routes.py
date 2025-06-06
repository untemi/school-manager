from flask import render_template, request, redirect, url_for, session
from .auth import check_credentials

def register_auth_routes(app):
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            
            if check_credentials(username, password):
                session['logged_in'] = True
                return redirect(url_for('home'))
            else:
                return render_template("login.html", error="Nom d'utilisateur ou mot de passe incorrect")
                
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.pop('logged_in', None)
        return redirect(url_for('login'))
