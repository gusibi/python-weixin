# -*- coding: utf-8 -*-

import sys

from weixin.client import WeixinAPI
from weixin.oauth2 import OAuth2AuthExchangeError

if len(sys.argv) > 1 and sys.argv[1] == 'local':
    try:
        from test_settings import *

        WeixinAPI.host = test_host
        WeixinAPI.base_path = test_base_path
        WeixinAPI.access_token_field = "access_token"
        WeixinAPI.authorize_url = test_authorize_url
        WeixinAPI.access_token_url = test_access_token_url
        WeixinAPI.protocol = test_protocol
    except Exception:
        pass


# Fix Python 2.x.
try:
    import __builtin__
    input = getattr(__builtin__, 'raw_input')
except (ImportError, AttributeError):
    pass


appid = input("App ID: ").strip()
app_secret = input("App Secret: ").strip()
redirect_uri = input("Redirect URI: ").strip()
raw_scope = input("Requested scope (separated by spaces, blank for just basic read): ").strip()
scope = raw_scope.split(' ')
# For basic, API seems to need to be set explicitly
if not scope or scope == [""]:
    scope = ["snsapi_login"]


api = WeixinAPI(appid=appid,
                app_secret=app_secret,
                redirect_uri=redirect_uri)
redirect_uri = api.get_authorize_login_url(scope=scope)

print ("Visit this page and authorize access in your browser: "+ redirect_uri)

code = (str(input("Paste in code in query string after redirect: ").strip()))

access_token = api.exchange_code_for_access_token(code)

print ("access token: " )
print (access_token)
