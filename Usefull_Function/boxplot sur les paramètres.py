import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pylab import figure, axes, pie, title, show

link='result_MultiClass.xls'
link='Cogalex_result_MultiClass.xls'
link='BBCSport_result_MultiClass.xls'
link='BBC_result_MultiClass.xls'
link='final results Tweet5C.xls'
#link='final results Tweet3C.xls'
link="final_results_IMDB.xls"
df=pd.read_excel(link)
models=list(set(df['Model']))
print(models)
d={}

for model in models:
    d_mod={'F1 Micro':[],'F1 Macro':[],'ACC Macro':[],'AUNU':[],'AUNP':[]}
    mod=model
    for row in df.itertuples():
        if row.Model==model:
            d_mod['F1 Micro'].append(float(row[5]))
            d_mod['F1 Macro'].append(float(row[6]))
            d_mod['ACC Macro'].append(float(row[7]))
            d_mod['AUNU'].append(float(row[8]))
            d_mod['AUNP'].append(float(row[9]))  
    d[model]=d_mod

mod=['ModelBaseline_MultiClass','ModelBaseline_OneVsRest','hier','ModelOneVsRest_SharedPrivate','ModelOneVsRest_AllShared', 'ModelOneVsRest_SharedPrivate_4Per4','ModelOneVsRest_AllShared_4Per4',  'ModelOneVsRest_SharedPrivate_3Per3','ModelOneVsRest_AllShared_3Per3','ModelOneVsRest_SharedPrivate_2Per2','ModelOneVsRest_All_shared_2Per2']
labelss=['MULTI','OR','HIER','ORSP','ORAS','ORSP4','ORAS4','ORSP3','ORAS3','ORSP2','ORAS2']
labelss_for_dic=mod
#for i in mod:
    #labelss_for_dic.append(i)
    #if 'hier' in i:
        #labelss.append(i)
    #else:
        #labelss.append(i[5:])

fig, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(5)
fig.suptitle("Over_parameters_"+link[:-4])
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