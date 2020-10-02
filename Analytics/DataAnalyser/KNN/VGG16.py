# import the necessary packages
from tensorflow.keras.applications.imagenet_utils import decode_predictions
from tensorflow.keras.applications.imagenet_utils import preprocess_input
from tensorflow.keras.applications import VGG16
import numpy as np
import cv2


from DataAnalyser import DataAnalyser

class VGG16imagenetKNN (DataAnalyser.DataAnalyser):

	model = None

	def __init__(self):
		# load the VGG16 network pre-trained on the ImageNet dataset
		print("[INFO] loading network...")
		self.model = VGG16(weights="imagenet")
		# classify the image


	def analyseImage(self, ogimage):
		image = ogimage.copy()
		image = cv2.resize(image,(224,224))

		#mozda je potrebno deljenje??? sa /255.0
		image = image[...,::-1].astype(np.float32)
		# our image is now represented by a NumPy array of shape (224, 224, 3),
		# assuming TensorFlow "channels last" ordering of course, but we need
		# to expand the dimensions to be (1, 3, 224, 224) so we can pass it
		# through the network -- we'll also preprocess the image by subtracting
		# the mean RGB pixel intensity from the ImageNet dataset
		image = np.expand_dims(image, axis=0)
		image = preprocess_input(image)

		#classify image
		preds = self.model.predict(image)
		p = decode_predictions(preds)

		(imagenetId, label, prob) = p[0][0]


		if(prob <0.5):
			return None

		if label.lower() == 'african_elephant':
			label = 'elephant'
		
		if label.lower() == 'water_buffalo':
			label = 'buffalo'

		data = { label : 1 }

		return super().nextAnalyser(ogimage, data)



