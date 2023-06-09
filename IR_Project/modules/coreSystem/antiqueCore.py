from ..preprocess import antiquePreProcess, preprocessores
from ..index import antiqueModel,antiqueWEModel
import pandas as pd
################################################################
#                              DATA
################################################################
#                           INITIALIZE
################################################################

antiqueData = None
antiquePPData = None
def initializeAntiqueModel():
    global  antiquePPData, antiqueData
    antiqueData:pd.DataFrame = pd.read_table('data\collection.tsv')
    antiquePPData:pd.DataFrame = pd.read_table('data\preprocessData.tsv')
    antiqueModel.initializeTfidfTable(antiquePPData)
    antiqueWEModel.loadModel()
    antiqueWEModel.makeVectors(antiquePPData)




################################################################
#                           SEARCH 
################################################################

def search(data):
    #antiqueData:pd.DataFrame = pd.read_table("data\collection.tsv")
    dataAfCorrection = preprocessores.correctWords(data.get('query'))
    dataPD: pd.DataFrame = antiquePreProcess.preprocesseSearchInput(data)
    global antiqueData 
    resultIds = antiqueModel.search(dataPD, antiqueData, data.get('n'))
    resultDict = {
        'reslutDictionary':{
            'result':{},
            'correction':dataAfCorrection
        }
    }
    return resultToDict(resultDict, resultIds)



################################################################

def searchWE(data):
    #antiqueData:pd.DataFrame = pd.read_table("data\collection.tsv")
    dataAfCorrection = preprocessores.correctWords(data.get('query'))
    dataPD: pd.DataFrame = antiquePreProcess.preprocesseSearchInput(data)
    global antiqueData
    resultIds = antiqueWEModel.search(dataPD, antiqueData, data.get('n'))
    resultDict = {
        'reslutDictionary':{
            'result':{},
            'correction':dataAfCorrection
        }
    }
    return resultToDict(resultDict, resultIds)




################################################################
##                          HELPERS
################################################################
def resultToDict(resultDict, resultIds):
    global antiqueData
    for i in range(0,len(resultIds)):
        temp = antiqueData.loc[antiqueData['id'] == resultIds[i],\
             ['title']].to_dict()

        tk = list(temp.keys())
        for sk in tk:
            k = list(temp[sk].keys())
            temp[sk] = temp[sk][k[0]]


        resultDict['reslutDictionary']['result'][i] = temp

    return resultDict

