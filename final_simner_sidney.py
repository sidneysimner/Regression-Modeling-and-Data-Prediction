# -*- coding: utf-8 -*-
"""Final_Simner_Sidney.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QCnkJ8133b2MHkIG0Zndf0p-W7z49nsM

# **Machine Learning Final Project**
## code and insights by Sidney Simner


---

# **Introduction**

## Column Definitions
- **track**: The Name of the track.

- **artist**: The Name of the Artist.

- **uri**: The resource identifier for the track.

- **danceability**: Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable. 

- **energy**: Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy. 

- **key**: The estimated overall key of the track. Integers map to pitches using standard Pitch Class notation. E.g. 0 = C, 1 = C?/D?, 2 = D, and so on. If no key was detected, the value is -1.

- **loudness**: The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). Values typical range between -60 and 0 db. 

- **mode**: Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 1 and minor is 0.

- **speechiness**: Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks. 

- **acousticness**: A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic. The distribution of values for this feature look like this:

- **instrumentalness**: Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0. The distribution of values for this feature look like this:

- **liveness**: Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.

- **valence**: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).

- **tempo**: The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration. 

- **duration_ms**:  The duration of the track in milliseconds.

- **time_signature**: An estimated overall time signature of a track. The time signature (meter) is a notational convention to specify how many beats are in each bar (or measure).

- **chorus_hit**: This the the author's best estimate of when the chorus would start for the track. Its the timestamp of the start of the third section of the track. This feature was extracted from the data received by the API call for Audio Analysis of that particular track.

- **sections**: The number of sections the particular track has. This feature was extracted from the data received by the API call for Audio Analysis of that particular track.

- **target**: The target variable for the track. It can be either '0' or '1'. '1' implies that this song has featured in the weekly list (Issued by Billboards) of Hot-100 tracks in that decade at least once and is therefore a 'hit'. '0' Implies that the track is a 'flop'.

- The author's condition of a track being 'flop' is as follows:

    - The track must not appear in the 'hit' list of that decade.
    - The track's artist must not appear in the 'hit' list of that decade.
    - The track must belong to a genre that could be considered non-mainstream and / or avant-garde. 
    - The track's genre must not have a song in the 'hit' list.
    - The track must have 'US' as one of its markets.

# Libraries
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.ensemble import BaggingClassifier
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier

from sklearn.metrics import (
    classification_report,
    recall_score,
    precision_score,
    accuracy_score)

from sklearn.ensemble import RandomForestRegressor
import seaborn as sns 
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
from yellowbrick.regressor import ResidualsPlot
from sklearn.model_selection import cross_val_score

"""# **Preprocessing**"""

data = pd.read_csv("dataset-of-70s.csv")

"""## Data Exploration"""

data.head()

"""From these columns, it is appearant that the first three columns will not be considered for regression as they are non numerical. This does present and unfortunate loss of data however to exclude the artist, as artist following may have a large impact on the success of a song. One improvement this dataset could make would be to have a cloumn rating the populattity of the artist. """

print(data.isnull().any())

"""the dataset includes no null values however one feature, key, gives a -1 value to any unkown keys. Let's count this to determine if there is too many unknown keys to make the column usefull. """

print(data.key[data.key == -1].count())

data.describe()

data.corr()

print(len(data[data['target']==0]))
print(len(data[data['target']==1]))

"""**there are exactly the same number of Hits and Flops -- baseline accuracy = 50 %**

# **Modeling**
"""

