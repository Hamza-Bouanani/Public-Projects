
only_phrase=True

print("...Start Imports")
import csv
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras import Model
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
import sklearn.metrics
from tensorflow.keras.callbacks import EarlyStopping
import keras.backend as K
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from pycm import *
from tensorflow.keras.layers import Dense, Add, concatenate , Subtract, Activation , average,multiply,add
from sklearn.cluster import AgglomerativeClustering
import scipy.cluster.hierarchy as sch
import xlrd
print("...End Imports")
def transfo_y(y_train):
    y_train_multi=[]
    for i in range(len(y_train)):
        if y_train[i]==0:
            y_train_multi.append([1,0,0,0,0])
        elif y_train[i]==1:
            y_train_multi.append([0,1,0,0,0])
        elif y_train[i]==2:
            y_train_multi.append([0,0,1,0,0])
        elif y_train[i]==3:
            y_train_multi.append([0,0,0,1,0])
        else:
            y_train_multi.append([0,0,0,0,1])
    return y_train_multi

# openning the file

df=pd.read_csv("train.tsv",sep="\t")

print("...Start Embedding")
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
print("...Embedding loaded")
text_embedded=[]
classes=[]
if only_phrase:
    i=1
    for row in df.itertuples():
        if row.SentenceId==i:
            text_embedded.append(row.Phrase)
            classes.append(row.Sentiment)
            i+=1
else:
    text_embedded=df["Phrase"]
    classes=df["Sentiment"]
text_embedded=list(embed(text_embedded))
classes=transfo_y(classes)
print("...Embedding ended")

print("len classes ",len(classes))
print("len text ", len(text_embedded))



list_cat=['negative','somewhat negative','neutral','somewhat positive','positive']

xtrain, xtest, ytrain, ytest = train_test_split(list(text_embedded), classes,stratify=classes, test_size=0.4, random_state=0)
xtrain, xvalid, ytrain, yvalid = train_test_split(xtrain, ytrain, stratify=ytrain,test_size=0.3, random_state=0)

print("end split")
xtrain=np.array(xtrain)
print(" still processing")
xvalid=np.array(xvalid)
print(" still processing")
ytrain=np.array(ytrain)
print(" still processing")
yvalid=np.array(yvalid)


print("...Data is ready!")
