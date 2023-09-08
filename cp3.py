import os
import numpy as np

# 讀取並解析 keypoints 檔案
def load_keypoints_file(filename):
    keypoints = []
    with open(filename, 'r') as file:
        for line in file:
            x, y, z = map(int, line.strip().split(','))
            keypoints.append((x, y, z))
    return np.array(keypoints)

# 計算歐氏距離
def euclidean_distance(keypoints1, keypoints2):
    return np.linalg.norm(keypoints1 - keypoints2)

# 計算一組 keypoint 與一個球員（folder）中的所有資料的平均歐氏距離
def calculate_average_distance(keypoints, player_folder):
    player_folder_path = os.path.join(player_folder)  # 使用提供的球員資料夾名稱
    player_files = os.listdir(player_folder_path)
    
    player_data = []
    for filename in player_files:
        data = load_keypoints_file(os.path.join(player_folder_path, filename))
        # 如果 keypoint 數量不符合，則忽略該檔案
        if data.shape[0] == keypoints.shape[0]:
            player_data.append(data)
    
    if not player_data:
        return float('inf')
    
    distances = [euclidean_distance(keypoints, data) for data in player_data]
    return np.mean(distances)

# 讀取要比較的新資料 (testkeypoint.txt)
keypoints_to_compare = load_keypoints_file('testkeypoint.txt')

# 找到與每個球員最相似的
players_folders = ['Kobe_Keypoints_Folder', 'RayAllen_Keypoints_Folder']  # 提供的球員資料夾名稱
most_similar_player = None
min_average_distance = float('inf')

for player_folder in players_folders:
    average_distance = calculate_average_distance(keypoints_to_compare, player_folder)
    if average_distance < min_average_distance:
        min_average_distance = average_distance
        most_similar_player = player_folder

print(f'最相似的球員是 {most_similar_player}，平均距離為 {min_average_distance}')


