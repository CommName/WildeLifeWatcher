from DataAnalyser import DataAnalyser
from DataAnalyser.KNN import VGG16
from DataAnalyser.KNN import KNNEating

def getAnalyser(args):
   
    analyser = VGG16.VGG16imagenetKNN()
    
    eatingAnalyser  = KNNEating.KNNEating(args["EatingModel"])
    analyser.parent = eatingAnalyser


    return analyser