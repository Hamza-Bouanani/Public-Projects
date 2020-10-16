
nom_data="BBC_Sport"
list_cat=['atheltics','cricket','football','rugby','tennis']

print("...Start Imports")

from sklearn.manifold import TSNE
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os

import matplotlib.pyplot as plt

print("...Loading embedding")
embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")
print('...Embedding loaded')
link_athletics="Data/athletics" # business class=-2
link_cricket="Data/cricket" #entertainment class=-1
link_football="Data/football" # politics class=0
link_rugby="Data/rugby" # sport class=1
link_tennis="Data/tennis" # tech class=2
text_to_embed=[]
classes=[]

 
path = link_athletics
files = os.listdir(path)
for i in files:
    f=open(link_athletics+"/"+i,'r', encoding='unicode_escape')
    t=f.read()
    text_to_embed.append(t)
    f.close()
    classes.append(-2)
    
path = link_cricket
files = os.listdir(path)
for i in files:
    f=open(link_cricket+"/"+i,'r', encoding='unicode_escape')
    text_to_embed.append(f.read())
    f.close()
    classes.append(-1)
    
path = link_football
files = os.listdir(path)
for i in files:
    f=open(link_football+"/"+i,'r', encoding='unicode_escape')
    text_to_embed.append(f.read())
    f.close()
    classes.append(0)
    
path = link_rugby
files = os.listdir(path)
for i in files:
    f=open(link_rugby+"/"+i,'r', encoding='unicode_escape')
    text_to_embed.append(f.read())
    f.close()
    classes.append(1)
    
path = link_tennis
files = os.listdir(path)
for i in files:
    f=open(link_tennis+"/"+i,'r', encoding='unicode_escape')
    text_to_embed.append(f.read())
    f.close()
    classes.append(2)

print("...Start Embedding")

text_embedded=embed(text_to_embed)

print("...Text embedded succesfully")


print("...Spliting the data")







print("...Data is ready!")


tsne = TSNE()
X=text_embedded
y=list(classes)
X_2d=tsne.fit_transform(X)
X_2d0=[]
X_2d1=[]
X_2d2=[]
X_2d3=[]
X_2d4=[]
for i in range(len(y)):
    if y[i]==-2:
        X_2d0.append(X_2d[i])
    elif y[i]==-1:
        X_2d1.append(X_2d[i])
    elif y[i]==0:
        X_2d2.append(X_2d[i])
    elif y[i]==1:
        X_2d3.append(X_2d[i])
    else:
        X_2d4.append(X_2d[i])
    
        
X_2d0=np.array(X_2d0)
X_2d1=np.array(X_2d1)
X_2d2=np.array(X_2d2)
X_2d3=np.array(X_2d3)
X_2d4=np.array(X_2d4)

plt.figure()
colors=['r','g','b','c','m']
i=0
plt.scatter(X_2d0[:,0], X_2d0[:,1],c=colors[i],label=list_cat[i])
i=1
plt.scatter(X_2d1[:,0], X_2d1[:,1],c=colors[i],label=list_cat[i])
i=2
plt.scatter(X_2d2[:,0], X_2d2[:,1],c=colors[i],label=list_cat[i])
i=3
plt.scatter(X_2d3[:,0], X_2d3[:,1],c=colors[i],label=list_cat[i])
i=4
plt.scatter(X_2d4[:,0], X_2d4[:,1],c=colors[i],label=list_cat[i])

plt.legend()
plt.title("Data viz 2D "+nom_data)
plt.show()
plt.savefig("Data viz 2D "+nom_data+".png")

tsne = TSNE(n_components=3)
X=text_embedded
y=list(classes)
X_2d=tsne.fit_transform(X)
X_2d0=[]
X_2d1=[]
X_2d2=[]
X_2d3=[]
X_2d4=[]
for i in range(len(y)):
    if y[i]==-2:
        X_2d0.append(X_2d[i])
    elif y[i]==-1:
        X_2d1.append(X_2d[i])
    elif y[i]==0:
        X_2d2.append(X_2d[i])
    elif y[i]==1:
        X_2d3.append(X_2d[i])
    else:
        X_2d4.append(X_2d[i])
    
        
X_2d0=np.array(X_2d0)
X_2d1=np.array(X_2d1)
X_2d2=np.array(X_2d2)
X_2d3=np.array(X_2d3)
X_2d4=np.array(X_2d4)

fig=plt.figure()
colors=['r','g','b','c','m']
ax=fig.add_subplot(111,projection='3d')
i=0
ax.scatter(X_2d0[:,0], X_2d0[:,1],X_2d0[:,2],c=colors[i],label=list_cat[i])
i=1
ax.scatter(X_2d1[:,0], X_2d1[:,1],X_2d1[:,2],c=colors[i],label=list_cat[i])
i=2
ax.scatter(X_2d2[:,0], X_2d2[:,1],X_2d2[:,2],c=colors[i],label=list_cat[i])
i=3
ax.scatter(X_2d3[:,0], X_2d3[:,1],X_2d3[:,2],c=colors[i],label=list_cat[i])
i=4
ax.scatter(X_2d4[:,0], X_2d4[:,1],X_2d4[:,2],c=colors[i],label=list_cat[i])
plt.legend()
plt.title("Data viz 3D "+nom_data)
plt.show()
plt.savefig("Data viz 3D "+nom_data+".png")