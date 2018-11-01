# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .reply import TextReply
from .config import AUTO_REPLY_CONTENT


ALLOWED_MSG_TYPES = set(['text', 'image', 'voice', 'video', 'miniprogrampage',
                         'shortvideo', 'location', 'link'])
ALLOWED_EVENTS = set(['subscribe', 'unsubscribe', 'unsub_scan',
                      'scan', 'click', 'location', 'view',
                      'templatesendjobfinish'])


class WXResponse(object):

    auto_reply_content = AUTO_REPLY_CONTENT

    def __init__(self, xml_dict):
        # 微信请求的数据
        self.data = xml_dict.get('xml') or xml_dict
        self.reply_params = {}
        self.reply = None

    def __call__(self):
        # make response
        return self.make_response()

    def check_event(self):
        '''
        接收的事件
        subscribe：订阅
        unsubscribe：取消订阅
        subscribe+EventKey+Ticket：用户未关注时，进行关注后的事件
        SCAN：用户已关注时扫描二维码
        LOCATION: 上报地理位置
        CLICK: 点击菜单
        VIEW: 点击菜单链接
        '''
        event = self.data.get('Event')
        if not event:
            return None
        if event == 'subscribe':
            if self.data.get('EventKey') and self.data.get('Ticket'):
                return 'unsub_scan'
            return event
        return event.lower()

    def _subscribe_event_handler(self):
        # 订阅事件处理逻辑
        self.reply_params['content'] = self.auto_reply_content
        self.reply = TextReply(**self.reply_params).render()

    def _unsubscribe_event_handler(self):
        # 取消订阅事件处理逻辑
        pass

    def _unsub_scan_event_handler(self):
        # 扫描二维码 用户未关注时，进行关注后的事件
        pass

    def _scan_event_handler(self):
        # 用户已关注时扫描二维码
        pass

    def _click_event_handler(self):
        # 点击菜单事件的逻辑
        pass

    def _location_event_handler(self):
        # 上报地理位置的处理逻辑
        pass

    def _view_event_handler(self):
        # 点击菜单链接的逻辑
        pass

    def _templatesendjobfinish_event_handler(self):
        # 模板消息推送完成逻辑
        pass

    def _text_msg_handler(self):
        # 文字消息处理逻辑
        self.reply_params['content'] = self.auto_reply_content
        self.reply = TextReply(**self.reply_params).render()

    def _image_msg_handler(self):
        # 图片消息处理逻辑
        pass

    def _voice_msg_handler(self):
        # 语音消息处理逻辑
        pass

    def _video_msg_handler(self):
        # 视频消息处理逻辑
        pass

    def _shortvideo_msg_handler(self):
        # 小视频消息处理逻辑
        pass

    def _location_msg_handler(self):
        # 地理位置消息处理逻辑
        pass

    def _link_msg_handler(self):
        # 链接消息处理逻辑
        pass

    def _miniprogrampage_msg_handler(self):
        # 小程序卡片处理逻辑
        pass

    def _data_handler(self):
        # 只取出消息类型和事件
        msg_type = self.data.get('MsgType')
        self.reply_params['to_user'] = self.data.get('FromUserName')
        self.reply_params['from_user'] = self.data.get('ToUserName')
        event = None
        if msg_type == 'event':
            event = self.check_event()
        elif msg_type == 'miniprogrampage':
            event = 'miniprogrampage'
        return msg_type, event

    def _event_handler(self, event):
        if event not in ALLOWED_EVENTS:
            # TODO raise except
            return
        methodname = '_{0}_event_handler'.format(event)
        method = getattr(self, methodname, None)
        if method:
            return method()
        return

    def handler(self):
        msg_type, event = self._data_handler()
        if msg_type == 'event':
            return self._event_handler(event)
        elif msg_type in ALLOWED_MSG_TYPES:
            methodname = '_{0}_msg_handler'.format(msg_type)
            return getattr(self, methodname, None)()
        else:
            # TODO raise except
            pass

    def make_response(self):
        """
        :param reply:  WXReply.render(**args)
        """
        self.handler()
        if not self.reply:
            return 'success'
        return self.reply
