import os
import shutil

labellings_root = 'backup_json3300_241127'
labelling_files = os.listdir(labellings_root)

test_label_root = 'G:/datasets/test_labelings'
val_label_root = 'G:/datasets/val_labelings'

data_folder_names = {
    'CAN 데이터': '5. CAN',
    '운전자 운전행동': '1. DH',
    '운전자 운전행동 이미지': '3. DH_images',
    '주행 환경정보': '2. CM',
    '주행 환경정보 이미지': '4. CM_images'
}

files_origin_root = 'G:/원천데이터_3300건_backup'
dh_origin_root = 'G:/원천데이터_3300건_backup/운전자 운전행동 이미지'
cm_origin_root = 'G:/원천데이터_3300건_backup/주행 환경정보 이미지'

origin_folders_list = os.listdir(files_origin_root)

dh_img_list = os.listdir(dh_origin_root)
cm_img_list = os.listdir(cm_origin_root)

new_test_root = 'G:/NIA_dataset_3300/test/원천데이터'
new_val_root = 'G:/NIA_dataset_3300/val/원천데이터'
new_train_root = 'G:/NIA_dataset_3300/train/원천데이터'

num_3300 = [i[-10:-5] for i in labelling_files]
num_test = [i[-10:-5] for i in os.listdir(test_label_root)]
num_val = [i[-10:-5] for i in os.listdir(val_label_root)]

def copy_to_dest(filename, origin_root, dest_train_test_val, type_dest):
    # print(f'{origin_root}/{filename}', f'{dest_train_test_val}/{type_dest}/{filename}')
    shutil.move(f'{origin_root}/{filename}', f'{dest_train_test_val}/{type_dest}/{filename}')

def check_ttv(filename):
    # file_num = filename.split('.')[0][-5:]
    file_num = filename.split('_')[-2][-5:]

    if file_num in num_test:
        return new_test_root
    
    elif file_num in num_val:
        return new_val_root
    
    else:
        return new_train_root

# cnt = 0
# for folder in origin_folders_list:
#     risky_type_list = os.listdir(f'{files_origin_root}/{folder}')
#     for file_type in risky_type_list:
#         type_dest = data_folder_names[file_type]
#         for filename in os.listdir(f'{files_origin_root}/{folder}/{file_type}'):
#             dest_train_test_val = check_ttv(filename)
#             origin_root = f'{files_origin_root}/{folder}/{file_type}'
#             cnt += 1
#             print(f'copying...{cnt}/23100     {filename}')
#             copy_to_dest(filename, origin_root, dest_train_test_val, type_dest)

for img in dh_img_list:
    dest_train_test_val = check_ttv(img)
    copy_to_dest(img, dh_origin_root, dest_train_test_val, '운전자 운전행동 이미지')

for img in cm_img_list:
    dest_train_test_val = check_ttv(img)
    copy_to_dest(img, cm_origin_root, dest_train_test_val, '주행 환경정보 이미지')


