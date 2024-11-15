import json
import os
import cv2
import matplotlib.pyplot as plt

json_root = './'
# json_root = 'can_yaw_export'
can_loc_list = []

for i in os.listdir(json_root):
    if i.split('.')[-1] == 'JSON' or i.split('.')[-1] == 'json':
        can_loc_list.append(i)

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")


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

def yaw_to_list(frames):
    yaws = []
    yawHs = []
    yawLs = []
    for frame in frames:
        yaw = frame['aim_gsensor']['yaw']
        yawH = frame['aim_gsensor']['yawH']
        yawL = frame['aim_gsensor']['yawL']

        yaws.append(yaw)
        yawHs.append(yawH)
        yawLs.append(yawL)
    
    return [yaws, yawHs, yawLs]

def yaw_to_degree(yaw_data_raw):
    yaws_degree = []

    for i in range(len(yaw_data_raw[1])):
        yawH = yaw_data_raw[1][i]
        yawL = yaw_data_raw[2][i]
        yaw_raw = (yawH << 8) | yawL

        yaw_degree = yaw_raw / 32768 * 180
        yaws_degree.append(yaw_degree)

    return yaws_degree

def degree_delta(yaw_data_degree):
    current_delta = 0.0
    degrees_delta = [0.0]
    for i in range(len(yaw_data_degree)-1):
        yaw1 = yaw_data_degree[i]
        yaw2 = yaw_data_degree[i+1]

        delta = yaw2 - yaw1

        if (yaw1 > 300.0 and yaw2 < 60.0):
            delta = 360.0 + delta
        elif (yaw1 < 60.0 and yaw2 > 300.0):
            delta = delta - 360.0

        current_delta += delta
        degrees_delta.append(current_delta)
    
    return degrees_delta

def frames_to_100ms(yaw_data_degree):
    yaw_degree_100ms = []
    total_100ms = len(yaw_data_degree) // 3
    for i in range(total_100ms):
        degree_in_100ms = sum(yaw_data_degree[i*3:(i+1)*3])//3
        yaw_degree_100ms.append(degree_in_100ms)

    return yaw_degree_100ms

def frames_yaw_to_100ms(yaw_data_degree):
    yaw_degree_100ms = []
    total_100ms = len(yaw_data_degree) // 3
    for i in range(total_100ms):
        degree_in_100ms = sum(yaw_data_degree[i*3:(i+1)*3])/3
        yaw_degree_100ms.append(degree_in_100ms)

    return yaw_degree_100ms

        
def filename_only(filename):
    return filename.split('/')[-1]


def can_to_yaw_raw(json_data_list):
    createDirectory(f'{json_root}/yaw_raw')
    for i in json_data_list:
        dict = {}
        dict['yaw_data'] = {}
        for frameCnt in range(len(i[5][0])):
            dict['yaw_data'][f'{frameCnt}'] = f'yaw: {i[5][0][frameCnt]}, yawH: {i[5][1][frameCnt]}, yawL: {i[5][2][frameCnt]}'


        filename = filename_only(i[0])
        with open(f'{json_root}/yaw_raw/yaw_{filename[:-5]}.JSON', 'w') as f:
            json.dump(dict, f, ensure_ascii=False, indent=4)

def can_to_yaw_degree(json_data_list):
    createDirectory(f'{json_root}/yaw_json_frame')
    for i in json_data_list:
        dict = {}
        dict['yaw_data'] = {}
        for frameCnt in range(len(i[2])):
            dict['yaw_data'][f'{frameCnt}'] = f'yaw_degree: {i[6][frameCnt]:.4f}'


        filename = filename_only(i[0])
        with open(f'{json_root}/yaw_json_frame/frame_degree_{filename[:-5]}.JSON', 'w') as f:
            json.dump(dict, f, ensure_ascii=False, indent=4)

