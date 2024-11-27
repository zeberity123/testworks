import cv2
import pandas as pd
import os
import json

meta_excel = 'metadata_meta.xlsx'
new_meta_excel = 'NI26_메타데이터_전체_241126.xlsx'
labellings_root = '3300_json'
labelling_files = os.listdir(labellings_root)

cols_metadata = ['row_num', 'dh_name', 'cm_name', 
                 'can_name', 'title', 'date', 
                 'time', 'weather', 'scenario', 
                 'length', 'Car info', 'Driver_ID', 'Sex', 
                 'Age', 'Driving Experience', 'Traffic', 
                 'Load_category', 'Load_Geo', 'Risky_type']

cols_new_metadata = ['title', 'date', 
                 'time', 'weather', 'scenario', 
                 'length', 'Car info', 'Driver_ID', 'Sex', 
                 'Age', 'Driving Experience', 'Traffic', 
                 'Load_category', 'Load_Geo', 'Risky_type']

# labelling_errors = []
checked_metadata_list = []

def meta_excel_to_list(meta_excel):
    df = pd.read_excel(f'{meta_excel}', engine='openpyxl', sheet_name=0, names=cols_metadata)
    file_num = df['title'].tolist()
    file_num = [i[-10:-5] for i in file_num]
    return df, file_num

def new_excel_to_list(new_meta_excel):
    df = pd.read_excel(f'{new_meta_excel}', engine='openpyxl', sheet_name=0, names=cols_new_metadata)
    file_num = df['title'].tolist()
    file_num = [i[-5:] for i in file_num]
    return df, file_num

old_metadata_list = meta_excel_to_list(meta_excel)
new_metadata_list = new_excel_to_list(new_meta_excel)

old_df = pd.DataFrame()
old_file_nums = []
new_df = new_metadata_list[0]

cols_to_copy = ['date', 
                 'time', 'scenario', 
                 'length', 'Car info', 'Driver_ID', 'Sex', 
                 'Age', 'Driving Experience', 
                 'Load_category', 'Load_Geo', 'Risky_type']

for i in range(len(new_metadata_list[1])):
# for i in range(5):
    file_num = new_metadata_list[1][i]
    for j in range(len(old_metadata_list[1])):
        if file_num == old_metadata_list[1][j]:
            old_df = pd.concat([old_df, pd.DataFrame([old_metadata_list[0].loc[j]])], ignore_index=True)
            for key in cols_to_copy:
                data_to_copy = str(new_df.loc[i][key])
                if key == 'date':
                    sp = data_to_copy.split('.')
                    data_to_copy = sp[0]+'.'+sp[1]+'.'+sp[2][:2]
                if data_to_copy == 'nan':
                    data_to_copy = 'NA'
                if key == 'scenario':
                    if data_to_copy == 'PG':
                        data_to_copy = 'Test'
                if data_to_copy == 'REAL':
                    data_to_copy = 'Real'
                if key == 'Load_Geo':
                    data_to_copy = data_to_copy.lower()
                old_df.at[i, key] = data_to_copy
            old_file_nums.append(old_metadata_list[1][j])

old_df = old_df.astype({'date':'str'})
old_df = old_df.astype({'Driver_ID':'str'})

for i in range(len(new_metadata_list[1])):
    date_data = old_df.loc[i]['date'].split(' ')[0]
    if '-' in date_data:
        # print(date_data)
        sp = date_data.split('-')
        old_df.at[i, 'date'] = sp[0]+'.'+sp[1]+'.'+sp[2]
    
    d_id = old_df.loc[i]['Driver_ID']
    len_0 = 6 - len(d_id)
    new_d_id = ''
    for j in range(len_0):
        new_d_id += '0'
    new_d_id += d_id
    old_df.at[i, 'Driver_ID'] = new_d_id

    weather_data = old_df.loc[i]['weather']
    old_df.at[i, 'weather'] = weather_data[0].upper()+weather_data[1:]
        

# print(old_file_nums == new_metadata_list[1])
old_df.to_excel('new_sorted_metadata.xlsx', index=False)

# df = df.astype({'시가':'int'}) 또는 df['시가'] = df['시가'].astype(int)
# df

# for i in range(len(new_metadata_list[1])):
#     new_df.loc[i:'weather'] = old_df.loc[i:'weather']
#     new_df.loc[i:'traffic'] = old_df.loc[i:'traffic']

# old_df = pd.concat([old_df, pd.DataFrame([old_metadata_list[0].loc[3299]])], ignore_index=True)

# print(old_df)


# print(new_df.loc[3299][['Age']])
# new_df.loc[3299:'Age'] = old_df.loc[3299:'Age']
# print(new_df.loc[3299][['Age']])