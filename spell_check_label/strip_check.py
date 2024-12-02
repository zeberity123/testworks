import os
import json

# 라벨링 json 모여있는 폴더
json_folder_root = 'TTA'
json_file_list = os.listdir(json_folder_root)

errors_in_jsons = []

def check_spelling_errors(sentence):
    spelling_errors = []

    # 띄어쓰기 2개 이상
    if '  ' in sentence:
        pre_post_sp = sentence.split('  ')
        pre_post = pre_post_sp[0][-1] + '  ' + pre_post_sp[1][:1]
        error_at = f'{sentence}' + "'" + f' ||{pre_post}'
        spelling_errors.append(error_at)

    # 문장 앞 띄어쓰기
    if sentence[0] == ' ':
        error_at = f'{sentence}' + "'" + f' || Leading space'
        spelling_errors.append(error_at)
    
    # 문장 뒤 띄어쓰기
    if sentence[-1] == ' ':
        error_at = f'{sentence}' + "'" + f' || Trailing space'
        spelling_errors.append(error_at)

    
    return spelling_errors

cnt = 0
for file_name in json_file_list:
    cnt += 1
    with open(f'{json_folder_root}/{file_name}', 'r', encoding='UTF-8') as f:
        label_data = json.load(f)
        keys = label_data['labeling'].keys()
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

    print(f'Scanning...: {cnt}/{len(json_file_list)}')

print('------------------')

error_cnt = 0
for file in errors_in_jsons:
    if len(file[1]) != 0:
        print(file[0])
        for detected_error in file[1]:
            print(detected_error)
        error_cnt += 1
 
print(f'{error_cnt} errors detected')