def can_to_yaw_degree_100ms(json_data_list):
    createDirectory(f'{json_root}/yaw_json_100ms')
    for i in json_data_list:
        time = [0.0]
        time += [str(second/10) for second in range(1, len(i[6]))]
        dict = {}
        dict['yaw_data'] = {}
        for j in range(len(i[7])):
            dict['yaw_data'][f'{time[j]}'] = f'yaw_degree: {i[7][j]:.4f}'


        filename = filename_only(i[0])
        with open(f'{json_root}/yaw_json_100ms/100ms_degree_{filename[:-5]}.JSON', 'w') as f:
            json.dump(dict, f, ensure_ascii=False, indent=4)

def check_sudden_action(gps_vss_100ms, yaw_data_degree):
    sudden_acc = []
    sudden_dec = []
    sudden_start = []
    sudden_stop = []
    sudden_rotation = []
    for i in range(len(gps_vss_100ms)):
        ms_1s = gps_vss_100ms[i:i+10]
        ms_3s = gps_vss_100ms[i:i+30]
        yaw_3s = yaw_data_degree[i:i+30]

        min_vss = min(ms_1s)
        min_index = ms_1s.index(min(ms_1s))
        max_vss = max(ms_1s)
        max_index = ms_1s.index(max(ms_1s))

        min_vss_3 = min(ms_3s)
        max_vss_3 = max(ms_3s)

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

        if min_vss_3 >= 10:
            total_rotation = []
            for j in range(len(yaw_3s)-1):
                delta = abs(yaw_3s[j+1] - yaw_3s[j])
                total_rotation.append(delta)
            
            if sum(total_rotation) >= 60.0:
                sudden_rotation.append([i/10, f'Rotation:{sum(total_rotation):.2f}°, VSS:{min_vss_3}~{max_vss_3}'])


    return [sudden_acc, sudden_dec, sudden_stop, sudden_start, sudden_rotation]

def check_continuous(sudden_actions):
    removed_continuous = []
    if sudden_actions:
        current_time = sudden_actions[0][0]
        removed_continuous.append([current_time, sudden_actions[0][1]])

        for i in range(1, len(sudden_actions)):
            if (sudden_actions[i][0] - current_time) >= 0.09 and (sudden_actions[i][0] - current_time) <= 0.11:
                current_time = sudden_actions[i][0]
            else:
                removed_continuous.append([sudden_actions[i][0], sudden_actions[i][1]])
                current_time = sudden_actions[i][0]

        return removed_continuous
    
    return []

