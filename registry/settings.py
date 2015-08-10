
import os

SECRET_KEY = os.getenv('SECRET_KEY', 'ngbit docker hub secret key')
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:////home/yy/docker/database/docker-registry.db')
