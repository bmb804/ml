import gzip
import pdb
import numpy as np
import sklearn.base as base
from sklearn import linear_model
#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import json
import pandas as pd
import dill
from sklearn import pipeline

#with open('est1.dill', 'rb') as f:
#    est1 = dill.load(f)
#with open('cat1.dill', 'rb') as f:
#    cat1 = dill.load(f)
#with open('att1.dill', 'rb') as f:
#    att1 = dill.load(f)
#with gzip.open('she1.dill.gz', 'rb') as f:
#    she1 = dill.load(f)

class EstTransformer(base.BaseEstimator, base.TransformerMixin):

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        import dill
        with open('../pickle/ml/est1.dill', 'rb') as f:
            est1 = dill.load(f)
        return est1.predict(X).reshape(-1,1) # transformation

class CatTransformer(base.BaseEstimator, base.TransformerMixin):

    def fit(self, X, y=None):
        return self
            
    def transform(self, X):
        import dill
        with open('../pickle/ml/cat1.dill', 'rb') as f:
            cat1 = dill.load(f)
        return cat1.predict(X).reshape(-1,1) # transformation

class AttTransformer(base.BaseEstimator, base.TransformerMixin):

    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        import dill
        with open('../pickle/ml/att1.dill', 'rb') as f:
            att1 = dill.load(f)
        return att1.predict(X).reshape(-1,1) # transformation

class SheTransformer(base.BaseEstimator, base.TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        import dill
        import gzip
        with gzip.open('../pickle/ml/she1.dill.gz', 'rb') as f:
            she1 = dill.load(f)
        return she1.predict(X).reshape(-1,1) # transformation

#load file and convert to pandas df
with open('../data/yelp_train_academic_dataset_business.json', 'r') as f:
    df = map(json.loads,f)
df = pd.DataFrame(df)
y = df['stars'].tolist()

af = pipeline.FeatureUnion([
            ('rest', EstTransformer()),
            ('rshe', SheTransformer()),
            ('rcat', CatTransformer()),
            ('ratt', AttTransformer()),
            ])

all_pipe = pipeline.Pipeline([
            ('features', af),
            ('lasso', linear_model.LinearRegression(fit_intercept=True))
            ])

print ('fitting')
all_pipe.fit(df,y)
print('fitting complete')

with open('../pickle/all.dill', "wb") as f:
    dill.dump(all_pipe,f)

test = df.sample()

test_dict = [test.attributes]

pdb.set_trace()

#print (att_pipe.predict(test_dict))
#print (test['stars'])
