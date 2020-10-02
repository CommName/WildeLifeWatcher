from DataAnalyser import DataAnalyser
from DataAnalyser.KNN import VGG16
from DataAnalyser.KNN import KNNEating
from DataAnalyser import AWSanalyser


def getAnalyser(args):
   
    #analyser = VGG16.VGG16imagenetKNN()
    analyser = AWSanalyser('','')
    eatingAnalyser  = KNNEating.KNNEating(args["EatingModel"])
    analyser.parent = eatingAnalyser


    return analyser