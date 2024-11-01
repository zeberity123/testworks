import json
import matplotlib.pyplot as plt
import os
import numpy as np

json_folder = 'jsonexample'
json_list = os.listdir(json_folder)


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


for i in json_list:
    with open(f'{json_folder}/{i}', 'r') as f:
        data = json.load(f)

        frames = data['frames']

        gps_vss_acceleration = []

        gps_vss_frame = vss_to_list(frames)

        gps_vss_seconds = frames_to_seconds(gps_vss_frame)

        gps_vss_100ms = frames_to_100ms(gps_vss_frame)

        # for test
        gps_vss_100ms = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 23, 24, 24, 24, 24, 24, 24, 24, 24, 24, 27, 27, 27, 27, 27, 27, 27, 27, 27, 27, 29, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 34, 
34, 34, 34, 34, 34, 34, 34, 34, 34, 36, 36, 36, 36, 36, 36, 36, 36, 36, 36, 37, 39, 39, 39, 39, 39, 39, 39, 39, 39, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 43, 43, 43, 43, 43, 43, 43, 43, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 42, 42, 42, 42, 42, 42, 42, 42, 39, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 34, 34, 34, 34, 34, 34, 34, 34, 34, 34, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 31, 31, 31, 
31, 31, 31, 31, 31, 31, 31, 31, 28, 28, 28, 28, 28, 28, 28, 28, 28, 25, 21, 21, 21, 21, 21, 21, 21, 21, 21, 15, 15, 15, 15, 15, 15, 15, 15, 15, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 21, 25, 25, 25, 25, 25, 25, 25, 26, 29, 29, 29, 29, 29, 29, 29, 29, 29, 29, 32, 32, 32, 32, 32, 32, 32, 32, 32, 32, 36, 38, 38, 
38, 38, 38, 38, 38, 38, 38, 38, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 40, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 41, 40, 40, 40, 40, 40, 40, 40, 40, 40, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 40, 40, 40, 40, 40, 40, 40, 40, 40, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 39, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 44, 44, 44, 44, 
44, 44, 44, 44, 44, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 44, 43, 41, 41, 41, 41, 41, 41, 41, 41, 41, 41, 43, 43, 43, 43, 43, 43, 43, 43, 43, 43, 42, 42, 42, 42, 42, 42, 42, 42, 42, 42, 41, 41, 41, 41, 41, 41, 41, 41, 41, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 29, 29, 29, 29, 29, 29, 29, 29, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
        
        gps_vss_seconds = ms_to_seconds(gps_vss_100ms)
        
        gps_vss_acceleration = vss_to_acceleration(gps_vss_seconds)
        # gps_vss_acceleration = vss_to_acceleration(gps_vss_frame)
        # gps_vss_acceleration = vss_to_acceleration(gps_vss_100ms)

        sudden_actions = check_sudden_action(gps_vss_100ms)

        json_data_list.append([i, gps_vss_seconds, gps_vss_acceleration, gps_vss_frame, gps_vss_100ms, sudden_actions])



data_vss = json_data_list[0][1]
data_acc = json_data_list[0][2]
data_frame = json_data_list[0][3]
data_vss_100ms = json_data_list[0][4]
sudden_actions = json_data_list[0][5]

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





'''
graph
blue: vss
green: acc
'''

plt.figure(figsize=(13, 7))
plt.subplot(211)

plt.title('GPS VSS (1s)', fontsize=16)
plt.plot(x1, data_vss, linestyle='-', color='blue', linewidth=2)

# plt.title('GPS VSS (frame)', fontsize=16)
# plt.plot(x1, data_frame, linestyle='-', color='blue', linewidth=2)

# plt.title('GPS VSS (0.1s)', fontsize=16)
# plt.plot(x1, data_vss_100ms, linestyle='-', color='blue', linewidth=2)

plt.xlabel('Time (Seconds)', fontsize=14)
plt.ylabel('km/h', fontsize=14)

plt.grid(True, linestyle='--', linewidth=0.5)

# plt.xticks([0, 600, 1200, 1800, 2400, 3000, 3600], [0, 20, 40, 60, 80, 100, 120])
# plt.xticks([0, 200, 400, 600, 800, 1000, 1200], [0, 20, 40, 60, 80, 100, 120])

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()

plt.subplot(212)
plt.title('Acceleration', fontsize=16)
plt.plot(x2, data_acc, linestyle='-', color='green', linewidth=2)
plt.xlabel('Time (Seconds)', fontsize=14)
plt.ylabel('km/h', fontsize=14)

plt.grid(True, linestyle='--', linewidth=0.5)

# plt.xticks([0, 600, 1200, 1800, 2400, 3000, 3600], [0, 20, 40, 60, 80, 100, 120])
# plt.xticks([0, 200, 400, 600, 800, 1000, 1200], [0, 20, 40, 60, 80, 100, 120])

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.tight_layout()
plt.show()
