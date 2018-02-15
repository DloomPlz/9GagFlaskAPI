from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
import os
from gimgurpython import ImgurClient

db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    # a set up dans les variables heroku
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY','ed66022b-ee9c-4047-9482-f1dff8addae1')
    app.config['IMGUR_CLIENT_ID'] = os.environ.get('IMGUR_CLIENT_ID','891edbe392e448f')
        # if app.config['IMGUR_CLIENT_ID'] is '':
    #   tout quitter wala
    app.config['IMGUR_CLIENT_SECRET'] = os.environ.get('IMGUR_CLIENT_SECRET','42a6a8cf176918ba8bca5c566fa6ff22c078c2d7')
    app.config['IMGUR_ACCESS_TOKEN'] = os.environ.get('IMGUR_ACCESS_TOKEN','f789dd33c63c0762544ab40857db68fc14f4647c')
    app.config['IMGUR_REFRESH_TOKEN'] = os.environ.get('IMGUR_REFRESH_TOKEN','fdc824324a050898edcd59bcd384c5ec1634cf29')

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)

    if os.environ.get('debug','') is not '':
        app.debug = debug

    from .api_v1 import api as api_v1_blueprint
    app.register_blueprint(api_v1_blueprint, url_prefix='/api/v1')

    with app.app_context():
        db.drop_all()
        db.create_all()
    return app
