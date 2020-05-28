from DataAnalyser import DataAnalyser
from DataAnalyser.KNN import VGG16

def getAnalyser(args):
    analyser = None

    if(args["analyser"]=="VGG16"):
        analyser = VGG16.VGG16imagenetKNN()

    return analyser