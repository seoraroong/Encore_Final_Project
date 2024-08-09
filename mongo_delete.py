#-------- 이 파일은 지우지 말아주세요-----------------#

# from pymongo import MongoClient
# from pymongo.errors import BulkWriteError
#
# # MongoDB 연결 설정
# client = MongoClient('mongodb://192.168.0.25:27017/')
# db = client['MyDiary']
# collection = db['users']
# user_model_collection = db['users_model']
#
# # 중복된 social_id가 None인 문서 식별
# pipeline = [
#     {
#         "$match": {"social_id": None}
#     },
#     {
#         "$group": {
#             "_id": {"email": "$email"},  # 이메일 기준으로 중복 그룹화
#             "uniqueIds": {"$addToSet": "$_id"},
#             "count": {"$sum": 1}
#         }
#     },
#     {
#         "$match": {
#             "count": {"$gt": 1}  # 중복된 그룹만 필터링
#         }
#     }
# ]
#
# duplicate_groups = list(collection.aggregate(pipeline))
# duplicate_groups_user_model = list(user_model_collection.aggregate(pipeline))
#
#
# # 중복된 문서 제거
# for group in duplicate_groups:
#     ids_to_keep = group["uniqueIds"]
#     # 최신 문서를 남기고 나머지 삭제
#     ids_to_keep.pop()  # 목록에서 남길 문서의 _id를 제거
#     try:
#         result = collection.delete_many({"_id": {"$in": ids_to_keep}})
#         print(f"Deleted {result.deleted_count} documents.")
#     except BulkWriteError as e:
#         print(f"An error occurred during delete operation: {e}")
#
# print("중복된 문서가 제거되었습니다.")
#
# # 중복된 문서 제거
# for group in duplicate_groups:
#     ids_to_keep = group["uniqueIds"]
#     # 최신 문서를 남기고 나머지 삭제
#     ids_to_keep.pop()  # 목록에서 남길 문서의 _id를 제거
#     try:
#         result = user_model_collection.delete_many({"_id": {"$in": ids_to_keep}})
#         print(f"Deleted {result.deleted_count} documents.")
#     except BulkWriteError as e:
#         print(f"An error occurred during delete operation: {e}")
#
# print("중복된 문서가 제거되었습니다.")

from pymongo import MongoClient

# MongoDB 연결 설정
client = MongoClient('mongodb://192.168.0.25:27017/')
db = client['MyDiary']
collection = db['users']
user_model_collection = db['users_model']


# 현재 인덱스 확인
indexes = collection.list_indexes()
for index in indexes:
    print(index)

# 유니크 인덱스 삭제
index_name = "users_email_0ea73cca_uniq"  # 인덱스 이름을 지정합니다. 실제 이름을 확인 후 수정하세요.
# users_role_id_1900a745
# users_email_0ea73cca_uniq
try:
    collection.drop_index(index_name)
    print(f"Index '{index_name}' has been dropped successfully in collection.")
    user_model_collection.drop_index(index_name)
    print(f"Index '{index_name}' has been dropped successfully in collection_model.")
except Exception as e:
    print(f"An error occurred while dropping the index: {e}")

    # python .\mongo_delete.py