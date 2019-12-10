'''Main application for twitoff'''
import uuid
from decouple import config
# import flask package, flask makes app objects
from flask import Flask, render_template, request
#import from same directory
from .models import DB, User, Tweet
from .twitter import add_or_update_user

def create_app():
    # create Flask web server, makes application
    app = Flask(__name__)

    # # before app root, configure
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    # app.config['ENV'] = config('ENV')
    DB.init_app(app)

    #routes determine location
    # @app.route('/')
    # def index():
    #     # rand_name = str(uuid.uuid4())
    #     # rand_u = User(name=rand_name)
    #     # DB.session.add(rand_u)
    #     # DB.session.commit()
    #     return 'Index Page'

    @app.route('/')
    def root():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

    @app.route('/user', methods=['POST', 'GET'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        # if user retrieval fails
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} successfully added!".format(name)
            tweets = User.query.filter(User.name == name).one().tweets
        except Exception as e:
            message = "Error adding {}: {}".format(name,e)
            tweets=[]
        return render_template('user.html', title=name, tweets=tweeets,
        message=message)

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title='DB Reset', users=[])

    @app.route('/about')
    def preds():
        return render_template('home.html')
    return app
