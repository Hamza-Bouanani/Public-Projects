import numpy as np
import pandas as pd
import os
import glob
from collections import defaultdict
from scipy import stats
from xlwt import Workbook 
import csv
import re

import pandas as pd
from matplotlib import pyplot as plt
from pylab import figure, axes, pie, title, show

link='Max_result_MultiClass.xls'
#link='Max_Cogalex_result_MultiClass.xls'
#link='Max_BBC_result_MultiClass.xls'
#link='Max_BBCSport_result_MultiClass.xls'
link="Max_final_results_IMDB.xls"
#df=pd.read_excel(link)
df=pd.ExcelFile(link)
df=pd.read_excel(df, 'F1_Micro')
#cnames = list(df.columns)

#print(cnames)
#for row in df.itertuples():
 #   print(row['Model'])

metrics=['F1 Micro','F1 Macro','ACC MACRO','AUNU','AUNP']
models=[]
semi_models={}
for row in df.itertuples():
    mod='_n1'+str(row[4])+'_n2_'+str(row[5])+str(row[3])
    models.append(mod)
    semi_models[str(row[3])]=mod



d={}
for model in models:
    d_mod={'F1 Micro':[],'F1 Macro':[],'ACC Macro':[],'AUNU':[],'AUNP':[]}
    lfiles = [glob.glob("Overall"+model+"_it_"+str(i)+'.csv') for i in range(24)]
    ldfs = [pd.read_csv(lfiles[i][0]) for i in range(24)]

    for df in ldfs:
        for row in df.itertuples():
            d_mod['F1 Micro'].append(float(row[2]))
            d_mod['F1 Macro'].append(float(row[3]))
            d_mod['ACC Macro'].append(float(row[4]))
            d_mod['AUNU'].append(float(row[5]))
            d_mod['AUNP'].append(float(row[6]))  
    d[model]=d_mod


mod=['ModelBaseline_MultiClass','ModelBaseline_OneVsRest','hier','ModelOneVsRest_SharedPrivate','ModelOneVsRest_AllShared', 'ModelOneVsRest_SharedPrivate_4Per4','ModelOneVsRest_AllShared_4Per4',  'ModelOneVsRest_SharedPrivate_3Per3','ModelOneVsRest_AllShared_3Per3','ModelOneVsRest_SharedPrivate_2Per2','ModelOneVsRest_All_shared_2Per2']
models=[]

for i in mod:
    models.append(semi_models[i])

labelss_for_dic=models
labelss=['MULTI','OR','HIER','ORSP','ORAS','ORSP4','ORAS4','ORSP3','ORAS3','ORSP2','ORAS2']

for i in range(len(labelss)):
    print(labelss[i],"   ",labelss_for_dic[i])

fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5)
fig.suptitle("Best_parameters_"+link[:-4])
ax1.boxplot([d[x]['F1 Micro'] for x in labelss_for_dic])
ax2.boxplot([d[x]['F1 Macro'] for x in labelss_for_dic])
ax3.boxplot([d[x]['ACC Macro'] for x in labelss_for_dic])
ax4.boxplot([d[x]['AUNU'] for x in labelss_for_dic])
ax5.boxplot([d[x]['AUNP'] for x in labelss_for_dic])



ax1.set(ylabel='F1 Micro')
ax2.set(ylabel='F1 Macro')
ax3.set(ylabel='ACC Macro')
ax4.set(ylabel='AUNU')
ax5.set(ylabel='AUNP')

axes = plt.gca()
axes.xaxis.set_ticklabels(labelss)
#plt.xticks(rotation = 'vertical')
plt.tick_params(axis='x',labelsize = 10)

plt.show()