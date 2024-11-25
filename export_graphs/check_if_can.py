import os
import cv2
import shutil

json_root = './'
txt_filename = 'txt_list.txt'
directoy_name = 'in_txt'
can_list = []

for i in os.listdir(json_root):
    if i.split('.')[-1] == 'JSON' or i.split('.')[-1] == 'json':
        can_list.append(i)

json_data_list = []

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

def parse_num_txt(txt_line):
    return txt_line[-5:]

def txt_to_list(txt_filename):
    parse_txt = txt_filename
    f = open(parse_txt, "r")
    txt_list = []
    while True:
        line = f.readline().strip()
        if not line: break
        txt_list.append(parse_num_txt(line))

    return txt_list

def parse_num_json(json_filename):
    return json_filename[-10:-5]

def filename_only(filename):
    return filename.split('/')[-1]

createDirectory(directoy_name)

txt_num_list = txt_to_list(txt_filename)
num_only_json = [parse_num_json(i) for i in can_list]
n_of_can = 0
copied = 0
e1 = cv2.getTickCount()
for i in txt_num_list:
    n_of_can += 1
    for j in can_list:
        if i == parse_num_json(j):
            shutil.copy(f'{j}', f'{directoy_name}/{j}')
            copied += 1
    
    print(f'searching... {n_of_can}/{len(txt_num_list)}')

e2 = cv2.getTickCount()
Total_time = (e2 - e1)/ cv2.getTickFrequency()

print(f'Total time taken: {Total_time} seconds')
print(f'Total copied number of can_data: {copied} files')
