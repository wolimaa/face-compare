import os
import logging
import config
from flask import Flask
from flask_environments import Environments
from flask_restx import Api
from flask_caching import Cache
from flask_injector import FlaskInjector
from flask_restx import Api
# from flask_script import Manager
from injector import Module, Binder, singleton, Injector, inject, provider
from controllers import api
from controllers import app
from core.application.services.face_compare_service import FaceCompareService
from core.domain.services.iface_compare_service import IFaceCompareService
from core.utils.injection_context import InjectionContext

env = Environments(app)
env.from_object(config)

class AppModule(Module):
    def __init__(self, app):
        self.app = app

    """Configure the application."""
    def configure(self, binder: Binder):
    
        binder.bind(interface=IFaceCompareService,
                    to=FaceCompareService(), scope=singleton)
        binder.bind(Cache, to=Cache(app), scope=singleton)
        binder.bind(Api, to=api)
    
def startup(params):
    # app.config.from_object(params)
    logging.basicConfig(filename='logging.conf', level=logging.DEBUG)
    logging.debug('This message should go to the log file')
    injector = Injector([AppModule(app)])
    InjectionContext(injector)
    FlaskInjector(app=app, injector=injector)
    return app


app = startup(
    f'config.{os.getenv("FLASK_ENV")}' or 'config.Developement')
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    app.run()
