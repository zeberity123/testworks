import cv2
import pandas as pd
import os
import shutil

ann_folder_name_1806 = 'json_10_30'

img_cm_dir = '241030_images/frames/frames_cm'
img_dh_dir = '241030_images/frames/frames_dh'

cm_img_list = os.listdir(img_cm_dir)
dh_img_list = os.listdir(img_dh_dir)

ann_loc_list_1806 = os.listdir(ann_folder_name_1806)

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


def annotation_to_list_1806(ann_loc_list, ann_folder_name):
    for i in ann_loc_list:
        df = pd.read_excel(f'{ann_folder_name}/{i}', engine='openpyxl', names=cols_1806)
        filename_list = df['filename'].tolist()
        video_nums = []
        for j in filename_list:
            video_nums.append(parse_video_num(j))

    return video_nums

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


ann_list = []
vid_name_list = []
ann_1806 = annotation_to_list_1806(ann_loc_list_1806, ann_folder_name_1806)
'''
'''
# cm_parsed = []
# cm_not_parsed = []
# dh_parsed = []

# cm_img_nums = [parse_img_num(i) for i in cm_img_list[::2]]
# dh_img_nums = [parse_img_num(i) for i in dh_img_list[::2]]

# for vid_num in ann_1806:
#     for cm_num in cm_img_nums:
#         if vid_num == cm_num:
#             cm_parsed.append(cm_num)

# diffs = list(set(ann_1806) - set(cm_parsed))
# print(diffs)
'''
'''
only_num_list = ann_1806[2:]
no_dup = list(set(only_num_list))
# diffs = list(set(only_num_list) - set(no_dup))
# diffs = list(no_dup - only_num_list)

# x = [] # 처음 등장한 값인지 판별하는 리스트
no_dup = []
diffs = [] # 중복된 원소만 넣는 리스트

for i in only_num_list:
    if i not in no_dup: # 처음 등장한 원소
        no_dup.append(i)
    else:
        if i not in diffs: # 이미 중복 원소로 판정된 경우는 제외
            diffs.append(i)

print(len(diffs)) # [1, 2] # 2회 이상 등장한 값들만 담긴 리스트

'''
'''
# for cm_img in cm_img_list:
#     for vid_num in ann_600:
#         if vid_num in cm_img:
#             cm_parsed.append(cm_img)

# for dh_img in dh_img_list:
#     for vid_num in ann_600:
#         if vid_num in dh_img:
#             dh_parsed.append(dh_img)

# print(len(cm_parsed))
# print(dh_parsed)
# print(len(dh_parsed))
# new_cm_dir = '241030_600/frames/frames_cm'
# new_dh_dir = '241030_600/frames/frames_dh'

# for cm_img in cm_parsed:
#     shutil.copy(f'{img_cm_dir}/{cm_img}', f'{new_cm_dir}/{cm_img}')

# for dh_img in dh_parsed:
#     shutil.copy(f'{img_dh_dir}/{dh_img}', f'{new_dh_dir}/{dh_img}')