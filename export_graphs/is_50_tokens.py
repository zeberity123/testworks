import json
import os
import cv2
import shutil

json_root = '3300_json'
directoy_name = 'below_50'
can_list = []
json_data_list = []
# download('punkt_tab')

for i in os.listdir(json_root):
    if i.split('.')[-1] == 'JSON' or i.split('.')[-1] == 'json':
        can_list.append(i)

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

pg_json = []
below_50 = []
n_of_can = 0
e1 = cv2.getTickCount()
# createDirectory(directoy_name)
s_action = ['급출발', '급가속', '급정지', '급감속', '급회전', '없음']
for json_name in can_list:
    n_of_can += 1
    with open(f'{json_root}/{json_name}', 'r') as f:
    # with open(f'{json_name}', 'r') as f:
        data = json.load(f)
        
        sen_5 = data['labeling']['SEN_5']

        tokens = sen_5.split(' ')

        if len(tokens) >= 50:
            
            json_data_list.append([json_name, tokens])

        else:
            below_50.append([json_name, tokens])
            # shutil.copy(f'{json_name}', f'{directoy_name}/{json_name}')
        
        if '_PG_' in json_name:
            s_box = [0, 0, 0, 0, 0, 0]
            for i in range(6):
                for token in tokens:
                    if s_action[i] in token:
                        s_box[i] += 1
            pg_json.append([json_name, s_box])

            
            

    print(f'scanning... {n_of_can}/{len(can_list)}')

e2 = cv2.getTickCount()
Total_time = (e2 - e1)/ cv2.getTickFrequency()

total_s_box = [0, 0, 0, 0, 0, 0]
for i in pg_json:
    print(i)
    for j in range(6):
        total_s_box[j] += i[1][j]

for i in range(6):
    print(f'{s_action[i]}: {total_s_box[i]}건')

percent_s = [(i/sum(total_s_box))*100 for i in total_s_box]
for i in range(6):
    print(f'{s_action[i]}: {percent_s[i]:.2f}%')

# for i in below_50:
#     print(i[0])

# print(len(below_50))

print(f'Total time taken: {Total_time} seconds')
print(f'Total scanned number of can_data: {n_of_can} files')

# while True:
#     user_input = input("\nEnter q to quit: ")
#     if user_input.lower() == 'q':
#         break
    