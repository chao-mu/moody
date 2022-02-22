# Ours
from moody.db import db, TwitterSentiment

# SQLAlchemy
from sqlalchemy.sql import text

TAGGED_SENTIMENT = """
with sentiments as (
    select 
        date_trunc('week', t.twitter_created_at) as week_of,
        sentiment, 
        tags.name as tag,
        count(sentiment) as c
    from tweets t
    join users u on u.twitter_id = t.twitter_author_id
    join users_tags ut on ut.user_id = u.id
    join tags on tags.id = ut.tag_id
    where 
        t.sentiment is not null
        and t.sentiment_score > 0.75
        and t.twitter_created_at > current_date - interval '1 year' 
        and date_trunc('day', t.twitter_created_at) < date_trunc('week', current_date)
    group by 1, 2, 3
)
select s1.week_of, s1.tag, s1.sentiment, totals.total, sum(s1.c) / totals.total as ratio
from sentiments s1,
    (
        select inner_s.week_of, inner_s.tag, sum(inner_s.c) as total
        from sentiments inner_s
        group by 1, 2
    ) totals
where totals.tag = s1.tag and totals.week_of = s1.week_of
group by 1, 2, 3, 4;
"""

def populate_sentiment():
    with db.get_engine(bind="data").connect() as conn:
        rows = conn.execute(text(TAGGED_SENTIMENT)).all()

    with db.get_engine(bind="metrics").connect() as conn:
        for row in rows:
            TwitterSentiment.create_or_update( 
                db.session,
                sentiment=row["sentiment"],
                week_of=row["week_of"],
                tag=row["tag"],
                total=int(row["total"]),
                ratio=row["ratio"]
            )

    db.session.commit()
