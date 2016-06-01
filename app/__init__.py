from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import config

db = SQLAlchemy()
mail = Mail()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    mail.init_app(app)

<<<<<<< HEAD
    from .business import business as business_blueprint
    app.register_blueprint(business_blueprint, url_prefix='/v1')
=======
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/v1')

    from .aaa import aaa as aaa_blueprint
    app.register_blueprint(aaa_blueprint, url_prefix='/v1')

    from .customer import customer as customer_blueprint
    app.register_blueprint(customer_blueprint, url_prefix='/v1')
>>>>>>> master

    return app
