#! -*- coding: utf-8 -*-
from os import environ, path
from pprint import pprint

from weixin import WxAppCloudAPI

appid = environ.get("WXAPP_APPID", "appid")
secret = environ.get("WXAPP_SECRET", "secret")
env = environ.get("WXAPP_ENV", "test-id")

app_cloud = WxAppCloudAPI(
    appid=appid, app_secret=secret, grant_type="client_credential"
)
token = app_cloud.client_credential_for_access_token().get("access_token")

cloud_api = WxAppCloudAPI(access_token=token)

path = "test/author.jpg"
filepath = "/Users/gs/Desktop/author.jpg"
path = "test/id2uid1.lua"
filepath = "/Users/gs/Desktop/id2uid.lua"
path = "test/aws-serverless-games.pdf"
filepath = "/Users/gs/Desktop/aws-serverless-games.pdf"
resp = cloud_api.upload_file(json_body={"env": env, "path": path, "filepath": filepath})
print(resp)
