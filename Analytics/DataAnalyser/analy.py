from DataAnalyser import DataAnalyser
from DataAnalyser.KNN import VGG16
from DataAnalyser.KNN import KNNEating
from DataAnalyser import AWSanalyser
import csv
import os

def getAnalyser(args):
    print("[INFO] Setting up Analyser")
    analyser = None
    if args["analyser"] == "VGG16":
        analyser = VGG16.VGG16imagenetKNN()
    elif args["analyser"] == "AWS":
        credentialsPath = os.path.abspath(os.path.join(os.path.dirname( __file__ ))) + "/credentials.csv"
        with open(credentialsPath, newline='') as csvfile:
            spamreader = csv.DictReader(csvfile)
            accessKey = ""
            secretKey = ""
            for row in spamreader:
                accessKey = row["Access key ID"]
                secretKey = row["Secret access key"]
            analyser = AWSanalyser.AWSanalyser(accessKey,secretKey, region_name=args["AWSregion"])


    eatingAnalyser  = KNNEating.KNNEating(args["EatingModel"])
    analyser.parent = eatingAnalyser


    return analyser