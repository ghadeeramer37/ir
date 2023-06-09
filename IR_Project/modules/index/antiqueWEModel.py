from statistics import mode
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from modules.index.antiqueModel import matching
from nltk.tokenize import word_tokenize
import gensim
from gensim.models import Word2Vec   

model=None
vectors=[]
def readData(data:pd.DataFrame):
    words:list=[]
    for id in data.index[1:]:
        tempWords=[]
        wt = word_tokenize(data.loc[id,'title'])
        for word in wt:
            tempWords.append(word)
        words.append(tempWords)
    return words
########################################################################
def makeModel(words:list):
    global model
    model=gensim.models.Word2Vec(words,min_count=1,vector_size=300,window=5)
    model.train(words, total_examples=len(words), epochs=10) 
##############################################################

def saveModel():
    global model
    model.save('word_embedding_model_final_training_words.bin')


#########################################################    
def loadModel():
    global model
    model = Word2Vec.load('word_embedding_model_final_training_words.bin')

#####################################################    

def makeVectors(dataFrame:pd.DataFrame()):
    global vectors
    try:
        for id in dataFrame.index:
            avgword2vec =None
            count=0
            tempTitle=dataFrame.loc[id,'title']
            for word in tempTitle.split():
                if word in model.wv:
                    count+=1
                    if avgword2vec is None:
                        avgword2vec  =model.wv[word]
                    else:
                        avgword2vec =avgword2vec + model.wv[word]

            if avgword2vec is not None:
                avgword2vec = avgword2vec / count

                vectors.append(avgword2vec)
            else:
                vectors.append([0]*300) 
        #print(len(te), len(vectors))
        
    except:
        print("error")


##########################################################################
def makeVectorQuery(query:str):
    try:
            avg=None
            count=0
            for word in query.split():
                if word in model.wv:
                    count+=1
                    if avg is None:
                        avg=model.wv[word]
                    else:
                        avg=avg+model.wv[word]
            if avg is not None:
                avg=avg/count
                return [avg]
    except:
        print('error')        
#######################################################
def matching(query)->np.ndarray:
    global vectors
    queryVector=makeVectorQuery(query)
    cosine_sim=cosine_similarity(queryVector,vectors).flatten()
    return cosine_sim
#################################################
def executionQuery(qDataFrame:pd.DataFrame,data:pd.DataFrame, n):
    ''' search for all queries in the queries file and get the most n similar document .I'''
    result = pd.DataFrame(columns=['qid','rid','rank'])
    
    for i in qDataFrame.index:
        tempFrame =pd.DataFrame(columns=['qid','rid','rank'])
        try:
            resultDict:dict = {}
            #tempIds:list = matching(pd.DataFrame(qDataFrame.loc[qDataFrame.index == i,:]))
            #tempW = QueryTitlePreProcesse(qDataFrame.loc[i,'title'])
            tempW=qDataFrame.loc[i,'title']
            tempFrame1= pd.DataFrame(columns = ['id', 'title'])
            tempFrame1.loc[len(tempFrame.index)] = [1,tempW]
            
            #query=QueryTitlePreProcesse(qDataFrame.loc[i,'title'])
            tempIds:list = matching(tempFrame1)
            tempIds = tempIds.argsort(axis=0)[-n:][::-1] 
            tempList = []
            qid=qDataFrame.loc[i,'query_id']
            for id in tempIds[0:n:]:
                #dataf=pd.DataFrame([qid,id])
                tempFrame.loc[len(tempFrame.index)] = [qid,data.loc[id,'id'],id]
            result = pd.concat([result,tempFrame], ignore_index=True)
                
        except:
            print(i)
            #raise
    return result

    
########################################################################
def absSub(a,b):
    return abs(a-b)

def search(qDF:pd.DataFrame,data:pd.DataFrame, n):
    ''' search for input and return list of ids of the result'''
    try:
        resultlis = []
        similars = matching(qDF)
        tempIds = similars.argsort(axis=0)[-n:][::-1]
        tempFrame = pd.DataFrame(columns = ['id', 'title'])
        for i in tempIds:
            tempFrame.loc[len(tempFrame.index)] = [data.loc[i,'id'],data.loc[i,"title"]]
        return tempFrame
    except:
        print("false")
        raise

#################################