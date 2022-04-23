
from flask import Flask, Response, request, jsonify
from flask_restx import Api, Resource, fields, Namespace
from PIL import Image
from io import BytesIO
import base64
from flask_injector import inject
from injector import Module, Binder, singleton, Injector

from core.domain.services.iface_compare_service import IFaceCompareService


api = Namespace(
    'Image Compare', description='Comparação de duas imagens de faces por semelhança')

baseCompare = api.model('BaseCompare', {
    'image_one': fields.String(required=True, description='Base64 da imagem principal'),
    'image_two': fields.String(required=True, description='Base64 da imagem que deve ser comparada')
})

result = api.model('Result', {
    'match': fields.boolean,
    'score': fields.Float,
})

@api.route('/images', endpoint='v1',  methods=["POST"])
class ImageResource(Resource):
    @inject
    def __init__(self, face_compare_service: IFaceCompareService, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.face_compare_service = face_compare_service

    @api.doc(body=baseCompare)
    @api.response(200, 'Success', result)
    def post(self):
        data = request.json
        # imgOne = Image.open(BytesIO(base64.b64decode(request.form['image_one'])))
        # imgTwo = Image.open(BytesIO(base64.b64decode(request.form['image_one'])))
        result =  self.face_compare_service.handle(data['image_one'], data['image_one'])
        return jsonify({'match': result, 'score': 0.6})