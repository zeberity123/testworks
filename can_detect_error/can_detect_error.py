import json
import os
import cv2

json_root = './'
can_loc_list = []

for i in os.listdir(json_root):
    if i.split('.')[-1] == 'JSON' or i.split('.')[-1] == 'json':
        can_loc_list.append(i)

json_data_list = []

def second_to_list(frames):
    gps_seconds = []
    frameCnts = []
    for frame in frames:
        gps_second = frame['aim_micom']['gps_second']
        gps_seconds.append(int(gps_second))
        frameCnt = frame['frameCnt']
        frameCnts.append(f'"{frameCnt}"')
    
    return gps_seconds, frameCnts

def has_time_error(gps_seconds, frameCnts):
    current_second = gps_seconds[0]
    for i in range(1, len(gps_seconds)):
        if (gps_seconds[i] - current_second) not in [0, 1, -59]:
            return [True, frameCnts[i]]
        current_second = gps_seconds[i]

    return [False, -1]

def check_errors(json_data_list):
    has_errors = []
    for json in json_data_list:
        time_error = has_time_error(json[1], json[2])
        if time_error[0]:
            has_errors.append([json, time_error])

    return has_errors
        
def print_error_list(error_json_list):
    if error_json_list:
        print(f'\nErrors in: ')
        for json in error_json_list:
            print(f'{json[0][0]}: frameCnt[{json[1][1]}]')
    else:
        print('No error detected')



def filename_only(filename):
    return filename.split('/')[-1]

n_of_can = 0
e1 = cv2.getTickCount()
for json_name in can_loc_list:
    n_of_can += 1
    with open(json_name, 'r') as f:
        data = json.load(f)

        frames = data['frames']

        gps_seconds, frameCnts = second_to_list(frames)

        json_data_list.append([json_name, gps_seconds, frameCnts])

    print(f'scanning... {n_of_can}/{len(can_loc_list)}')

e2 = cv2.getTickCount()
Total_time = (e2 - e1)/ cv2.getTickFrequency()

print(f'Total time taken: {Total_time} seconds')
print(f'Total scanned number of can_data: {n_of_can} files')

error_json_list = check_errors(json_data_list)

print_error_list(error_json_list)

while True:
    user_input = input("\nEnter q to quit: ")
    if user_input.lower() == 'q':
        break

