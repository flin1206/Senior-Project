import os
import numpy as np
from scipy.stats import pearsonr

# 讀取並解析 keypoints 檔案
def load_keypoints_file(filename):
    keypoints = []
    with open(filename, 'r') as file:
        for line in file:
            x, y, z = map(int, line.strip().split(','))
            keypoints.append((x, y, z))
    return np.array(keypoints)

# 計算相關性
def calculate_correlation(keypoints1, keypoints2):
    _, p_value = pearsonr(keypoints1.flatten(), keypoints2.flatten())
    return 1 - p_value

# 計算一組 keypoint 與一個球員（folder）中的所有資料的平均相關性
def calculate_average_correlation(keypoints, player_folder):
    player_folder_path = os.path.join(player_folder)  # 使用提供的球員資料夾名稱
    player_files = os.listdir(player_folder_path)
    
    player_data = []
    correlations = []
    for filename in player_files:
        data = load_keypoints_file(os.path.join(player_folder_path, filename))
        if data.shape[0] == keypoints.shape[0]:
            player_data.append(data)
            correlation = calculate_correlation(keypoints, data)
            correlations.append(correlation)
    
    if len(correlations) == 0:
        return None, None  # 若所有檔案的 keypoints 數量都不符合，則回傳 None
    
    return np.mean(correlations), correlations

# 讀取要比較的新資料 (testkeypoint.txt)
keypoints_to_compare = load_keypoints_file('testkeypoint.txt')

# 找到與每個球員最相似的
players_folders = ['Kobe_Keypoints_Folder', 'RayAllen_Keypoints_Folder']  # 提供的球員資料夾名稱

for player_folder in players_folders:
    average_correlation, all_correlations = calculate_average_correlation(keypoints_to_compare, player_folder)
    if average_correlation is not None:
        print(f'與球員 {player_folder} 的平均相關性為 {average_correlation}')
        print(f'與球員 {player_folder} 的相關性詳細資訊：')
        for i, correlation in enumerate(all_correlations):
            print(f'楨數 {i} 的相關性：{correlation}')
    else:
        print(f'所有與球員 {player_folder} 的檔案的 keypoints 數量都不符合，已忽略')
    print()
