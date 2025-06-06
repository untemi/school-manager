from flask import Flask
from app.config.database import init_db
from app.api import register_routes
from app.auth.auth import init_auth
from app.auth.routes import register_auth_routes

app = Flask(__name__)

init_db(app)
init_auth(app)
register_auth_routes(app)
register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
