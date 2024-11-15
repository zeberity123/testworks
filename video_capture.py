import cv2
import pandas as pd
import os

ann_folder_name = 'json_11_15'
source_vids_folder_name = 'G:/'

ann_loc_list = os.listdir(ann_folder_name)
video_loc_list = os.listdir(source_vids_folder_name)

def get_vids_list_source(video_loc_list):
    source_vids_list = []
    for i in video_loc_list:
        if 'DATA_' in i[:5]:
            loc_to_source = f'{source_vids_folder_name}/{i}'
            for dh in os.listdir(f'{loc_to_source}/1. DH'):
                source_vids_list.append(f'{loc_to_source}/1. DH/{dh}')
            for cm in os.listdir(f'{loc_to_source}/2. CM'):
                source_vids_list.append(f'{loc_to_source}/2. CM/{cm}')

    return source_vids_list



source_vids_list = get_vids_list_source(video_loc_list)

cols = ['filename', 'before', 'after']

ann_list = []

no_video = []

'''
ann_list
i = annotation.xlsx
filename_list = 2024_NIA_LAB_LAB_REAL_M_A2_AFA_RE_D_00291...
before_list = 34455...
after_list = 71156.038...
'''
def annotation_to_list(ann_loc_list, ann_list):
    for i in ann_loc_list:
        df = pd.read_excel(f'{ann_folder_name}/{i}', engine='openpyxl', names=cols)
        filename_list = df['filename'].tolist()
        before_list = df['before'].tolist()
        after_list = df['after'].tolist()

        ann_list.append([i, filename_list, before_list, after_list])

def parse_ann_list(ann_list):
    parse_txt = 'parse_txt_excel/filelist_2800.txt'
    f = open(parse_txt, "r")
    txt_json_list = []
    while True:
        line = f.readline().strip()
        if not line: break
        txt_json_list.append(parse_video_num(line))

    
    ann_len = len(ann_list[0][1])
    fefa = []
    # print(ann_list[0][1][3:6])
    only_num_list = [parse_video_num(i) for i in ann_list[0][1]][3:]
    only_num_list = txt_json_list

    # for i in range(ann_len):
    #     if parse_video_num(ann_list[0][1][i]) in txt_json_list:
    #         fefa.append(ann_list[0][1][i])

    # print(len(fefa))

    no_dup = list(set(only_num_list))
    # diffs = list(set(only_num_list) - set(no_dup))
    # diffs = list(no_dup - only_num_list)

    # x = [] # 처음 등장한 값인지 판별하는 리스트
    no_dup = []
    dups = [] # 중복된 원소만 넣는 리스트

    for i in only_num_list:
        if i not in no_dup: # 처음 등장한 원소
            no_dup.append(i)
        else:
            if i not in dups: # 이미 중복 원소로 판정된 경우는 제외
                dups.append(i)


    print((dups)) # [1, 2] # 2회 이상 등장한 값들만 담긴 리스트


def parse_video_num(video_name):
    if video_name[-4:] == '.MP4':
        # print(f'mp44444, {video_name[-9:-4]}')
        return video_name[-9:-4]
    elif video_name[-4:] == 'JSON':
        # print(f'jsonnnn, {video_name[-10:-5]}')
        return video_name[-10:-5]
    elif video_name[-4:] == '.mp4':
        return 'nonamegiven'
    else:
        # print(video_name[-5:])
        return video_name[-5:]

# 영상파일과 엑셀 파일이 숫자5자리 기준으로 정렬되어있으면 더 빠를 것 같음
def parse_vids(ann_list):
    n_of_parsed_img = 0
    e1 = cv2.getTickCount()
    for i in ann_list:
        start_num = 1
        n_of_files = len(i[1])
        for j in range(n_of_files):
        # for j in range(143, 144):
            print(f'parsing... {start_num}/{n_of_files}')
            vid_file_num = parse_video_num(i[1][j])
            # print(f'vid_filenum = {vid_file_num}')

            for video_name in source_vids_list:
                if vid_file_num in video_name:
                    e2 = cv2.getTickCount()
                    parse_vid(video_name, i[2][j], i[3][j])
                    e3 = cv2.getTickCount()
                    time = (e3 - e2)/ cv2.getTickFrequency()
                    # print(f'Time taken: {time} seconds')
                    n_of_parsed_img += 1
            
            start_num += 1
    
    e4 = cv2.getTickCount()

    Total_time = (e4 - e1)/ cv2.getTickFrequency()
    print(f'Total time taken: {Total_time} seconds')
    print(f'Total number of parsed images(pairs): {n_of_parsed_img} pairs')


def seconds_to_frame(second):
    return int(float(second) * 0.03)


def parse_vid(video_name, before_sec, after_sec):
    # print(f'video_name: {video_name}, row: {row}, before_sec: {before_sec}, after_sec: {after_sec}')

    # 동영상 파일의 경로
    # video_path = f"{source_vids_folder_name}/{video_name}"
    video_path = video_name
    video_name = video_path.split("/")[-1]

    # 동영상 파일 열기
    video = cv2.VideoCapture(video_path)

    # 동영상의 프레임 수
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    before_frame = seconds_to_frame(before_sec)
    after_frame = seconds_to_frame(after_sec)

    seconds = [before_frame, after_frame]


    # print(video_name)
    # 프레임을 이미지로 변환하고 파일로 저장

    cnt = 0
    for second in seconds:
        video.set(cv2.CAP_PROP_POS_FRAMES, second)
        ret, frame = video.read()
        if cnt == 0:
            image_path = f'241115_images/frames/{"frames_cm" if "CM" in video_name else "frames_dh"}/{video_name[:-4]}_Pre.jpg'
            cv2.imwrite(image_path, frame)
            # print(video_name, second)
        else:
            image_path = f'241115_images/frames/{"frames_cm" if "CM" in video_name else "frames_dh"}/{video_name[:-4]}_Post.jpg'
            cv2.imwrite(image_path, frame)
            # print(video_name, second)
        cnt += 1

    # 동영상 파일 닫기
    video.release()



annotation_to_list(ann_loc_list, ann_list)

# parse_ann_list(ann_list)
# print(ann_list[0][1][3:])
# print(ann_list[0][2][3:5])
# print(ann_list[0][3][3:5])

parse_vids(ann_list)