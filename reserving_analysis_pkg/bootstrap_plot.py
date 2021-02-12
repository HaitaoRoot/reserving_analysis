

import seaborn as sns
import matplotlib.pyplot as plt
from pylab import *


def plot_factors(df_fac, tf, asofdate):

    col_names = list(df_fac.columns)

    sns.set(rc={'figure.figsize': (18,14)})
    fig, ax = plt.subplots()

    for i in range(1,df_fac.shape[1]+1):
        subplot(4,6,i)
        ax = sns.histplot(df_fac[col_names[i-1]])
        ax.axvline(tf.iloc[-1, i-1], color='red',ls='-', linewidth=1)

    fig.suptitle('CLM factor (bootstrap) distributions by accident month for coverage coll as of '+asofdate, fontsize=16)
    plt.tight_layout()
    plt.show()




def plot_lr(df_lr, df_cls_act_lr, asofdate):
    df_lr_str = df_lr.T
    df_lr_str.columns = df_lr_str.columns.astype(str)
    col_names = list(df_lr_str.columns)
    #clm_loss_exposure = df_all[['clm']]

    sns.set(rc={'figure.figsize': (18,14)})
    fig, ax = plt.subplots()
    
    for i in range(1,df_lr_str.shape[1]):
        subplot(4,6,i)
        ax = sns.histplot(df_lr_str[col_names[i]])
        #ax.axvline(clm_loss_exposure.iloc[i-1].values[0], color='red',ls='-', linewidth=1)
        ax.axvline(df_cls_act_lr.iloc[i,1], color='red',ls='-', linewidth=1)
        ax.axvline(df_cls_act_lr.iloc[i,0], color='black',ls='-', linewidth=1)
    
    
        ax.axvline(x=np.percentile(df_lr_str[col_names[i]],[2.5]), ymin=0, ymax=1,c='y')
        ax.axvline(x=np.percentile(df_lr_str[col_names[i]],[97.5]), ymin=0, ymax=1,c='g')
    fig.suptitle('CLM lr prediction (bootstrap) distributions by accident month for coverage coll as of '+asofdate, fontsize=16)
    plt.tight_layout()