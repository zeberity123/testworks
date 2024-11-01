import json
import matplotlib.pyplot as plt
import os
import cv2

json_folder = 'jsonexample'
ex_json_list = os.listdir(json_folder)

json_root = 'G:/'
can_loc_list = os.listdir(json_root)

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
json_filename
gps_vss_seconds
gps_vss_acceleration
'''
json_data_list = []

def vss_to_list(frames):
    gps_vss_frame = []
    for frame in frames:
        gps_vss = frame['aim_micom']['gps_vss']
        gps_vss_frame.append(int(gps_vss))
    
    return gps_vss_frame

def frames_to_seconds(gps_vss_frame):
    gps_vss_seconds = []
    total_seconds = len(gps_vss_frame) // 30
    for i in range(total_seconds):
        vss_in_second = sum(gps_vss_frame[i*30:(i+1)*30])//30
        gps_vss_seconds.append(vss_in_second)
    
    return gps_vss_seconds

def ms_to_seconds(gps_vss_100ms):
    gps_vss_seconds = []
    total_seconds = len(gps_vss_100ms) // 10
    for i in range(total_seconds):
        vss_in_second = sum(gps_vss_100ms[i*10:(i+1)*10])//10
        gps_vss_seconds.append(vss_in_second)
    
    return gps_vss_seconds

def frames_to_100ms(gps_vss_frame):
    gps_vss_100ms = []
    total_100ms = len(gps_vss_frame) // 3
    for i in range(total_100ms):
        vss_in_second = sum(gps_vss_frame[i*3:(i+1)*3])//3
        gps_vss_100ms.append(vss_in_second)

    return gps_vss_100ms

def vss_to_acceleration(gps_vss_seconds):
    gps_vss_acceleration = []
    for i in range(len(gps_vss_seconds)-1):
        acceleration = gps_vss_seconds[i+1] - gps_vss_seconds[i]
        gps_vss_acceleration.append(acceleration)

    return gps_vss_acceleration

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

n_of_can = 0
e1 = cv2.getTickCount()
for i in source_can_list:
    n_of_can += 1
    # with open(f'{json_folder}/{i}', 'r') as f:
    with open(i, 'r') as f:
        data = json.load(f)

        frames = data['frames']

        gps_vss_acceleration = []

        gps_vss_frame = vss_to_list(frames)

        gps_vss_seconds = frames_to_seconds(gps_vss_frame)

        gps_vss_100ms = frames_to_100ms(gps_vss_frame)

#         # for test
#         gps_vss_100ms = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
# 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23, 24, 24, 24, 24, 24, 24, 24, 24, 24, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 29, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 34, 
# 34, 34, 34, 34, 34, 34, 34, 34, 34, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 37, 39, 39, 39, 39, 39, 39, 39, 39, 39, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 43, 43, 43, 43, 43, 43, 43, 43, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 42, 42, 42, 42, 42, 42, 42, 42, 39, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 31, 31, 31, 
# 31, 31, 31, 31, 31, 31, 31, 31, 28, 28, 28, 28, 28, 28, 28, 28, 28, 25, 21, 21, 21, 21, 21, 21, 21, 21, 21, 15, 15, 15, 15, 15, 15, 15, 15, 15, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
# 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
# 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 21, 25, 25, 25, 25, 25, 25, 25, 26, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 36, 38, 38, 
# 38, 38, 38, 38, 38, 38, 38, 38, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 40, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 41, 40, 40, 40, 40, 40, 40, 40, 40, 40, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 40, 40, 40, 40, 40, 40, 40, 40, 40, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 44, 44, 44, 44, 
# 44, 44, 44, 44, 44, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 43, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 41, 41, 41, 41, 41, 41, 41, 41, 41, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 29, 29, 29, 29, 29, 29, 29, 29, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
        
        # gps_vss_seconds = ms_to_seconds(gps_vss_100ms)
        
        gps_vss_acceleration = vss_to_acceleration(gps_vss_seconds)
        # gps_vss_acceleration = vss_to_acceleration(gps_vss_frame)
        # gps_vss_acceleration = vss_to_acceleration(gps_vss_100ms)
        
        have_all = False
        sudden_actions = check_sudden_action(gps_vss_100ms)

        if sudden_actions[0] and sudden_actions[1] and sudden_actions[2] and sudden_actions[3]:
            have_all = True

        json_data_list.append([i, gps_vss_seconds, gps_vss_acceleration, gps_vss_frame, gps_vss_100ms, sudden_actions, have_all])

    print(f'scanning... {n_of_can}/{len(source_can_list)}')

e2 = cv2.getTickCount()
Total_time = (e2 - e1)/ cv2.getTickFrequency()

print(f'Total time taken: {Total_time} seconds')
print(f'Total scanned number of can_data: {n_of_can} files')

have_alls = []

for can_json in json_data_list:
    if can_json[6]:
        have_alls.append(can_json[0])

for have_all in have_alls:
    print(have_all)

json_filename = json_data_list[0][0]
data_vss = json_data_list[0][1]
data_acc = json_data_list[0][2]
data_frame = json_data_list[0][3]
data_vss_100ms = json_data_list[0][4]
sudden_actions = json_data_list[0][5]
have_all = json_data_list[0][6]

x1 = [i for i in range(len(data_vss))]
# x1 = [i for i in range(len(data_frame))]
# x1 = [i for i in range(len(data_vss_100ms))]
x2 = [i for i in range(len(data_acc))]


'''
급출발
'''
sudden_acc = sudden_actions[0]
sudden_dec = sudden_actions[1]
sudden_stops = sudden_actions[2]
sudden_starts = sudden_actions[3]

for i in sudden_acc:
    print(f'sudden accceleration: {i}')

for i in sudden_dec:
    print(f'sudden deceleration: {i}')

for i in sudden_stops:
    print(f'sudden stop: {i}')

for i in sudden_starts:
    print(f'sudden start: {i}')

# print(json_filename, have_all)
# print(data_frame)
'''
graph
blue: vss
green: acc
'''

# plt.figure(figsize=(13, 7))
# plt.subplot(211)

# plt.title('GPS VSS (1s)', fontsize=16)
# plt.plot(x1, data_vss, linestyle='-', color='blue', linewidth=2)

# # plt.title('GPS VSS (frame)', fontsize=16)
# # plt.plot(x1, data_frame, linestyle='-', color='blue', linewidth=2)

# # plt.title('GPS VSS (0.1s)', fontsize=16)
# # plt.plot(x1, data_vss_100ms, linestyle='-', color='blue', linewidth=2)

# plt.xlabel('Time (Seconds)', fontsize=14)
# plt.ylabel('km/h', fontsize=14)

# plt.grid(True, linestyle='--', linewidth=0.5)

# # plt.xticks([0, 600, 1200, 1800, 2400, 3000, 3600], [0, 20, 40, 60, 80, 100, 120])
# # plt.xticks([0, 200, 400, 600, 800, 1000, 1200], [0, 20, 40, 60, 80, 100, 120])

# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)
# plt.tight_layout()

# plt.subplot(212)
# plt.title('Acceleration', fontsize=16)
# plt.plot(x2, data_acc, linestyle='-', color='green', linewidth=2)
# plt.xlabel('Time (Seconds)', fontsize=14)
# plt.ylabel('km/h', fontsize=14)

# plt.grid(True, linestyle='--', linewidth=0.5)

# # plt.xticks([0, 600, 1200, 1800, 2400, 3000, 3600], [0, 20, 40, 60, 80, 100, 120])
# # plt.xticks([0, 200, 400, 600, 800, 1000, 1200], [0, 20, 40, 60, 80, 100, 120])

# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)
# plt.tight_layout()
# plt.show()
