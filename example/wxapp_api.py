#! -*- coding: utf-8 -*-
from os import environ
from datetime import datetime

from weixin import WXAPPAPI
from weixin.helper import smart_bytes

appid = environ.get("WXAPP_APPID", "appid")
secret = environ.get("WXAPP_SECRET", "secret")

api = WXAPPAPI(appid=appid, app_secret=secret, grant_type="client_credential")
token = api.client_credential_for_access_token().get("access_token")
print(token)

# send template
template_id = ""
openid = ""
form_id = "0e282a55bc674d9abf9aa2e33eed2768"
imageId = ""
json_body = {
    "touser": openid,
    "template_id": template_id,
    "page": "/pages/history/detail/detail?id=%s" % imageId,
    "form_id": form_id,
    "data": {
        "keyword1": {
            # 时间
            "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "keyword2": {
            # 备注
            "value": smart_bytes("请点击查看").decode("latin1")
        },
        "keyword3": {
            # 状态
            "value": smart_bytes("图片已经生成").decode("latin1"),
            "color": "#173177",
        },
    },
    "emphasis_keyword": "keyword3.DATA",
}

api = WXAPPAPI(access_token=token)
resp = api.send_template(json_body=json_body)
print(resp)

