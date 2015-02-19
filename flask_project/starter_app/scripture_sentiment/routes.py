from scripture_sentiment import app
from flask import render_template, request, flash, session, url_for, redirect
from models import db, Verse
from sentiment import sentiment

# Fill in the routes
@app.route('/polarize/', methods=['GET'])
def polarize():
    verses = Verse.query.all()
    for v in verses:
        v.polarity = sentiment(v.scripture_text)
        print("%6.8f %s" % (v.polarity, v.scripture_text))
    db.session.commit()
    return "Done"