import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers


# 載入並解析 keypoints 檔案
def load_keypoints_file(filename):
    keypoints = []
    with open(filename, 'r') as file:
        for line in file:
            _, x, y, z = map(float, line.strip().split(','))
            keypoints.append([x, y, z])
    return np.array(keypoints)


# 主要程式
player_names = ["Klay", "Kobe", "RayAllen", "Curry", "Damian", "KD", "Korver", "Lebron"]  # 設定球員名稱的順序
max_keypoints = 700  # 用於確保所有特徵集的大小相同

# 載入已保存的模型
loaded_model = tf.keras.models.load_model("my_model.h5")

# 預測 new_keypoints 來自哪位球員
new_keypoints = load_keypoints_file('testkeypoint.txt')  # 替換成您的測試 keypoints 檔案路徑
# 正規化新 keypoints
while len(new_keypoints) < max_keypoints:
    new_keypoints = np.vstack((new_keypoints, [0, 0, 0]))
# 截斷或填充新 keypoints 以滿足模型的期望形狀
new_keypoints = new_keypoints[:max_keypoints]

predicted_probabilities_dl = loaded_model.predict(np.expand_dims(new_keypoints, axis=0))
predicted_player_index_dl = np.argmax(predicted_probabilities_dl)
predicted_player_dl = player_names[predicted_player_index_dl]

print(f'深度學習模型 預測 new_keypoints 最有可能來自 {predicted_player_dl}')
