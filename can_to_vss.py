import json
import os
import cv2
import pandas as pd

json_root = 'jsonexample'
ex_json_list = os.listdir(json_root)

json_root = 'G:/'
can_loc_list = os.listdir(json_root)

new_json_root = 'vss_json_list'

def get_vids_list_source(can_loc_list):
    source_can_list = []
    for i in can_loc_list:
        if '데이터_' in i[:5]:
            loc_to_source = f'{json_root}/{i}'
            for can_json in os.listdir(f'{loc_to_source}/3. CAN'):
                source_can_list.append(f'{loc_to_source}/3. CAN/{can_json}')

    return source_can_list

source_can_list = get_vids_list_source(can_loc_list)
# source_can_list = ex_json_list

'''
json_data_list[]

string: json_filename
list: gps_vss_acceleration
list: gps_vss_frame
list: gps_vss_100ms
'''
json_data_list = []

def vss_to_list(frames):
    gps_vss_frame = []
    for frame in frames:
        gps_vss = frame['aim_micom']['gps_vss']
        gps_vss_frame.append(int(gps_vss))
    
    return gps_vss_frame

def frames_to_100ms(gps_vss_frame):
    gps_vss_100ms = []
    total_100ms = len(gps_vss_frame) // 3
    for i in range(total_100ms):
        vss_in_second = sum(gps_vss_frame[i*3:(i+1)*3])//3
        gps_vss_100ms.append(vss_in_second)

    return gps_vss_100ms

def vss_to_acceleration(gps_vss_100ms):
    gps_vss_acceleration = []
    for i in range(len(gps_vss_100ms)-1):
        acceleration = gps_vss_100ms[i+1] - gps_vss_100ms[i]
        gps_vss_acceleration.append(acceleration)

    return gps_vss_acceleration

        
def filename_only(filename):
    return filename.split('/')[-1]


def can_to_vss(json_data_list):
    for i in json_data_list:
        time = [0.0]
        time += [str(second/10) for second in range(1, len(i[1]))]
        dict = {}
        dict['vss_100ms'] = {}
        i[2].insert(0, 0)
        for j in range(len(i[1])):
            dict['vss_100ms'][f'{time[j]}'] = f'vss: {i[1][j]}, acc: {i[2][j]}'


        filename = filename_only(i[0])
        with open(f'{new_json_root}/vss_{filename[:-5]}.json', 'w') as f:
            json.dump(dict, f, ensure_ascii=False, indent=4)

        # print(len(i[0]))
        # print(len(i[1]))
        # print(len(i[2]))


n_of_can = 0
e1 = cv2.getTickCount()
for json_name in source_can_list[164:165]:
# for json_name in source_can_list[:1]:
    n_of_can += 1
    # with open(f'{json_root}/{json_name}', 'r') as f:
    with open(json_name, 'r') as f:
        data = json.load(f)

        frames = data['frames']

        gps_vss_acceleration = []

        gps_vss_frame = vss_to_list(frames)

        gps_vss_100ms = frames_to_100ms(gps_vss_frame)

        gps_vss_acceleration = vss_to_acceleration(gps_vss_100ms)

        json_data_list.append([json_name, gps_vss_100ms, gps_vss_acceleration])
    print(f'scanning... {n_of_can}/{len(source_can_list)}')

e2 = cv2.getTickCount()
Total_time = (e2 - e1)/ cv2.getTickFrequency()

print(f'Total time taken: {Total_time} seconds')
print(f'Total scanned number of can_data: {n_of_can} files')


can_to_vss(json_data_list)