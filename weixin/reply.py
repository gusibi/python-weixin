# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# https://github.com/wechat-python-sdk/wechat-python-sdk/blob/master/wechat_sdk/reply.py

import time

from .msg_template import (TEXT_TEMPLATE, IMAGE_TEMPLATE,
                           VOICE_TEMPLATE, VIDEO_TEMPLATE,
                           THUM_MUSIC_TEMPLATE, NOTHUM_MUSIC_TEMPLATE,
                           ARITICLE_TEMPLATE, ARITICLE_ITEM_TEMPLATE)


class WXReply(object):

    def __init__(self, to_user=None, from_user=None, create_time=None, **kwargs):
        '''
        MsgType: text|image|voice|video|music|news
        '''
        kwargs['to_user'] = to_user
        kwargs['from_user'] = from_user
        kwargs['create_time'] = create_time or int(time.time())

        self.params = {k: v for k, v in kwargs.items() if kwargs[k]}

    def render(self):
        raise NotImplementedError()


class TextReply(WXReply):
    """
    回复文字消息
    """
    TEMPLATE = TEXT_TEMPLATE

    def __init__(self, content, *args, **kwargs):
        """
        :param content: 文字回复内容
        """
        super(TextReply, self).__init__(content=content, *args, **kwargs)

    def render(self):
        return self.TEMPLATE.format(**self.params)


class ImageReply(WXReply):
    """
    回复图片消息
    """
    TEMPLATE = IMAGE_TEMPLATE

    def __init__(self, media_id):
        """
        :param media_id: 图片的 MediaID
        """
        super(ImageReply, self).__init__(media_id=media_id)

    def render(self):
        return self.TEMPLATE.format(**self.params)


class VoiceReply(WXReply):
    """
    回复语音消息
    """
    TEMPLATE = VOICE_TEMPLATE

    def __init__(self, media_id):
        """
        :param media_id: 语音的 MediaID
        """
        super(VoiceReply, self).__init__(media_id=media_id)

    def render(self):
        return self.TEMPLATE.format(**self.params)


class VideoReply(WXReply):
    """
    回复视频消息
    """

    TEMPLATE = VIDEO_TEMPLATE

    def __init__(self, media_id, title=None, description=None):
        """
        :param media_id: 视频的 MediaID
        :param title: 视频消息的标题
        :param description: 视频消息的描述
        """
        title = title or ''
        description = description or ''
        super(VideoReply, self).__init__(media_id=media_id, title=title,
                                         description=description)

    def render(self):
        return self.TEMPLATE.format(**self.params)


class MusicReply(WXReply):
    """
    回复音乐消息
    """
    TEMPLATE_THUMB = THUM_MUSIC_TEMPLATE
    TEMPLATE_NOTHUMB = NOTHUM_MUSIC_TEMPLATE

    def __init__(self, title='', description='', music_url='',
                 hq_music_url='', thumb_media_id=None):
        title = title or ''
        description = description or ''
        music_url = music_url or ''
        hq_music_url = hq_music_url or music_url
        super(MusicReply, self).__init__(
            title=title, description=description, music_url=music_url,
            hq_music_url=hq_music_url, thumb_media_id=thumb_media_id)

    def render(self):
        if self._args['thumb_media_id']:
            return self.TEMPLATE.format(**self.params)
        else:
            return self.TEMPLATE.format(**self.params)


class ArticleReply(WXReply):

    TEMPLATE = ARITICLE_TEMPLATE
    ITEM_TEMPLATE = ARITICLE_ITEM_TEMPLATE

    def __init__(self, **kwargs):
        super(ArticleReply, self).__init__(**kwargs)
        self._articles = []

    def render(self):
        items = []
        for article in self._articles:
            items.append(ArticleReply.ITEM_TEMPLATE.format(
                title=article.title,
                description=article.description,
                picurl=article.picurl,
                url=article.url,
            ))
        self.params["items"] = ''.join(items)
        self.params["count"] = len(items)
        return self.TEMPLATE.format(**self.params)
