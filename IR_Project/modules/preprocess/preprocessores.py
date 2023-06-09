


def toLower(text):
    ''' Convert text to lower case'''
    return text.lower()



################################################################
import inflect
p = inflect.engine()

import re
reg = r'([0-9]+)'

def isFLoat(strNum):
    '''converte float number to word'''
    try:
        float(strNum)
        return True
    except:
        return False


def convertNumbers(text):
    ''' Convert texnumbers to words'''
    tempText = text.split()
    newText = []
    for word in tempText:
        tempList = re.split(reg,word)
        for miniWord in tempList:
            if miniWord.isdigit() or isFLoat(miniWord):
                temp = p.number_to_words(miniWord)
                newText.append(removePunctuation(temp))
            else:
                newText.append(miniWord)        
    tempText = ' '.join(newText)
    return tempText

################################################################

import string
translator = str.maketrans(string.punctuation,' '*len(string.punctuation))
def removePunctuation(text):
    ''' remove punctuation from text'''
    global translator
    return text.translate(translator)

################################################################

def removeWhiteSpace(text):
    '''remove whitespace from text'''
    return " ".join(text.split())

################################################################

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist

def removeStopWords(text):
    ''' remove stopwords from text'''
    sw = set(stopwords.words("english"))
    wt = word_tokenize(text)
    filteredText = [word for word in wt if word not in sw]
    return ' '.join(filteredText)

################################################################


################################################################

from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize

stemmer = PorterStemmer()
def stemmingWords(text):
    ''' stemm words'''
    global stemmer
    wt = word_tokenize(text)
    stems = []
    for word in wt:
        temp = stemmer.stem(word)
        stems.append(temp)
    return ' '.join(stems)

################################################################

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from nltk import pos_tag, defaultdict

lemmatizer = WordNetLemmatizer()

tag_map = defaultdict(lambda: wn.NOUN)
tag_map['J'] = wn.ADJ
tag_map['V'] = wn.VERB
tag_map['R'] = wn.ADV

def lemmatizeWords(text):
    ''' lemmatize words'''
    tokens = word_tokenize(text)
    lmtzr = WordNetLemmatizer()
    lemmas = [lmtzr.lemmatize(token, tag_map[tag[0]]) for token, tag in pos_tag(tokens) ]
    return ' '.join(lemmas)

################################################################
from nltk.metrics.distance import jaccard_distance
from nltk.util import ngrams
from nltk.corpus import words

correct_words = words.words()
result = []

def correctWords(text):
    try:
        for word in text.split():
                temp = [(jaccard_distance(set(ngrams(word, 2)),
                                          set(ngrams(w, 2))),w)
                                          for w in correct_words if w[0] == word[0]]
                result.append(sorted(temp, key = lambda val:val[0])[0][1])
        return ' '.join(result)
    except:
        pass
    return ''

def QueryTitlePreProcesse(a):
    tempText = toLower(a)
    tempText = removePunctuation(tempText)
    tempText = removeWhiteSpace(tempText)
    tempText = removeStopWords(tempText)
    tempText = stemmingWords(tempText)
    tempText = lemmatizeWords(tempText)
    return tempText