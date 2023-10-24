import os
from app import app
from app.db import db

basedir = os.path.abspath(os.path.dirname(__file__))


if __name__ == "__main__":
	
	# with app.app_context():
	# 	db.create_all()
	app.run(debug=True)
