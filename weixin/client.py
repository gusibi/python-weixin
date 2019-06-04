# -*-coding: utf-8 -*-
from __future__ import unicode_literals

"""
File:   client.py
Author: goodspeed
Email:  cacique1103@gmail.com
Github: https://github.com/gusibi
Date:   2015-02-06
Description: Weixin OAuth2
"""

from . import oauth2
from .bind import bind_method
from .helper import genarate_signature


SUPPORTED_FORMATS = ["", "json"]


class WeixinAPI(oauth2.OAuth2API):

    host = "open.weixin.qq.com"
    base_path = ""
    access_token_field = "access_token"
    authorize_url = "https://open.weixin.qq.com/connect/qrconnect"
    access_token_url = "https://api.weixin.qq.com/sns/oauth2/access_token"
    refresh_token_url = "https://api.weixin.qq.com/sns/oauth2/refresh_token"
    protocol = "https"
    api_name = "Weixin"
    x_ratelimit_remaining = None
    x_ratelimit = None

    def __init__(self, *args, **kwargs):
        format = kwargs.get("format", "")
        if format in SUPPORTED_FORMATS:
            self.format = format
        else:
            raise Exception("Unsupported format")
        super(WeixinAPI, self).__init__(*args, **kwargs)

    validate_token = bind_method(
        path="/sns/auth", accepts_parameters=["openid"], response_type="entry"
    )

    user = bind_method(
        path="/sns/userinfo", accepts_parameters=["openid"], response_type="entry"
    )


class WeixinMpAPI(oauth2.OAuth2API):

    host = "open.weixin.qq.com"
    base_path = ""
    access_token_field = "access_token"
    authorize_url = "https://open.weixin.qq.com/connect/oauth2/authorize"
    access_token_url = "https://api.weixin.qq.com/sns/oauth2/access_token"
    refresh_token_url = "https://api.weixin.qq.com/sns/oauth2/refresh_token"
    client_credential_token_url = "https://api.weixin.qq.com/cgi-bin/token"
    protocol = "https"
    api_name = "WeixinMp"
    x_ratelimit_remaining = None
    x_ratelimit = None

    def __init__(self, *args, **kwargs):
        self.mp_token = kwargs.get("mp_token", None)
        self.timestamp = kwargs.get("timestamp", None)
        self.nonce = kwargs.get("nonce", None)
        self.signature = kwargs.get("signature", None)
        self.echostr = kwargs.get("echostr", None)
        self.xml_body = kwargs.get("xml_body", None)
        self.form_body = kwargs.get("form_body", None)
        self.json_body = kwargs.get("json_body", None)
        self.grant_type = kwargs.get("grant_type", None)
        format = kwargs.get("format", "")

        if format in SUPPORTED_FORMATS:
            self.format = format
        else:
            raise Exception("Unsupported format")
        super(WeixinMpAPI, self).__init__(*args, **kwargs)

    def validate_signature(self):
        params = {
            "timestamp": self.timestamp,
            "token": self.mp_token,
            "nonce": self.nonce,
        }
        signature = genarate_signature(params)
        return signature == self.signature

    user = bind_method(
        path="/sns/userinfo", accepts_parameters=["openid"], response_type="entry"
    )

    validate_user = bind_method(
        path="/sns/auth", accepts_parameters=["openid"], response_type="entry"
    )

    jsapi_ticket = bind_method(
        path="/cgi-bin/ticket/getticket",
        accepts_parameters=["type"],
        response_type="entry",
    )

    create_menu = bind_method(
        path="/cgi-bin/menu/create",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )

    get_menu = bind_method(
        path="/cgi-bin/menu/get", accepts_parameters=["type"], response_type="entry"
    )

    delete_menu = bind_method(
        path="/cgi-bin/menu/delete", accepts_parameters=["type"], response_type="entry"
    )

    add_customservice = bind_method(
        path="/customservice/kfaccount/add",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )

    update_customservice = bind_method(
        path="/customservice/kfaccount/update",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )

    delete_customservice = bind_method(
        path="/customservice/kfaccount/delete",
        accepts_parameters=["json_body"],
        response_type="entry",
    )

    getall_customservice = bind_method(
        path="/customservice/kfaccount/getkflist",
        accepts_parameters=["json_body"],
        response_type="entry",
    )

    # TODO 待实现
    # uploadheadimg_customservice = bind_method(
    #     path='/customservice/kfaccount/uploadheadimg',
    #     method='POST',
    #     accepts_parameters=['json_body'],
    #     response_type="entry")

    custom_message_send = bind_method(
        path="/cgi-bin/message/custom/send",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )

    template_message_send = bind_method(
        path="/cgi-bin/message/template/send",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )

    qrcode = bind_method(
        path="/cgi-bin/qrcode/create",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )


