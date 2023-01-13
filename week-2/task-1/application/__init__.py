from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from application.config import Config

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('config.py')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
ma = Marshmallow()

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    
    app.config.from_pyfile('config.py')
    app.config.from_object(Config)
    db.init_app(app)
    ma.init_app(app)
   
    from application.goods.view import train_application
    app.register_blueprint(train_application)


    return app