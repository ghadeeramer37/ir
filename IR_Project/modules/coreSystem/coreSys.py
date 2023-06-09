from .import antiqueCore

corpus = 'corpus'
################################################################
#                           INITIALIZE 
################################################################
def initialize():
    antiqueCore.initializeAntiqueModel()


################################################################
#                           SEARCH 
################################################################

def search(data:dict):
     return antiqueCore.search(data)

################################################################


def searchWE(data:dict):
    return antiqueCore.searchWE(data)
    



