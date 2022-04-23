import pandas as pd
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from collections import Counter
import pickle
import language_tool_python


global model
global vectorizer
global minmax_scalar


# to count the no. of occurences of each pos tag
def countpos(l, pos):
    cnt = 0
    for x in l:

        if x == pos:
            cnt = cnt + 1
    return cnt


def preprocess(essay):
    tool = language_tool_python.LanguageTool('en-US')
    nlp = spacy.load('en_core_web_sm')

    dict = {}


    res = pd.DataFrame(
        columns=[ 'mistake_count', 'sentence_count', 'noun', 'verb', 'adj', 'punct', 'adv', 'pron',
                 'ner_count', 'pos' ])

    txt = essay
    strings = txt.split('.')  # making the splits at '.'
    tot_mist = 0
    for i in range(0, len(strings)):  ## go to every sentence
        s = strings[i]
        # print(i,s)
        mistakes = tool.check(s)
        tot_mist = tot_mist + len(mistakes)

    dict['mistake_count'] = tot_mist
    dict['sentence_count'] = len(strings)

    pos = []
    ner = []
    #tokens = []
    #stop_wrds = []
    #stop_words = set(STOP_WORDS)

    essay = [essay]

    for ess in nlp.pipe(essay):
        if ess.has_annotation("DEP"):
            # add the pos tag for each word in the esssay to the list
            pos.append([e.pos_ for e in ess])
            # add the NER present in the essay tothe list
            ner.append([e.text for e in ess.ents])
            # add the tokens present in the essay to the list
            #tokens.append([e.text for e in ess])

    import itertools
    dict['pos'] = pos[0]
    #print(dict['pos'])

    dict['ner_count'] = len(ner[0])
    #dict['tokens'] = tokens
    dict['noun'] = countpos(dict['pos'], 'NOUN')

    dict['adv'] = countpos(dict['pos'], 'ADV')
    dict['adj'] = countpos(dict['pos'], 'ADJ')
    dict['verb'] = countpos(dict['pos'], 'VERB')
    dict['pron'] = countpos(dict['pos'], 'PRON')
    dict['punct'] = countpos(dict['pos'], 'PUNCT')

    res.loc[len(res.index)] = [ dict['mistake_count'], dict['sentence_count'], dict['noun'],
                               dict['verb'], dict['adj'], dict['punct'], dict['adv'], dict['pron'], dict['ner_count'],
                               dict['pos']]
    res.drop(['pos'],axis='columns',inplace=True)

    '''Scale'''

    minmax_scalar = pickle.load(open('minmax_scalar.pickle', 'rb'))
    X_minmax = pd.DataFrame(minmax_scalar.transform(res),columns=[res.columns])

    return X_minmax


def loading_artifacts():

    global model

    global minmax_scalar

    with open('RF_scaled_model.pickle', 'rb') as f:  # since the model was saved as binary file we use 'rb'
        model = pickle.load(f)


    minmax_scalar = pickle.load(open('minmax_scalar.pickle', 'rb'))

def predict(df):

    return model.predict(df)


if __name__=='__main__':
    loading_artifacts()
    rest=preprocess('hello')
    print(rest,type(rest))
    t=predict(rest)
    print(t)









