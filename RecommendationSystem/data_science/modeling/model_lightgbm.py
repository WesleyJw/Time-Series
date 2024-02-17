# %%

## Machine Learning Model - LightGBM and Bayesin Optimization

import pandas as pd
import numpy as np
import re
import time
import glob
import tqdm
from datetime import datetime, timezone

from sklearn import tree
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score
from lightgbm import LGBMClassifier
from skopt import forest_minimize

from scipy.sparse import hstack, vstack

# %%
#scikit-learn = "1.2.2"
# Loading data
df = pd.read_csv("../../dataset/gold/general_table_youtube_taged.csv")
df['publishedAt'] = pd.to_datetime(df['publishedAt'], infer_datetime_format=True)
df["date"] = pd.to_datetime(df['publishedAt'].dt.date)


# %%
df_clean = pd.DataFrame(index=df.index)
df_clean['title'] = df['title']
df_clean['publishedAt'] = df['publishedAt']
df_clean["date"] = df["date"] 
df_clean["statistics.viewCount"] = df["statistics.viewCount"]


# %%
# Features

features = pd.DataFrame(index=df_clean.index)
y = df['y'].copy()


# %%
current_time = datetime.now(timezone.utc)
features["time_since_pub"] = (pd.to_datetime(current_time) - df_clean["publishedAt"]) / np.timedelta64(1, "D")
features["views"] = df_clean["statistics.viewCount"]
features["views_by_day"] = features["views"] / features["time_since_pub"]
features = features.drop(["time_since_pub"], axis=1)


# %%
features.tail()


# %%

# Spliting Data

mask_train = (df_clean['date'] < "2022-01-01") 

mask_val = (df_clean['date'] >= "2022-01-01")

Xtrain, Xval = features[mask_train], features[mask_val]
ytrain, yval = y[mask_train], y[mask_val]
Xtrain.shape, Xval.shape, ytrain.shape, yval.shape


# %%

title_train = df_clean[mask_train]['title']
title_val = df_clean[mask_val]['title']

title_vec = TfidfVectorizer(min_df=2, ngram_range=(1,4))
title_bow_train = title_vec.fit_transform(title_train)
title_bow_val = title_vec.transform(title_val)

# %%

Xtrain_wtitle = hstack([Xtrain, title_bow_train])
Xval_wtitle = hstack([Xval, title_bow_val])

Xtrain_wtitle.shape, Xval_wtitle.shape

# %%

mdl = LGBMClassifier(random_state=0, class_weight="balanced", n_jobs=6)
mdl.fit(Xtrain_wtitle, ytrain)

# %%

p = mdl.predict_proba(Xval_wtitle)[:, 1]

# %%
average_precision_score(yval, p), roc_auc_score(yval, p)

# %%

# Bayesian Optimization

def tune_lgbm(params):
    print(params)
    lr = params[0]
    max_depth = params[1]
    min_child_samples = params[2]
    subsample = params[3]
    colsample_bytree = params[4]
    n_estimators = params[5]
    
    min_df = params[6]
    ngram_range = (1, params[7])
    
    title_vec = TfidfVectorizer(min_df=min_df, ngram_range=ngram_range)
    title_bow_train = title_vec.fit_transform(title_train)
    title_bow_val = title_vec.transform(title_val)
    
    Xtrain_wtitle = hstack([Xtrain, title_bow_train])
    Xval_wtitle = hstack([Xval, title_bow_val])
    
    mdl = LGBMClassifier(learning_rate=lr, num_leaves=2 ** max_depth, max_depth=max_depth, 
                         min_child_samples=min_child_samples, subsample=subsample,
                         colsample_bytree=colsample_bytree, bagging_freq=1,n_estimators=n_estimators, random_state=0, 
                         class_weight="balanced", n_jobs=6)
    mdl.fit(Xtrain_wtitle, ytrain)
    
    p = mdl.predict_proba(Xval_wtitle)[:, 1]
    
    print(roc_auc_score(yval, p))
    
    return -average_precision_score(yval, p)


# %%

space = [(1e-3, 1e-1, 'log-uniform'), # lr
          (1, 10), # max_depth
          (1, 20), # min_child_samples
          (0.05, 1.), # subsample
          (0.05, 1.), # colsample_bytree
          (100,1000), # n_estimators
          (1,5), # min_df
          (1,5)] # ngram_range

res = forest_minimize(tune_lgbm, space, random_state=160745, n_random_starts=20, n_calls=50, verbose=1)


# %%

res.x
# %%
