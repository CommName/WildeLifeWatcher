from DataAnalyser import DataAnalyser
import boto3
import numpy as np
import cv2
from botocore.config import Config
from PIL import Image
import io

class AWSanalyser (DataAnalyser):

    client = None
    officalAnimals = []

    def __init__(self,aws_access_key_id, aws_secret_access_key, region_name = 'us-east-2'):
        awsConfig = Config(region_name = 'us-east-2')
        self.client = boto3.client('rekognition', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, config=awsConfig)


        self.officalAnimals = []
        with open('animals.txt') as afile:
            for animalName in afile:
                self.officalAnimals.append(animalName.strip())


    def analyseImage(self,ogimage):
        pil_img = Image.fromarray(ogimage)
        stream = io.BytesIO()
        pil_img.save(stream, format='JPEG')
        bin_img = stream.getvalue()

        response = self.client.detect_labels(Image={"Bytes": bin_img })

        labels = response['Labels']
    
        data = {}
        for label in labels:
            if label['Name'] in self.officalAnimals:

                if label['Confidence'] > 50:
                    numberOfAnimals = len(label['Instances'])
                    if numberOfAnimals ==0:
                        numberOfAnimals = 1

                    data[label['Name'].lower()] = numberOfAnimals
            
        return super().nextAnalyser(ogimage, data)

