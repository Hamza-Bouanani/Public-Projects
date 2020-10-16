import pandas as pd
import os
import glob
from collections import defaultdict
from scipy import stats
from xlwt import Workbook 
import csv
import re

book1 = Workbook()
feuil1 = book1.add_sheet('feuille 1',cell_overwrite_ok=True)
feuil1.write(0,1,"Model")
feuil1.write(0,2,"n1")
feuil1.write(0,3,"n2")
feuil1.write(0,4,"F1 Micro ")
feuil1.write(0,5,"F1 Macro")
feuil1.write(0,6,"ACC Macro")
feuil1.write(0,7,"AUNU")
feuil1.write(0,8,"AUNP")
metric_class=['F1','ACC','AUC','AUPR']
classes=['negative','somewhat negative','neutral','somewhat positive','positive']
for i in range(len(classes)):
    for j in range(len(metric_class)):
        feuil1.write(0,9+j+i*4,classes[i]+" "+metric_class[j])

def tofloat(l):
    s=[]
    for x in l:
        if x=='None':
            s.append(0)
        else:
            s.append(float(x))
    return s
def tostr(l):
    return [str(x) for x in l]
indice_ligne=1
l = [glob.glob("Overall"+'*'+'20.csv')]
models=[ i[:-10] for i in l[0]]
for model in models:
    files=[model+'_it_'+str(i)+'.csv' for i in range(24)]
    ldfs=[pd.read_csv(model+'_it_'+str(i)+'.csv') for i in range(24)] 
    alldata= defaultdict(dict)
    cnames = list(ldfs[0].columns)  
    for ldf in ldfs:
        for line in ldf.values:
            for j,x in enumerate(line[1:]):
                i = j + 1
                if not cnames[i] in alldata[line[0]]:
                    alldata[line[0]][cnames[i]]=[]
                alldata[line[0]][cnames[i]].append(str(x))
    alldata=alldata[0.0]

    mot=model
    mot=mot[8:]

    n=re.search("n1",mot).span()
    p=re.search("_",mot).span()

    n1=mot[n[1]:p[0]]
    mot_bis=mot[p[1]+3:]

    p=re.search("[a-z]",mot_bis).span()
    p2=re.search("[A-Z]",mot_bis)

    if p2==None:
        n2=mot_bis[:p[0]]
        nom_model=mot_bis[p[0]:]
    else:
        p2=p2.span()
        m=min(p[0],p2[0])
        n2=mot_bis[:m]
        nom_model=mot_bis[m:]

    feuil1.write(indice_ligne,1,nom_model)
    feuil1.write(indice_ligne,2,n1)
    feuil1.write(indice_ligne,3,n2)
    feuil1.write(indice_ligne,4,sum(tofloat(alldata['F1 Micro']))/len(alldata['F1 Micro']))
    feuil1.write(indice_ligne,5,sum(tofloat(alldata['F1 Macro']))/len(alldata['F1 Macro']))
    feuil1.write(indice_ligne,6,sum(tofloat(alldata['ACC MACRO']))/len(alldata['ACC MACRO']))
    feuil1.write(indice_ligne,7,sum(tofloat(alldata['AUNU']))/len(alldata['AUNU']))
    feuil1.write(indice_ligne,8,sum(tofloat(alldata['AUNP']))/len(alldata['AUNP']))


    model_class="Classes"+model[7:]
    files_class=[model_class+'_it_'+str(i)+'.csv' for i in range(24)]
    ldfs_class=[pd.read_csv(model_class+'_it_'+str(i)+'.csv') for i in range(24)] 
    cnames_class = list(ldfs_class[0].columns)  
    alldata_class= defaultdict(dict) 
    for ldf in ldfs_class:
        for line in ldf.values:
            for j,x in enumerate(line[1:]):
                i = j + 1
                if not cnames_class[i] in alldata_class[line[0]]:
                    alldata_class[line[0]][cnames_class[i]]=[]
                alldata_class[line[0]][cnames_class[i]].append(str(x))
    for i in range(len(classes)):
        for j in range(len(metric_class)):
            D=alldata_class[classes[i]][metric_class[j]]
            D=tofloat(D)
            feuil1.write(indice_ligne,9+j+i*4,sum(D)/len(D))
    indice_ligne+=1

print("book to save")
book1.save("final_results_IMDB.xls")
print("book saved")