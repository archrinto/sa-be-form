class Config(object):
    DEBUG = False
    TESTING = False

    UPLOAD_DIR = '/home/archrinto/Pictures/jerawat'

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True
