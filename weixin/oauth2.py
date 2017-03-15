# -*-coding: utf-8 -*-
# !/usr/bin/env python
# from __future__ import unicode_literals

"""
File:   oauth2.py
Author: goodspeed
Email:  cacique1103@gmail.com
Github: https://github.com/zongxiao
Date:   2015-02-06
Description: Weixin OAuth2
"""


import json
import requests
from requests.exceptions import (ConnectTimeout, ReadTimeout,
                                 ConnectionError as _ConnectionError)
from six.moves.urllib.parse import urlencode, urlparse


from .json_import import simplejson
from .helper import (error_parser, get_encoding, url_encode, iteritems,
                     text_type, smart_str)


TIMEOUT = 2


class OAuth2AuthExchangeError(Exception):
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def __str__(self):
        return '%s: %s' % (self.code, self.description)


class ConnectTimeoutError(Exception):
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def __str__(self):
        return '%s: %s' % (self.code, self.description)


class ConnectionError(Exception):
    def __init__(self, code, description):
        self.code = code
        self.description = description

    def __str__(self):
        return '%s: %s' % (self.code, self.description)


class OAuth2API(object):
    host = None
    base_path = None
    authorize_url = None
    access_token_url = None
    refresh_token_url = None
    client_credential_token_url = None
    redirect_uri = None
    # some providers use "oauth_token"
    access_token_field = "access_token"
    protocol = "https"
    # override with 'Instagram', etc
    api_name = "Generic API"

    def __init__(self, appid=None, app_secret=None,
                 access_token=None, timestamp=None, nonce=None,
                 signature=None, mp_token=None, echostr=None,
                 body=None, xml_body=None, json_body=None,
                 redirect_uri=None, grant_type=None):
        self.appid = appid
        self.app_secret = app_secret
        self.access_token = access_token
        self.redirect_uri = redirect_uri
        self.grant_type = grant_type

    def client_credential_for_access_token(self):
        req = OAuth2AuthExchangeRequest(self)
        return req.exchange_for_access_token()

    def get_authorize_url(self, scope=None, state=None):
        req = OAuth2AuthExchangeRequest(self)
        return req.get_authorize_url(scope=scope, state=state)

    def get_authorize_login_url(self, scope=None, state=None):
        """ scope should be a tuple or list of requested scope access levels """
        req = OAuth2AuthExchangeRequest(self)
        return req.get_authorize_login_url(scope=scope, state=state)

    def exchange_code_for_access_token(self, code):
        req = OAuth2AuthExchangeRequest(self)
        return req.exchange_for_access_token(code=code)

    def exchange_refresh_token_for_access_token(self, refresh_token):
        req = OAuth2AuthExchangeRequest(self)
        return req.exchange_for_access_token(refresh_token=refresh_token)

    def exchange_code_for_session_key(self, code):
        req = OAuth2AuthExchangeRequest(self)
        return req.exchange_for_session_key(js_code=code)


class OAuth2AuthExchangeRequest(object):
    def __init__(self, api):
        self.api = api

    def _url_for_authorize(self, scope=None, state=None):
        client_params = {
            "appid": self.api.appid,
            "response_type": "code",
            "redirect_uri": self.api.redirect_uri,
        }
        if scope:
            client_params.update(scope=' '.join(scope))
        if state:
            client_params.update(state=state)
        # url_params = urlencode(client_params)
        url_params = url_encode(client_params, sort=True)
        return "%s?%s" % (self.api.authorize_url, url_params)

    def _data_for_exchange(self, code=None, js_code=None,
                           refresh_token=None, scope=None):
        app_params = {
            "appid": self.api.appid,
        }
        if code:
            app_params.update(code=code,
                              secret=self.api.app_secret,
                              redirect_uri=self.api.redirect_uri,
                              grant_type="authorization_code")
        elif js_code:
            app_params.update(js_code=js_code,
                              secret=self.api.app_secret,
                              grant_type="authorization_code")
        elif refresh_token:
            app_params.update(refresh_token=refresh_token,
                              grant_type="refresh_token")
        elif self.api.app_secret:
            app_params.update(secret=self.api.app_secret,
                              grant_type=self.api.grant_type)
        if scope:
            app_params.update(scope=' '.join(scope))
        str_app_parmas = {}
        for k, v in iteritems(app_params):
            str_app_parmas[k] = text_type(v).encode('utf-8')
        url_params = urlencode(str_app_parmas)
        if code:
            return "%s?%s" % (self.api.access_token_url, url_params)
        elif js_code:
            return "%s?%s" % (self.api.access_token_url, url_params)
        elif refresh_token:
            return "%s?%s" % (self.api.refresh_token_url, url_params)
        elif self.api.app_secret:
            return "%s?%s" % (self.api.client_credential_token_url, url_params)

    def get_authorize_url(self, scope=None, state=None):
        return self._url_for_authorize(scope=scope, state=state)

    def get_authorize_login_url(self, scope=None, state=None):
        url = self._url_for_authorize(scope=scope, state=state)
        try:
            response = requests.get(url, timeout=TIMEOUT)
        except (ConnectTimeout, ReadTimeout):
            raise ConnectTimeoutError('timeout', 'Connect timeout')
        except _ConnectionError:
            raise ConnectionError('conntect_error',
                                  'Failed to establish a new connection')
        headers = response.headers
        if int(headers.get('content-length', 384)) < 500:
            # 微信 参数错误返回html页面 http 状态码也是200
            # 暂时只能根据数据大小判断
            encoding = get_encoding(headers=headers)
            error_data = error_parser(response.content, encoding)
            if error_data:
                raise OAuth2AuthExchangeError(
                    error_data.get("errcode", 0),
                    error_data.get("errmsg", ""))
        return url

    def exchange_for_access_token(self, code=None,
                                  refresh_token=None, scope=None):
        access_token_url = self._data_for_exchange(
            code, refresh_token, scope=scope)
        try:
            response = requests.get(access_token_url, timeout=TIMEOUT)
        except (ConnectTimeout, ReadTimeout):
            raise ConnectTimeoutError('timeout', 'Connect timeout')
        except _ConnectionError:
            raise ConnectionError('conntect_error',
                                  'Failed to establish a new connection')
        parsed_content = simplejson.loads(response.content.decode())
        if parsed_content.get('errcode', 0):
            raise OAuth2AuthExchangeError(
                parsed_content.get("errcode", 0),
                parsed_content.get("errmsg", ""))
        return parsed_content

    def exchange_for_session_key(self, js_code=None, scope=None):
        access_token_url = self._data_for_exchange(js_code=js_code, scope=scope)
        try:
            response = requests.get(access_token_url, timeout=TIMEOUT)
        except (ConnectTimeout, ReadTimeout):
            raise ConnectTimeoutError('timeout', 'Connect timeout')
        except _ConnectionError:
            raise ConnectionError('conntect_error',
                                  'Failed to establish a new connection')
        parsed_content = simplejson.loads(response.content.decode())
        if parsed_content.get('errcode', 0):
            raise OAuth2AuthExchangeError(
                parsed_content.get("errcode", 0),
                parsed_content.get("errmsg", ""))
        return parsed_content


