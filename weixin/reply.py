# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# https://github.com/wechat-python-sdk/wechat-python-sdk/blob/master/wechat_sdk/reply.py

import time

from .msg_template import (TEXT_TEMPLATE, IMAGE_TEMPLATE,
                           VOICE_TEMPLATE, VIDEO_TEMPLATE,
                           THUM_MUSIC_TEMPLATE, NOTHUM_MUSIC_TEMPLATE,
                           ARITICLE_TEMPLATE, ARITICLE_ITEM_TEMPLATE)


class Article(object):

    def __init__(self, title=None, description=None, picurl=None, url=None):
        self.title = title or ''
        self.description = description or ''
        self.picurl = picurl or ''
        self.url = url or ''


class WXReply(object):

    def __init__(self, to_user=None, from_user=None,
                 create_time=None, **kwargs):
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

    def __init__(self, media_id, *args, **kwargs):
        """
        :param media_id: 图片的 MediaID
        """
        super(ImageReply, self).__init__(media_id=media_id, *args, **kwargs)

    def render(self):
        return self.TEMPLATE.format(**self.params)


class VoiceReply(WXReply):
    """
    回复语音消息
    """
    TEMPLATE = VOICE_TEMPLATE

    def __init__(self, media_id, *args, **kwargs):
        """
        :param media_id: 语音的 MediaID
        """
        super(VoiceReply, self).__init__(media_id=media_id, *args, **kwargs)

    def render(self):
        return self.TEMPLATE.format(**self.params)


class VideoReply(WXReply):
    """
    回复视频消息
    """

    TEMPLATE = VIDEO_TEMPLATE

    def __init__(self, media_id, title=None, description=None,
                 *args, **kwargs):
        """
        :param media_id: 视频的 MediaID
        :param title: 视频消息的标题
        :param description: 视频消息的描述
        """
        title = title or ''
        description = description or ''
        super(VideoReply, self).__init__(media_id=media_id, title=title,
                                         description=description,
                                         *args, **kwargs)

    def render(self):
        return self.TEMPLATE.format(**self.params)


class MusicReply(WXReply):
    """
    回复音乐消息
    """
    TEMPLATE_THUMB = THUM_MUSIC_TEMPLATE
    TEMPLATE_NOTHUMB = NOTHUM_MUSIC_TEMPLATE

    def __init__(self, title='', description='', music_url='',
                 hq_music_url='', thumb_media_id=None, *args, **kwargs):
        self.title = title or ''
        self.description = description or ''
        self.music_url = music_url or ''
        self.hq_music_url = hq_music_url or music_url
        self.thumb_media_id = thumb_media_id or ''
        super(MusicReply, self).__init__(
            title=self.title, description=self.description,
            music_url=self.music_url,
            hq_music_url=self.hq_music_url,
            thumb_media_id=self.thumb_media_id)

    def render(self):
        if self.thumb_media_id:
            return self.TEMPLATE_THUMB.format(**self.params)
        else:
            return self.TEMPLATE_NOTHUMB.format(**self.params)


class ArticleReply(WXReply):

    TEMPLATE = ARITICLE_TEMPLATE
    ITEM_TEMPLATE = ARITICLE_ITEM_TEMPLATE

    def __init__(self, **kwargs):
        super(ArticleReply, self).__init__(**kwargs)
        self._articles = []

    def add_article(self, article):
        if len(self._articles) >= 8:
            raise AttributeError(
                "Can't add more than 8 articles in an ArticleReply")
        else:
            self._articles.append(article)

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


class WXCustomReply(object):

    def __init__(self, to_user=None, msgtype=None, **kwargs):
        '''
        MsgType: text|image|voice|video|music|news
        '''
        kwargs['to_user'] = to_user
        kwargs['msgtype'] = msgtype

        self.params = {k: v for k, v in kwargs.items() if kwargs[k]}

    def render(self):
        raise NotImplementedError()


class CustomTextReply(WXCustomReply):
    """
    回复文字消息
    """

    def __init__(self, content, *args, **kwargs):
        """
        :param content: 文字回复内容
        """
        super(CustomTextReply, self).__init__(msgtype='text',
                                              *args, **kwargs)
        self.content = content

    def render(self):
        self.params['text'] = {
            'content': self.content
        }
        return self.params


class CustomImageReply(WXCustomReply):
    """
    回复图片消息
    """

    def __init__(self, media_id, *args, **kwargs):
        """
        :param media_id: 图片的 MediaID
        """
        super(CustomImageReply, self).__init__(msgtype='image', *args, **kwargs)
        self.media_id = media_id

    def render(self):
        self.params['image'] = {
            'media_id': self.media_id
        }
        return self.params


class CustomVoiceReply(WXCustomReply):
    """
    回复语音消息
    """

    def __init__(self, media_id, *args, **kwargs):
        """
        :param media_id: 语音的 MediaID
        """
        super(CustomVoiceReply, self).__init__(msgtype='voice',
                                               *args, **kwargs)
        self.media_id = media_id

    def render(self):
        self.params['image'] = {
            'media_id': self.media_id
        }
        return self.params


class CustomVideoReply(WXCustomReply):
    """
    回复视频消息
    """

    def __init__(self, media_id, title=None, description=None,
                 *args, **kwargs):
        """
        :param media_id: 视频的 MediaID
        :param title: 视频消息的标题
        :param description: 视频消息的描述
        """
        super(CustomVideoReply, self).__init__(msgtype='music', *args, **kwargs)
        self.media_id = media_id
        self.title = title or ''
        self.description = description or ''

    def render(self):
        self.params['video'] = {
            'media_id': self.media_id,
            'title': self.title,
            'description': self.description
        }
        return self.params


class CustomMusicReply(WXCustomReply):
    """
    回复音乐消息
    """

    def __init__(self, title='', description='', music_url='',
                 hq_music_url='', thumb_media_id=None,
                 *args, **kwargs):
        self.title = title or ''
        self.description = description or ''
        self.musicurl = music_url or ''
        self.hqmusicurl = hq_music_url or music_url
        self.thumb_media_id = thumb_media_id
        super(CustomMusicReply, self).__init__(msgtype='music',
                                               *args, **kwargs)

    def render(self):
        self.params['music'] = {
            'title': self.title,
            'description': self.description,
            'musicurl': self.musicurl,
            'hqmusicurl': self.hqmusicurl,
            'thumb_media_id': self.thumb_media_id,
        }
        return self.params


class CustomArticleReply(WXCustomReply):

    def __init__(self, **kwargs):
        self._articles = []
        super(CustomArticleReply, self).__init__(msgtype='news', **kwargs)

    def add_article(self, article):
        '''
        :params article (dict)
        {
            "title":"Happy Day",
            "description":"Is Really A Happy Day",
            "url":"URL",
            "picurl":"PIC_URL"
        }

        '''
        if len(self._articles) >= 8:
            raise AttributeError(
                "Can't add more than 8 articles in an CustomArticleReply")
        else:
            self._articles.append(article)

    def render(self):
        items = []
        for article in self._articles:
            items.append(article)
        self.params['news'] = {'articles': items}
        return self.params
