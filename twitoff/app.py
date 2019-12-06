'''Main application for twitoff'''
import uuid
# import flask package, flask makes app objects
from flask import Flask, render_template
#import from same directory
from .models import DB, User, Tweet

def create_app():
    # create Flask web server, makes application
    app = Flask(__name__)

    # # before app root, configure
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    DB.init_app(app)

    #routes determine location
    @app.route('/')
    def index():
        # rand_name = str(uuid.uuid4())
        # rand_u = User(name=rand_name)
        # DB.session.add(rand_u)
        # DB.session.commit()
        return 'Index Page'

    @app.route('/hello')
    def hello():
        return render_template('base.html', title='hello')

    @app.route('/about')
    def preds():
        return render_template('home.html')
    return app
