import os
import shutil

dh_vids = []
cm_vids = []
dh_imgs = []
cm_imgs = []
can_jsons = []
label_jsons = []

can_origin = 'G:/backup/can'
dh_origin = 'G:/backup/dh'
cm_origin = 'G:/backup/cm'
img_dh_origin = 'G:/backup/images_dh'
img_cm_origin = 'G:/backup/images_cm'
label_origin = 'G:/backup/labellings'

for i in os.listdir(can_origin):
    if i.split('.')[-1] == 'JSON' or i.split('.')[-1] == 'json':
        can_jsons.append([can_origin, i])

for i in os.listdir(dh_origin):
    if i.split('.')[-1] == 'mp4' or i.split('.')[-1] == 'MP4':
        dh_vids.append([dh_origin, i])

for i in os.listdir(cm_origin):
    if i.split('.')[-1] == 'mp4' or i.split('.')[-1] == 'MP4':
        cm_vids.append([cm_origin, i])

for i in os.listdir(img_dh_origin):
    if i.split('.')[-1] == 'jpg' or i.split('.')[-1] == 'JPG':
        dh_imgs.append([img_dh_origin, i])

for i in os.listdir(img_cm_origin):
    if i.split('.')[-1] == 'jpg' or i.split('.')[-1] == 'JPG':
        cm_imgs.append([img_cm_origin, i])

for i in os.listdir(label_origin):
    if i.split('.')[-1] == 'JSON' or i.split('.')[-1] == 'json':
        label_jsons.append([label_origin, i])


source_oa_des = 'G:/원천데이터_3300건/기타구간_OA/'
source_afa_des = 'G:/원천데이터_3300건/사고다발구간_AFA/'
source_ara_des = 'G:/원천데이터_3300건/사고위험구간_ARA/'
source_c2h_des = 'G:/원천데이터_3300건/차대사람및차대자전거_C2H/'
source_c2c_des = 'G:/원천데이터_3300건/차대차및차량단독_C2C/'

source_oa_des = 'G:/원천데이터_3300건/기타구간/'
source_afa_des = 'G:/원천데이터_3300건/사고다발구간/'
source_ara_des = 'G:/원천데이터_3300건/사고위험구간/'
source_c2h_des = 'G:/원천데이터_3300건/차대사람및차대자전거/'
source_c2c_des = 'G:/원천데이터_3300건/차대차및차량단독/'

label_oa_des = 'G:/라벨링데이터_3300건/기타구간_OA'
label_afa_des = 'G:/라벨링데이터_3300건/사고다발구간_AFA'
label_ara_des = 'G:/라벨링데이터_3300건/사고위험구간_ARA'
label_c2h_des = 'G:/라벨링데이터_3300건/차대사람및차대자전거_C2H'
label_c2c_des = 'G:/라벨링데이터_3300건/차대차및차량단독_C2C'

can_route = 'CAN 데이터'
dh_route = '운전자 운전행동'
cm_route = '주행 환경정보'
img_dh_route = '운전자 운전행동 이미지'
img_cm_route = '주행 환경정보 이미지'


source_dir_route = {
    'OA': source_oa_des,
    'AFA': source_afa_des,
    'ARA': source_ara_des,
    'C2H': source_c2h_des,
    'C2C': source_c2c_des
}

label_dir_route = {
    'OA': label_oa_des,
    'AFA': label_afa_des,
    'ARA': label_ara_des,
    'C2H': label_c2h_des,
    'C2C': label_c2c_des
}

route_1 = ['OA', 'AFA', 'ARA', 'C2H', 'C2C']
# dh_vids = []
# cm_vids = []
# dh_imgs = []
# cm_imgs = []
# can_jsons = []
# label_jsons = []

files_to_move = []

for i in dh_vids:
    destination = ''
    split_name = i[1].split('_')
    for j in split_name:
        if j in route_1:
            destination += source_dir_route[j]
            destination += dh_route
    files_to_move.append([i[0], i[1], destination, i[1]])

for i in cm_vids:
    destination = ''
    split_name = i[1].split('_')
    for j in split_name:
        if j in route_1:
            destination += source_dir_route[j]
            destination += cm_route
    files_to_move.append([i[0], i[1], destination, i[1]])

for i in dh_imgs:
    destination = ''
    split_name = i[1].split('_')
    for j in split_name:
        if j in route_1:
            destination += source_dir_route[j]
            destination += img_dh_route
    files_to_move.append([i[0], i[1], destination, i[1].split('.')[0] + '.JPG'])

for i in cm_imgs:
    destination = ''
    split_name = i[1].split('_')
    for j in split_name:
        if j in route_1:
            destination += source_dir_route[j]
            destination += img_cm_route
    files_to_move.append([i[0], i[1], destination, i[1].split('.')[0] + '.JPG'])

for i in can_jsons:
    destination = ''
    split_name = i[1].split('_')
    for j in split_name:
        if j in route_1:
            destination += source_dir_route[j]
            destination += can_route
    files_to_move.append([i[0], i[1], destination, i[1]])

for i in label_jsons:
    destination = ''
    split_name = i[1].split('_')
    for j in split_name:
        if j in route_1:
            destination += label_dir_route[j]
    files_to_move.append([i[0], i[1], destination, i[1]])


# for i in files_to_move:
#     print(i)

print(len(files_to_move))

# scan_cnt = 0
# for i in files_to_move:
#     scan_cnt += 1
#     shutil.move(f'{i[0]}/{i[1]}', f'{i[2]}/{i[3]}')
#     print(f'moving files...{scan_cnt}/{len(files_to_move)}')

