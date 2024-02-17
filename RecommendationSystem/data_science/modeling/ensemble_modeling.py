# %%

import pandas as pd
import numpy as np
import re
import time
import glob
import tqdm
from datetime import datetime, timezone
import joblib as jb

from sklearn import tree
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score
from sklearn.preprocessing import MaxAbsScaler, StandardScaler
from sklearn.pipeline import make_pipeline

from lightgbm import LGBMClassifier

from scipy.sparse import csr_matrix
from scipy.sparse import hstack, vstack

# %%

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

# Random Forest

mdl_rf = RandomForestClassifier(n_estimators=1000, random_state=0, min_samples_leaf=1, class_weight="balanced", n_jobs=6)
mdl_rf.fit(Xtrain_wtitle, ytrain)

# %%
p_rf = mdl_rf.predict_proba(Xval_wtitle)[:, 1]

# %%
average_precision_score(yval, p_rf), roc_auc_score(yval, p_rf)

# %%

# LGBM
params = [0.05, 7, 1, 0.7251351011494334, 0.07547006552546137, 839, 1, 2]
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

mdl_lgbm = LGBMClassifier(learning_rate=lr, num_leaves=2 ** max_depth, max_depth=max_depth, 
                     min_child_samples=min_child_samples, subsample=subsample,
                     colsample_bytree=colsample_bytree, bagging_freq=1,n_estimators=n_estimators, random_state=0, 
                     class_weight="balanced", n_jobs=6)
mdl_lgbm.fit(Xtrain_wtitle, ytrain)

p_lgbm = mdl_lgbm.predict_proba(Xval_wtitle)[:, 1]

# %%
average_precision_score(yval, p_lgbm), roc_auc_score(yval, p_lgbm)

# %%

# Logistic Regression

Xtrain_wtitle2 = csr_matrix(Xtrain_wtitle.copy())
Xval_wtitle2 = csr_matrix(Xval_wtitle.copy())

#scaler = StandardScaler()
#scaler = MaxAbsScaler()

#Xtrain_wtitle2[:, :2] = scaler.fit_transform(Xtrain_wtitle2[:, :2].todense())
#Xval_wtitle2[:, :2] = scaler.transform(Xval_wtitle2[:, :2].todense())
#Xtrain_wtitle2 = scaler.fit_transform(Xtrain_wtitle2)
#Xval_wtitle2 = scaler.transform(Xval_wtitle2)

lr_pipeline = make_pipeline(MaxAbsScaler(), LogisticRegression(C=1, penalty='l2',n_jobs=6, random_state=0))
lr_pipeline.fit(Xtrain_wtitle2, ytrain)

p_lr = lr_pipeline.predict_proba(Xval_wtitle2)[:, 1]

# %%
average_precision_score(yval, p_lr), roc_auc_score(yval, p_lr)

# %%
# previous results

# (0.31859071600360855, 0.6888655462184874) - RF
# (0.3220147516688634, 0.6121848739495799) - LGBM
# (0.32282593488244726, 0.680366692131398) - LR

# Ensemble 
p = (p_lr + p_rf + p_lgbm)/3
average_precision_score(yval, p), roc_auc_score(yval, p)

# %%

# Models score correlation
pd.DataFrame({"LR": p_lr, "RF": p_rf, "LGBM": p_lgbm}).corr()

# %%
# Ponderations

p = 0.6*p_rf + 0.2*p_lgbm + 0.2*p_lr
average_precision_score(yval, p), roc_auc_score(yval, p)

# (0.31859071600360855, 0.6888655462184874) - RF
# (0.3220147516688634, 0.6121848739495799) - LGBM
# (0.32282593488244726, 0.680366692131398) - LR
# (0.34412283003356553, 0.6845874713521773) - LR + RF + LGBM
# (0.34188688022487945, 0.6674560733384263) - 0.5LR + 0.5LGBM
# (0.34412283003356553, 0.6845874713521773) - 0.5RF + 0.5LGBM
# (0.34454918453266775, 0.6936783804430865) - 0.7RF + 0.3LGBM
# (0.3374454514151525, 0.6761077158135981)- 0.7LR + 0.3LGBM
# (0.3443247914706543, 0.6969251336898397) -  0.6RF + 0.2LGBM + 02LR

# %%
# Save models
jb.dump(mdl_lgbm, "../../data_science/models/lgbm_20240217.pkl.z")
jb.dump(mdl_rf, "../../data_science/models/random_forest_20240217.pkl.z")
jb.dump(lr_pipeline, "../../data_science/models/logistic_reg_20240217.pkl.z")
jb.dump(title_vec, "../../data_science/models/title_vectorizer_20240217.pkl.z")
