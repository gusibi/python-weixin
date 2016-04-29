# -*-coding: utf-8 -*-
# !/usr/bin/env python
from __future__ import unicode_literals

"""
File:   bind.py
Author: goodspeed
Email:  cacique1103@gmail.com
Github: https://github.com/zongxiao
Date:   2015-02-12
Description: WeixinAPI bind
"""

import re
import six
import hmac
from hashlib import sha256
from six.moves.urllib.parse import quote

from .oauth2 import OAuth2Request
from .json_import import simplejson


re_path_template = re.compile('{\w+}')


def encode_string(value):
    return value.encode('utf-8') \
        if isinstance(value, six.text_type) else str(value)


class WeixinClientError(Exception):

    def __init__(self, error_message, status_code=None):
        self.status_code = status_code,
        self.error_message = error_message

    def __str__(self):
        if self.status_code:
            return "(%s) %s" % (self.status_code, self.error_message)
        else:
            return self.error_message


class WeixinAPIError(Exception):

    def __init__(self, status_code, error_type, error_message, *args, **kwargs):
        self.status_code = status_code
        self.error_type = error_type
        self.error_message = error_message

    def __str__(self):
        return "(%s) %s-%s" % (self.status_code, self.error_type,
                               self.error_message)


def bind_method(**config):

    class WeixinAPIMethod(object):

        path = config['path']
        method = config.get('method', 'GET')
        accepts_parameters = config.get("accepts_parameters", [])
        signature = config.get("signature", False)
        requires_target_user = config.get('requires_target_user', False)
        paginates = config.get('paginates', False)
        root_class = config.get('root_class', None)
        response_type = config.get("response_type", "list")
        include_secret = config.get("include_secret", False)
        objectify_response = config.get("objectify_response", True)

        def __init__(self, api, *args, **kwargs):
            self.api = api
            self.as_generator = kwargs.pop("as_generator", False)
            self.return_json = kwargs.pop("return_json", True)
            self.parameters = {}
            self._build_parameters(args, kwargs)
            self._build_path()

        def _build_parameters(self, args, kwargs):
            for index, value in enumerate(args):
                if value is None:
                    continue
                try:
                    self.parameters[self.accepts_parameters[index]] = encode_string(value)
                except IndexError:
                    raise WeixinClientError("Too many arguments supplied")

            for key, value in six.iteritems(kwargs):
                if value is None:
                    continue
                if key in self.parameters:
                    raise WeixinClientError("Parameter %s already supplied" % key)
                if key not in set(['json_body']):
                    value = encode_string(value)
                self.parameters[key] = value

            # if 'openid' in self.accepts_parameters and \
            #         'openid' not in self.parameters and \
            #         not self.requires_target_user:
            #     self.parameters['openid'] = 'self'

        def _build_path(self):
            for variable in re_path_template.findall(self.path):
                name = variable.strip('{}')

                try:
                    value = quote(self.parameters[name])
                except KeyError:
                    raise Exception('No parameter value found for path variable: %s' % name)
                del self.parameters[name]

                self.path = self.path.replace(variable, value)

            if self.api.format:
                self.path = self.path + '.%s' % self.api.format
            else:
                self.path = self.path

        def _build_pagination_info(self, content_obj):
            pass

        def _do_api_request(self, url, method='GET', body=None,
                            json_body=None, headers=None):
            headers = headers or {}
            if self.signature and self.api.app_secret is not None:
                secret = self.api.app_secret
                signature = hmac.new(secret, sha256).hexdigest()
                headers['X-Weixin-Forwarded-For'] = '|'.join([signature])
            response = OAuth2Request(self.api).make_request(
                url, method=method, body=body,
                json_body=json_body, headers=headers)
            status_code = response.status_code
            try:
                content_obj = simplejson.loads(response.content)
            except ValueError:
                raise WeixinClientError(
                    'Unable to parse response, not valid JSON.',
                    status_code=status_code)

            api_responses = []
            if status_code == 200:
                if not self.objectify_response:
                    return content_obj, None

                if self.response_type == 'list':
                    for entry in content_obj['data']:
                        if self.return_json:
                            api_responses.append(entry)
                elif self.response_type == 'entry':
                    data = content_obj
                    if self.return_json:
                        api_responses = data
                elif self.response_type == 'empty':
                    pass
                return api_responses, self._build_pagination_info(content_obj)
            else:
                raise WeixinAPIError(
                    status_code, content_obj['errcode'], content_obj['errmsg'])

        def _paginator_with_url(self, url, method="GET", body=None, headers=None):
            pass

        def _get_with_next_url(self, url, method="GET", body=None, headers=None):
            pass

        def execute(self):
            url, method, body, json_body, headers = (
                OAuth2Request(self.api).prepare_request(
                    self.method, self.path, self.parameters,
                    include_secret=self.include_secret))
            if self.as_generator:
                return self._paginator_with_url(url, method, body, headers)
            else:
                content, next = self._do_api_request(url, method, body,
                                                     json_body, headers)
            if self.paginates:
                return content, next
            else:
                return content

    def _call(api, *args, **kwargs):
        method = WeixinAPIMethod(api, *args, **kwargs)
        return method.execute()

    return _call
