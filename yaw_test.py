# Sample data for frames 940 to 943
data = {
    "940": {"yawH": 36, "yawL": 152},
    "941": {"yawH": 36, "yawL": 148},
    "942": {"yawH": 36, "yawL": 138},
    "943": {"yawH": 36, "yawL": 117},
}

degrees_per_unit = 360.0 / 65536.0
previous_yaw_raw = None
total_rotation = 0.0

for frame in sorted(data.keys()):
    yawH = data[frame]['yawH']
    yawL = data[frame]['yawL']
    yaw_raw = (yawH << 8) | yawL
    
    if previous_yaw_raw is not None:
        delta_yaw_raw = yaw_raw - previous_yaw_raw
        # Adjust for wraparound
        if delta_yaw_raw > 32768:
            delta_yaw_raw -= 65536
        elif delta_yaw_raw < -32768:
            delta_yaw_raw += 65536
        
        delta_yaw_degrees = delta_yaw_raw * degrees_per_unit
        total_rotation += delta_yaw_degrees
        print(f"Frame {frame}: ΔYaw = {delta_yaw_degrees:.4f}°, Total Rotation = {total_rotation:.4f}°")
    else:
        print(f"Frame {frame}: Starting Yaw = {yaw_raw * degrees_per_unit:.4f}°")
    
    previous_yaw_raw = yaw_raw