class WXAPPAPI(oauth2.OAuth2API):

    host = "api.weixin.qq.com"
    base_path = ""
    access_token_field = "access_token"
    authorize_url = ""
    access_token_url = "https://api.weixin.qq.com/sns/jscode2session"
    refresh_token_url = ""
    client_credential_token_url = "https://api.weixin.qq.com/cgi-bin/token"
    protocol = "https"
    api_name = "WXAPP"
    x_ratelimit_remaining = None
    x_ratelimit = None

    def __init__(self, *args, **kwargs):
        self.grant_type = kwargs.get("grant_type", None)
        format = kwargs.get("format", "")
        if format in SUPPORTED_FORMATS:
            self.format = format
        else:
            raise Exception("Unsupported format")
        super(WXAPPAPI, self).__init__(*args, **kwargs)


class WxAppCloudAPI(oauth2.OAuth2API):

    # 微信小程序云开发 http api SDK

    host = "api.weixin.qq.com"
    base_path = ""
    access_token_field = "access_token"
    authorize_url = ""
    access_token_url = "https://api.weixin.qq.com/sns/jscode2session"
    refresh_token_url = ""
    client_credential_token_url = "https://api.weixin.qq.com/cgi-bin/token"
    protocol = "https"
    api_name = "WxAppCloud"
    x_ratelimit_remaining = None
    x_ratelimit = None

    def __init__(self, *args, **kwargs):
        format = kwargs.get("format", "")
        if format in SUPPORTED_FORMATS:
            self.format = format
        else:
            raise Exception("Unsupported format")
        super(WxAppCloudAPI, self).__init__(*args, **kwargs)

    # 触发云函数
    invoke_func = bind_method(
        path="/tcb/invokecloudfunction",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )

    # 统计集合记录数或统计查询语句对应的结果记录数
    db_count = bind_method(
        path="/tcb/databasecount",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )

    # 数据库查询记录
    db_query = bind_method(
        path="/tcb/databasequery",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )

    # 数据库更新记录
    db_update = bind_method(
        path="/tcb/databaseupdate",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )

    # 数据库删除记录
    db_delete = bind_method(
        path="/tcb/databasedelete",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )

    # 数据库插入记录
    db_add = bind_method(
        path="/tcb/databaseadd",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )

    # 获取特定云环境下集合信息
    db_collection_info = bind_method(
        path="/tcb/databasecollectionget",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )

    # 删除集合
    db_collection_delete = bind_method(
        path="/tcb/databasecollectiondelete",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )

    # 新增集合
    db_collection_add = bind_method(
        path="/tcb/databasecollectionadd",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )

    # 数据库迁移状态查询
    db_migrate_query_info = bind_method(
        path="/tcb/databasemigratequeryinfo",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )

    # 数据库导出
    db_migrate_export = bind_method(
        path="/tcb/databasemigrateexport",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )

    # 数据库导入
    db_migrate_import = bind_method(
        path="/tcb/databasemigrateimport",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )

    # 上传文件 获取文件上传链接
    upload_file = bind_method(
        path="/tcb/uploadfile",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )

    # 获取文件下载链接
    batch_download_file = bind_method(
        path="/tcb/batchdownloadfile",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )
    batch_download_file.__doc__ = """
    获取文件下载链接
    参数：json_body  字典
        json_body 结构：
            env string 云环境ID
            file_list	Array.<Object>	文件列表
            file_list 的结构
            fileid	string	文件ID
            max_age	number	下载链接有效期
    batch_download_file(json_body={"env": "envid", [{"fileid": "cloud://test2-4a89da.7465-test2-4a89da/A.png", "max_age": 7200}]})
    """

    # 批量删除文件
    batch_delete_file = bind_method(
        path="/tcb/batchdeletefile",
        method="POST",
        accepts_parameters=["json_body"],
        response_type="entry",
    )
    batch_delete_file.__doc__ = """
    批量删除文件
    参数：json_body  字典
        json_body 结构：
            env string 云环境ID
            file_list	Array.string 文件列表
    example: batch_delete_file(json_body={"env": "envid", ["cloud://test2-4a89da.7465-test2-4a89da/A.png"]})
    """
