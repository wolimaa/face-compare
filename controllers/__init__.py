from flask import Flask
from flask_restx import Api
from controllers.face_compare_controller import api as ns1

app = Flask(__name__)
api = Api(app, version='1.0', title='Face Compare API',
          description='Restfull API Face Compare')
# api.init_app(app)
api.add_namespace(ns1, path='/faceCompare')