import cv2
import mediapipe as mp
import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
sys.stdout.reconfigure(encoding='utf-8')

if len(sys.argv) != 2:
    print("Usage: python Trans_to_keypoints.py <video_filename>")
    sys.exit(1)

video_filename = sys.argv[1]

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# 指定影片所在檔案夾路徑和 Keypoints 檔案的輸出檔案夾路徑
video_folder = "uploads"  # 影片所在檔案夾名稱
output_folder = "New_Keypoints_Folder"  # Keypoints 檔案輸出檔案夾名稱

# 創建 Keypoints 檔案輸出檔案夾（如果不存在）
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

video_filepath = os.path.join(video_folder, video_filename)
output_filename = os.path.join(
    output_folder, video_filename[:-4] + '_keypoints' + '.txt')

# 打開影片文件
cap = cv2.VideoCapture(video_filepath)

# 創建一個檔案以寫入關鍵點座標
output_file = open(output_filename, 'w')

# 初始化行数计数器
line_count = 0

# 啟用姿勢偵測
with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:

    if not cap.isOpened():
        print(f"Cannot open video file {video_filename}")

    while True:
        ret, img = cap.read()
        if not ret:
            print(f"End of video {video_filename}")
            break

        img = cv2.resize(img, (520, 300))
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(img2)

        if results.pose_landmarks:
            # 遍歷每個關鍵點並將座標附加到檔案
            for idx, landmark in enumerate(results.pose_landmarks.landmark):
                h, w, c = img.shape
                cx, cy, cz = int(
                    landmark.x * w), int(landmark.y * h), landmark.z

                # 处理 z 值为空的情况
                if cz is None:
                    cz = 0  # 将 z 值替换为零

                output_file.write(f"{idx},{cx},{cy},{cz}\n")
                line_count += 1

                # 检查行数计数器是否达到限制
                if line_count >= 1155:
                    break

        mp_drawing.draw_landmarks(
            img,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

        cv2.imshow('oxxostudio', img)
        if cv2.waitKey(1) == ord('q') or line_count >= 1155:
            break

    # 關閉檔案
    output_file.close()
    cap.release()
    cv2.destroyAllWindows()

##########################################################################################################

# 載入並解析 keypoints 檔案
def load_keypoints_file(filename):
    keypoints = []
    with open(filename, 'r') as file:
        for line in file:
            _, x, y, z = map(float, line.strip().split(','))
            keypoints.append([x, y, z])
    return np.array(keypoints)

# 主要程式
player_names = ["Klay", "Kobe", "RayAllen"]  # 設定球員名稱的順序
max_keypoints = 1155  # 用於確保所有特徵集的大小相同

# 載入已保存的模型
loaded_model = tf.keras.models.load_model("current_model")

# 預測 new_keypoints 來自哪位球員
new_keypoints = load_keypoints_file(output_filename)  # 替換成您的測試 keypoints 檔案路徑
# 正規化新 keypoints
while len(new_keypoints) < max_keypoints:
    new_keypoints = np.vstack((new_keypoints, [0, 0, 0]))
predicted_probabilities_dl = loaded_model.predict(np.expand_dims(new_keypoints, axis=0))
predicted_player_index_dl = np.argmax(predicted_probabilities_dl)
predicted_player_dl = player_names[predicted_player_index_dl]

print(f'{predicted_player_dl}')

#########################################################################################
import pymongo
from bson import ObjectId
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient["video_upload_app"]
mycol = mydb["videos"]

x = mycol.find_one(sort=[("createdAt", pymongo.DESCENDING)])
if x:
    document_id = x["_id"]
# print(x)
query = {"_id": ObjectId(document_id)}

# 获取要更新的文档
existing_document = mycol.find_one(query)

# 更新文档
existing_document["result"] = predicted_player_dl

# 保存更新后的文档
mycol.save(existing_document)

# 打印更新后的文档
updated_document = mycol.find_one(query)
#　print(updated_document)