from flask import Flask

# create a function that will return an application
def create_app():
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return '<font color="blue"><b>Hello, there!!!</b></font>'

    @app.route('/hello')
    def hello():
        return 'hello world'

    return app
