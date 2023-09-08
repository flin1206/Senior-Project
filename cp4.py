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

# 列出當前目錄下的所有資料夾
directories = [name for name in os.listdir('.') if os.path.isdir(name)]

names = ["Kobe", "RayAllen", "Klay"]
# 初始化最小平均距離和相關球員變數
min_avg_distance = float('inf')
most_similar_player = None

# 對每個資料夾進行 keypoints 比對
for name in names:
    avg_distances = []  # 平均距離列表
    for directory in directories:
        if directory == name + '_Keypoints_Folder':
            keypoints_files = [f for f in os.listdir(directory) if f.startswith(name + '_keypoints_')]
            keypoints_data = [load_keypoints_file(os.path.join(directory, filename)) for filename in keypoints_files]

            # 讀取新的 keypoints8 檔案
            keypoints8 = load_keypoints_file(os.path.join('testkeypoint.txt'))

            # 初始化距離列表
            distances = []

            # 對每個 keypoints 檔案計算平均歐氏距離
            for i, keypoints in enumerate(keypoints_data):
                average_distance = np.mean([euclidean_distance(keypoint1, keypoint2) for keypoint1, keypoint2 in zip(keypoints, keypoints8)])
                distances.append(average_distance)
                print(f'檔案 {keypoints_files[i]} 與新資料的平均距離為 {average_distance}')

            # 計算資料夾內所有檔案的平均距離
            avg_distance = np.mean(distances)
            avg_distances.append(avg_distance)

            print(f'在資料夾 {directory} 中，平均距離為 {avg_distance}')

    # 找到最相似的檔案
    min_avg_distance_player = min(avg_distances)
    if min_avg_distance_player < min_avg_distance:
        min_avg_distance = min_avg_distance_player
        most_similar_player = name

print(f'最相似的球員是 {most_similar_player}，平均距離為 {min_avg_distance}')
