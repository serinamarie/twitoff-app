'''Main application for twitoff'''
import uuid
from decouple import config
from dotenv import load_dotenv
# import flask package, flask makes app objects
from flask import Flask, render_template, request
#import from same directory
from .models import DB, User, Tweet
from .predict import predict_user
from .twitter import add_or_update_user

load_dotenv()

def create_app():
    # create Flask web server, makes application
    app = Flask(__name__)

    # # before app root, configure
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    # app.config['ENV'] = config('ENV')
    DB.init_app(app)

    @app.route('/')
    def root():
        DB.create_all()
        return render_template('base.html', title='Home', users=User.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='hello')

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        # if user retrieval fails
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = f"User {name} successfully added!"
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = f"Error adding {name}: {e}"
            tweets=[]
        return render_template('user.html', title=name,
                                tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1 = request.values['user1']
        user2 = request.values['user2']
        tweet_text = request.values['tweet_text']

        if user1 == user2:
            message = "Cannot compare same user"
        else:
            prediction = predict_user(user1, user2, tweet_text)
            message = '"{}" is more likely to be said by {} than {}'.format(
            request.values['tweet_text'], user1 if prediction else user2,
            user2 if prediction else user1)
        return render_template('prediction.html', title="Results",
        message=message)

    return app
