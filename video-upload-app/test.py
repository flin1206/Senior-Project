import pymongo
from bson import ObjectId
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
mydb = myclient["video_upload_app"]
mycol = mydb["videos"]

x = mycol.find_one(sort=[("createdAt", pymongo.DESCENDING)])
if x:
    document_id = x["_id"]
print(x)
query = {"_id": ObjectId(document_id)}

# 获取要更新的文档
existing_document = mycol.find_one(query)

# 更新文档
existing_document["result"] = "kobe"

# 保存更新后的文档
mycol.save(existing_document)

# 打印更新后的文档
updated_document = mycol.find_one(query)
print(updated_document)