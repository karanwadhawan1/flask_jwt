from app.db import db
from datetime import datetime

class User(db.Model):
    __table_name = 'users'
    id = db.Column(db.Integer, primary_key = True, autoincrement= True)
    email = db.Column(db.String(150), unique = True, nullable = False)
    password = db.Column(db.String(150), nullable = False)
    date_registered = db.Column(db.DateTime, default = datetime.utcnow())
    
