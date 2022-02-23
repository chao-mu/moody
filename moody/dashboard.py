# Flask
from flask import current_app, Blueprint, render_template, request

# SQLAlchemy
from sqlalchemy.sql import text

# Ours
from moody.db import db, TwitterSentiment

# Core
import json

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

    sentiments_by_tag_x = {}
    sentiments_by_tag_y = {}
    tag_names = {
        "Republican (US Political Party)": "Republican",
        "Democrat (US Political Party)": "Democrat",
    }
    for sentiment in sentiment_results:
        if sentiment.tag not in tag_names:
            continue

        tag = tag_names[sentiment.tag]

        if tag not in sentiments_by_tag_x:
            sentiments_by_tag_x[tag] = []
            sentiments_by_tag_y[tag] = []

        sentiments_by_tag_x[tag].append(sentiment.week_of)
        sentiments_by_tag_y[tag].append(sentiment.ratio)

    if requested_sentiment == "POSITIVE":
        title = "Positivity Index"
    else:
        title = "Negativity Index"

    return render_template("index.html.j2",
            sentiments_x=json.dumps(sentiments_by_tag_x, default=str),
            sentiments_y=json.dumps(sentiments_by_tag_y, default=str),
            title=title)
