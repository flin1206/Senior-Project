import cv2
import mediapipe as mp
import os

mp_drawing = mp.solutions.drawing_utils          # mediapipe 繪圖方法
mp_drawing_styles = mp.solutions.drawing_styles  # mediapipe 繪圖樣式
mp_pose = mp.solutions.pose  # mediapipe 姿勢偵測

# 指定影片所在檔案夾路徑和 Keypoints 檔案的輸出檔案夾路徑
name = "Klay"
video_folder = name + "_Video_Folder"  # 影片所在檔案夾名稱
output_folder = name + "_Keypoints_Folder"  # Keypoints 檔案輸出檔案夾名稱

# 創建 Keypoints 檔案輸出檔案夾（如果不存在）
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 取得影片檔案名稱列表
video_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]

# 迴圈處理多個影片文件
for video_filename in video_files:
    video_filepath = os.path.join(video_folder, video_filename)
    output_filename = os.path.join(output_folder, os.path.splitext(video_filename)[0] + '_keypoints.txt')

    # 打開影片文件
    cap = cv2.VideoCapture(video_filepath)

    # 創建一個檔案以寫入關鍵點座標
    output_file = open(output_filename, 'w')

    # 啟用姿勢偵測
    with mp_pose.Pose(
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:

        if not cap.isOpened():
            print(f"Cannot open video file {video_filename}")
            continue

        while True:
            ret, img = cap.read()
            if not ret:
                print(f"End of video {video_filename}")
                break

            img = cv2.resize(img, (520, 300))               # 縮小尺寸，加快演算速度
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)     # 將 BGR 轉換成 RGB
            results = pose.process(img2)                    # 取得姿勢偵測結果

            if results.pose_landmarks:
                # 遍歷每個關鍵點並將座標附加到檔案
                for idx, landmark in enumerate(results.pose_landmarks.landmark):
                    h, w, c = img.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    output_file.write(f"{idx},{cx},{cy}\n")
            mp_drawing.draw_landmarks(
            img,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            cv2.imshow('oxxostudio', img)
            if cv2.waitKey(1) == ord('q'):
                break     # 按下 q 鍵停止

    # 關閉檔案
    output_file.close()
    cap.release()
    cv2.destroyAllWindows()

print("已完成所有影片的 Keypoints 輸出。")
