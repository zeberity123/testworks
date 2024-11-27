import os
import shutil

labellings_root = 'backup_json3300_241127'
labelling_files = os.listdir(labellings_root)

test_label_root = 'G:/datasets/test_labelings'
val_label_root = 'G:/datasets/val_labelings'

new_test_root = 'G:/NIA_dataset_3300/test/라벨링데이터'
new_val_root = 'G:/NIA_dataset_3300/val/라벨링데이터'
new_train_root = 'G:/NIA_dataset_3300/train/라벨링데이터'

num_3300 = [i[-10:-5] for i in labelling_files]
num_test = [i[-10:-5] for i in os.listdir(test_label_root)]
num_val = [i[-10:-5] for i in os.listdir(val_label_root)]

def copy_to_dest(file_name, dest_root):
    shutil.copy(f'{labellings_root}/{file_name}', f'{dest_root}/{file_name}')

cnt = 0
for i in labelling_files:
    cnt += 1
    if i[-10:-5] in num_test:
        copy_to_dest(i, new_test_root)
    
    elif i[-10:-5] in num_val:
        copy_to_dest(i, new_val_root)
    
    else:
        copy_to_dest(i, new_train_root)

    print(f'copying files...{cnt}/{len(labelling_files)}')