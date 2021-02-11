import pandas as pd
import numpy as np
from .clm import compute_triangle_factor, fill_triangle_loss


def CountFrequency(my_list): 
  
    freq = {} 
    for item in my_list: 
        if (item in freq): 
            freq[item] += 1
        else: 
            freq[item] = 1
    return freq


def ZeroCountNonShownID(my_list):
    
    freq = {} 
    for item in my_list: 
        if (item in freq): 
            pass
        else: 
            freq[item] = 0
    return freq

def MergeDict(dict1, dict2):
    res = {**dict1, **dict2}
    return res


def resample_feat_id(uni_acc):
    
    uni_acc_rep = np.random.choice(uni_acc, len(uni_acc))

    uni_all_feat_id = set(uni_acc)
    uni_resampled_feat_id = set(uni_acc_rep)
    resampled_feat_id = list(uni_acc_rep)
    
    uni_non_shown_feat_id = uni_all_feat_id - uni_resampled_feat_id

    feat_id_count_dict = CountFrequency(resampled_feat_id)
    non_shown_feat_id_count_dict = ZeroCountNonShownID(uni_non_shown_feat_id)
    all_feat_id_count_dict = MergeDict(feat_id_count_dict, non_shown_feat_id_count_dict)
    
    
    
    return all_feat_id_count_dict


def cal_loss(acc_data, feat_dict):
    loss = 0
    cal = acc_data[['claim_feature_id', 'reported_loss']].values
    for i in range(0, len(cal)):
        feat_report_loss = cal[i][1]
        feat_count = feat_dict[cal[i][0]]
        feat_loss = feat_report_loss*feat_count
        loss += feat_loss


    return loss

# def boostrap_fill_all(df, df_exposure, df_exposure_age, random_seed):
def bootstrap_fill_all(df, df_exposure, df_exposure_age):   
    triangle_df = creat_triangle_df(df)
    
    for i in range(0, len(df_exposure_age)):
      
#         all_feat_id_count_dict = resample_feat_id(df_exposure[i][2], random_seed)
        all_feat_id_count_dict = resample_feat_id(df_exposure[i][2])
    
        acc_month_df = df_exposure_age[i][1]
        acc_month = df_exposure_age[i][0]
        
        for j in range(0, len(acc_month_df)):
            
            acc_month_age = acc_month_df[j][1]
            loss = cal_loss(acc_month_age, all_feat_id_count_dict)
            
            
            triangle_df.loc[str(acc_month), 'reported_loss_age'+str(j+1)] = loss
            
            
    return triangle_df
       

def creat_triangle_df(df):
    
    acc_month_list = df.accident_month.unique()
    col_names = []
    for i in range(1, len(df.development_age.unique())+1):
        col_names.append('reported_loss_age'+str(i))
    
    triangle_df = pd.DataFrame(index=pd.to_datetime(acc_month_list), columns=col_names)
    
    return triangle_df


def bootstrap_clm(df, df_exposure, df_exposure_age, df_ep):
    
    triangle_loss = bootstrap_fill_all(df, df_exposure, df_exposure_age)
    triangle_factor = compute_triangle_factor(triangle_loss, df_ep)
    triangle_loss_filled = fill_triangle_loss(triangle_loss, triangle_factor) 
    
            
    return triangle_factor, triangle_loss_filled


# use reported loss times factor (from boostrap samples)
def bootstrap_clm_reported_loss_b_factor(df, df_exposure, df_exposure_age, triangle_loss_origin, df_ep):
    
    triangle_loss = bootstrap_fill_all(df, df_exposure, df_exposure_age)
    triangle_factor_b = compute_triangle_factor(triangle_loss, df_ep)

    triangle_loss_filled_b = fill_triangle_loss(triangle_loss_origin, triangle_factor_b)
    
            
    return triangle_factor_b, triangle_loss_filled_b


def bootstrap_pre_by_exposure(df, df_exposure, df_exposure_age, df_ep, n):
    
    factors_df = pd.DataFrame([])
    df_b = pd.DataFrame([])
    for i in range(0, n):
        if i%100 == 0:
            print("current number: ", i)
        fa_df, df_loss = bootstrap_clm(df, df_exposure, df_exposure_age, df_ep)
        factors_df = pd.concat([factors_df, fa_df.loc[['mean']]], axis=0)
        df_b['clm_b'+ str(i)] =  df_loss.iloc[:,-1]
        
    return factors_df, df_b


def bootstrap_pre_b_factor_by_exposure(df, df_exposure, df_exposure_age, df_loss, df_ep, n):
    
    factors_df = pd.DataFrame([])
    df_b = pd.DataFrame([])
    for i in range(0, n):
        if i%100 == 0:
            print("current number: ", i)
        fa_df, df_loss = bootstrap_clm_reported_loss_b_factor(df, df_exposure, df_exposure_age, df_loss, df_ep)
        factors_df = pd.concat([factors_df, fa_df.loc[['mean']]], axis=0)
        df_b['clm_b'+ str(i)] =  df_loss.iloc[:,-1]
        
    return factors_df, df_b