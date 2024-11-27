import cv2
import pandas as pd
import os
import json

meta_excel = 'newnew_metadata.xlsx'
labellings_root = '3300_json'
labellings_root = 'new_3300_json'
labelling_files = os.listdir(labellings_root)

cols_metadata = ['row_num', 'dh_name', 'cm_name', 
                 'can_name', 'title', 'date', 
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

def check_metadata(label_file, df, row):
    with open(f'{labellings_root}/{label_file}', 'r') as f:
        label_data = json.load(f)
        # print(f'searching..{label_file}')
        l_dataset = label_data['dataset'].keys()
        for key in l_dataset:
            l_data = label_data['dataset'][key]
            d_data = df[key][row]
            # if key == 'date':
            #     # print(type(d_data))
            #     l_data = l_data.split('.')
            #     d_data = str(d_data).split('-')
            #     d_data[2] = d_data[2][:2]
            # if key == 'date':
            #     # print(type(d_data))
            #     l_data = l_data.split('.')
            #     d_data = str(d_data).split('-')
            #     d_data[2] = d_data[2][:2]
            # if key == 'scenario':
            #     l_data = 'PG' if l_data == 'Test' else 'Real'

            if key == 'weather':
                d_data = d_data[0].upper()+d_data[1:]
            # if key == 'Driver_ID':
            #     d_data = int(d_data)
            if l_data != d_data:
                checked_metadata_list.append([label_file, l_data, d_data, key])
                print(label_file, l_data, d_data, key)

        l_collection_info = label_data['Collection_info'].keys()
        for key in l_collection_info:
            l_data = label_data['Collection_info'][key]
            d_data = df[key][row]
            if key == 'Driver_ID':
                l_data = int(l_data)
                d_data = d_data.item()
            if l_data != d_data:
                checked_metadata_list.append([label_file, l_data, d_data, key])
                print(label_file, l_data, d_data, key)

        l_load = label_data['Load'].keys()
        for key in l_load:
            l_data = label_data['Load'][key]
            d_data = df[key][row]
            if pd.isnull(d_data):
                d_data = 'NA'
            if l_data == 'NA':
                l_data = 'NAA'
            # if key == 'Load_Geo':
            #     d_data = d_data.lower()
            if l_data != d_data:
                checked_metadata_list.append([label_file, l_data, d_data, key])
                print(label_file, l_data, d_data, key)

        l_risky = label_data['Risky'].keys()
        for key in l_risky:
            l_data = label_data['Risky'][key]
            d_data = df[key][row]
            if l_data != d_data:
                checked_metadata_list.append([label_file, l_data, d_data, key])
                print(label_file, l_data, d_data, key)

metadata_list = meta_excel_to_list(meta_excel)

checked_box = []
cnt = 0
for file in labelling_files:
    cnt += 1
    label_num = file[-10:-5]
    for row in range(len(metadata_list[1])):
        if label_num == metadata_list[1][row]:
            check_metadata(file, metadata_list[0], row)
    
    print(f'searching...{cnt}/{len(labelling_files)}')

# for i in checked_metadata_list:
#     print(i)

error_keys = list(set(i[3] for i in checked_metadata_list))
print(error_keys)
# error_keys = ['time', 'Load_category', 'length', 'date', 'weather', 'title', 'Sex', 'Driving Experience', 'Load_Geo']

sorted_error_list = []
for i in cols_metadata:
    for j in checked_metadata_list:
        if j[3] == i:
            sorted_error_list.append(j)

for i in sorted_error_list:
    print(i)

print(len(list(set([i[0] for i in checked_metadata_list]))))
print(len([i[0] for i in checked_metadata_list]))
