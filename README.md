python-weixin
-----
A Python client for the Weixin REST APIs

0.0.4 新功能
-----
* 修改目录结构

0.0.3 新功能
-----
* 添加超时处理
* 修改包名

0.0.2 新功能
-----
增加微信公众平台支持


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
Weixin API 使用 OAuth2 认证方式
详情见: https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list&t=resource/res_list&verify=1&lang=zh_CN


### Authenticating a user
具体使用方法参考 sample app


### Using an access token
获取到access token 后，可以使用token 获取 用户信息等:

微信开放平台使用示例：

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

微信公众平台使用示例：

``` python
from weixin.client import WeixinMpAPI

scope = ("snsapi_base", )
api = WeixinMpAPI(appid=APP_ID,
                  app_secret=APP_SECRET,
                  redirect_uri=REDIRECT_URI)
authorize_url = api.get_authorize_url(scope=scope)

access_token = api.exchange_code_for_access_token(code=code)

api = WeixinMpAPI(access_token=access_token)

user = api.user(openid="openid")
```
