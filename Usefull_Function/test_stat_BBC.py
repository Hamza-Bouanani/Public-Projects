import numpy as np
import pandas as pd
import os
import glob
from collections import defaultdict
from scipy import stats
from xlwt import Workbook 
import csv
import re

#link='Max_result_MultiClass.xls'
#link='Max_Cogalex_result_MultiClass.xls'
#link='Max_BBC_result_MultiClass.xls'
#link='Max_BBCSport_result_MultiClass.xls'
link="Max_final_results_IMDB.xls"

df=pd.read_excel(link)
def getscore_etoile(p):
    if p<=0.01:
        return '***'
    if p<=0.05:
        return '**'
    if p<=0.10:
        return '*'
    return ''
def getscore_plus(p):
    if p<=0.01:
        return '+++'
    if p<=0.05:
        return '++'
    if p<=0.10:
        return '+'
    return ''

def tofloat(l):
    return [float(x) for x in l]
metrics=['F1 Micro','F1 Macro','ACC MACRO','AUNU','AUNP']
df=pd.ExcelFile(link)
df1=pd.read_excel(df, 'F1_Micro')
df2=pd.read_excel(df, 'F1 macro')
df3=pd.read_excel(df, 'Acc Macro')
df4=pd.read_excel(df, 'AUNU')
df5=pd.read_excel(df, 'AUNP')
book1 = Workbook()
for metric in metrics:
    feuil1 = book1.add_sheet(metric,cell_overwrite_ok=True)
    feuil1.write(0,1,"model")
    feuil1.write(0,2,"n1")
    feuil1.write(0,3,"n2")
    if metric=='F1 Micro':
        df=df1
        feuil1.write(0,4,"F1 Micro model ")
    elif metric=='F1 Macro':
        df=df2
        feuil1.write(0,4,"F1 Macro model")
    elif metric=='ACC MACRO':
        df=df3
        feuil1.write(0,4,"ACC Macro model")
    elif metric=='AUNU':
        df=df4
        feuil1.write(0,4,"AUNU model")
    elif metric=='AUNP':
        df=df5
        feuil1.write(0,4,"AUNP model")
    models_to_compare=[]
    base_line=[]
    for i in range(len(df['Model'])):
        if 'Baseline' in df['Model'][i]:
            base_line.append("Overall_n1"+str(df['n1'][i])+"_n2_"+str(df['n2'][i])+df['Model'][i]+"_it_")
        else:
            models_to_compare.append("Overall_n1"+str(df['n1'][i])+"_n2_"+str(df['n2'][i])+df['Model'][i]+"_it_")

    indice_ligne=1

    for model in models_to_compare:
        res=''
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
            nom_model=mot_bis[m:-4]
        
        feuil1.write(indice_ligne,1,nom_model)
        feuil1.write(indice_ligne,2,str(n1))
        feuil1.write(indice_ligne,3,str(n2))

        for base in base_line:
            
            
            
            
            
            models=[model,base]
            lfiles = [glob.glob(model+'*'+'.csv') for model in models]
            ldfs_base = [pd.read_csv(f) for f in lfiles[1]]
            ldfs_to_compare = [pd.read_csv(f) for f in lfiles[0]]
            cnames = list(ldfs_base[0].columns)

            alldata_base = defaultdict(dict)
            for ldf in ldfs_base:
                for line in ldf.values:
                    for j,x in enumerate(line[1:]):
                        i = j + 1
                        if not cnames[i] in alldata_base[line[0]]:
                            alldata_base[line[0]][cnames[i]]=[]
                        alldata_base[line[0]][cnames[i]].append(str(x))
            
            alldata_to_compare = defaultdict(dict)
            for ldf in ldfs_to_compare:
                for line in ldf.values:
                    for j,x in enumerate(line[1:]):
                        i = j + 1
                        if not cnames[i] in alldata_to_compare[line[0]]:
                            alldata_to_compare[line[0]][cnames[i]]=[]
                        alldata_to_compare[line[0]][cnames[i]].append(str(x))
            
            alldata_base=alldata_base[0.0]
            alldata_to_compare=alldata_to_compare[0.0]


            p=stats.ttest_rel(tofloat(alldata_to_compare[metric]), tofloat(alldata_base[metric]))[1]
            p_etoile=getscore_etoile(p)
            p_plus=getscore_plus(p)
            m_base=sum(tofloat(alldata_base[metric]))/len(alldata_base[metric])
            m_to_compare=sum(tofloat(alldata_to_compare[metric]))/len(alldata_to_compare[metric])
            if 'MultiClass' in base:
                #get_score with *
                if m_to_compare>=m_base:
                    if len(res)<=3:
                        res+=str(m_to_compare)[:6]+p_etoile
                    else:
                        res+=p_etoile
                else:
                    if len(res)<=3:
                        res=str(m_to_compare)[:6]
            else:
                #get_score with +
                if m_to_compare>=m_base:
                    if len(res)<=3:
                        res+=str(m_to_compare)[:6]+p_plus
                    else:
                        res+=p_plus
                else:
                    if len(res)<=3:
                        res=str(m_to_compare)[:6]
        feuil1.write(indice_ligne,4,res)
        indice_ligne+=1


    for base in base_line:
        mot=base
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
            nom_model=mot_bis[m:-4]
        
        feuil1.write(indice_ligne,1,nom_model)
        feuil1.write(indice_ligne,2,str(n1))
        feuil1.write(indice_ligne,3,str(n2))
        models=[model,base]
        lfiles = [glob.glob(model+'*'+'.csv') for model in models]
        ldfs_base = [pd.read_csv(f) for f in lfiles[1]]
        ldfs_to_compare = [pd.read_csv(f) for f in lfiles[0]]
        cnames = list(ldfs_base[0].columns)

        alldata_base = defaultdict(dict)
        for ldf in ldfs_base:
            for line in ldf.values:
                for j,x in enumerate(line[1:]):
                    i = j + 1
                    if not cnames[i] in alldata_base[line[0]]:
                        alldata_base[line[0]][cnames[i]]=[]
                    alldata_base[line[0]][cnames[i]].append(str(x))
        alldata_base=alldata_base[0.0]
        m_base=sum(tofloat(alldata_base[metric]))/len(alldata_base[metric])
        feuil1.write(indice_ligne,4,str(m)[:6])
        indice_ligne+=1

print("book to save")
book1.save("stat results IMDB.xls")
print("book saved")