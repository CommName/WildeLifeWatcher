

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np

import cv2



from DataAnalyser import DataAnalyser

class KNNEating (DataAnalyser.DataAnalyser):

    model = None

    def __init__(self, model):
        print("[INFO] loading custom model...")
        self.model = load_model(model)


    def analyseImage(self, image):

        image = image.copy()
        image = cv2.resize(image,(224,224))

        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (224, 224))
        image = img_to_array(image)
        image = preprocess_input(image)
        image = np.expand_dims(image, axis=0)
        (eating, notEating) = self.model.predict(image)[0]

        data = {}

        if eating > 0.45:
            data["Eating"] = True
        else:
            data["Eating"] = False

        return super().nextAnalyser(image,data)
