# coding=utf-8

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True 
    MAIL_SERVER = 'pop.exmail.qq.com'
    MAIL_PORT = 995
    MAIL_USE_TLS = True
    MAIL_USERNAME = "xuhuan@bukeu.com"
    MAIL_PASSWORD = "1122aabbccdd"
    YIAVE_MAIL_SUBJECT_PREFIX = '[ImmI]'
    YIAVE_MAIL_SENDER = 'ImmI Admin <xuhuan@bukeu.com>'
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
    mysql_db_username = 'root'
    mysql_db_password = 'fcz5jiayou'
    mysql_db_name = 'yiave'
    mysql_db_hostname = 'localhost'

    HOST = "127.0.0.1"
    PORT = 8088 
    SQLALCHEMY_ECHO = False
    SECRET_KEY = "IMMI TOP SECRET"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}".format(DB_USER=mysql_db_username,
                                                                                               DB_PASS=mysql_db_password,
                                                                                               DB_ADDR=mysql_db_hostname,
                                                                                               DB_NAME=mysql_db_name)
    # Email Server Configuration
    MAIL_DEFAULT_SENDER = "immi@localhost"

    PASSWORD_RESET_EMAIL = """
        Hi,

          Please click on the link below to reset your password

          <a href="/forgotpassword/{token}> Click here </a>
    """

config = {
    'development': DevelopmentConfig,

    'default': DevelopmentConfig
}
