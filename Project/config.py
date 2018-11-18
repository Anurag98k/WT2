import os


class Config(object):
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + '../app.db' 
	SQLALCHEMY_TRACK_MODIFICATIONS = False #do not signal app everytime a change is made in db
