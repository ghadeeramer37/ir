from sklearn.metrics import precision_score, recall_score
import pandas as pd

def reSizeLists(l1:list, l2:list, n :int):
    '''resize lists to have the same len'''
    
    if len(l1) < len(l2):
        l2 = l2[0:len(l1)]
    while len(l1) > len(l2):
        l1 = l1[0:len(l2)]
    if len(l1)<n:
        n=len(l1)
    return l1[0:n], l2[0:n]

def getQrelsArray( qrelsData: pd.DataFrame,qid):
    qrelsArray:list = []
    for index in qrelsData.index:
        if qrelsData.loc[index,'query_id']==qid:
            qrelsArray.append(qrelsData.loc[index,'relevance'])
    return qrelsArray

###############################################
def precisionAtK(resData:pd.DataFrame, qrelsData: pd.DataFrame,n):
    precisionsAtK:list = []
    for i in resData.index[1::10]:
        resArray:list = []
        for inde in range(int(i),int(i)+10):
            resArray.append(resData.loc[inde,'rid'])
        qrelsArray=getQrelsArray(qrelsData,resData.loc[i,'qid'])
        if len(qrelsArray) == 0: 
            continue
        resArray, qrelsArray = reSizeLists(resArray, qrelsArray,n)
        precisionsAtK.append(precision_score(qrelsArray, resArray, average='micro'))
    return sum(precisionsAtK) / len(precisionsAtK)

################################################################
def recallsAtK(resData:pd.DataFrame, qrelsData: pd.DataFrame,n):
    recallsAtK:list = []
    for i in resData.index[1::10]:
        resArray:list = []
        for inde in range(int(i),int(i)+10):
            resArray.append(resData.loc[inde,'rid'])
        qrelsArray=getQrelsArray(qrelsData,resData.loc[i,'qid'])
        if len(qrelsArray) == 0: 
            continue
        resArray, qrelsArray = reSizeLists(resArray, qrelsArray,n)
        recallsAtK.append(recall_score(qrelsArray, resArray, average='micro'))
    return sum(recallsAtK) / len(recallsAtK)

###############################################################
def MAPAtK(resData:pd.DataFrame, qrelsData: pd.DataFrame,n):
    APAtk:list=[]
    for i in resData.index[1::10]:
        resArray:list = []
        for inde in range(int(i),int(i)+10):
            resArray.append(resData.loc[inde,'rid'])
        qrelsArray=getQrelsArray(qrelsData,resData.loc[i,'qid'])
        if len(qrelsArray) == 0: 
            continue
        resArray, qrelsArray = reSizeLists(resArray, qrelsArray,n)
        for id in len(resArray):
            resArray, qrelsArray = reSizeLists(resArray, qrelsArray,id)
            APAtk.append(precision_score(qrelsArray,resArray,average='micro'))
    return sum(APAtk) / len(APAtk)

###############################################################    
def MRR(resData:pd.DataFrame,qrelsData: pd.DataFrame):
    mrr:list=[]
    for i in resData.index[1::10]:
        resArray:list = []
        for inde in range(int(i),int(i)+10):
            resArray.append(resData.loc[inde,'rid'])
        qrelsArray=getQrelsArray(qrelsData,resData.loc[i,'qid'])
        
        for id in len(resArray):
            if resArray[id] in qrelsArray:
                mrr.appent(1/(id+1))
                break
    
    return sum(mrr)/len(mrr)  