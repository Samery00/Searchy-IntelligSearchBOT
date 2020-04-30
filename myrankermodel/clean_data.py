import json
import pandas as pd
import numpy as np
import os
import re
import operator
import pickle
import nltk
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
import pymongo


pd.set_option('mode.chained_assignment', None)

def wordLemmatizer(data):
    Langage = 'english'
    tag_map = defaultdict(lambda : wn.NOUN)
    tag_map['J'] = wn.ADJ
    tag_map['V'] = wn.VERB
    tag_map['R'] = wn.ADV
    file_clean_k =pd.DataFrame()
    for index,entry in enumerate(data):

        # Declaring Empty List to store the words that follow the rules for this step
        Final_words = []
        # Initializing WordNetLemmatizer()
        word_Lemmatized = WordNetLemmatizer()
        # pos_tag function below will provide the 'tag' i.e if the word is Noun(N) or Verb(V) or something else.
        for word, tag in pos_tag(entry):
            # Below condition is to check for Stop words and consider only alphabets
            if len(word)>1 and word not in stopwords.words(Langage) and word.isalpha():
                word_Final = word_Lemmatized.lemmatize(word,tag_map[tag[0]])
                Final_words.append(word_Final)
            # The final processed set of words for each iteration will be stored in 'text_final'
                file_clean_k.loc[index,'Keyword_final'] = str(Final_words)
                file_clean_k.loc[index,'Keyword_final'] = str(Final_words)
                #file_clean_k=file_clean_k.replace(to_replace ="\[.", value = '', regex = True)
                #file_clean_k=file_clean_k.replace(to_replace ="'", value = '', regex = True)
                #file_clean_k=file_clean_k.replace(to_replace =" ", value = '', regex = True)
                #file_clean_k=file_clean_k.replace(to_replace ='\]', value = '', regex = True)
    return file_clean_k

if __name__ == "__main__":
    # connection = pymongo.MongoClient("localhost", 27017)
    # db = connection["Knowledge_Base"]
    # collection = db["websites"]
    # # df = collection.find()
    # docs = pd.DataFrame(list(collection.find()))
    # # for num, doc in enumerate(collection.find()):
    # #     doc["_id"] = str(doc["_id"])
    # #     # get document _id from dict
    # #     doc_id = doc["_id"]
    # #     # create a Series obj from the MongoDB dict
    # #     series_obj = pd.Series( doc, name=doc_id )
    # #     # append the MongoDB Series obj to the DataFrame obj
    # #     docs = docs.append( series_obj )

    # d = pd.DataFrame(list(collection.find()))
    # docs.to_json('knowledge_Data.json')
    # dataset = docs[:10].copy(deep=True)
    dataset = pd.read_json('websites.json')
    print(dataset)
    data = dataset[['title','contents','url']]
    print(data[:10])
    data['contents']=[entry.lower() for entry in data['contents']]
    data.title = data.title.replace(to_replace='lines:(.*\n)',value='',regex=True)
    data.title =data.title.replace(to_replace='  ',value='',regex=True)
    data.contents =data.contents.replace(to_replace='from:(.*\n)',value='',regex=True) #remove from to email
    data.contents =data.contents.replace(to_replace='lines:(.*\n)',value='',regex=True)
    data.contents =data.contents.replace(to_replace='[!"#$%&\'()*+,/:;<=>?@[\\]^_`{|}~]',value=' ',regex=True) #remove punctuation except
    data.contents =data.contents.replace(to_replace='-',value=' ',regex=True)
    data.contents =data.contents.replace(to_replace='\s+',value=' ',regex=True)    #remove new line
    data.contents =data.contents.replace(to_replace='  ',value='',regex=True)                #remove double white space
    data.contents =data.contents.apply(lambda x:x.strip())  # Ltrim and Rtrim of whitespace
    data.title =data.title.apply(lambda x:x.strip())  # Ltrim and Rtrim of whitespace

    # for i,sen in enumerate(data.contents):
    #     if len(sen.strip()) ==0:
    #         # print(str(i))
    #         data=data.drop(str(i),axis=0).reset_index().drop('index',axis=1)
    print("Here tokenization started")
    data['Word tokenize']= [word_tokenize(entry) for entry in data.contents]

    print("Here lemmatizing started")
    data_clean = wordLemmatizer(data['Word tokenize'])
    data_clean=data_clean.replace(to_replace ="\[.", value = '', regex = True)
    data_clean=data_clean.replace(to_replace ="'", value = '', regex = True)
    data_clean=data_clean.replace(to_replace =" ", value = '', regex = True)
    data_clean=data_clean.replace(to_replace ='\]', value = '', regex = True)

    data.insert(loc=4, column ='Clean_Keyword', value=data_clean['Keyword_final'].tolist())
    print("Here exporting data started")
    data.to_csv("data_processed.csv", index=False, header=True)
