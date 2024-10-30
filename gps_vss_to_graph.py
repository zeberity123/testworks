import json
import matplotlib.pyplot as plt
import os

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

def vss_to_acceleration(gps_vss_seconds):
    gps_vss_acceleration = []
    for i in range(len(gps_vss_seconds)-1):
        acceleration = gps_vss_seconds[i+1] - gps_vss_seconds[i]
        gps_vss_acceleration.append(acceleration)

    return gps_vss_acceleration

def check_sudden_action(check_sudden_action):
    

for i in json_list:
    with open(f'{json_folder}/{i}', 'r') as f:
        data = json.load(f)

        frames = data['frames']

        gps_vss_acceleration = []

        gps_vss_frame = vss_to_list(frames)

        gps_vss_seconds = frames_to_seconds(gps_vss_frame)

        gps_vss_acceleration = vss_to_acceleration(gps_vss_seconds)

        sudden_actions = check_sudden_action(gps_vss_frame)

        json_data_list.append([i, gps_vss_seconds, gps_vss_acceleration, gps_vss_frame])



# data_vss = json_data_list[0][1]
# data_acc = json_data_list[0][2]
# data_frame = json_data_list[0][3]

# x1 = [i for i in range(len(data_vss))]
# x2 = [i for i in range(len(data_acc))]

# print(data_vss)

# plt.figure(figsize=(13, 7))

# plt.subplot(211)
# plt.title('GPS VSS', fontsize=16)
# plt.plot(x1, data_vss, linestyle='-', color='blue', linewidth=2)
# plt.xlabel('Time (Seconds)', fontsize=14)
# plt.ylabel('km/h', fontsize=14)

# plt.subplot(212)
# plt.title('Acceleration', fontsize=16)
# plt.plot(x2, data_acc, linestyle='-', color='green', linewidth=2)
# plt.xlabel('Time (Seconds)', fontsize=14)
# plt.ylabel('km/h', fontsize=14)

# plt.grid(True, linestyle='--', linewidth=0.5)
# plt.xticks(fontsize=12)
# plt.yticks(fontsize=12)
# plt.tight_layout()
# plt.show()
