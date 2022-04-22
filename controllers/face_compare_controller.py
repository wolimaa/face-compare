
from flask import Flask, Response, request, jsonify
from flask_restx import Api, Resource, fields, Namespace
from PIL import Image
from io import BytesIO
import base64

api = Namespace(
    'Image Compare', description='Comparação de duas imagens de faces por semelhança')

baseCompare = api.model('BaseCompare', {
    'image_one': fields.String(required=True, description='Base64 da imagem principal'),
    'image_two': fields.String(required=True, description='Base64 da imagem que deve ser comparada')
})

result = api.model('Result', {
    'code': fields.String,
    'score': fields.Float,
})

@api.route('/images', endpoint='v1',  methods=["POST"])
class ImageResource(Resource):
    @api.doc(body=baseCompare)
    @api.response(200, 'Success', result)
    def post(self):
        data = request.json
        # imgOne = Image.open(BytesIO(base64.b64decode(request.form['image_one'])))
        # imgTwo = Image.open(BytesIO(base64.b64decode(request.form['image_one'])))
        return jsonify({'code': 'success', 'score': 99.9})