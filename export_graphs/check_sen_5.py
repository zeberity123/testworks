import pandas as pd
import os
import json

meta_excel = 'newnew_metadata.xlsx'
labellings_root = 'backup_json3300_241127'
labelling_files = os.listdir(labellings_root)
new_labellings_root = 'new_3300_json'

error_in_sen_5 = []

def check_sen_5(label_file):
    with open(f'{labellings_root}/{label_file}', 'r') as f:
        label_data = json.load(f)
        sen_5 = label_data['labeling']['SEN_5']
        case_1 = '위험 상황'
        case_2 = '위험상황'
        case_3 = '위험 구간'
        # case_4 = '위험구간'

        if case_1 in sen_5 or case_2 in sen_5 or case_3 in sen_5:
            error_in_sen_5.append([label_file, sen_5])
cnt = 0

for file in labelling_files:
    cnt += 1
    check_sen_5(file)

    print(f'searching...{cnt}/{len(labelling_files)}')

# for i in error_in_sen_5:
#     print(i)

print(len(error_in_sen_5))

# sen = "위험 구간 전에는 운전자의 눈은 왼쪽을 보고 있고, 손은 핸들을 조작하고 있으며, 주행 차량은 곡선 도로에서 주행하고 있고, 앞차는 없다. 날씨는 맑고, 도로 포장 상태는 건조하다. 위험구간 후에는 운전자의 눈은 정면을 보고 있고, 손은 핸들을 조작하고 있으며, 주행 차량은 직진하고 있고, 전방에는 사람이 있다. 날씨는 맑은 상태이고, 도로 포장 상태는 건조한 상태를 유지하고 있다. 차는 급감속 한 적이 있다."
# print('위험 구간' in sen)