X = data.iloc[:,3:-1]
y = data['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify = y, random_state = 42)

"""## Mulitple Linear Regression"""

model_linear = linear_model.LinearRegression()
model_linear.fit(X_train, y_train)
pred_linear = model_linear.predict(X_test)

#predicition is between 0 and 1 -- round to the nearest integer to predict if the song is a hit 
rounded = np.round(pred_linear)

#compare for accuracy 
acc_linear = round(metrics.accuracy_score(y_test, rounded),4)
print('Linear Regression Accuracy = ', acc_linear)


#plot residuals
from yellowbrick.regressor import ResidualsPlot
visualizer = ResidualsPlot(model_linear)
visualizer.fit(X_train, y_train)
visualizer.score(X_test, y_test)
visualizer.poof()

"""## Decision Tree"""

dt = DecisionTreeClassifier(max_depth = 6, max_features=15, random_state = 42)
dt.fit(X_train, y_train)
pred_dt = dt.predict(X_test)

#compare for accuracy 
acc_dt = round(metrics.accuracy_score(y_test, pred_dt),4)
print('Decision Tree Accuracy = ', acc_dt)

#print the tree
from sklearn import tree

fn = X.columns
classList = list(map(str,dt.classes_.tolist()))

plt.figure(figsize=(12,12))
tree.plot_tree(dt, feature_names=fn, class_names=classList, filled=True)
plt.show()

"""## Ada Boost"""

base_est = DecisionTreeClassifier(max_depth =6, max_features=15, random_state = 42)

ada_boost = AdaBoostClassifier(base_est, n_estimators=100)
ada_boost.fit(X_train, y_train)

acc_boost = accuracy_score(y_test, ada_boost.predict(X_test))
print('Ada Boost Accuracy = ', round(acc_boost,4))

"""## Bagging"""

base_est = DecisionTreeClassifier(max_depth =6, max_features=15, random_state = 42)

model_bagging = BaggingClassifier(base_estimator = base_est, n_estimators = 100)
model_bagging.fit(X_train, y_train)
pred_bagging = model_bagging.predict(X_test)

acc_bagging = round(metrics.accuracy_score(y_test, pred_bagging),4)
print('Bagging Accuracy = ', acc_bagging)

"""## Random Forest"""

model_rf = RandomForestClassifier(n_estimators=100, max_depth =6, max_features=15, random_state = 42)
model_rf.fit(X_train, y_train)
pred_rf = model_rf.predict(X_test)

#compare for accuracy 
acc_forest = round(metrics.accuracy_score(y_test, pred_rf),4)
print('Random Forest Accuracy = ', acc_forest)

"""## Most promising model"""

print('Linear Regression Accuracy = ', acc_linear)
print('Decision Tree Accuracy = ', acc_dt)
print('AdaBoost Accuracy = ', round(acc_boost,4))
print('Bagging Accuracy = ', acc_bagging)
print('Random Forest Accuracy = ', acc_forest)

bestModel = {'Bagging': acc_bagging, 'Random Forest': acc_forest, 'AdaBoost': round(acc_boost,4), 'Linear Regression': acc_linear, 'Decision Tree':acc_dt}
print("\nBest Model Accuracy:", max(bestModel, key = bestModel.get))

"""Random Forest was the best classification method (of those explored) to use on this data as it had the highest accuracy score. It is the best fit because it has the most diversity of trees and accounts for the high variability in the data. This is a good model for the data due to the large number of features and the indepedence of each feature.

# **Cross Validation**
"""

# split the data three ways

X = data.iloc[:,3:-1]
y = data['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.395, stratify = y, random_state = 42)
X_val, X_test, y_val, y_test = train_test_split(X_test, y_test, test_size=0.5, stratify = y_test, random_state = 42)

print(X.shape, y.shape)
print(X_train.shape, y_train.shape)
print(X_val.shape, y_val.shape)
print(X_test.shape, y_test.shape)

model_rf = RandomForestClassifier(n_estimators=100, max_depth =6, max_features=15, random_state = 42)
model_rf.fit(X_train, y_train)
pred_rf2 = model_rf.predict(X_val)

print("Cross Validation Score: ", cross_val_score(model_rf, X_val, y_val, cv=10, scoring='accuracy').mean())

acc_forest2 = round(metrics.accuracy_score(y_val, pred_rf2),4)
print('Random Forest Accuracy= ', acc_forest2)

# find the optimal depth and features

depth = []
features = []
for i in range(3,16):
    rf1 = RandomForestClassifier(n_estimators=100, max_depth=i)
    rf1 = rf1.fit(X_train,y_train)
    scores1 = cross_val_score(estimator=rf1, X=X_val, y=y_val, cv=10)
    depth.append((i,scores1.mean()))

    rf2 = RandomForestClassifier(n_estimators=100, max_features=i)
    rf2 = rf2.fit(X_train,y_train)
    scores2 = cross_val_score(estimator=rf2, X=X_val, y=y_val, cv=10)
    features.append((i,scores2.mean()))

print(depth)
print(features)

#best depth = 13
#best features = 9

# find optimal n estimators

n_estimators = [3,10,50,100,150, 200, 250, 300, 400, 500]

train_error = []
test_error = []

for i in n_estimators:
    RF = RandomForestRegressor(n_estimators=i, max_depth =13, max_features=10, random_state = 42)
    RF.fit(X_train, y_train)
    train_error.append(np.sqrt(mean_squared_error(y_train, RF.predict(X_train))))
    test_error.append(np.sqrt(mean_squared_error(y_test, RF.predict(X_test))))

plt.figure(figsize = (15, 10))
plt.title('Random Forest: Model Complexity vs RMSE', fontsize=20)
plt.ylabel('RMSE', fontsize=20)
plt.xlabel('Number of Trees', fontsize=20)
sns.lineplot(n_estimators, train_error, label='Train')
sns.lineplot(n_estimators, test_error, color='r', label='Test')
plt.show()

model_rf_cv = RandomForestClassifier(n_estimators=500, max_depth =13, max_features=9, random_state = 42)
model_rf_cv.fit(X_train, y_train)
pred_rf_cv = model_rf_cv.predict(X_test)

print("Cross Validation Score after cross validation: ", cross_val_score(model_rf_cv, X_val, y_val, cv=10, scoring='accuracy').mean())

acc_forest_cv = round(metrics.accuracy_score(y_test, pred_rf_cv),4)
print('Random Forest Accuracy after cross validation= ', acc_forest_cv)

"""# **Lasso Model**"""

alpha_space = np.logspace(-4, 0, 50)
model_scores = []

lasso_model = Lasso(normalize=True)
for alpha in alpha_space:

    # Specify the alpha value to use
    lasso_model.alpha = alpha
    
    # Perform 10-fold CV
    lasso_cv_scores = cross_val_score(lasso_model,X,y,cv=10)
    
    # Append the mean of lasso_cv_scores to model_scores = []
    model_scores.append(np.mean(lasso_cv_scores))

print(model_scores)

# best alpha index for lasso 
print(np.argmax(model_scores))
#plus in this index to the list of alphas

#best alpha to use 
print(alpha_space[0])
# this is th best alpha to use in the model

from sklearn.linear_model import Lasso

#use the alpha previously found 
alpha_user = 0.0001
lasso_model = Lasso(alpha=alpha_user,normalize=True)
lasso_model.fit(X_train,y_train)
lasso_pred = lasso_model.predict(X_test)

#predicition is between 0 and 1 -- round to the nearest integer to predict if the song is a hit 
rounded_lasso = np.round(lasso_pred)

print("Lasso Model Accuracy:", metrics.accuracy_score(y_test, rounded_lasso))

print("\nLasso Model Coefficients:", lasso_model.coef_)

cols = list(X.columns.values)
lasso_importance = pd.DataFrame(lasso_model.coef_, index=cols).nlargest(3,[0])
print("\nLargest Lasso coefficients:\n", lasso_importance)

"""The Lasso model score is similar to the linear regression model -- very low and not a good fit for the data. It's coefficients shows that the first feature, danceability, is the most important feature. This is not surprising as we are analyzing music from the 1970s

# **Performance**
Using a Random Forest Model
"""

print(classification_report(y_test, pred_rf_cv))

"""# **Graphing and Other Insights**"""

#most important features 

feature_importances = model_rf_cv.feature_importances_
features = X_train.columns
df = pd.DataFrame({'features': features, 'importance': feature_importances}).nlargest(3, 'importance')
print(df)

# list of x locations for plotting
x_values = list(range(len(feature_importances)))
# Make a bar chart
plt.bar(x_values, feature_importances, orientation = 'vertical')
# Tick labels for x axis
plt.xticks(x_values, X.columns, rotation='vertical')
# Axis labels and title
plt.ylabel('Importance')
plt.xlabel('Variable')
plt.title('Variable Importances')

plt.hist(data.instrumentalness, bins = 50)
plt.xlabel('value')
plt.ylabel('count')
plt.title('Histogram of Instrumentalness')

plt.show()

"""Instrumentalness seems to be a highly skewed feature. Considering it is heavly considered in the Random Forest model, it might be wise to remove it and see if the accuracy improves. 

Danceability was the most important feature int the Lasso model and is more equally weighted.
"""

plt.hist(data.danceability, bins = 50)
plt.xlabel('value')
plt.ylabel('count')
plt.title('Histogram of Danceability')

plt.show()

"""### What makes the perfect song?"""

data[data.target == 1].mean()

"""### What artist had the most hits?"""

hit_artists = data[data.target == 1].iloc[:,:2]
hit_artists = hit_artists.groupby('artist').count()
hit_artists = hit_artists.sort_values(by=['track'], ascending=False)

print(hit_artists.head())