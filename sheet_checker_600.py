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

# print(len(contain_list))

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

# for cm_img in cm_parsed:
#     shutil.copy(f'{img_cm_dir}/{cm_img}', f'{new_cm_dir}/{cm_img}')

# for dh_img in dh_parsed:
#     shutil.copy(f'{img_dh_dir}/{dh_img}', f'{new_dh_dir}/{dh_img}')


dups = ['00233', '01174', '01175', '01176', '01179', '01180', '01181', '01182', '01183', '01184', '01185', '01186', '01187', '00979', '00978', '00977', '00976', '00975', '00974', '00973', '00972', '00971', '00970', '00969', '00968', '00967', '00966', '00965', '00964', '00963', '00962', '00961', '00960', '00959', '00958', '00957', '00956', '00955', '00954', '00953', '00952']
# print(len(dups))
# print(cm_img_list)

# cm_parsed = []
# dh_parsed = []

cm_img_nums = [parse_img_num(i) for i in cm_parsed[::2]]
dh_img_nums = [parse_img_num(i) for i in dh_parsed[::2]]


dups_in_600 = []
for i in dups:
    if i in cm_img_nums:
        dups_in_600.append(i)

print(dups_in_600)