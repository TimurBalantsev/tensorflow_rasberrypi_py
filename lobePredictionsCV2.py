import cv2
from lobe import ImageModel
import datetime

model = ImageModel.load('./Armee ou non TFLite')


class prediction:
    def __init__(self, etiquette, confidence, file):
        self.etiquette = etiquette
        self.confidence = confidence
        self.file = file

def take_capture():
    capture = cv2.VideoCapture(0)
    curr_time = datetime.datetime.now().strftime('%d-%b-%Y-%H:%M:%S')
    file = f"./static/img{curr_time}.jpg"
    _, img = capture.read()
    cv2.imwrite(file, img)
    result = model.predict_from_file(file)
    etiquette = result.prediction
    confidence = result.labels[0][1]
    capture.release()
    return prediction(etiquette, confidence, file)

if __name__ == "__main__":

    print(take_capture().etiquette)