import cv2
import pandas as pd
import os

ann_loc_list = os.listdir('ann')
video_loc_list = os.listdir('source_data')

cols = ['filename', 'before', 'after', 'ext0', 'ext1']

ann_list = []

no_video = []

def parse_vid(video_name, row, before_sec, after_sec):
    print(f'video_name: {video_name}, row: {row}, before_sec: {before_sec}, after_sec: {after_sec}')



'''
ann_list
i = annotation.xlsx
filename_list = 2024_NIA_LAB_LAB_REAL_M_A2_AFA_RE_D_00291...
before_lsit = 34455...
after_list = 71156.038...
'''
for i in ann_loc_list:
    df = pd.read_excel(f'ann/{i}', engine='openpyxl', names=cols)
    filename_list = df['filename'].tolist()
    before_list = df['before'].tolist()
    after_list = df['after'].tolist()

    ann_list.append([i, filename_list, before_list, after_list])


# 영상파일과 엑셀 파일이 숫자5자리 기준으로 정렬되어있으면 더 빠름
for i in ann_list:
    n_of_files = len(i[1])
    for j in range(n_of_files):
        vid_file_num = i[1][j][-5:]
        for video_name in video_loc_list:
            # print('w')
            if vid_file_num in video_name:
                parse_vid(video_name, j, i[2][j], i[3][j])


# # 동영상 파일의 경로
# video_filename = '2024_NIA_CM_SOU_REAL_F_A2_ARA_NA_D_01689.MP4'
# video_path = f"source_data/{video_filename}"

# # 동영상 파일 열기
# video = cv2.VideoCapture(video_path)

# # 동영상의 프레임 수
# frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

# seconds = [500, 1200]

# e1 = cv2.getTickCount()
# cnt = 0
# # 프레임을 이미지로 변환하고 파일로 저장
# for i in range(frame_count):
#     ret, frame = video.read()
#     if i in seconds:
#         image_path = f'captured_img/{video_filename}_{i}.jpg'
#         cv2.imwrite(image_path, frame)
#         cnt += 1
#     if cnt == 2:
#         cnt = 0
#         break
# # 동영상 파일 닫기
# video.release()
# e2 = cv2.getTickCount()

# time = (e2 - e1)/ cv2.getTickFrequency()
# print(f'Time taken: {time} seconds')