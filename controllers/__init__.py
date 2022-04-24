from flask import Flask, render_template
from flask_restx import Api
from controllers.face_compare_controller import api as ns1
from flask_triangle import Triangle

app = Flask(__name__, template_folder='../templates', static_folder='../static')
Triangle(app)

api = Api(app, version='1.0', title='Face Compare API',
          description='Restfull API Face Compare')
# api.init_app(app)
api.add_namespace(ns1, path='/face-compare')

@app.route('/test')
def home():
    return render_template('index.html')