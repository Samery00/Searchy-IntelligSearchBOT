import nltk
from nltk.corpus import reuters

nltk.download("reuters")
nltk.download("punkt")

max_samples = 256
categories = ['wheat', 'tea', 'strategic-metal',
              'housing', 'money-supply', 'fuel']

S, X, Y = [], [], []

for category in categories:
  print(category)

  sents = reuters.sents(categories=category)
  sents = [' '.join(sent) for sent in sents][:max_samples]
  X.append(bert_vectorizer(sents, verbose=True))
  Y += [category] * len(sents)
  S += sents

X = np.vstack(X)
X.shape
    
