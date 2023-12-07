import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# 載入現有的球員 keypoints 資料
def load_player_keypoints(player_folder):
    player_files = [f for f in os.listdir(player_folder)]
    if not player_files:
        print(f"No keypoints files found in folder: {player_folder}")
        return [], 0
    
    keypoints_data = []
    max_keypoints = 700  # 用於確保所有特徵集的大小相同
    for filename in player_files:
        # print("found " + filename)
        keypoints = load_keypoints_file(os.path.join(player_folder, filename))
        if len(keypoints) > max_keypoints:
            max_keypoints = len(keypoints)
        keypoints_data.append(keypoints)
    
    # 將所有特徵集調整為相同的大小，補0
    for i in range(len(keypoints_data)):
        while len(keypoints_data[i]) < max_keypoints:
            keypoints_data[i] = np.vstack((keypoints_data[i], [0, 0, 0]))
    
    return keypoints_data, max_keypoints

# 載入並解析 keypoints 檔案
def load_keypoints_file(filename):
    keypoints = []
    with open(filename, 'r') as file:
        for line in file:
            _, x, y, z = map(float, line.strip().split(','))
            keypoints.append([x, y, z])
    return np.array(keypoints)

# 主要程式
player_folders = ["Klay_Keypoints_Folder", "Kobe_Keypoints_Folder", "RayAllen_Keypoints_Folder", "curry_Keypoints_Folder", 
                  "damian_Keypoints_Folder", "KD_Keypoints_Folder", "korver_Keypoints_Folder", "Lebron_Keypoints_Folder"]  # 指定所有球員的目錄

# 收集所有球員的 keypoints 資料
all_keypoints_data = []
max_keypoints = 0  # 用於確保所有特徵集的大小相同
for player_folder in player_folders:
    print(f"Found Folder: {player_folder}")
    player_keypoints, folder_max_keypoints = load_player_keypoints(player_folder)
    all_keypoints_data.extend(player_keypoints)
    max_keypoints = max(max_keypoints, folder_max_keypoints)  # 找到最大的特徵集長度

print(f"Max Keypoints: {max_keypoints}")
print(f"Number of All Keypoints Data: {len(all_keypoints_data)}")

# 檢查 max_keypoints 是否大於0
if max_keypoints > 0:
    # 正規化資料，將每個資料集的 keypoints 數量補齊為 max_keypoints
    for i in range(len(all_keypoints_data)):
        while len(all_keypoints_data[i]) < max_keypoints:
            all_keypoints_data[i] = np.vstack((all_keypoints_data[i], [0, 0, 0]))

    # 使用深度學習進行預測
    model = keras.Sequential([
        layers.Input(shape=(max_keypoints, 3)),  # 輸入層，3個特徵值（x、y、z）
        layers.LSTM(64, return_sequences=False),  # LSTM層，return_sequences 設為 False
        layers.Dense(8, activation='softmax')  # 輸出層，8個球員的分類
    ])

    # 編譯模型
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.summary()
    # 訓練樣本的標籤
    player_names = ["Klay", "Kobe", "RayAllen", "Curry", "Damian", "KD", "Korver", "Lebron"]  # 設定球員名稱的順序
    y_dl = np.repeat(player_names, len(all_keypoints_data) // len(player_names))  # 標籤集

    # 將標籤進行編碼
    label_to_index = {name: index for index, name in enumerate(player_names)}
    y_encoded = np.array([label_to_index[name] for name in y_dl])
    y_dl = tf.keras.utils.to_categorical(y_encoded)


    # 訓練深度學習模型
    X_dl = np.array(all_keypoints_data)  # 特徵集
    X_dl = X_dl.reshape(-1, max_keypoints, 3)  # 重塑特徵集的形狀

    model.fit(X_dl, y_dl, epochs=1000)
    model.save("my_model.h5")

    # 預測 new_keypoints 來自哪位球員
    new_keypoints = load_keypoints_file('testkeypoint.txt')  # 替換成您的測試 keypoints 檔案路徑
    # 正規化新 keypoints
    while len(new_keypoints) < max_keypoints:
        new_keypoints = np.vstack((new_keypoints, [0, 0, 0]))
    predicted_probabilities_dl = model.predict(np.expand_dims(new_keypoints, axis=0))
    predicted_player_index_dl = np.argmax(predicted_probabilities_dl)
    predicted_player_dl = player_names[predicted_player_index_dl]

    print(f'深度學習模型 預測 new_keypoints 最有可能來自 {predicted_player_dl}')
else:
    print("Error: max_keypoints is 0. Check your data loading process.")
