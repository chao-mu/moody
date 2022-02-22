# Flask
from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy
from sqlalchemy import Column, Date, String, Integer, Float, PrimaryKeyConstraint

# PyYaml
import yaml

db = SQLAlchemy()

class TwitterSentiment(db.Model):
    __tablename__ = "twitter_sentiments"

    sentiment = Column(String, nullable=False)
    week_of = Column(Date, nullable=False)
    tag = Column(String, nullable=False)
    total = Column(Integer, nullable=False)
    ratio = Column(Float, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint(sentiment, week_of, tag),
        {},
    )

    def create_or_update(session, sentiment, week_of, tag, total, ratio):
        key = {'sentiment': sentiment, 'week_of': week_of, 'tag': tag}
        sentiment = session.query(TwitterSentiment).filter_by(**key).first()

        if not sentiment:
            sentiment = TwitterSentiment(**key)
        
        sentiment.total = total
        sentiment.ratio = ratio

        session.add(sentiment)
