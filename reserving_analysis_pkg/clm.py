

import pandas as pd

def triangle_report_loss_origin(df):
    
    reported_loss_acc_age = pd.DataFrame([])
    for i in range(1, len(df.development_age.unique())+1):
        age = df[df.development_age == i ]
        age_loss = age.groupby('accident_month').sum()[['reported_loss']].rename(columns={'reported_loss':'reported_loss_age'+str(i)})
        reported_loss_acc_age = pd.concat([reported_loss_acc_age, age_loss], axis=1)
    return reported_loss_acc_age


def compute_triangle_factor(df, df_ep=None):
    
    triangle_factor = pd.DataFrame([])
    for i in range(0, df.shape[1]-1):
        triangle_factor['age_'+str(i+1)+'_to_'+str(i+2)] = df.iloc[:,i+1]/df.iloc[:,i]

    if df_ep is None:
        print(df_ep== None)
        # simple average 
        triangle_factor.loc['mean'] = triangle_factor.mean()
    else:
        # weighted average 
        df_ep_1 = df_ep.iloc[0:,1:]
        df_ep_1.columns=list(triangle_factor.columns)
        triangle_factor.loc['mean'] = (df_ep_1*triangle_factor).sum()/df_ep_1.sum()
        
    return triangle_factor


def fill_triangle_loss(df, df_fact):

    df1 = df.copy()
    num_rows, num_col = df.shape
    for i in range(0, num_col-1):
        factor = df_fact.loc['mean'][i]

        for j in range(0, i+1):
            df1.iloc[num_rows-1-j,i+1] = df1.iloc[num_rows-1-j,i]*factor 
    return df1


def triangle_ultimate_loss_act(df):
    
    ultimate_loss_acc_age = pd.DataFrame([])
    for i in range(1, len(df.development_age_in_months.unique())+1):
        age = df[df.development_age_in_months == i ]
        age_loss = age.groupby('exposure_month').sum()[['act_ultimate_loss']].rename(columns={'act_ultimate_loss':'cls_ultimate_loss_age'+str(i)})
        ultimate_loss_acc_age = pd.concat([ultimate_loss_acc_age, age_loss], axis=1)
    return ultimate_loss_acc_age 

def triangle_ultimate_loss_cls(df):
    
    ultimate_loss_acc_age = pd.DataFrame([])
    for i in range(1, len(df.development_age_in_months.unique())+1):
        age = df[df.development_age_in_months == i ]
        age_loss = age.groupby('exposure_month').sum()[['cls_ultimate_loss']].rename(columns={'cls_ultimate_loss':'cls_ultimate_loss_age'+str(i)})
        ultimate_loss_acc_age = pd.concat([ultimate_loss_acc_age, age_loss], axis=1)
    return ultimate_loss_acc_age 

def triangle_ep(df):
    
    ep_acc_age = pd.DataFrame([])
    for i in range(1, len(df.development_age_in_months.unique())+1):
        age = df[df.development_age_in_months == i ]
        age_ep = age.groupby('exposure_month').sum()[['earned_premium']].rename(columns={'earned_premium':'ep_age'+str(i)})
        ep_acc_age = pd.concat([ep_acc_age, age_ep], axis=1)
    return ep_acc_age 

def act_cls_combined(df_act, df_cls):
    
    col_name = ['act', 'cls']
    
    df_act_cls = pd.DataFrame(index=df_act.index, columns=col_name)
    rows, cols = df_act.shape

    for i in range(0, rows):
        df_act_cls.iloc[i, 0] = df_act.iloc[i,cols-1-i]  
        df_act_cls.iloc[i, 1] = df_cls.iloc[i,cols-1-i]
    return df_act_cls

def convert_ep_to_column(df):
    
    col_name = ['ep']
    
    ep_col = pd.DataFrame(index=df.index, columns=col_name)
    rows, cols = df.shape

    for i in range(0, rows):
        ep_col.iloc[i, 0] = df.iloc[i,cols-1-i]  
    return ep_col

def convert_loss_to_lr(df, df_ep):
    
    df_lr = pd.DataFrame([])
    cols = df.columns
    
    for c in cols:
        df_lr[c +'_lr'] =  df[c]/df_ep['ep']
    
    return df_lr


def slice_data_by_exposure_and_age(df):
    
    sliced_data = []
    acc_month_list = list(df.accident_month.unique())
    for acc_month in acc_month_list:
        acc_month_df = df[df.accident_month == acc_month]
        develop_age_num = len(acc_month_df.development_age.unique())
        
        sliced_data_age = []
        for i in range(1, develop_age_num+1):
            temp = acc_month_df[acc_month_df.development_age == i]
            sliced_data_age.append([i, temp])
        sliced_data.append([acc_month, sliced_data_age])
    return sliced_data

def slice_data_by_exposure(df):
    
    sliced_data = []
    acc_month_list = list(df.accident_month.unique())
    for acc_month in acc_month_list:
        acc_month_df = df[df.accident_month == acc_month]
        uni_acc = acc_month_df.claim_feature_id.unique()
        
        sliced_data.append([acc_month, acc_month_df, uni_acc])
        
    return sliced_data
