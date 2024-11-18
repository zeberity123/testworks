import cv2
import pandas as pd
import os

ann_folder_name = 'json_11_18'
source_vids_folder_name = 'G:/'

ann_loc_list = []

for i in os.listdir(ann_folder_name):
    if i.split('.')[-1] == 'JSON' or i.split('.')[-1] == 'json':
        ann_loc_list.append(i)

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
source_vids_list_dh = vid_num_only(source_vids_list_dh)
source_vids_list_cm = vid_num_only(source_vids_list_cm)

# source_vids_list_dh.sort()
# source_vids_list_cm.sort()

# print(source_vids_list_dh[:15])
# print(source_vids_list_cm[:15])
# print(source_vids_list_dh == source_vids_list_cm)

txt_file_list =  txt_to_list('json_11_18/3300_filelist.txt')

not_in_txt = []
for i in source_vids_list_dh:
    if i not in txt_file_list:
        not_in_txt.append(i)

print(not_in_txt, len(not_in_txt))