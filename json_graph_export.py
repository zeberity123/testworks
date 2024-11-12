import json
import matplotlib.pyplot as plt
import os
import cv2

json_root = '00169'
# json_root = '00049'
json_root = '03287'
json_root = '02946'
ex_json_list = os.listdir(json_root)

# json_root = 'G:/'
can_loc_list = os.listdir(json_root)


source_can_list = can_loc_list

'''
json_data_list[]

string: json_filename
list: gps_vss_seconds
list: gps_vss_acceleration
list: gps_vss_frame
list: gps_vss_100ms
list: sudden_actions
list: bool_sudden_actions
bool: has_all
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

def print_has_all(json_data_list):
    has_alls = []

    for can_json in json_data_list:
        if can_json[6]:
            has_alls.append(can_json[0])

    for has_all in has_alls:
        print(has_all)
        
def filename_only(filename):
    return filename.split('/')[-1]


def check_continuous(sudden_actions):
    removed_continuous = []
    if sudden_actions:
        current_time = sudden_actions[0][0]
        removed_continuous.append([current_time, sudden_actions[0][1]])

        for i in range(1, len(sudden_actions)):
            # print(f'{sudden_actions[i][0] - current_time}')
            if (sudden_actions[i][0] - current_time) >= 0.09 and (sudden_actions[i][0] - current_time) <= 0.11:
                # removed_continuous.pop()
                # removed_continuous.append([sudden_actions[i][0], sudden_actions[i][1]])
                current_time = sudden_actions[i][0]
            else:
                removed_continuous.append([sudden_actions[i][0], sudden_actions[i][1]])
                current_time = sudden_actions[i][0]

        return removed_continuous
    
    return []



n_of_can = 0
e1 = cv2.getTickCount()
# for json_name in source_can_list[164:165]:
for json_name in source_can_list:
    n_of_can += 1
    with open(f'{json_root}/{json_name}', 'r') as f:
    # with open(json_name, 'r') as f:
        data = json.load(f)

        frames = data['frames']

        gps_vss_acceleration = []

        gps_vss_frame = vss_to_list(frames)

        gps_vss_seconds = frames_to_seconds(gps_vss_frame)

        gps_vss_100ms = frames_to_100ms(gps_vss_frame)
        
        gps_vss_acceleration = vss_to_acceleration(gps_vss_seconds)
        
        has_all = False
        sudden_actions = check_sudden_action(gps_vss_100ms)
        for i in range(4):
            sudden_actions[i] = check_continuous(sudden_actions[i])

        bool_sudden_actions = ['X', 'X', 'X', 'X']

        for i in range(len(sudden_actions)):
            bool_sudden_actions[i] = 'O' if sudden_actions[i] else 'X'

        json_data_list.append([json_name, gps_vss_acceleration, gps_vss_frame, gps_vss_100ms, sudden_actions, bool_sudden_actions])

    print(f'scanning... {n_of_can}/{len(source_can_list)}')

e2 = cv2.getTickCount()
Total_time = (e2 - e1)/ cv2.getTickFrequency()

print(f'Total time taken: {Total_time} seconds')
print(f'Total scanned number of can_data: {n_of_can} files')


'''
그래프 및 이상행동 (파일1개)
'''

json_filename = json_data_list[0][0]
data_acc = json_data_list[0][1]
data_frame = json_data_list[0][2]
data_vss_100ms = json_data_list[0][3]
sudden_actions = json_data_list[0][4]
bool_sudden_actions = json_data_list[0][5]

x1 = [i for i in range(len(data_vss_100ms))]
x2 = [i for i in range(len(data_acc))]


sudden_acc = sudden_actions[0]
sudden_dec = sudden_actions[1]
sudden_stops = sudden_actions[2]
sudden_starts = sudden_actions[3]

print(data_frame)


for i in sudden_acc:
    print(f'sudden accceleration: {[i[0], i[1]]}')

for i in sudden_dec:
    print(f'sudden deceleration: {[i[0], i[1]]}')

for i in sudden_stops:
    print(f'sudden stop: {[i[0], i[1]]}')

for i in sudden_starts:
    print(f'sudden start: {[i[0], i[1]]}')

# print(json_filename)
# print(data_vss_100ms)

'''
graph
blue: vss
green: acc
'''
plt.figure(figsize=(13, 7))
plt.subplot(211)

plt.title('GPS VSS (0.1s)', fontsize=16)
plt.plot(x1, data_vss_100ms, linestyle='-', color='blue', linewidth=2)
sudden_action_list = ['sudden_acc ', 'sudden_dec ', 'sudden_stop ', 'sudden_start ']
for i in range(4):
    if sudden_actions[i]:
        for sudden_action in sudden_actions[i]:
            target_time = int(sudden_action[0]*10)
            plt.plot(target_time, data_vss_100ms[target_time], marker='o',markerfacecolor='r')
            plt.text(target_time, data_vss_100ms[target_time], sudden_action_list[i], horizontalalignment='right', verticalalignment='bottom')

plt.xlabel('Time (Seconds)', fontsize=14)
plt.ylabel('km/h', fontsize=14)

plt.grid(True, linestyle='--', linewidth=0.5)

plt.xticks([i*100 for i in range(13)], [i*10 for i in range(13)])

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()

plt.subplot(212)
plt.title('Acceleration', fontsize=16)
plt.plot(x2, data_acc, linestyle='-', color='green', linewidth=2)
plt.xlabel(f'sudden_acc:{[i for i in sudden_acc] if sudden_acc else "[None]"}\n' +
           f'sudden_dec:{[i for i in sudden_dec] if sudden_dec else "[None]"}\n' +
           f'sudden_stops:{[i for i in sudden_stops] if sudden_stops else "[None]"}\n' +
           f'sudden_starts:{[i for i in sudden_starts] if sudden_starts else "[None]"}', fontsize=14, loc='left')
plt.ylabel('km/h', fontsize=14)

plt.grid(True, linestyle='--', linewidth=0.5)

plt.xticks([i*10 for i in range(13)], [i*10 for i in range(13)])

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()  