import cv2

def get_face(img):
    '''Corta a imagem para incluir apenas o rosto e uma borda'''
    height, width, _ = img.shape
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    face_box = face_cascade.detectMultiScale(img)
    # Obter dimensões da caixa delimitadora
    x, y, w, h = tuple(map(tuple, face_box))[0]
    # Calcule o preenchimento, pois a segmentação é muito apertada.
    pad_w = int(w/2.5)
    pad_h = int(h/2.5)
    # Obter coordenadas de crop
    x1 = max(0, x-pad_w)
    y1 = max(0, y-pad_h)
    x2 = min(width, x+w+pad_w)
    y2 = min(height, y+h+pad_h)
    # Crop da imagem
    cropped = img[y1:y2,x1:x2]
    return cropped