class OAuth2Request(object):

    def __init__(self, api):
        self.api = api
        self.host = 'api.weixin.qq.com'

    def url_for_get(self, path, parameters):
        return self._full_url_with_params(path, parameters)

    def get_request(self, path, **kwargs):
        return self.make_request(self.prepare_request("GET", path, kwargs))

    def post_request(self, path, **kwargs):
        return self.make_request(self.prepare_request("POST", path, kwargs))

    def _full_url(self, path, include_secret=False):
        auth_query = self._auth_query(include_secret)
        base_url = '%s://%s%s%s' % (self.api.protocol,
                                    self.host,
                                    self.api.base_path,
                                    path)
        if auth_query:
            return '%s?%s' % (base_url, auth_query)
        return base_url

    def _full_url_with_params(self, path, params, include_secret=False):
        base_url = self._full_url(path, include_secret)
        base_query = urlparse(base_url).query
        other_query = self._full_query_with_params(params)
        if base_query and other_query:
            return '%s&%s' % (base_url, other_query)
        elif other_query:
            return '%s?%s' % (base_url, other_query)
        else:
            return base_url

    def _full_query_with_params(self, params):
        params = urlencode(params) if params else ""
        return params

    def _auth_query(self, include_secret=False):
        if self.api.access_token:
            return ("%s=%s" % (self.api.access_token_field,
                                self.api.access_token))
        return ''

    def _post_body(self, params):
        return urlencode(params)

    def _encode_multipart(params, files):
        pass

    def perpare_and_make_request(self, method, path,
                                 params, include_secret=False):
        url, method, body, json_body,  headers = self.prepare_request(
            method, path, params, include_secret)
        return self.make_request(url, method, body, json_body, headers)

    def prepare_request(self, method, path, params, include_secret=False):
        url = body = None
        headers = {}

        json_body = params.pop('json_body', None)
        if not params.get('files'):
            if method == 'POST':
                body = self._post_body(params)
                headers = {'Content-type': 'application/x-www-form-urlencoded'}
                url = self._full_url(path, include_secret)
            else:
                url = self._full_url_with_params(path, params, include_secret)
        else:
            body, headers = self._encode_multipart(params, params['files'])
            url = self._full_url(path)

        return url, method, body, json_body, headers

    def make_request(self, url, method="GET", body=None,
                     xml_body=None, json_body=None, headers=None):
        headers = headers or {}

        # if 'User-Agent' not in headers:
        #     headers.update({b"User-Agent":
        #                     b"%s Python Client" % self.api.api_name})
        if json_body:
            headers['Content-type'] = 'application/json'
            body = json.dumps(json_body, ensure_ascii=False)
            body = smart_str(body)
        if xml_body:
            headers['Content-type'] = 'application/xml'
            #TODO xml
            body = json.dumps(json_body, ensure_ascii=False)
        try:
            return requests.request(method, url, data=body,
                                    headers=headers, timeout=TIMEOUT)
        except (ConnectTimeout, ReadTimeout):
            raise ConnectTimeoutError('timeout', 'Connect timeout')
        except _ConnectionError:
            raise ConnectionError('conntect_error',
                                  'Failed to establish a new connection')
