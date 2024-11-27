import pandas as pd
import os
import json

meta_excel = 'newnew_metadata.xlsx'
labellings_root = '3300_json'
labelling_files = os.listdir(labellings_root)
new_labellings_root = 'new_3300_json'

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

def merge_from_excel_to_json(label_file, df):

    with open(f'{labellings_root}/{label_file}', 'r') as f:
        label_data = json.load(f)
        new_date = df['date']
        new_length = df['length']
        new_d_id = df['Driver_ID']
        new_d_e = df['Driving Experience']
        new_load_geo = df['Load_Geo']

        label_data['dataset']['date'] = new_date
        label_data['dataset']['length'] = new_length
        label_data['Collection_info']['Driver_ID'] = new_d_id
        label_data['Collection_info']['Driving Experience'] = new_d_e
        label_data['Load']['Load_Geo'] = new_load_geo

        # print(label_data)
        with open(f'{new_labellings_root}/{label_file}','w') as g:
            json.dump(label_data, g, ensure_ascii=False, indent=4)


excel_df = meta_excel_to_list(meta_excel)

cnt = 0

for file in labelling_files:
    cnt += 1
    label_num = file[-10:-5]
    for row in range(len(excel_df[1])):
        if label_num == excel_df[1][row]:
            merge_from_excel_to_json(file, excel_df[0].loc[row])

    print(f'searching...{cnt}/{len(labelling_files)}')