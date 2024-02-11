# %%

## Data Processing to Active Learning Model

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
import graphviz

from scipy.sparse import hstack, vstack

pd.set_option("display.max_columns", 30)
%matplotlib inline

# %%
df = pd.read_csv("../../dataset/silver/general_table_youtube_2024-02-10 06:24:00.csv")
df = df[df["y"].notnull()]
df['publishedAt'] = pd.to_datetime(df['publishedAt'], infer_datetime_format=True)
df["date"] = pd.to_datetime(df['publishedAt'].dt.date)

# %%
# Features
features = pd.DataFrame(index=df.index)

y = df["y"].copy()

# %%
current_time = datetime.now(timezone.utc)
features["time_since_pub"] = (pd.to_datetime(current_time) - df["publishedAt"]) / np.timedelta64(1, "D")
features["views"] = df["statistics.viewCount"]
features["views_by_day"] = features["views"] / features["time_since_pub"]
features = features.drop(["time_since_pub"], axis=1)

# %%
# Split Data Set
mask_train = df['date'] < "2022-01-01"
mask_val = df['date'] >= "2022-01-01"
Xtrain, Xval = features[mask_train], features[mask_val]
ytrain, yval = y[mask_train], y[mask_val]
Xtrain.shape, Xval.shape, ytrain.shape, yval.shape


# %%
# TFid tectnique to extract text information from title.

title_train = df[mask_train]["title"]
title_val = df[mask_val]["title"]

title_vec = TfidfVectorizer(min_df=2)
title_bow_train = title_vec.fit_transform(title_train)
title_bow_val = title_vec.transform(title_val)

# %%
Xtrain_wtitle = hstack([Xtrain, title_bow_train])
Xval_wtitle = hstack([Xval, title_bow_val])

# %%
mdl = RandomForestClassifier(n_estimators=1000, random_state=0, class_weight="balanced", n_jobs=6)
mdl.fit(Xtrain_wtitle, ytrain)

# %%
p = mdl.predict_proba(Xval_wtitle)[:, 1]

# %%
average_precision_score(yval, p)

# %%
roc_auc_score(yval, p)