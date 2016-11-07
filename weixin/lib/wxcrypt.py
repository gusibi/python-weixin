# -*- coding:utf-8 -*-

"""
对小程序获取的用户信息解密代码.
"""
import base64
from Crypto.Cipher import AES

from ..json_import import simplejson as json


class WXBizDataCrypt:

    def __init__(self, appid, session_key):
        self.appid = appid
        self.session_key = session_key

    def decrypt(self, encrypted_data, iv):
        '''
        aes decode
        将加密后的信息解密
        @param encrypted_data: 包括敏感数据在内的完整用户信息的加密数据
        @param iv: 加密算法的初始向量
        @return: 解密后数据
        '''
        session_key = base64.b64decode(self.session_key)
        encrypted_data = base64.b64decode(encrypted_data)
        iv = base64.b64decode(iv)

        cipher = AES.new(session_key, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encrypted_data)))

        if decrypted['watermark']['appid'] != self.appid:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]
