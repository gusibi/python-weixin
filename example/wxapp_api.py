#! -*- coding: utf-8 -*-
from os import environ

from weixin import WXAPPAPI

appid = environ.get("WXAPP_APPID", "appid")
secret = environ.get("WXAPP_SECRET", "secret")

api = WXAPPAPI(appid=appid, app_secret=secret, grant_type="client_credential")
token = api.client_credential_for_access_token().get("access_token")
print(token)
