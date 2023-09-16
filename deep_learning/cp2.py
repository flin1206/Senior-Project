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

name = "Kobe"
# 對每個資料夾進行 keypoints 比對
for directory in directories:
    if directory == name + '_Keypoints_Folder':
        keypoints_files = [f for f in os.listdir(directory) if f.startswith(name + '_keypoints_')]
        keypoints_data = [load_keypoints_file(os.path.join(directory, filename)) for filename in keypoints_files]

        # 讀取新的 keypoints8 檔案
        keypoints8 = load_keypoints_file(os.path.join('testkeypoint.txt'))

        # 初始化距離列表
        distances = []

        # 對每個 keypoints 檔案計算平均歐氏距離
        for keypoints in keypoints_data:
            average_distance = np.mean([euclidean_distance(keypoint1, keypoint2) for keypoint1, keypoint2 in zip(keypoints, keypoints8)])
            distances.append(average_distance)

        # 找到最相似的檔案
        most_similar_index = np.argmin(distances)
        most_similar_file = keypoints_files[most_similar_index]
        min_distance = min(distances)
        for i, keypoints in enumerate(keypoints_data):
            average_distance = np.mean([euclidean_distance(keypoint1, keypoint2) for keypoint1, keypoint2 in zip(keypoints, keypoints8)])
            print(f'檔案 {keypoints_files[i]} 與檔案 8 的平均距離為 {average_distance}')
        print(f'在資料夾 {directory} 中，最相似的檔案是 {most_similar_file}，平均距離為 {min_distance}')
