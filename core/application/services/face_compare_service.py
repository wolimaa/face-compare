import io
import cv2
import numpy as np
import base64
from PIL import Image
from flask_injector import inject
from injector import Module, Binder, singleton, Injector
from Interface import implements, Interface
from core.domain.models.check_result import CheckResult
from core.domain.services.iface_compare_service import IFaceCompareService
from core.utils.images import get_face
from core.utils.model import facenet_model, img_to_encoding

model = facenet_model(input_shape=(3, 96, 96))


class FaceCompareService(implements(IFaceCompareService)):
    @inject
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
            
    def handle(self, code_image_one, code_image_two, threshold=0.6):
        image_one = self.data_uri_to_cv2_img(code_image_one)
        image_two = self.data_uri_to_cv2_img(code_image_two)
        return self.process(image_one, image_two, threshold)

    def process(self, image_one, image_two, threshold):
        match = False
        # Load images
        face_one = get_face(image_one)
        face_two = get_face(image_two)

        # Calculate embedding vectors
        embedding_one = img_to_encoding(face_one, model)
        embedding_two = img_to_encoding(face_two, model)

        if threshold < 0.1 or threshold > 0.6:
            threshold=0.6

        dist = np.linalg.norm(embedding_one - embedding_two)
        print(f'Distance between two images is {dist}')
        if dist > threshold:
            match = False
        else:
            match = True
        
        return CheckResult(match, threshold, str(dist))

    def data_uri_to_cv2_img(self, uri):


        image = uri.split(',')[1]
        decoded_data = base64.b64decode(image)
        np_data = np.fromstring(decoded_data,np.uint8)
        img = cv2.imdecode(np_data,cv2.IMREAD_UNCHANGED)



        # nparr = np.fromstring(encoded_data.decode('base64'), np.uint8)
        # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img
