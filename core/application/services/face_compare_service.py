import io
import time
import argparse
import cv2
import itertools
import os
import numpy as np
np.set_printoptions(precision=2)
import openface
import base64
from PIL import Image
from flask_injector import inject
from injector import Module, Binder, singleton, Injector
from interface import implements, Interface
from core.domain.services.iface_compare_service import IFaceCompareService

start = time.time()
fileDir = os.path.dirname(os.path.realpath(__file__))
modelDir = os.path.join(fileDir, 'models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')
parser = argparse.ArgumentParser()
parser.add_argument('imgs', type=str, nargs='+', help="Input images.")
parser.add_argument('--dlibFacePredictor', type=str, help="Caminho para o face predictor do dlib.",
                    default=os.path.join(dlibModelDir, "shape_predictor_68_face_landmarks.dat"))
parser.add_argument('--networkModel', type=str, help="Caminho para o modelo de rede do Torch.",
                    default=os.path.join(openfaceModelDir, 'nn4.small2.v1.t7'))

parser.add_argument('--imgDim', type=int,
                    help="Dimensão de imagem padrão.", default=96)
parser.add_argument('--verbose', action='store_true')
args = parser.parse_args()

if args.verbose:
    print("Argument parsing and loading libraries took {} seconds.".format(
        time.time() - start))

start = time.time()
align = openface.AlignDlib(args.dlibFacePredictor)
net = openface.TorchNeuralNet(args.networkModel, args.imgDim)
if args.verbose:
    print("O carregamento dos modelos dlib e OpenFace levou {} segundos.".format(
        time.time() - start))

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
        args.imgs.append (rgbImgOne)
        args.imgs.append (rgbImgTwo)

        for (img1, img2) in itertools.combinations(args.imgs, 2):
            d = self.getRepresentation(img1, "Imagem Principal") - self.getRepresentation(img2, "Imagem Secundaria")
        print("Comparando {} com {}.".format(img1, img2))
        print(
            "  + Distância l2 entre as representações: {:0.3f}".format(np.dot(d, d)))
        return True

    def getRepresentation(bgrImg, imgName):
        if bgrImg is None:
            raise Exception("Não foi possivel ler a imagem: {}".format(imgName))
        rgbImg = cv2.cvtColor(bgrImg, cv2.COLOR_BGR2RGB)
        if args.verbose:
            print("  + Original size: {}".format(rgbImg.shape))

        start = time.time()
        bb = align.getLargestFaceBoundingBox(rgbImg)
        if bb is None:
            raise Exception("Não foi possível encontrar um rosto na imagem: {}".format(imgName))
        if args.verbose:
            print("  + A detecção de rosto levou {} segundos.".format(time.time() - start))

        start = time.time()
        alignedFace = align.align(args.imgDim, rgbImg, bb,
                                landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)
        if alignedFace is None:
            raise Exception("Não foi possível alinhar a imagem: {}".format(imgName))
        if args.verbose:
            print("  + O alinhamento do rosto levou {} segundos.".format(time.time() - start))

        start = time.time()
        rep = net.forward(alignedFace)
        if args.verbose:
            print("  + OpenFace levou {} segundos para executar.".format(time.time() - start))
            print("Representação:")
            print(rep)
            print("-----\n")
        return rep   