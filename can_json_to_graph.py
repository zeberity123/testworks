import json
import matplotlib.pyplot as plt
import os

json_folder = 'jsonexample'
json_list = os.listdir(json_folder)

# Load the JSON data
with open(f'{json_folder}/{json_list[0]}', 'r') as f:
    data = json.load(f)

frames = data['frames']

# Extract 'frameCnt' and 'gps_vss' for non-zero 'gps_vss' values
frameCnt_list = []
gps_vss_list = []
acceleration_list = []

frame_in_graph = 0

for frame in frames:
    gps_vss = frame['aim_micom']['gps_vss']
    frameCnt = frame_in_graph
    frameCnt_list.append(frameCnt)
    gps_vss_list.append(int(gps_vss))
    frame_in_graph += 1

# Calculate acceleration by differentiating gps_vss with respect to frame count
# for i in range(0, len(gps_vss_list), 30):
#     acceleration = 0
#     for j in range(1,31):
#         acceleration += (gps_vss_list[i+j] - gps_vss_list[j+i-1])
#     acceleration_list.append(acceleration/30)

acceleration_per_second = []
time_seconds = []

for i in range(30, len(gps_vss_list), 30):
    # Calculate acceleration per second as the change in speed over 30 frames (1 second)
    acceleration = (gps_vss_list[i] - gps_vss_list[i - 30]) / 1  # 1 second
    acceleration_per_second.append(acceleration)
    time_seconds.append(i // 30)  # Time in seconds

# for i in range(1, len(gps_vss_list)):
#     # Acceleration = change in speed / change in frame count
#     acceleration = (gps_vss_list[i] - gps_vss_list[i - 1])  # Assuming 1 frame interval
#     acceleration_list.append(acceleration)

# Adjust frame count list for acceleration plot
acceleration_frameCnt_list = frameCnt_list[1:]

# Check if there is data to plot after removing zeros
if not acceleration_frameCnt_list:
    print("No data to plot.")
else:
    # for vss
    plt.figure(figsize=(12, 6))
    # plt.plot(frameCnt_list[::30], gps_vss_list[::30], linestyle='-', color='blue', linewidth=2)
    plt.plot(frameCnt_list, gps_vss_list, linestyle='-', color='blue', linewidth=2)

    # Enhancements
    plt.xlabel('frame', fontsize=14)
    plt.ylabel('km/h', fontsize=14)
    plt.title('GPS VSS', fontsize=16)
    plt.grid(True, linestyle='--', linewidth=0.5)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.tight_layout()
    plt.show()

    # for acc/sec
    # plt.figure(figsize=(12, 6))
    # plt.plot(time_seconds, acceleration_per_second, linestyle='-', color='green', linewidth=2)
    # plt.xlabel('Time (Seconds)', fontsize=14)
    # plt.ylabel('Acceleration (km/h per second)', fontsize=14)
    # plt.title('Acceleration per Second', fontsize=16)

    
    # for acc/frame
    # plt.figure(figsize=(12, 6))
    # plt.plot(acceleration_frameCnt_list, acceleration_list, linestyle='-', color='red', linewidth=2)

    # Enhancements
    # plt.xlabel('Frame Count', fontsize=14)
    # plt.ylabel('Acceleration (km/h per frame)', fontsize=14)
    # plt.title('Acceleration per Frame', fontsize=16)

    # plt.grid(True, linestyle='--', linewidth=0.5)
    # plt.xticks(fontsize=12)
    # plt.yticks(fontsize=12)
    # plt.tight_layout()
    # plt.show()
