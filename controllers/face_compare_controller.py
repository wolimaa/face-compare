
from flask import Flask, Response
from flask_restx import Api, Resource, fields, Namespace

api = Namespace(
    'faceCompare', description='Comparação de duas imagens de faces por semelhança')

@api.route('/hello')
@api.doc(params={'id': 'An ID'})
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}



