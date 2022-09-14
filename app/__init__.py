from flask import Flask
from config import Config
from .extensions import db, scheduler
from flask_migrate import Migrate
from . import models
from . import scheduled_task



app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate = Migrate(app, db)
scheduler.init_app(app)
scheduler.start()
from . import routes

