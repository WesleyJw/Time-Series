# %%

## Data Processing to Active Learning Model

import pandas as pd
import numpy as np
from datetime import datetime, timezone

from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
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
# TFidf tectnique to extract text information from title.

title_train = df[mask_train]["title"]
title_val = df[mask_val]["title"]

title_vec = TfidfVectorizer(min_df=2)
title_bow_train = title_vec.fit_transform(title_train)
title_bow_val = title_vec.transform(title_val)

# %%
Xtrain_wtitle = hstack([Xtrain, title_bow_train])
Xval_wtitle = hstack([Xval, title_bow_val])

# %%
# Training a Random Forest Classifier
mdl = RandomForestClassifier(n_estimators=1000, random_state=0, class_weight="balanced", n_jobs=6)
mdl.fit(Xtrain_wtitle, ytrain)

# %%
p = mdl.predict_proba(Xval_wtitle)[:, 1]

# %%
average_precision_score(yval, p)

# %%
roc_auc_score(yval, p)


# %%

# Reading the data not taged to create Active Learnig
# Activity learning select a few sample that the model has more difficul to modeling. With this sample is possible create a tag.

# Reading the data not taged.
df_unlabeled = pd.read_csv("../../dataset/silver/general_table_youtube_2024-02-10 06:24:00.csv")
df_unlabeled = df_unlabeled[df_unlabeled['y'].isnull()].dropna(how='all')
df_unlabeled['publishedAt'] = pd.to_datetime(df_unlabeled['publishedAt'], infer_datetime_format=True)
df_unlabeled["date"] = pd.to_datetime(df_unlabeled['publishedAt'].dt.date)

df_unlabeled.shape


# %%
df_clean_u = pd.DataFrame(index=df_unlabeled.index)
df_clean_u['title'] = df_unlabeled['title']
df_clean_u['publishedAt'] = df_unlabeled['publishedAt']
df_clean_u["date"] = df_unlabeled["date"] 
df_clean_u["statistics.viewCount"] = df_unlabeled["statistics.viewCount"]

# %%
features_u = pd.DataFrame(index=df_clean_u.index)

# %%
current_time = datetime.now(timezone.utc)
features_u["time_since_pub"] = (pd.to_datetime(current_time) - df_clean_u["publishedAt"]) / np.timedelta64(1, "D")
features_u["views"] = df_clean_u["statistics.viewCount"]
features_u["views_by_day"] = features_u["views"] / features_u["time_since_pub"]
features_u = features_u.drop(["time_since_pub"], axis=1)


# %%
# Using the model Random forest classifier to predict the sparce matrix of tfidf to title
title_u = df_clean_u["title"]
title_bow_u = title_vec.transform(title_u)

# %%
Xu_wtitle = hstack([features_u, title_bow_u])


# %%
# Using the Random Forest to Predict probability of like or dislike
pu = mdl.predict_proba(Xu_wtitle)[:, 1]

# %%
df_unlabeled['p'] = pu

# %%
df_unlabeled.head()

# %%
# How to if a example is hard predict to model
# Select example with proba more than 0.45 and less than 0.55
# if this mask has a lrge count, your model has difficult to predict
mask_u = (df_unlabeled['p'] >= 0.45) & (df_unlabeled['p'] <= 0.55)
mask_u.sum()

# %%
# We will get a sample of aprox 80 hard elements and 40 random elements
hard_examples = df_unlabeled[mask_u]
random_examples = df_unlabeled[~mask_u].sample(37, random_state=0)
pd.concat([hard_examples, random_examples]).to_csv("../../dataset/bronze/active_label.csv", index=False)

# %%
# Active Learnig Results
df_active = pd.read_csv("../../dataset/bronze/active_label.csv")
df_active['publishedAt'] = pd.to_datetime(df_active['publishedAt'], infer_datetime_format=True)
df_active = df_active[df_active['y'].notnull()]
df_active['new'] = 1
df_active.dtypes

# %%
df_active.isna().sum()

# %%
average_precision_score(df_active['y'],df_active['p']), roc_auc_score(df_active['y'],df_active['p'])

# %%
df = pd.concat([df, df_active.drop("p", axis=1)])


# %%
df_clean = pd.DataFrame(index=df.index)
df_clean['title'] = df['title']
df_clean['publishedAt'] = df['publishedAt']
df_clean["date"] = df["date"] 
df_clean["statistics.viewCount"] = df["statistics.viewCount"]
df_clean["new"] = df["new"].fillna(0)

# %%
df_clean.isna().sum()

# %%
features = pd.DataFrame(index=df_clean.index)
y = df['y'].copy()

# %%
current_time = datetime.now(timezone.utc)
features["time_since_pub"] = (pd.to_datetime(current_time) - df_clean["publishedAt"]) / np.timedelta64(1, "D")
features["views"] = df_clean["statistics.viewCount"]
features["views_by_day"] = features["views"] / features["time_since_pub"]
features = features.drop(["time_since_pub"], axis=1)


# %%
features.isna().sum()

# %%

df_clean["date"] = pd.to_datetime(df_clean["date"] )

# %%
mask_train = (df_clean['date'] < "2022-01-01") & (df_clean['new'] == 0)

mask_val = (df_clean['date'] >= "2022-01-01")

Xtrain, Xval = features[mask_train], features[mask_val]
ytrain, yval = y[mask_train], y[mask_val]
Xtrain.shape, Xval.shape, ytrain.shape, yval.shape

# %%
#Xval[Xval["views_by_day"].isnull()]
#features[mask_val]
Xval.isnull().sum()

# %%
title_train = df_clean[mask_train]['title']
title_val = df_clean[mask_val]['title']

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
average_precision_score(yval, p), roc_auc_score(yval, p)

# %%
# Increase train data

# %%
mask_train = (df_clean['date'] < "2022-01-01")
#mask_val = (df_clean['date'] >= "2022-01-01")  & (df_clean['new'] == 0)
mask_val = (df_clean['date'] >= "2022-01-01")

Xtrain, Xval = features[mask_train], features[mask_val]
ytrain, yval = y[mask_train], y[mask_val]
Xtrain.shape, Xval.shape, ytrain.shape, yval.shape

title_train = df_clean[mask_train]['title']
title_val = df_clean[mask_val]['title']

title_vec = TfidfVectorizer(min_df=2)
title_bow_train = title_vec.fit_transform(title_train)
title_bow_val = title_vec.transform(title_val)

Xtrain_wtitle = hstack([Xtrain, title_bow_train])
Xval_wtitle = hstack([Xval, title_bow_val])

mdl = RandomForestClassifier(n_estimators=1000, random_state=0, class_weight="balanced", n_jobs=6)
mdl.fit(Xtrain_wtitle, ytrain)

p = mdl.predict_proba(Xval_wtitle)[:, 1]

average_precision_score(yval, p), roc_auc_score(yval, p)
# %%

#-1 (0.39522043738133117, 0.6035393879808283)
#-2 (0.5079326717252145, 0.6906593406593406)
#-3 (0.3922846007035085, 0.6204989553889639)