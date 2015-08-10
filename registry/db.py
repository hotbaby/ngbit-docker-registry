
from app import app
from flask.ext.sqlalchemy import SQLAlchemy

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/yy/docker/database/docker-registry.db'
db = SQLAlchemy(app)
