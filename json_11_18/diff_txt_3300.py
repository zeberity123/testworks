import cv2
import pandas as pd
import os
import shutil

json_folder_name = 'G:/DATA_ALL_3205건_1110까지/3. CAN'
source_vids_folder_name = 'G:/'

json_list = []

for i in os.listdir(json_folder_name):
    if i.split('.')[-1] == 'JSON' or i.split('.')[-1] == 'json':
        json_list.append(i)

video_loc_list = os.listdir(source_vids_folder_name)

def get_vids_list_source(video_loc_list):
    source_vids_list_dh = []
    source_vids_list_cm = []

    for i in video_loc_list:
        if 'DATA_' in i[:5]:
            loc_to_source = f'{source_vids_folder_name}/{i}'
            for dh in os.listdir(f'{loc_to_source}/1. DH'):
                source_vids_list_dh.append(f'{dh}')
            for cm in os.listdir(f'{loc_to_source}/2. CM'):
                source_vids_list_cm.append(f'{cm}')

    return source_vids_list_dh, source_vids_list_cm

def filename_only(filename):
    return filename.split('/')[-1]

def vid_num_only(source_vids_list):
    vids_num_list = []
    for vid in source_vids_list:
        vids_num_list.append(vid.split('.')[0][-5:])
    return vids_num_list

def parse_video_num(video_name):
    if video_name[-4:] == '.MP4':
        # print(f'mp44444, {video_name[-9:-4]}')
        return video_name[-9:-4]
    elif video_name[-4:] == 'JSON':
        # print(f'jsonnnn, {video_name[-10:-5]}')
        return video_name[-10:-5]
    else:
        # print(video_name[-5:])
        return video_name[-5:]

def txt_to_list(txt_filename):
    parse_txt = txt_filename
    f = open(parse_txt, "r")
    txt_json_list = []
    while True:
        line = f.readline().strip()
        if not line: break
        txt_json_list.append(parse_video_num(line))

    return txt_json_list

source_vids_list_dh, source_vids_list_cm = get_vids_list_source(video_loc_list)
source_vids_num_list_dh = vid_num_only(source_vids_list_dh)
source_vids_num_list_cm = vid_num_only(source_vids_list_cm)

txt_file_list =  txt_to_list('3300_filelist.txt')

not_in_txt = []
for i in source_vids_num_list_dh:
    if i not in txt_file_list:
        not_in_txt.append(i)

# print(not_in_txt, len(not_in_txt))


cm_parsed = []
dh_parsed = []
json_parsed = []

for cm_vid in source_vids_list_cm:
    for vid_num in not_in_txt:
        if vid_num in cm_vid:
            cm_parsed.append(cm_vid)

for dh_vid in source_vids_list_dh:
    for vid_num in not_in_txt:
        if vid_num in dh_vid:
            dh_parsed.append(dh_vid)

for json_file in json_list:
    for vid_num in not_in_txt:
        if vid_num in json_file:
            json_parsed.append(json_file)

# print(json_parsed)
# print(len(cm_parsed))
# print(cm_parsed[:10])
# print(len(dh_parsed))
new_cm_dir = 'G:/DATA_ALL_3205건_1110까지/etc_58/2. CM'
new_dh_dir = 'G:/DATA_ALL_3205건_1110까지/etc_58/1. DH'
new_json_dir = 'G:/DATA_ALL_3205건_1110까지/etc_58/3. CAN'
vid_cm_dir = 'G:/DATA_ALL_3205건_1110까지/2. CM'
vid_dh_dir = 'G:/DATA_ALL_3205건_1110까지/1. DH'
old_json_dir = 'G:/DATA_ALL_3205건_1110까지/3. CAN'


scan_cnt = 0
for cm_vid in cm_parsed:
    scan_cnt += 1
    shutil.move(f'{vid_cm_dir}/{cm_vid}', f'{new_cm_dir}/{cm_vid}')
    print(f'scanning...{scan_cnt}/{len(not_in_txt)}')

scan_cnt = 0
for dh_vid in dh_parsed:
    scan_cnt += 1
    shutil.move(f'{vid_dh_dir}/{dh_vid}', f'{new_dh_dir}/{dh_vid}')
    print(f'copying...{scan_cnt}/{len(not_in_txt)}')

scan_cnt = 0
for json_file in json_parsed:
    scan_cnt += 1
    shutil.move(f'{old_json_dir}/{json_file}', f'{new_json_dir}/{json_file}')
    print(f'moving...{scan_cnt}/{len(not_in_txt)}')