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
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score
import graphviz 

pd.set_option("display.max_columns", 30)
%matplotlib inline

# %%
df = pd.read_csv("../../dataset/silver/general_table_youtube_2024-02-10 06:24:00.csv")
df = df[df["y"].notnull()]
df['publishedAt'] = pd.to_datetime(df['publishedAt'], infer_datetime_format=True)
df["date"] = pd.to_datetime(df['publishedAt'].dt.date)
# %%
df.dtypes

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
features.head()

# %%
pd.to_datetime(df['publishedAt'].dt.date).value_counts().plot(figsize=(20,10))

# %%
# Split Data Set

Xtrain, Xval = features[df['date'] < "2022-01-01"], features[df['date'] >= "2022-01-01"]
ytrain, yval = y[df['date'] < "2022-01-01"], y[df['date'] >= "2022-01-01"]
Xtrain.shape, Xval.shape, ytrain.shape, yval.shape

# %%
ytrain.mean()

# %%
mdl = DecisionTreeClassifier(random_state=0, max_depth=2, class_weight="balanced")
mdl = mdl.fit(Xtrain, ytrain)



# %%

tree.plot_tree(mdl)

# %%
p = mdl.predict_proba(Xval)[:, 1]

# %%
average_precision_score(yval, p)


# %%
roc_auc_score(yval, p)

# %%
dot_data = tree.export_graphviz(mdl,
                                feature_names=features.columns,
                                filled=True, 
                                rounded=True,
                                special_characters=True, 
                                out_file=None) 
graph = graphviz.Source(dot_data) 
graph.render("tree_vizualitation")


# %%

# %%
df.columns[2]
# %%
