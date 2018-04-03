from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from  app import app

db = SQLAlchemy(app)