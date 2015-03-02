from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Fill in the models
class Verse(db.Model):
    __tablename__ = 'verses'
    id = db.Column(db.Integer, primary_key=True)
    scripture_text = db.Column(db.String)
    polarity = db.Column(db.Integer)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'))
    chapter = db.relationship('Chapter', backref=db.backref('verses', lazy='dynamic'))

class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)
    chapter_number = db.Column(db.Integer)
    