python-weixin
-----
A Python client for the Weixin REST APIs

0.1.5 添加 模板消息处理
-----
添加模板消息处理

0.1.4 新增功能
-----
添加消息回复模块 加密解密模块

0.1.3 新增功能
-----
支持 自定义公众号菜单管理（添加|删除）
支持 客服管理（添加|修改|删除|获取）
支持 发送客服消息
支持 发送模板消息


0.1.2 新增功能
-----
完善服务异常处理

0.1.1 新增功能
-----
完善服务异常处理

0.1.0 功能
-----
微信公众平台 和开放平台 支持


Installation
-----
pip install python-weixin

Requires
-----
* requests
* simplejson
* six
* lxml
* xmltodict
* pycrypto


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


#### 创建自定义菜单

#### 支持的按钮类型

1. click：点击推事件用户点击click类型按钮后，微信服务器会通过消息接口推送消息类型为event的结构给开发者（参考消息接口指南），并且带上按钮中开发者填写的key值，开发者可以通过自定义的key值与用户进行交互；
2. view：跳转URL用户点击view类型按钮后，微信客户端将会打开开发者在按钮中填写的网页URL，可与网页授权获取用户基本信息接口结合，获得用户基本信息。
3. scancode_push：扫码推事件用户点击按钮后，微信客户端将调起扫一扫工具，完成扫码操作后显示扫描结果（如果是URL，将进入URL），且会将扫码的结果传给开发者，开发者可以下发消息。
4. scancode_waitmsg：扫码推事件且弹出“消息接收中”提示框用户点击按钮后，微信客户端将调起扫一扫工具，完成扫码操作后，将扫码的结果传给开发者，同时收起扫一扫工具，然后弹出“消息接收中”提示框，随后可能会收到开发者下发的消息。
5. pic_sysphoto：弹出系统拍照发图用户点击按钮后，微信客户端将调起系统相机，完成拍照操作后，会将拍摄的相片发送给开发者，并推送事件给开发者，同时收起系统相机，随后可能会收到开发者下发的消息。
6. pic_photo_or_album：弹出拍照或者相册发图用户点击按钮后，微信客户端将弹出选择器供用户选择“拍照”或者“从手机相册选择”。用户选择后即走其他两种流程。
7. pic_weixin：弹出微信相册发图器用户点击按钮后，微信客户端将调起微信相册，完成选择操作后，将选择的相片发送给开发者的服务器，并推送事件给开发者，同时收起相册，随后可能会收到开发者下发的消息。
8. location_select：弹出地理位置选择器用户点击按钮后，微信客户端将调起地理位置选择工具，完成选择操作后，将选择的地理位置发送给开发者的服务器，同时收起位置选择工具，随后可能会收到开发者下发的消息。
9. media_id：下发消息（除文本消息）用户点击media_id类型按钮后，微信服务器会将开发者填写的永久素材id对应的素材下发给用户，永久素材类型可以是图片、音频、视频、图文消息。请注意：永久素材id必须是在“素材管理/新增永久素材”接口上传后获得的合法id。
10. view_limited：跳转图文消息URL用户点击view_limited类型按钮后，微信客户端将打开开发者在按钮中填写的永久素材id对应的图文消息URL，永久素材类型只支持图文消息。请注意：永久素材id必须是在“素材管理/新增永久素材”接口上传后获得的合法id。

#### 自定义菜单参数说明

|参数	        |是否必须	            |说明
|:------        |:--------              |:-----
| button	    | 是	                | 一级菜单数组，个数应为1~3个
| sub_button	| 否	                | 二级菜单数组，个数应为1~5个
| type	        | 是	                | 菜单的响应动作类型
| name	        | 是	                | 菜单标题，不超过16个字节，子菜单不超过40个字节
| key	        | click等点击类型必须	| 菜单KEY值，用于消息接口推送，不超过128字节
| url	        | view类型必须	        | 网页链接，用户点击菜单可打开链接，不超过1024字节
media_id	media_id类型和view_limited类型必须	调用新增永久素材接口返回的合法media_id

### 消息管理

#### 被动回复

被动回复是在用户发出请求后在respone 中包含的内容

消息体见官方参考文档:
[被动回复用户消息](https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140543&token=&lang=zh_CN)

#### 客服消息

API 列表

* add_customservice     添加客服帐号
* update_customservice  修改客服帐号
* delete_customservice  删除客服帐号
* getall_customservice  获取所有客服帐号
* custom_message_send   发送客服消息

消息体见官方参考文档:
[客服消息](https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1421140547&token=&lang=zh_CN)

#### 模板消息

API 列表

* template_message_send

消息体见官方参考文档:
[模板消息](https://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433751277&token=&lang=zh_CN)
