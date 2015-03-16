python-weixin
-----
A Python client for the Weixin REST APIs

Installation
-----
python setup.py install

Requires
-----
* requests
* simplejson
* six


Authentication
-----
Weixin API uses the OAuth2 protocol for authentication, but not all functionality requires authentication.
See the docs for more information: https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&t=resource/res_list&verify=1&lang=zh_CN


### Authenticating a user
(TODO)The provided sample app shows a simple OAuth flow for authenticating a user and getting an access token for them.


### Using an access token
Once you have an access token (whether via the script or from the user flow), you can  pass that token into the WeixinAPI constructor:

``` python
from weixin.client import WeixinAPI

scope = ("snsapi_login", )
api = WeixinAPI(appid=APP_ID,
                app_secret=APP_SECRET,
                redirect_uri=REDIRECT_URI)
authorize_url = api.get_authorize_url(scope=scope)

access_token = api.exchange_code_for_access_token(code=code)

api = WeixinAPI(access_token=access_token)

user = api.user(openid="openid")
```