def save_graphs(json_data_list):
    createDirectory(f'{json_root}/yaw_graphs')
    e3 = cv2.getTickCount()
    n_of_can = 0
    for data in json_data_list:
        n_of_can += 1

        json_filename = data[0]
        # data_acc = data[1]
        # data_frame = data[2]
        data_vss_100ms = data[3]
        sudden_actions = data[4]
        # yaw_data_raw = data[5]
        # yaw_data_degree = data[6]
        yaw_degree_100ms = data[7]
        # bool_sudden_actions = data[8]

        sudden_acc = sudden_actions[0]
        sudden_dec = sudden_actions[1]
        sudden_stops = sudden_actions[2]
        sudden_starts = sudden_actions[3]
        sudden_rotations = sudden_actions[4]

        
        x1 = [i for i in range(len(data_vss_100ms))]
        x2 = [i for i in range(len(yaw_degree_100ms))]

        plt.figure(figsize=(13, 7))
        plt.subplot(211)

        plt.title(f'{json_filename}', fontsize=16)
        plt.plot(x1, data_vss_100ms, linestyle='-', color='blue', linewidth=2)

        sudden_action_list = ['sudden_acc ', 'sudden_dec ', 'sudden_stop ', 'sudden_start ', 'sudden_rotation']
        
        for i in range(len(sudden_action_list)):
            if sudden_actions[i]:
                for sudden_action in sudden_actions[i]:
                    target_index = int(sudden_action[0]*10)
                    plt.plot(target_index, data_vss_100ms[target_index], marker='o',markerfacecolor='r')
                    plt.text(target_index, data_vss_100ms[target_index], sudden_action_list[i], horizontalalignment='right', verticalalignment='bottom')

        plt.xlabel('Time (Seconds)', fontsize=14)
        plt.ylabel('km/h', fontsize=14)

        plt.grid(True, linestyle='--', linewidth=0.5)

        plt.xticks([i*100 for i in range(13)], [i*10 for i in range(13)])

        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.tight_layout()


        plt.subplot(212)
        plt.plot(x2, yaw_degree_100ms, linestyle='-', color='green', linewidth=2)
        
        # only sudden rotation
        if sudden_rotations:
            for sudden_action in sudden_rotations:
                target_index = int(sudden_action[0]*10)
                plt.plot(target_index, yaw_degree_100ms[target_index], marker='o',markerfacecolor='r')
                plt.text(target_index, yaw_degree_100ms[target_index], sudden_action_list[4], horizontalalignment='right', verticalalignment='bottom')
        
        plt.xlabel(f'>sudden_acc:{[i for i in sudden_acc] if sudden_acc else "[None]"}\n' +
                f'>sudden_dec:{[i for i in sudden_dec] if sudden_dec else "[None]"}\n' +
                f'>sudden_stops:{[i for i in sudden_stops] if sudden_stops else "[None]"}\n' +
                f'>sudden_starts:{[i for i in sudden_starts] if sudden_starts else "[None]"}\n' +
                f'>sudden_rotation:{[i for i in sudden_rotations] if sudden_rotations else "[None]"}', fontsize=14, loc='left')
        plt.ylabel('YAW Degree°', fontsize=14)

        plt.grid(True, linestyle='--', linewidth=0.5)

        plt.xticks([i*100 for i in range(13)], [i*10 for i in range(13)])

        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)

        plt.tight_layout()
        # plt.show()
        plt.savefig(f'{json_root}/yaw_graphs/yaw_{json_filename[:-5]}.png')
        plt.close()

        print(f'saving graphs... {n_of_can}/{len(json_data_list)}')
    e4 = cv2.getTickCount()
    Total_time = (e4 - e3)/ cv2.getTickFrequency() 
    print(f'Total time taken: {Total_time} seconds')
    print(f'Total saved number of graphs: {n_of_can} files')
    # print(f'Cleaning Memory...')

n_of_can = 0
e1 = cv2.getTickCount()
for json_name in can_loc_list:
    n_of_can += 1
    with open(f'{json_root}/{json_name}', 'r') as f:
        data = json.load(f)

        frames = data['frames']

        gps_vss_frame = vss_to_list(frames)
        gps_vss_seconds = frames_to_seconds(gps_vss_frame)
        gps_vss_100ms = frames_to_100ms(gps_vss_frame)        
        gps_vss_acceleration = vss_to_acceleration(gps_vss_seconds)

        yaw_data_raw = yaw_to_list(frames)
        yaw_data_degree = yaw_to_degree(yaw_data_raw)
        yaw_data_degree = degree_delta(yaw_data_degree)
        yaw_degree_100ms = frames_yaw_to_100ms(yaw_data_degree)

        sudden_actions = check_sudden_action(gps_vss_100ms, yaw_degree_100ms)
        for i in range(len(sudden_actions)):
            sudden_actions[i] = check_continuous(sudden_actions[i])

        bool_sudden_actions = ['X', 'X', 'X', 'X', 'X']

        for i in range(len(sudden_actions)):
            bool_sudden_actions[i] = 'O' if sudden_actions[i] else 'X'

        json_data_list.append([json_name, gps_vss_acceleration, gps_vss_frame, gps_vss_100ms, sudden_actions, yaw_data_raw, yaw_data_degree, yaw_degree_100ms, bool_sudden_actions])
    print(f'scanning... {n_of_can}/{len(can_loc_list)}')

e2 = cv2.getTickCount()
Total_time = (e2 - e1)/ cv2.getTickFrequency()

print(f'Total time taken: {Total_time} seconds')
print(f'Total scanned number of can_data: {n_of_can} files')



save_graphs(json_data_list)


while True:
    user_input = input("\nEnter q to quit: ")
    if user_input.lower() == 'q':
        break