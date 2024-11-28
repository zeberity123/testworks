from hanspell import spell_checker
import os
import json
import cv2

json_folder_root = 'backup_json3300_241127'
json_file_list = os.listdir(json_folder_root)

errors_in_jsons = []

def check_spelling_errors(sentence):
    spelling_errors = []
    checked_sentence = spell_checker.check(sentence)
    dict_checked_sentence = checked_sentence.as_dict()
    word_list = dict_checked_sentence['words']
    # print(word_list)
    for word, error_type in word_list.items():
        if error_type == 1:
            print(word)
            spelling_errors.append([word, error_type])
        # elif error_type != 0:
        #     spelling_errors.append([word, error_type])
    
    return spelling_errors

cnt = 0
for file_name in json_file_list:
    cnt += 1
    e1 = cv2.getTickCount()
    with open(f'{json_folder_root}/{file_name}', 'r') as f:
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

for file in errors_in_jsons:
    if len(file[1]) != 0:
        print(file[0], file[1])
    # print(file[1])