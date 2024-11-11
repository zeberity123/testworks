import json
import os
import cv2

json_root = 'can_to_vss_246'
ex_json_list = os.listdir(json_root)

json_root = 'can_to_vss_246'
can_loc_list = os.listdir(json_root)

new_json_root = 'can_to_vss_246/vss_CAN_1111_246건'


source_can_list = ex_json_list

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

def check_sudden_action(data_vss_100ms):
    sudden_acc = []
    sudden_dec = []
    sudden_start = []
    sudden_stop = []
    for i in range(len(data_vss_100ms)):
        ms_100 = data_vss_100ms[i:i+10]

        min_vss = min(ms_100)
        min_index = ms_100.index(min(ms_100))
        max_vss = max(ms_100)
        max_index = ms_100.index(max(ms_100))

        if min_vss <= 5 and (max_vss - min_vss) >= 10:
            if min_index < max_index:
                sudden_start.append([i/10, f'VSS:{min_vss}~{max_vss}'])
            else:
                sudden_stop.append([i/10, f'VSS:{max_vss}~{min_vss}'])

        if min_vss >= 6 and (max_vss - min_vss) >= 15:
            if min_index < max_index:
                sudden_acc.append([i/10, f'VSS:{min_vss}~{max_vss}'])
            else:
                sudden_dec.append([i/10, f'VSS:{max_vss}~{min_vss}'])


    return [sudden_acc, sudden_dec, sudden_stop, sudden_start]

def check_continuous(sudden_actions):
    removed_continuous = []
    if sudden_actions:
        current_time = sudden_actions[0][0]
        removed_continuous.append([current_time, sudden_actions[0][1]])

        for i in range(1, len(sudden_actions)):
            # print(f'{sudden_actions[i][0] - current_time}')
            if (sudden_actions[i][0] - current_time) >= 0.09 and (sudden_actions[i][0] - current_time) <= 0.11:
                removed_continuous.pop()
                removed_continuous.append([sudden_actions[i][0], sudden_actions[i][1]])
                current_time = sudden_actions[i][0]
            else:
                removed_continuous.append([sudden_actions[i][0], sudden_actions[i][1]])
                current_time = sudden_actions[i][0]

        return removed_continuous
    
    return []

def can_to_vss(json_data_list):
    for i in json_data_list:
        time = [0.0]
        time += [str(second/10) for second in range(1, len(i[1]))]
        dict = {}
        dict['summary'] = {}
        dict['summary']['급가속'] = f'{len(i[3][0]) if i[3][0] else 0}건'
        dict['summary']['급감속'] = f'{len(i[3][1]) if i[3][1] else 0}건'
        dict['summary']['급정지'] = f'{len(i[3][2]) if i[3][2] else 0}건'
        dict['summary']['급출발'] = f'{len(i[3][3]) if i[3][3] else 0}건'
        dict['vss_100ms'] = {}
        i[2].insert(0, 0)
        for j in range(len(i[1])):
            dict['vss_100ms'][f'{time[j]}'] = f'vss: {i[1][j]}, acc: {i[2][j]}'


        filename = filename_only(i[0])
        with open(f'{new_json_root}/vss_{filename[:-5]}.JSON', 'w') as f:
            json.dump(dict, f, ensure_ascii=False, indent=4)

        # print(len(i[0]))
        # print(len(i[1]))
        # print(len(i[2]))


n_of_can = 0
e1 = cv2.getTickCount()
for json_name in source_can_list[:-1]:
    n_of_can += 1
    with open(f'{json_root}/{json_name}', 'r') as f:
    # with open(json_name, 'r') as f:
        data = json.load(f)

        frames = data['frames']

        gps_vss_acceleration = []

        gps_vss_frame = vss_to_list(frames)

        gps_vss_100ms = frames_to_100ms(gps_vss_frame)

        gps_vss_acceleration = vss_to_acceleration(gps_vss_100ms)

        sudden_actions = check_sudden_action(gps_vss_100ms)
        for i in range(4):
            sudden_actions[i] = check_continuous(sudden_actions[i])

        json_data_list.append([json_name, gps_vss_100ms, gps_vss_acceleration, sudden_actions])
    print(f'scanning... {n_of_can}/{len(source_can_list)}')

e2 = cv2.getTickCount()
Total_time = (e2 - e1)/ cv2.getTickFrequency()

print(f'Total time taken: {Total_time} seconds')
print(f'Total scanned number of can_data: {n_of_can} files')




can_to_vss(json_data_list)