import io
import cv2
import base64
import face_recognition
from PIL import Image
from flask_injector import inject
from injector import Module, Binder, singleton, Injector
from interface import implements, Interface
from core.domain.services.iface_compare_service import IFaceCompareService


class FaceCompareService(implements(IFaceCompareService)):
    @inject
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
            
    def handle(self, image_one, image_two):
        imageOne = Image.open(io.BytesIO(base64.b64decode(str('image_one'))))
        imageTwo = Image.open(io.BytesIO(base64.b64decode(str('image_two'))))

        # bgrImgOne = cv2.imread(imageOne)

        rgbImgOne = cv2.cvtColor(imageOne, cv2.COLOR_BGR2RGB)
        rgbImgTwo = cv2.cvtColor(imageTwo, cv2.COLOR_BGR2RGB)

        print("  + Tamanho da imagem principal: {}".format(rgbImgOne.shape))
        print("  + Tamanho da imagem secundaria: {}".format(rgbImgTwo.shape))

        imgOne = face_recognition.load_image_file(rgbImgOne)
        imgOneFaceEncoding = face_recognition.face_encodings(imgOne)[0]
        
        imgTwo = face_recognition.load_image_file(rgbImgTwo)
        imgTwoFaceEncoding = face_recognition.face_encodings(imgTwo)[0]

        results = face_recognition.compare_faces([imgOneFaceEncoding], imgTwoFaceEncoding)
        
        return results