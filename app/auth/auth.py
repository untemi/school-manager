import os
from functools import wraps
from flask import session, redirect, url_for
from dotenv import load_dotenv

load_dotenv()

def init_auth(app):
    app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    
    return decorated_function

def check_credentials(username, password):
    expected_username = os.getenv('ADMIN_USERNAME', 'admin')
    expected_password = os.getenv('ADMIN_PASSWORD', 'admin123')

    return username == expected_username and password == expected_password
