from flask import Flask
import os.path
 
app = Flask(__name__)

app.secret_key = 'development key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@127.0.0.1/scriptures'
 
from models import db
db.init_app(app)
 
import flask_project.routes
