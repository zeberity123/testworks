import json
import os
import cv2
import matplotlib.pyplot as plt

json_root = '03259'
ex_json_list = os.listdir(json_root)[:-1]

new_json_root = '03259/degree_rotation_03259'

source_can_list = ex_json_list

def createDirectory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error: Failed to create the directory.")

# createDirectory('03259/rotation_03259')

'''
json_data_list[]

string: json_filename
list: gps_vss_acceleration
list: gps_vss_frame
list: gps_vss_100ms
'''
json_data_list = []

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

def frames_to_100ms(yaw_data_degree):
    yaw_degree_100ms = []
    total_100ms = len(yaw_data_degree) // 3
    for i in range(total_100ms):
        degree_in_100ms = sum(yaw_data_degree[i*3:(i+1)*3])/3
        yaw_degree_100ms.append(degree_in_100ms)

    return yaw_degree_100ms

        
def filename_only(filename):
    return filename.split('/')[-1]


def can_to_yaw_raw(json_data_list):
    createDirectory('03259/degree_rotation_03259')
    for i in json_data_list:
        dict = {}
        dict['yaw_data'] = {}
        for frameCnt in range(len(i[1][0])):
            dict['yaw_data'][f'{frameCnt}'] = f'yaw: {i[1][0][frameCnt]}, yawH: {i[1][1][frameCnt]}, yawL: {i[1][2][frameCnt]}'


        filename = filename_only(i[0])
        with open(f'{new_json_root}/yaw_{filename[:-5]}.JSON', 'w') as f:
            json.dump(dict, f, ensure_ascii=False, indent=4)

def can_to_yaw_degree(json_data_list):
    createDirectory('03259/degree_rotation_03259')
    for i in json_data_list:
        dict = {}
        dict['yaw_data'] = {}
        for frameCnt in range(len(i[2])):
            dict['yaw_data'][f'{frameCnt}'] = f'yaw_degree: {i[2][frameCnt]:.4f}'


        filename = filename_only(i[0])
        with open(f'{new_json_root}/frame_degree_{filename[:-5]}.JSON', 'w') as f:
            json.dump(dict, f, ensure_ascii=False, indent=4)

def can_to_yaw_degree_100ms(json_data_list):
    createDirectory('03259/degree_rotation_03259')
    for i in json_data_list:
        time = [0.0]
        time += [str(second/10) for second in range(1, len(i[2]))]
        dict = {}
        dict['yaw_data'] = {}
        for j in range(len(i[3])):
            dict['yaw_data'][f'{time[j]}'] = f'yaw_degree: {i[3][j]:.4f}'


        filename = filename_only(i[0])
        with open(f'{new_json_root}/100ms_degree_{filename[:-5]}.JSON', 'w') as f:
            json.dump(dict, f, ensure_ascii=False, indent=4)

n_of_can = 0
e1 = cv2.getTickCount()
for json_name in source_can_list:
    n_of_can += 1
    with open(f'{json_root}/{json_name}', 'r') as f:
        data = json.load(f)

        frames = data['frames']

        yaw_data_raw = yaw_to_list(frames)

        yaw_data_degree = yaw_to_degree(yaw_data_raw)

        yaw_degree_100ms = frames_to_100ms(yaw_data_degree)


        json_data_list.append([json_name, yaw_data_raw, yaw_data_degree, yaw_degree_100ms])
    print(f'scanning... {n_of_can}/{len(source_can_list)}')

e2 = cv2.getTickCount()
Total_time = (e2 - e1)/ cv2.getTickFrequency()

print(f'Total time taken: {Total_time} seconds')
print(f'Total scanned number of can_data: {n_of_can} files')




# can_to_yaw_raw(json_data_list)
# can_to_yaw_degree(json_data_list)
# can_to_yaw_degree_100ms(json_data_list)


time = [0.0]
time += [str(second/10) for second in range(1, len(json_data_list[0][3]))] 
x1 = time
x1 = [i for i in range(len(json_data_list[0][2]))]
yaw_degree_100ms = json_data_list[0][3]
yaw_degree_frame = json_data_list[0][2]

plt.figure(figsize=(13, 7))

plt.title('Yaw_degree', fontsize=16)
plt.plot(x1, yaw_degree_frame, linestyle='-', color='blue', linewidth=2)
plt.xlabel('Time (Seconds)', fontsize=14)
plt.ylabel('degree°', fontsize=14)

plt.grid(True, linestyle='--', linewidth=0.5)

# plt.xticks([i*100 for i in range(13)], [i*10 for i in range(13)])

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)

plt.tight_layout()
plt.show()