# -*- coding: utf-8 -*-
from __future__ import unicode_literals

TEXT_TEMPLATE = """
<xml>
    <ToUserName><![CDATA[{to_user}]]></ToUserName>
    <FromUserName><![CDATA[{from_user}]]></FromUserName>
    <CreateTime>{create_time}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{content}]]></Content>
</xml>
"""

IMAGE_TEMPLATE = """
<xml>
    <ToUserName><![CDATA[{to_user}]]></ToUserName>
    <FromUserName><![CDATA[{from_user}]]></FromUserName>
    <CreateTime>{create_time}</CreateTime>
    <MsgType><![CDATA[image]]></MsgType>
    <Image>
        <MediaId><![CDATA[{media_id}]]></MediaId>
    </Image>
</xml>
"""

VOICE_TEMPLATE = """
<xml>
    <ToUserName><![CDATA[{to_user}]]></ToUserName>
    <FromUserName><![CDATA[{from_user}]]></FromUserName>
    <CreateTime>{create_time}</CreateTime>
    <MsgType><![CDATA[voice]]></MsgType>
    <Voice>
        <MediaId><![CDATA[{media_id}]]></MediaId>
    </Voice>
</xml>
"""

VIDEO_TEMPLATE = """
<xml>
    <ToUserName><![CDATA[{to_user}]]></ToUserName>
    <FromUserName><![CDATA[{from_user}]]></FromUserName>
    <CreateTime>{create_time}</CreateTime>
    <MsgType><![CDATA[video]]></MsgType>
    <Video>
        <MediaId><![CDATA[{media_id}]]></MediaId>
        <Title><![CDATA[{title}]]></Title>
        <Description><![CDATA[{description}]]></Description>
    </Video>
</xml>
"""

THUM_MUSIC_TEMPLATE = """
<xml>
    <ToUserName><![CDATA[{to_user}]]></ToUserName>
    <FromUserName><![CDATA[{from_user}]]></FromUserName>
    <CreateTime>{create_time}</CreateTime>
    <MsgType><![CDATA[music]]></MsgType>
    <Music>
        <Title><![CDATA[{title}]]></Title>
        <Description><![CDATA[{description}]]></Description>
        <MusicUrl><![CDATA[{music_url}]]></MusicUrl>
        <HQMusicUrl><![CDATA[{hq_music_url}]]></HQMusicUrl>
        <ThumbMediaId><![CDATA[{thumb_media_id}]]></ThumbMediaId>
    </Music>
</xml>
"""

NOTHUM_MUSIC_TEMPLATE = """
<xml>
    <ToUserName><![CDATA[{to_user}]]></ToUserName>
    <FromUserName><![CDATA[{from_user}]]></FromUserName>
    <CreateTime>{create_time}</CreateTime>
    <MsgType><![CDATA[music]]></MsgType>
    <Music>
        <Title><![CDATA[{title}]]></Title>
        <Description><![CDATA[{description}]]></Description>
        <MusicUrl><![CDATA[{music_url}]]></MusicUrl>
        <HQMusicUrl><![CDATA[{hq_music_url}]]></HQMusicUrl>
    </Music>
</xml>
"""

ARITICLE_TEMPLATE = """
<xml>
    <ToUserName><![CDATA[{to_user}]]></ToUserName>
    <FromUserName><![CDATA[{from_user}]]></FromUserName>
    <CreateTime>{create_time}</CreateTime>
    <MsgType><![CDATA[news]]></MsgType>
    <ArticleCount>{count}</ArticleCount>
    <Articles>{items}</Articles>
</xml>
"""

ARITICLE_ITEM_TEMPLATE = """
    <item>
    <Title><![CDATA[{title}]]></Title>
    <Description><![CDATA[{description}]]></Description>
    <PicUrl><![CDATA[{picurl}]]></PicUrl>
    <Url><![CDATA[{url}]]></Url>
    </item>
"""
