import cv2
import pandas as pd
import os
import shutil

ann_folder_name_600 = 'ann'
ann_folder_name_1806 = 'json_10_30'

img_cm_dir = '241030_images/frames/frames_cm'
img_dh_dir = '241030_images/frames/frames_dh'

cm_img_list = os.listdir(img_cm_dir)
dh_img_list = os.listdir(img_dh_dir)

ann_loc_list_600 = os.listdir(ann_folder_name_600)
ann_loc_list_1806 = os.listdir(ann_folder_name_1806)
cols_600 = ['num', 'filename']
cols_1806 = ['filename', 'before', 'after']



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

def annotation_to_list_600(ann_loc_list, ann_folder_name):
    for i in ann_loc_list:
        df = pd.read_excel(f'{ann_folder_name}/{i}', engine='openpyxl', sheet_name=2, names=cols_600)
        filename_list = df['filename'].tolist()
        video_nums = []
        for j in filename_list:
            video_nums.append(parse_video_num(j))
        # print(filename_list[0])
        # print(len(filename_list))

    return video_nums

def annotation_to_list_1806(ann_loc_list, ann_folder_name):
    for i in ann_loc_list:
        df = pd.read_excel(f'{ann_folder_name}/{i}', engine='openpyxl', names=cols_1806)
        filename_list = df['filename'].tolist()
        video_nums = []
        for j in filename_list:
            video_nums.append(parse_video_num(j))

    return video_nums

ann_list = []
vid_name_list = []
ann_600 = annotation_to_list_600(ann_loc_list_600, ann_folder_name_600)
ann_1806 = annotation_to_list_1806(ann_loc_list_1806, ann_folder_name_1806)

contain_list = []
for i in ann_600:
    if i in ann_1806:
        contain_list.append(i)

print(len(contain_list))

cm_parsed = []
dh_parsed = []

for cm_img in cm_img_list:
    for vid_num in ann_600:
        if vid_num in cm_img:
            cm_parsed.append(cm_img)

for dh_img in dh_img_list:
    for vid_num in ann_600:
        if vid_num in dh_img:
            dh_parsed.append(dh_img)

# print(len(cm_parsed))
# print(dh_parsed)
# print(len(dh_parsed))
new_cm_dir = '241030_600/frames/frames_cm'
new_dh_dir = '241030_600/frames/frames_dh'

for cm_img in cm_parsed:
    shutil.copy(f'{img_cm_dir}/{cm_img}', f'{new_cm_dir}/{cm_img}')

for dh_img in dh_parsed:
    shutil.copy(f'{img_dh_dir}/{dh_img}', f'{new_dh_dir}/{dh_img}')