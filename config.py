import os

app_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    
    SWAGGER_UI_OPERATION_ID = True
    SWAGGER_UI_REQUEST_DURATION = True

    RESTX_VALIDATE = True

    # Flask-Restplus 
    # RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    # RESTPLUS_VALIDATE = True
    # RESTPLUS_MASK_SWAGGER = False
    # RESTPLUS_ERROR_404_HELP = False


class Developement(BaseConfig):
    DEBUG = True
class Testing(BaseConfig):
    DEBUG = True
class Production(BaseConfig):
    DEBUG = False
