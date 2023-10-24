from flask import Flask
from config import Config
from app.db import db
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
migrate = Migrate()


db.init_app(app)
migrate.init_app(app, db)


from app.auth.routes import auth_bp

app.register_blueprint(auth_bp, url_prefix='/api/v1')

