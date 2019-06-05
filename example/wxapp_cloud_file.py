#! -*- coding: utf-8 -*-
from os import environ, path
from pprint import pprint

from weixin import WxAppCloudAPI

appid = environ.get("WXAPP_APPID", "appid")
secret = environ.get("WXAPP_SECRET", "secret")
env = "test-id"

app_cloud = WxAppCloudAPI(
    appid=appid, app_secret=secret, grant_type="client_credential"
)
token = app_cloud.client_credential_for_access_token().get("access_token")

cloud_api = WxAppCloudAPI(access_token=token)

path = "test/file.py"
filepath = "./file.py"
resp = cloud_api.upload_file(json_body={"env": env, "path": path, "filepath": filepath})
print(resp)
