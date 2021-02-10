

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

def creat_triangle_df(df):
    
    acc_month_list = df.accident_month.unique()
    col_names = []
    for i in range(1, len(df.development_age.unique())+1):
        col_names.append('reported_loss_age'+str(i))
    
    triangle_df = pd.DataFrame(index=pd.to_datetime(acc_month_list), columns=col_names)
    
    return triangle_df

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


def creat_triangle_df(df):
    
    acc_month_list = df.accident_month.unique()
    col_names = []
    for i in range(1, len(df.development_age.unique())+1):
        col_names.append('reported_loss_age'+str(i))
    
    triangle_df = pd.DataFrame(index=pd.to_datetime(acc_month_list), columns=col_names)
    
    return triangle_df


def compute_triangle_factor(df):
    
    triangle_factor = pd.DataFrame([])
    for i in range(0, df.shape[1]-1):
        triangle_factor['age_'+str(i+1)+'_to_'+str(i+2)] = df.iloc[:,i+1]/df.iloc[:,i]

    triangle_factor.loc['mean'] = triangle_factor.mean()
    return triangle_factor


def fill_triangle_loss(df, df_fact):
    num_rows, num_col = df.shape
    for i in range(0, num_col-1):
        factor = df_fact.loc['mean'][i]

        for j in range(0, i+1):
            df.iloc[num_rows-1-j,i+1] = df.iloc[num_rows-1-j,i]*factor 
    return df


def boostrap_clm(df, df_exposure, df_exposure_age):
    
    triangle_loss = boostrap_fill_all(df, df_exposure, df_exposure_age)
    triangle_factor = compute_triangle_factor(triangle_loss)
    triangle_loss_filled = fill_triangle_loss(triangle_loss, triangle_factor) 
    
            
    return triangle_factor,triangle_loss_filled


# use reported loss times factor (from boostrap samples)
def boostrap_clm_reported_loss_b_factor(df, df_exposure, df_exposure_age, triangle_loss_origin):
    
    triangle_loss = boostrap_fill_all(df, df_exposure, df_exposure_age)
    triangle_factor_b = compute_triangle_factor(triangle_loss)

    triangle_loss_filled_b = fill_triangle_loss(triangle_loss_origin, triangle_factor_b)
    
            
    return triangle_factor_b, triangle_loss_filled_b