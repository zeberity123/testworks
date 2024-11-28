
import os
import json
import cv2

json_folder_root = 'backup_json3300_241127'
json_file_list = os.listdir(json_folder_root)
# json_file_list = ['2024_NIA_LAB_LAB_PG_F_A1_C2C_PG_D_02820.JSON']

errors_in_jsons = []

def check_spelling_errors(sentence):
    spelling_errors = []
    if '  ' in sentence:
        pre_post_sp = sentence.split('  ')
        pre_post = pre_post_sp[0][-1] + '  ' + pre_post_sp[1][:1]
        print(pre_post)
        sentence = f'{sentence} || {pre_post}'
        spelling_errors.append(sentence)

    
    return spelling_errors

cnt = 0
for file_name in json_file_list:
    cnt += 1
    e1 = cv2.getTickCount()
    with open(f'{json_folder_root}/{file_name}', 'r') as f:
    # with open(f'{file_name}', 'r') as f:
        label_data = json.load(f)
        keys = label_data['labeling'].keys()
        # print(keys)
        key_cnt = 0
        error_words_in_json = []
        for key in keys:
            key_cnt += 1
            line = label_data['labeling'][key]
            error_words_in_line = check_spelling_errors(line)
            for word_error in error_words_in_line:
                error_words_in_json.append([f'SEN_{key_cnt}', word_error])
                print(file_name, error_words_in_json)
        
        errors_in_jsons.append([file_name, error_words_in_json])
    e2 = cv2.getTickCount()
    Total_time = (e2 - e1)/ cv2.getTickFrequency()
    # print(f'Total time taken: {Total_time} seconds')
    print(f'Total number of parsed images(pairs): {cnt}/{len(json_file_list)} pairs')

print('------------------')

error_cnt = 0
for file in errors_in_jsons:
    if len(file[1]) != 0:
        print(file[0])
        for detected_error in file[1]:
            print(detected_error)
        error_cnt += 1
 
print(f'{error_cnt} errors detected')