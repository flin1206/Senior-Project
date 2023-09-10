import os

# 获取当前目录
current_directory = os.getcwd()

# 遍历当前目录下的所有文件
for filename in os.listdir(current_directory):
    if filename.endswith(".txt"):
        with open(filename, 'r') as file:
            # 读取文件内容
            lines = file.readlines()
        
        # 判断文件是否有足够的行数
        if len(lines) > 1155:
            # 只保留前1387行
            lines = lines[:1155]
            
            # 重新写入文件
            with open(filename, 'w') as file:
                file.writelines(lines)
            
            print(f"文件 {filename} 已被修改")
        else:
            print(f"文件 {filename} 行数不足1156，未修改")