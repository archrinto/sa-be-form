class Config(object):
    DEBUG = False
    TESTING = False

    UPLOAD_DIR = '/home/archrinto/Pictures/jerawat'

class ProductionConfig(Config):
    UPLOAD_DIR = '/home/july/storage/sa-form'

class DevelopmentConfig(Config):
    DEBUG = True
