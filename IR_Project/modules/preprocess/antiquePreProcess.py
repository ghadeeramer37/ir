import pandas as pd

from modules.preprocess.preprocessores import *

########################################################################
#                           data section
########################################################################
def titlePreProcesse(text):
    
    tempText = toLower(text)
    tempText = removePunctuation(tempText)
    tempText = convertNumbers(tempText)
    tempText = removeWhiteSpace(tempText)
    tempText = removeStopWords(tempText)
    tempText = lemmatizeWords(tempText)
    return tempText

########################################################################

def preprocessedAntiqueData(dataFrame:pd.DataFrame):
    tempFrame = pd.DataFrame(columns = ['id', 'title'])
    tempFrame1 = pd.DataFrame(columns = ['id', 'title'])
    tempFrame2 = pd.DataFrame(columns = ['id', 'title'])
    tempFrame3 = pd.DataFrame(columns = ['id', 'title'])
    tempFrame4 = pd.DataFrame(columns = ['id', 'title'])

    for i in dataFrame.index[0:100000:1]:
        try:
            tempT = titlePreProcesse(dataFrame.loc[i, 'title'])
            dataf=pd.DataFrame([[dataFrame.loc[i,'id'],tempT]],columns=['id','title'])
            tempFrame1 = pd.concat([tempFrame1,dataf], ignore_index=True)
        except:
            print(i,dataFrame.loc[i, 'title'])
            continue
            #raise 

    for i in dataFrame.index[100000:200000:1]:
        try:
            tempT = titlePreProcesse(dataFrame.loc[i, 'title'])
            dataf=pd.DataFrame([[dataFrame.loc[i,'id'],tempT]],columns=['id','title'])
            tempFrame2 = pd.concat([tempFrame2,dataf], ignore_index=True)
        except:
            print(i,dataFrame.loc[i, 'title'])
            continue
            #raise  
      
    for i in dataFrame.index[200000:300000:1]:
        try:
            tempT = titlePreProcesse(dataFrame.loc[i, 'title'])
            dataf=pd.DataFrame([[dataFrame.loc[i,'id'],tempT]],columns=['id','title'])
            tempFrame3 = pd.concat([tempFrame3,dataf], ignore_index=True)
        except:
            print(i,dataFrame.loc[i, 'title'])
            continue
            #raise  
      
    for i in dataFrame.index[300000::1]:
        try:
            tempT = titlePreProcesse(dataFrame.loc[i, 'title'])
            dataf=pd.DataFrame([[dataFrame.loc[i,'id'],tempT]],columns=['id','title'])
            tempFrame4 = pd.concat([tempFrame4,dataf], ignore_index=True)
        except:
            print(i,dataFrame.loc[i, 'title'])
            continue
            #raise   
    
    tempFrame=pd.concat([tempFrame1,tempFrame2,tempFrame3,tempFrame4],ignore_index=True)
    tempFrame.fillna('', inplace=True)
    return tempFrame
########################################################################
#                           query section
########################################################################


def QueryTitlePreProcesse(a):
    tempText = toLower(a)
    tempText = removePunctuation(tempText)
    tempText = removeWhiteSpace(tempText)
    tempText = removeStopWords(tempText)
    tempText = stemmingWords(tempText)
    tempText = lemmatizeWords(tempText)
    return tempText
########################################################################

def preprocesseQuery(dataFrame:pd.DataFrame):
    tempFrame = pd.DataFrame(columns = ['id', 'title'])
    for i in dataFrame.index:
        try:
            tempTitle=None
            tempTilte=QueryTitlePreProcesse(dataFrame.loc[i,'title'])
            tempFrame.loc[len(tempFrame.index)] = [dataFrame.loc[i,'id'],tempTitle]
        except:
            print(i)
            continue
            #raise 
    
    tempFrame.fillna('', inplace=True)
    return tempFrame

########################################################################
#                           search input section
########################################################################

def preprocesseSearchInput(dataDic) -> pd.DataFrame:
    
    data = dataDic.get('query')
    tempI = 1
    tempW = QueryTitlePreProcesse(data)
    #tempT = addMostFreq(tempW)
    tempFrame = pd.DataFrame(columns = ['id', 'title'])
    tempFrame.loc[len(tempFrame.index)] = [tempI,tempW]
    
    tempFrame.fillna('', inplace=True)

    return tempFrame
########################################################################