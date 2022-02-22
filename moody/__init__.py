__version__ = '0.1.0'

# Flask
from flask import Flask, request

# SQLAlchemy
from sqlalchemy.sql import text 

# PyYaml
import yaml

# Ours
from moody.jobs import populate_sentiment

def create_app():
    app = Flask(__name__)

    with open('database.yml', 'r') as f:
        db_conf = yaml.safe_load(f)

    app.config['SQLALCHEMY_BINDS'] = {
        "data": db_conf['url'],
        "metrics": "sqlite:///metrics.db",
    }

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from moody.db import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
        populate_sentiment()

    from moody.dashboard import dashboard
    app.register_blueprint(dashboard)

    return app
