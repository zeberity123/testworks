import pandas as pd
import os
import json

meta_excel = 'new_sorted_metadata.xlsx'
labellings_root = '3300_json'
labelling_files = os.listdir(labellings_root)

cols_metadata = ['row_num', 'dh_name', 'cm_name', 
                 'can_name', 'title', 'date', 
                 'time', 'weather', 'scenario', 
                 'length', 'Car info', 'Driver_ID', 'Sex', 
                 'Age', 'Driving Experience', 'Traffic', 
                 'Load_category', 'Load_Geo', 'Risky_type']

cols_dtypes = {
    'row_num': str,
    'dh_name': str,
    'cm_name': str,
    'can_name': str,
    'title': str,
    'date': str,
    'time': str,
    'weather': str,
    'scenario': str,
    'length': str,
    'Car info': str,
    'Driver_ID': str,
    'Sex': str,
    'Age': str,
    'Driving Experience': str,
    'Traffic': str,
    'Load_category': str,
    'Load_Geo': str,
    'Risky_type': str
}

checked_metadata_list = []


def meta_excel_to_list(meta_excel):
    df = pd.read_excel(f'{meta_excel}', engine='openpyxl', sheet_name=0, names=cols_metadata, dtype=cols_dtypes)
    file_num = df['title'].tolist()
    file_nums = [i[-10:-5] for i in file_num]
    return df, file_nums

def input_weather_from_json(label_file, df):
    with open(f'{labellings_root}/{label_file}', 'r') as f:
        label_data = json.load(f)
        weather_label = label_data['dataset']['weather']
        line = df.copy()
        line['weather'] = weather_label
        s = line['Load_category']
        if pd.isnull(s):
            # print('nnnwnnnnnnnnnnn')
            line['Load_category'] = 'NAA'
        return line
    
excel_df = meta_excel_to_list(meta_excel)

cnt = 0
new_df = pd.DataFrame()
for row in range(len(excel_df[1])):
    cnt += 1
    for file in labelling_files:
        label_num = file[-10:-5]
        if label_num == excel_df[1][row]:
            new_line = input_weather_from_json(file, excel_df[0].loc[row])
            new_df = pd.concat([new_df, pd.DataFrame([new_line])], ignore_index=True)

    print(f'searching...{cnt}/{len(labelling_files)}')

new_df.to_excel('newnew_metadata.xlsx', index=False)
