
from flask import Flask, Response, request, jsonify, render_template, abort
from flask_restx import Api, Resource, fields, Namespace
from PIL import Image
from io import BytesIO
import base64
from flask_injector import inject
from injector import Module, Binder, singleton, Injector
from  werkzeug.debug import get_current_traceback
from core.domain.services.iface_compare_service import IFaceCompareService


api = Namespace(
    'Image Compare', description='Comparação de duas imagens de faces por semelhança')

input = api.model('Input', {
    'image_one': fields.String(required=True, description='Base64 da imagem principal'),
    'image_two': fields.String(required=True, description='Base64 da imagem que deve ser comparada'),
    'threshold': fields.Float(required=False, description='Valor limite de classificação em regressão logística para uma categoria binária. Valor atual 0.6'),
})

prediction = api.model('Prediction', {
    'match': fields.Boolean(required=True, description='Indicador que essas imagens são da mesma pessoa ou não'),
    'threshold': fields.Float(required=True, description='Valor limite de classificação usado para determinar se eles são a mesma pessoa ou não.'),
    'distance': fields.Float(required=True, description='A distância entre duas imagens em relação ao threshold')
})

@api.route('/images', endpoint='v1',  methods=["POST"])
class ImageResource(Resource):
    @inject
    def __init__(self, face_compare_service: IFaceCompareService, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.face_compare_service = face_compare_service

    @api.doc(body=input)
    @api.response(200, 'Success', prediction)
    def post(self):
        try:
            data = request.json
            try:
                threshold = data['threshold']
                result = self.face_compare_service.handle(data['image_one'], data['image_two'], threshold)
            except:
                threshold = None
                result =  self.face_compare_service.handle(data['image_one'], data['image_two'])            
            return jsonify({'match': result.match, 'threshold': result.threshold, 'distance':  float(result.distance) })
        except Exception:
            track= get_current_traceback(skip=1, show_hidden_frames=True,
                ignore_system_exceptions=False)
            track.log()
            abort(500)
















       
   
    