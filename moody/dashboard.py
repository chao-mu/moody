# Flask
from flask import current_app, Blueprint, render_template, request

# SQLAlchemy
from sqlalchemy.sql import text

# Ours
from moody.db import db, TwitterSentiment

dashboard = Blueprint('dashboard', __name__,
        url_prefix='/', template_folder='templates')

hosts_to_sentiment = {
    "negativityindex.com": "NEGATIVE",
    "positivityindex.com": "POSITIVE",
    "127.0.0.1:5000": "POSITIVE",
    "localhost:5000": "NEGATIVE"
}

@dashboard.route("/")
def index():
    requested_sentiment = hosts_to_sentiment[request.host]

    sentiment_results = db.session.query(TwitterSentiment).filter_by(
        sentiment=requested_sentiment).order_by(TwitterSentiment.week_of).all()

    sentiments_by_tag = {}
    for sentiment in sentiment_results:
        if sentiment.tag not in sentiments_by_tag:
            sentiments_by_tag[sentiment.tag] = []

        sentiments_by_tag[sentiment.tag].append(
            (sentiment.week_of, sentiment.ratio))

    if requested_sentiment == "POSITIVE":
        title = "Positivity Index"
    else:
        title = "Negativity Index"

    return render_template("index.html.j2", sentiments=sentiments_by_tag, title=title)
