import os
import shutil

can_folder_name = 'H:/DATA_ALL_3205건_1110까지/3. CAN'
dh_folder_name = 'H:/DATA_ALL_3205건_1110까지/1. DH'
cm_folder_name = 'H:/DATA_ALL_3205건_1110까지/2. CM'

# labelling_folder_name = 'G:/DATA_ALL_3205건_1110까지/241115_model_2800/3. labelings'

can_list = []
dh_list = []
cm_list = []
# labelling_list = []

for i in os.listdir(can_folder_name):
    if i.split('.')[-1] == 'JSON' or i.split('.')[-1] == 'json':
        can_list.append(i)

for i in os.listdir(dh_folder_name):
    if i.split('.')[-1] == 'mp4' or i.split('.')[-1] == 'MP4':
        dh_list.append(i)

for i in os.listdir(cm_folder_name):
    if i.split('.')[-1] == 'mp4' or i.split('.')[-1] == 'MP4':
        cm_list.append(i)

# for i in os.listdir(labelling_folder_name):
#     if i.split('.')[-1] == 'JSON' or i.split('.')[-1] == 'json':
#         labelling_list.append(i)


def filename_only(filename):
    return filename.split('/')[-1]

def vid_num_only(source_vids_list):
    vids_num_list = []
    for vid in source_vids_list:
        vids_num_list.append(vid.split('.')[0][-5:])
    return vids_num_list

def parse_video_num(video_name):
    if video_name[-4:] == '.MP4' or video_name[-4:] == '.mp4':
        # print(f'mp44444, {video_name[-9:-4]}')
        return video_name[-9:-4]
    elif video_name[-4:] == 'JSON' or video_name[-4:] == 'json':
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

def parse_num_d_n(filename):
    return filename[-12:-5]
    # return filename[-10:-5]


diff = []
diff_dh = []
diff_cm = []

new_dh_list = []
new_cm_list = []

not_in_can = []
for i in dh_list:
    vid_num = parse_video_num(i)
    for labels in can_list:
        if vid_num in labels:
            new_dh_name = i[:-11] + labels[-12:-5] + '.MP4'
            new_dh_list.append(new_dh_name)

for i in cm_list:
    vid_num = parse_video_num(i)
    for labels in can_list:
        if vid_num in labels:
            new_cm_name = i[:-11] + labels[-12:-5] + '.MP4'
            new_cm_list.append(new_cm_name)

print(len(new_dh_list), len(new_cm_list))

for i in range(len(dh_list)):
    if dh_list[i] != new_dh_list[i]:
        diff_dh.append([dh_list[i], new_dh_list[i], i])

for i in range(len(cm_list)):
    if cm_list[i] != new_cm_list[i]:
        diff_cm.append([cm_list[i], new_cm_list[i], i])

print(len(diff_dh))
print(len(diff_cm))
# for i in diff_dh:
#     print(i)

# for i in range(len(dh_list)):
#     if dh_list[i] != new_dh_list[i]:
#         # print(can_list[i], new_can_list[i], i)
#         diff.append([can_list[i], new_dh_list[i], i])


# for i in old_can_list:
#     vid_num = parse_video_num(i)
#     for labels in labelling_list:
#         if vid_num in labels:
#             new_can_name = i[:-12] + labels[-12:-5] + '.JSON'
#             new_can_list.append(new_can_name)


# for i in range(len(can_list)):
#     if can_list[i] != new_can_list[i]:
#         # print(can_list[i], new_can_list[i], i)
#         diff.append([can_list[i], new_can_list[i], i])

# for i in diff:
#     print(i)

# print(len(diff))

temp_name = 'H:/DATA_ALL_3205건_1110까지/4. temp'
# scan_cnt = 0
# for i in diff_dh:
#     scan_cnt += 1
#     shutil.move(f'{dh_folder_name}/{i[0]}', f'{temp_name}/{i[1]}')
#     print(f'scanning...{scan_cnt}/{len(diff_dh)}')

scan_cnt = 0
for i in diff_cm:
    scan_cnt += 1
    shutil.move(f'{cm_folder_name}/{i[0]}', f'{temp_name}/{i[1]}')
    print(f'scanning...{scan_cnt}/{len(diff_cm)}')

# scan_cnt = 0
# for dh_vid in dh_parsed:
#     scan_cnt += 1
#     shutil.copy(f'{vid_dh_dir}/{dh_vid}', f'{new_dh_dir}/{dh_vid}')
#     print(f'copying...{scan_cnt}/{len(not_in_txt)}')

# scan_cnt = 0
# for json_file in json_parsed:
#     scan_cnt += 1
#     shutil.copy(f'{old_json_dir}/{json_file}', f'{new_json_dir}/{json_file}')
#     print(f'moving...{scan_cnt}/{len(not_in_txt)}')

# scan_cnt = 0
# for json_file in labelling_parsed:
#     scan_cnt += 1
#     shutil.copy(f'{old_labelling_dir}/{json_file}', f'{new_labelling_dir}/{json_file}')
#     print(f'moving...{scan_cnt}/{len(not_in_txt)}')

