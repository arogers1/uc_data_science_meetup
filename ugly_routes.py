from flask import Flask, request
from flask.ext.sqlalchemy import SQLAlchemy
from sentiment_analyzer import sentiment
import matplotlib.pyplot as plt

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/scriptures'

class Verse(db.Model):
    __tablename__ = 'verses'
    id = db.Column(db.Integer, primary_key=True)
    scripture_text = db.Column(db.String)
    polarity = db.Column(db.Integer)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))

class Chapter(db.Model):
    __tablename__ = 'chapters'
    id = db.Column(db.Integer, primary_key=True)
    chapter_number = db.Column(db.Integer)
    # book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    # verses = db.relationship('Verse', backref='chapter',
                                # lazy='select')

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    book_title = db.Column(db.String)
    book_long_title = db.Column(db.String)
    book_subtitle = db.Column(db.String)
    book_short_title = db.Column(db.String)
    book_lds_url = db.Column(db.String)
    # chapters = db.relationship('Chapter', backref='book',
                                # lazy='select')

@app.route('/polarize/', methods=['GET'])
def polarize():
    verses = Verse.query.all()
    for v in verses:
        v.polarity = sentiment(v.scripture_text)
        print("%6.8f %s" % (v.polarity, v.scripture_text))
    db.session.commit()
    return "Done"

@app.route('/plot/')
def plot():
    verses = Verse.query.filter(Verse.id.between(20312,20466)).all()
    polarities = [v.polarity for v in verses]
    ids = [v.id for v in verses]
    plt.plot(ids,polarities)
    plt.ylabel('Polarity')
    plt.show()


if __name__ == '__main__':
    app.run(debug=True)