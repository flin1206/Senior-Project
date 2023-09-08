import os

# 指定目標資料夾的路徑
name = "Klay"
target_folder = name + "_Video_Folder"  # 資料夾名稱，請根據實際情況修改

# 當前目錄的路徑
current_directory = os.getcwd()

# 指定新檔案名稱的前綴
new_filename_prefix = name + "_Video_"

# 列出目標資料夾下的所有檔案
files = os.listdir(target_folder)

# 初始化計數器，用於生成新檔案名稱
count = 0

# 迭代處理目標資料夾中的每個檔案
for file in files:
    # 檢查是否是檔案（而不是目錄）
    if os.path.isfile(os.path.join(target_folder, file)):
        # 生成新的檔案名稱
        new_filename = f"{new_filename_prefix}{count}.mp4"

        # 舊檔案的完整路徑
        old_filepath = os.path.join(target_folder, file)

        # 新檔案的完整路徑
        new_filepath = os.path.join(target_folder, new_filename)

        # 重命名檔案
        os.rename(old_filepath, new_filepath)

        print(f"將檔案名稱 '{file}' 更改為 '{new_filename}'")
        
        # 增加計數器
        count += 1

print("已完成目標資料夾下的所有檔案名稱的更改。")
