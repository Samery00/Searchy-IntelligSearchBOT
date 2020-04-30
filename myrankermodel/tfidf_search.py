import pandas as pd
import numpy as np
import os
import re
import operator
import pickle
from collections import defaultdict
from nltk.corpus import wordnet as wn
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from clean_data import wordLemmatizer


data = pd.read_csv("data_processed.csv")
## Create Vocabulary
vocabulary = set()

for doc in data.Clean_Keyword:
    vocabulary.update(doc.split(','))

vocabulary = list(vocabulary)

# Intializating the tfIdf model
tfidf = TfidfVectorizer(vocabulary=vocabulary,dtype=np.float32)

# Fit the TfIdf model
tfidf.fit(data.Clean_Keyword)

# Transform the TfIdf model
tfidf_tran=tfidf.transform(data.Clean_Keyword)

with open('tfid.pkl','wb') as handle:
    pickle.dump(tfidf_tran, handle)

### load model
# t = pickle.load(open('tfid.pkl','rb'))

### Save Vacabulary
with open("vocabulary_websites.txt", "w", encoding="utf-8") as file:
    file.write(str(vocabulary))
### load Vacabulary
# with open("vocabulary_websites.txt", "r", encoding="utf-8") as file:
    # data2 = eval(file.readline())


## Create vector for Query/search keywords

def gen_vector_T(tokens):

    Q = np.zeros((len(vocabulary)))

    x= tfidf.transform(tokens)
    for token in tokens[0].split(','):
        try:
            ind = vocabulary.index(token)
            Q[ind]  = x[0, tfidf.vocabulary_[token]]
        except:
            pass
    return Q

# Calculate Cosine Similarity with formula
def cosine_sim(a, b):
    cos_sim = np.dot(a, b)/(np.linalg.norm(a)*np.linalg.norm(b))
    return cos_sim

# Calculate Cosine similarity of trained Tfidf to input query
def cosine_similarity_T(num_results, query):
    #print("Cosine Similarity")
    preprocessed_query = preprocessed_query = re.sub("\W+", " ", query).strip()
    tokens = word_tokenize(str(preprocessed_query))
    q_df = pd.DataFrame(columns=['q_clean'])
    q_df.loc[0,'q_clean'] =tokens
    q_df['q_clean'] =wordLemmatizer(q_df.q_clean)
    q_df=q_df.replace(to_replace ="\[.", value = '', regex = True)
    q_df=q_df.replace(to_replace ="'", value = '', regex = True)
    q_df=q_df.replace(to_replace =" ", value = '', regex = True)
    q_df=q_df.replace(to_replace ='\]', value = '', regex = True)
    #print("\nQuery:", query)
    #print("")
    #print(tokens)

    d_cosines = []

    query_vector = gen_vector_T(q_df['q_clean'])

    for d in tfidf_tran.A:

        d_cosines.append(cosine_sim(query_vector, d))

    out = np.array(d_cosines).argsort()[-num_results:][::-1]
    #print("")
    d_cosines.sort()
    #print(out)
    results = pd.DataFrame()
    for i,index in enumerate(out):
        results.loc[i,'ID'] = str(index)
        results.loc[i,'title'] = data['title'][index]
        results.loc[i,'contents'] = data['contents'][index]
        results.loc[i,'url'] = data['url'][index]
    for j,simScore in enumerate(d_cosines[-num_results:][::-1]):
        results.loc[j,'Score'] = simScore
    return results
results = cosine_similarity_T(10,'privacy, data')
print(results)
