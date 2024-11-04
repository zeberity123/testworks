import json
import cv2

source_can_list = ['2024_NIA_CAN_SOU_REAL_M_A2_AFA_RE_D_00169.JSON']

# json_data_list[] 구조
'''
json_data_list[]:
    string: json_filename - 파일이름
    list: gps_vss_seconds - 초당 평균 속도
    list: gps_vss_acceleration - 초당 가속도
    list: gps_vss_frame - 1프레임 당 속도 (json 내 raw data)
    list: gps_vss_100ms - 0.1초당 속도 (3프레임)
    list: sudden_actions - 이상행동 리스트[급가속:list, 급감속:list, 급정지:list, 급출발list]
    list: box_sudden_actions - 이상행동 유무 [급가속O/X, 급감속O/X, 급정지O/X, 급출발O/X]
'''
json_data_list = []

# json에서 속도값 추출 후 프레임 당 속도 기록
def vss_to_list(frames):
    gps_vss_frame = []
    for frame in frames:
        gps_vss = frame['aim_micom']['gps_vss']  # Extract VSS from each frame
        gps_vss_frame.append(int(gps_vss))
    
    return gps_vss_frame

# 프레임당 속도를 초당 속도로 변환
def frames_to_seconds(gps_vss_frame):
    gps_vss_seconds = []
    total_seconds = len(gps_vss_frame) // 30  # 1초당 30프레임
    for i in range(total_seconds):
        vss_in_second = sum(gps_vss_frame[i*30:(i+1)*30]) // 30  # 30프레임의 속도 평균
        gps_vss_seconds.append(vss_in_second)
    
    return gps_vss_seconds

# 프레임당 속도를 0.1초당 속도로 변환
def frames_to_100ms(gps_vss_frame):
    gps_vss_100ms = []
    total_100ms = len(gps_vss_frame) // 3  # 0.1초당 3프레임
    for i in range(total_100ms):
        vss_in_100ms = sum(gps_vss_frame[i*3:(i+1)*3]) // 3  # 3프레임의 속도 평균
        gps_vss_100ms.append(vss_in_100ms)

    return gps_vss_100ms

# 가속도 구하기
def vss_to_acceleration(gps_vss_seconds):
    gps_vss_acceleration = []
    for i in range(len(gps_vss_seconds) - 1):
        acceleration = gps_vss_seconds[i+1] - gps_vss_seconds[i] # 속도 변화량
        gps_vss_acceleration.append(acceleration)

    return gps_vss_acceleration

# 이상운전행동 체크 (0.1초 단위)
def check_sudden_action(data_vss_100ms):
    sudden_acc = []  # Sudden acceleration
    sudden_dec = []  # Sudden deceleration
    sudden_start = []  # Sudden start
    sudden_stop = []  # Sudden stop

    for i in range(len(data_vss_100ms)):
        ms_100 = data_vss_100ms[i:i+10]  # 1초내(0.1)초 * 10 유무 확인

        min_vss = min(ms_100)
        min_index = ms_100.index(min_vss)
        max_vss = max(ms_100)
        max_index = ms_100.index(max_vss)

        # 급정지, 급출발
        if min_vss <= 5 and (max_vss - min_vss) >= 10:
            if min_index < max_index:
                sudden_start.append([i/10, f'VSS:{min_vss}~{max_vss}'])
            else:
                sudden_stop.append([i/10, f'VSS:{max_vss}~{min_vss}'])

        # 급가속, 급감속
        if min_vss >= 6 and (max_vss - min_vss) >= 15:
            if min_index < max_index:
                sudden_acc.append([i/10, f'VSS:{min_vss}~{max_vss}'])
            else:
                sudden_dec.append([i/10, f'VSS:{max_vss}~{min_vss}'])

    return [sudden_acc, sudden_dec, sudden_stop, sudden_start]

# 이상운전행동이 검출된 파일의 이름과 박스 출력
def print_any_sudden_actions(json_data_list):
    for can_json in json_data_list:
        print(f'{can_json[0]}: {can_json[6]}')

# json 파일 스캔
def scan_json(source_can_list):
    n_of_can = 0
    e1 = cv2.getTickCount()  # 시작시간
    for json_name in source_can_list:
        n_of_can += 1
        with open(f'{json_name}', 'r') as f:
            data = json.load(f)
            frames = data['frames']
            gps_vss_frame = vss_to_list(frames)  # 프레임당 속도
            gps_vss_seconds = frames_to_seconds(gps_vss_frame)  # 초당 속도
            gps_vss_100ms = frames_to_100ms(gps_vss_frame)  # 0.1초당 속도
            gps_vss_acceleration = vss_to_acceleration(gps_vss_seconds)  # 초당 가속도
            
            sudden_actions = check_sudden_action(gps_vss_100ms)  # 이상운전행동 체크

            # 이상운전행동 박스 기본값
            box_sudden_actions = ['X', 'X', 'X', 'X']
            for i in range(len(sudden_actions)):
                box_sudden_actions[i] = 'O' if sudden_actions[i] else 'X'

            json_data_list.append([json_name, gps_vss_seconds, gps_vss_acceleration, gps_vss_frame, gps_vss_100ms, sudden_actions, box_sudden_actions])

        print(f'scanning... {n_of_can}/{len(source_can_list)}')

    e2 = cv2.getTickCount()  # 종료 시간
    Total_time = (e2 - e1) / cv2.getTickFrequency()

    print(f'Total time taken: {Total_time} seconds')
    print(f'Total scanned number of can_data: {n_of_can} files')

# json 스캔
scan_json(source_can_list)

# 이상운전행동 박스 출력
print_any_sudden_actions(json_data_list)

# 이상운전행동 상세 출력
sudden_actions = json_data_list[0][5]
for i, j in zip(sudden_actions, ['sudden acceleration', 'sudden deceleration', 'sudden stop', 'sudden start']):
    for sudden_action in i:
        print(f'{j}: {sudden_action}')
