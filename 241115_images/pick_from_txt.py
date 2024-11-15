import cv2
import pandas as pd
import os
import shutil


img_cm_dir = 'frames/frames_cm'
img_dh_dir = 'frames/frames_dh'

cm_img_list = os.listdir(img_cm_dir)
dh_img_list = os.listdir(img_dh_dir)


def txt_to_list(txt_filename):
    parse_txt = txt_filename
    f = open(parse_txt, "r")
    txt_json_list = []
    while True:
        line = f.readline().strip()
        if not line: break
        txt_json_list.append(parse_video_num(line))

    return txt_json_list


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


def parse_img_num(img_name):
    if img_name[-5:] == 'e.jpg':
        # print(f'mp44444, {video_name[-9:-4]}')
        return img_name[-16:-11]
    elif img_name[-5:] == 'r.jpg':
        # print(f'jsonnnn, {video_name[-10:-5]}')
        return img_name[-15:-10]
    else:
        # print(video_name[-5:])
        return img_name[-5:]


txt_file_list =  txt_to_list('filelist_2800.txt')

print(len(txt_file_list))

cm_parsed = []
dh_parsed = []

for cm_img in cm_img_list:
    for vid_num in txt_file_list:
        if vid_num in cm_img:
            cm_parsed.append(cm_img)

for dh_img in dh_img_list:
    for vid_num in txt_file_list:
        if vid_num in dh_img:
            dh_parsed.append(dh_img)

print(len(cm_parsed))
# print(cm_parsed[:10])
# # print(len(dh_parsed))
new_cm_dir = 'frame_2800/frames/frames_cm'
new_dh_dir = 'frame_2800/frames/frames_dh'

scan_cnt = 0
for cm_img in cm_parsed:
    scan_cnt += 1
    shutil.copy(f'{img_cm_dir}/{cm_img}', f'{new_cm_dir}/{cm_img}')
    print(f'scanning...{scan_cnt}/{len(txt_file_list)*2}')

scan_cnt = 0
for dh_img in dh_parsed:
    scan_cnt += 1
    shutil.copy(f'{img_dh_dir}/{dh_img}', f'{new_dh_dir}/{dh_img}')
    print(f'copying...{scan_cnt}/{len(txt_file_list)*2}')


# dups = ['00233', '01174', '01175', '01176', '01179', '01180', '01181', '01182', '01183', '01184', '01185', '01186', '01187', '00979', '00978', '00977', '00976', '00975', '00974', '00973', '00972', '00971', '00970', '00969', '00968', '00967', '00966', '00965', '00964', '00963', '00962', '00961', '00960', '00959', '00958', '00957', '00956', '00955', '00954', '00953', '00952']
# print(len(dups))
# print(cm_img_list)

# cm_parsed = []
# dh_parsed = []

# cm_img_nums = [parse_img_num(i) for i in cm_parsed[::2]]
# dh_img_nums = [parse_img_num(i) for i in dh_parsed[::2]]