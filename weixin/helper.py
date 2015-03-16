# -*-coding: utf-8 -*-
# !/usr/bin/env python
from __future__ import unicode_literals

"""
File:   client.py
Author: goodspeed
Email:  cacique1103@gmail.com
Github: https://github.com/zongxiao
Date:   2015-02-11
Description: Weixin helpers
"""

from six.moves import html_parser


error_dict = {
    'AppID 参数错误': {
        'errcode': 40013,
        'errmsg': 'invalid appid'
    }
}


def get_encoding(html=None, headers=None):
    try:
        import chardet
        if html:
            encoding = chardet.detect(html).get('encoding')
            return encoding
    except ImportError:
        pass
    if headers:
        content_type = headers.get('content-type')
        try:
            encoding = content_type.split(' ')[1].split('=')[1]
            return encoding
        except IndexError:
            pass


class WeixiErrorParser(html_parser.HTMLParser):

    def __init__(self):
        html_parser.HTMLParser.__init__(self)
        self.recording = 0
        self.data = []

    def handle_starttag(self, tag, attrs):
        if tag != 'h4':
            return
        if self.recording:
            self.recording += 1
        self.recording = 1

    def handle_endtag(self, tag):
        if tag == 'h4' and self.recording:
            self.recording -= 1

    def handle_data(self, data):
        if self.recording:
            self.data.append(data)


def error_parser(error_html, encoding='gbk'):
    html = unicode(error_html, encoding or 'gbk')
    error_parser = WeixiErrorParser()
    error_parser.feed(html)
    if error_parser.data:
        return error_dict.get(error_parser.data[0], None)
