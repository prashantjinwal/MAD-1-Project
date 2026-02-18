from flask import Flask
from werkzeug.security import generate_password_hash
from app.extensions import db, login_manager



def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    from app.auth import auth
    app.register_blueprint(auth)
    from app.home import home
    app.register_blueprint(home)

    with app.app_context():
        from app import models
        db.create_all()
        create_admin()
    return app

def create_admin():
    from app.models import User

    if not User.query.filter_by(role='admin').first():
        admin  = User(
            email = "prashantjinwal888@gmail.com",
            password = generate_password_hash("admin@5120"),
            role = "admin"
        )
        db.session.add(admin)
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))


 