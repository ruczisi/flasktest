import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'abcdefghijklmnopqrstuvwxyz'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TSL = False
    MAIL_USERNAME = 'ruczisi@vip.qq.com'
    MAIL_PASSWORD = 'icymuzzenuubcafj'
    TEST_MAIL_SUBJECT_PREFIX = '[ToolPack]'
    TEST_MAIL_SENDER = 'TP_Admin<ruczisi@vip.qq.com>'
    TEST_ADMIN = os.environ.get('TEST_ADMIN')
    TEST_POSTS_PER_PAGE = 20
    TEST_FOLLOWERS_PER_PAGE = 20
    TEST_COMMENTS_PER_PAGE = 20
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir,'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLE = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    @classmethod
    def init_app(cls,app):
        Config.init_app(app)
        import logging
        from logging.handlers import SMTPHandler
        credentials = None
        secure = None
        if getattr(cls,"MAIL_USERNAME",None) is not None:
            credentials = (cls.MAIL_USERNAME,cls.MAIL_PASSWORD)
            if getattr(cls,'MAIL_USE_TLS',None):
                secure = ()
        mail_handler = SMTPHandler(
            mailhost= (cls.MAIL_SERVER,cls.MAIL_PORT),
            fromadd = cls.TEST_MAIL_SENDER,
            toaddrs=[cls.TEST_ADMIN],
            subject = cls.TEST_MAIL_SUBJECT_PREFIX + "应用错误日志",
            credentials = credentials,
            secure =secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
