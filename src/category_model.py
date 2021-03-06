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

#load file and convert to pandas df
with open('../data/yelp_train_academic_dataset_business.json', 'r') as f:
    df = map(json.loads,f)
df = pd.DataFrame(df)

#pdb.set_trace()


class SelectCat(base.BaseEstimator, base.TransformerMixin):
    def fit(self, X, y=None):
        # fit the transformation
        return self

    def transform(self, X):
        return [dict((key, 1) for key in items) for items in X.categories]

'''
class CatShellEstimator(base.BaseEstimator, base.RegressorMixin):
    def __init__(self):
        self.transformer = CategoryVectorizer()
        self.model = linear_model.LassoCV()

    def fit(self, X, y):
        X_trans = self.transformer.fit(X, y).transform(X)
#        self.model.fit(X_trans, y)
#        self.mean_all = y.mean()
        return self
    
    def score(self, X, y):
        X_test = self.transformer.transform(X)
        return self.model.score(X_test, y)
    
    def predict(self, X):
        if ('categories' in X):
            X_test = self.transformer.transform(X)
            return self.model.predict(X_test)
        return self.mean_all

    def trans(self, X):
        print self.transformer.transform(X)
'''
from sklearn import pipeline

cat_pipe = pipeline.Pipeline([
        ('col_sel', SelectCat()),
        ('cat_vec', DictVectorizer()),
        ('c_tfidf', TfidfTransformer()),
        ('linreg', linear_model.LassoCV())
        ])

X, y = df,df['stars'].tolist()

#X, y = df.drop('stars', 1), df['stars']

print ('fitting')
cat_pipe.fit(X,y)
print('fitting complete')

with open('../pickle/cat.dill', "wb") as f:
    dill.dump(cat_pipe,f)

#cat  = CatShellEstimator()
#cat.fit(X, y)

test = df.sample()

pdb.set_trace()

test_dict = [dict((key, 1) for key in items) for items in test.categories]

#print ("Results:")
print (cat_pipe.predict(test_dict))
print (test['stars'])

#ipdb.set_trace()

