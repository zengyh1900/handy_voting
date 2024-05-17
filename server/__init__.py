from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from omegaconf import OmegaConf


app = Flask(__name__)
config = OmegaConf.load("./config.yaml")
app.config.from_mapping(config.APP_SETTINGS)

db = SQLAlchemy()
db.init_app(app)

from . import views
from .models import Model
