from flask import Flask
from config import Config
from .extensions import db, scheduler
from flask_migrate import Migrate
from flask_login import LoginManager
from . import models
from . import scheduled_task


#flask application
app = Flask(__name__)
app.config.from_object(Config)

#database config
db.init_app(app)
migrate = Migrate(app, db)
app.app_context().push()
db.create_all()

#scheduler config
scheduler.init_app(app)
scheduler.start()

#login manage config
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))

from . import routes

