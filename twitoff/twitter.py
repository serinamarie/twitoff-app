'''Retrieve tweets, embedding, save into database'''

import basilica
from decouple import config
from .models import DB, User, Tweet
import tweepy

TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('BASILICA_KEY'))

# def add_or_update_user(username):
#     '''Add or update a user and their Tweets, or else error'''
#     try:
#         twitter_user=TWITTER.get_user(username)
#         db_user=(User.query.get(twitter_user.id) or
#         User(id=twitter_user.id, name=username))
#         DB.session.add(db_user)
#         tweets=twitter_user.timeline(count=200,
#                                         exclude_replies=True,
#                                         include_rts=False,
#                                         tweet_mode='extended',
#                                         since_id=db_user.newest_tweet_id)
#         if tweets:
#             db_user.newest_tweet_id = tweets[0].id
#         for tweet in tweets:
#             #Calculate embedding on the full tweet
#             embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
#             db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:300],
#             embedding=embedding)
#             db_user.tweets.append(db_tweet)
#             DB.session.add(db_tweet)
#     except Exception as e:
#         print(f'Error processing {username} : {e}'.format())
#         raise e
#     else:
#         DB.session.commit()

def add_or_update_user(name):
    """Add or update a user and their Tweets, or else error"""
    try:
        twitter_user=TWITTER.get_user(name)
        db_user=(User.query.get(twitter_user.id) or
        User(id=twitter_user.id, name=name))
        DB.session.add(db_user)
        tweets = twitter_user.timeline(count=200, exclude_replies=True,
        include_rts=False, since_id=db_user.newest_tweet_id)
        if tweets:
            db_user.newest_tweet_id = tweets[0].id
        for tweet in tweets:
            #Calculate embedding on the full tweet
            embedding = BASILICA.embed_sentence(tweet.text, model='twitter')
            db_tweet = Tweet(id=tweet.id, text=tweet.text[:300],
            embedding=embedding)
            db_user.tweets.append(db_tweet)
            DB.session.add(db_tweet)
    except Exception as e:
        print('Error processing {name}: {e}')
        raise e
    else:
        DB.session.commit()
