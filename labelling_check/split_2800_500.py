import os
import shutil

can_jsons = []
label_jsons = []

can_origin = 'G:/DATA_ALL_3205건_1110까지/241115_model_2800/2. can'
label_origin = 'G:/DATA_ALL_3205건_1110까지/241118_model_500/3. labelings'

for i in os.listdir(can_origin):
    if i.split('.')[-1] == 'JSON' or i.split('.')[-1] == 'json':
        can_jsons.append([can_origin, i])

for i in os.listdir(label_origin):
    if i.split('.')[-1] == 'JSON' or i.split('.')[-1] == 'json':
        label_jsons.append([label_origin, i])

can_500_dest = 'G:/DATA_ALL_3205건_1110까지/241118_model_500/2. can'

files_to_move = []

for i in label_jsons:
    destination = ''
    json_num = i[1][-10:-5]
    for j in can_jsons:
        if json_num in j[1]:
            destination += can_500_dest
            files_to_move.append([j[0], j[1], destination, j[1]])




# for i in files_to_move:
#     print(i)

print(len(files_to_move))

scan_cnt = 0
for i in files_to_move:
    scan_cnt += 1
    shutil.move(f'{i[0]}/{i[1]}', f'{i[2]}/{i[3]}')
    print(f'moving files...{scan_cnt}/{len(files_to_move)}')

