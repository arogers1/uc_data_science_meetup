from flask import Flask
import os.path
 
app = Flask(__name__)

app.config['AFINN_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)),'AFINN/')

app.secret_key = 'development key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/scriptures'
 
from models import db
db.init_app(app)
 
import scripture_sentiment.routes
