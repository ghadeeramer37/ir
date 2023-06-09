from logging import exception
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import  cosine_similarity
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import FeatureUnion, Pipeline


########################################################################

transformer = None
tfidfTable  = None
def initializeTfidfTable(data: pd.DataFrame):
    #global transformer, tfidfTable
    transformer = FeatureUnion([('title_tfidf', 
                      Pipeline([
                        ('extract_field',
                                  FunctionTransformer(lambda x: x['title'], 
                                                      validate=False)),
                                ('tfidf', 
                                  TfidfVectorizer(norm='l1' ,ngram_range=(1,2)))]))                              
                      
    ])
    tfidfTable = transformer.fit_transform(data.dropna())
########################################################################
def matching(query):
    global transformer, tfidfTable
    querytfidf = transformer.transform(query)

    return cosine_similarity(querytfidf,tfidfTable).flatten()
    

########################################################################

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
        similars = matching(qDF)
        tempIds = similars.argsort(axis=0)[-n:][::-1]
        tempFrame = pd.DataFrame(columns = ['id', 'title'])
        for i in tempIds:
            tempFrame.loc[len(tempFrame.index)] = [data.loc[i,'id'],data.loc[i,"title"]]
        return tempFrame
    except:
        print("false")
        raise

########################################################################