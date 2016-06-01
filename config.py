# coding=utf-8

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # mail config
    MAIL_SERVER = 'smtp.exmail.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = "admin@yiave.com"
    MAIL_PASSWORD = "Terminal@207"
    MAIL_DEFAULT_SENDER = "admin@yiave.com"
    YIAVE_MAIL_SUBJECT_PREFIX = '[Yiave]'
    YIAVE_MAIL_SENDER = 'Yiave Admin <admin@yiave.com>'

    YIAVE_ADMIN = "admin"
    YIAVE_POSTS_PER_PAGE = 20
    YIAVE_PROMOTIONS_PER_PAGE = 20
    YIAVE_BUSINESSES_PER_PAGE = 20
    YIAVE_FOLLOWERS_PER_PAGE = 50
    YIAVE_COMMENTS_PER_PAGE = 30
    YIAVE_SLOW_DB_QUERY_TIME=0.5

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    # MySQL SETTINGS
<<<<<<< HEAD
    mysql_db_username = 'yiave'
    mysql_db_password = 'Yiave@207'
=======
    mysql_db_username = 'root'
    mysql_db_password = ''
>>>>>>> master
    mysql_db_name = 'yiave'
    mysql_db_hostname = '120.24.177.49'

    HOST = "0.0.0.0"
    PORT = 8088 
    SQLALCHEMY_ECHO = False
    SECRET_KEY = "YIAVE TOP SECRET"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=mysql_db_username,
                                                                                               DB_PASS=mysql_db_password,
                                                                                               DB_ADDR=mysql_db_hostname,
                                                                                               DB_NAME=mysql_db_name)
    # Email Server Configuration
    PASSWORD_RESET_EMAIL = """
        Hi,

          Please click on the link below to reset your password

          <a href="/forgotpassword/{token}> Click here </a>
    """

config = {
    'development': DevelopmentConfig,

    'default': DevelopmentConfig
}
