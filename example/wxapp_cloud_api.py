#! -*- coding: utf-8 -*-
from os import environ, path

from weixin import WxAppCloudAPI

appid = environ.get("WXAPP_APPID", "appid")
secret = environ.get("WXAPP_SECRET", "secret")
env = "test-id"

example_db = path.abspath(path.join(path.dirname(__file__), "./example_db"))


app_cloud = WxAppCloudAPI(
    appid=appid, app_secret=secret, grant_type="client_credential"
)
token = app_cloud.client_credential_for_access_token().get("access_token")
print(token)

cloud_api = WxAppCloudAPI(access_token=token)

# 获取库的集合信息
db_info = cloud_api.db_collection_info(json_body={"env": env, "limit": 10})
print(db_info)
# 新建集合
resp = cloud_api.db_collection_add(json_body={"env": env, "collection_name": "example"})
print("new collection: ", resp)

# 获取库的集合信息
db_info = cloud_api.db_collection_info(json_body={"env": env, "limit": 10})
print("db info: ", db_info)

# 导入数据
resp = cloud_api.db_migrate_import(
    json_body={
        "env": env,
        "collection_name": "example",
        "file_path": example_db,
        "file_type": 2,
        "stop_on_error": False,
        "conflict_mode": 2,
    }
)
print("db migrate import: ", resp)

# 数据库统计记录数量
resp = cloud_api.db_count(
    json_body={"env": env, "query": 'db.collection("example").count()'}
)
print("count", resp)

# 插入数据
resp = cloud_api.db_add(
    json_body={"env": env, "query": 'db.collection("example").add({data: [{age: 12}]})'}
)
print("add: ", resp)

id_list = resp.get("id_list")
item_id = id_list[0]

# 数据库统计记录数量
resp = cloud_api.db_count(
    json_body={"env": env, "query": 'db.collection("example").count()'}
)
print("count", resp)
# 查询记录

resp = cloud_api.db_query(
    json_body={
        "env": env,
        "query": 'db.collection("example").where({_id: "%s"}).limit(10).skip(0).get()'
        % item_id,
    }
)
print("query: ", resp)

# 更新数据

resp = cloud_api.db_update(
    json_body={
        "env": env,
        "query": 'db.collection("example").where({_id: "%s"}).update({data: {age: _.inc(1)}})'
        % item_id,
    }
)
print("update: ", resp)

# 查询记录
resp = cloud_api.db_query(
    json_body={
        "env": env,
        "query": 'db.collection("example").where({_id: "%s"}).limit(10).skip(0).get()'
        % item_id,
    }
)
print("query: ", resp)
# 删除数据
resp = cloud_api.db_delete(
    json_body={
        "env": env,
        "query": 'db.collection("example").where({_id: "%s"}).remove()' % item_id,
    }
)
print("remove: ", resp)

# 查询记录
resp = cloud_api.db_query(
    json_body={
        "env": env,
        "query": 'db.collection("example").where({_id: "%s"}).limit(10).skip(0).get()'
        % item_id,
    }
)
print("query: ", resp)
# 删除集合
resp = cloud_api.db_collection_delete(
    json_body={"env": env, "collection_name": "example"}
)

# 获取库的集合信息

db_info = cloud_api.db_collection_info(json_body={"env": env, "limit": 10})
print("db info: ", db_info)
