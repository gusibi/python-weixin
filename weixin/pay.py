# -*- coding: utf-8 -*-
'''
Created on 2016-05-01
微信接口
@author: zongxiao
'''

import time
import string
import random
import socket

import requests
import xmltodict

from weixin.helper import smart_str, smart_unicode, md5_constructor as md5

TIMEOUT = 5

try:
    SPBILL_CREATE_IP = socket.gethostbyname(socket.gethostname())
except:
    SPBILL_CREATE_IP = '127.0.0.1'


def generate_nonce_str(length=32):
    return ''.join(random.SystemRandom().choice(
        string.ascii_letters + string.digits) for _ in range(length))


def params_encoding(params, charset='utf-8'):
    newparams = {}
    for k, v in params.items():
        newparams[k] = smart_unicode(v)
    return newparams


def params_filter(params, delimiter='&', charset='utf-8',
                  excludes=['sign', 'sign_type']):
    ks = params.keys()
    ks.sort()
    newparams = {}
    prestr = ''
    if params.get('input_charset', None):
        charset = params['input_charset']
    for k in ks:
        v = params[k]
        k = smart_str(k, charset)
        if k not in excludes and v != '':
            newparams[k] = smart_str(v, charset)
            prestr += '%s=%s%s' % (k, newparams[k], delimiter)
    prestr = prestr[:-1]
    return newparams, prestr


# 生成签名结果
def build_mysign(prestr, key=None, sign_type='MD5'):
    if sign_type == 'MD5':
        prestr += '&key=%s' % str(key)
        return md5(prestr).hexdigest().upper()
    return ''


class WeixinPay(object):

    BASE_URL = 'https://api.mch.weixin.qq.com/'
    PAY_SOURCE = 'weixin'

    def __init__(self, appid, mch_id, *args, **kwargs):
        """
        微信支付接口
        :param appid: 微信公众号 appid
        :param api_key: 商户 key
        :param mch_id: 商户号
        :param sub_mch_id: 可选，子商户号，受理模式下必填
        :param mch_cert: 可选，商户证书路径 申请退款必须
        :param mch_key: 可选，商户证书私钥路径 申请退款必选
        :param notify_url: 可选 接收微信支付异步通知回调地址 统一下单接口必选
        :param partner_key: 商户支付Key
        """
        self.appid = appid
        self.mch_id = mch_id
        self.mch_cert = kwargs.get('mch_cert')
        self.mch_key = kwargs.get('mch_key')
        self.notify_url = kwargs.get('notify_url')
        self.partner_key = kwargs.get('partner_key')

    def _full_url(self, path):
        return '%s%s' % (self.BASE_URL, path)

    def get_base_params(self):
        params = {
            'appid': self.appid,                    # 公众账号ID
            'mch_id': self.mch_id,                  # 商户号
            'nonce_str': generate_nonce_str(),      # 随机字符串
        }
        return params

    def prepare_request(self, method, path, params):
        kwargs = {}
        _params = self.get_base_params()
        params.update(_params)
        newparams, prestr = params_filter(params)
        sign = build_mysign(prestr, self.partner_key)
        # 将内容转化为unicode xmltodict 只支持unicode
        newparams = params_encoding(newparams)
        newparams['sign'] = sign
        xml_dict = {'xml': newparams}
        kwargs['data'] = smart_str(xmltodict.unparse(xml_dict))
        url = self._full_url(path)
        if self.mch_cert and self.mch_key:
            kwargs['cert'] = (self.mch_cert, self.mch_key)
        return method, url, kwargs

    # 统一下单
    # https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_1
    def unifiedorder(self, body='', out_trade_no='', total_fee='', openid='',
                     detail='', attach='', time_start='', time_expire='',
                     goods_tag='', product_id='', limit_pay='', device_info='',
                     fee_type='CNY', spbill_create_ip=SPBILL_CREATE_IP,
                     trade_type='JSAPI', notify_url=''):
        """
        统一下单接口
        https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_1
        :param trade_type: 交易类型，取值如下：JSAPI，NATIVE，APP，WAP, MWEB
        :param body: 商品描述
        :param total_fee: 总金额，单位分
        :param notify_url: 接收微信支付异步通知回调地址
        :param client_ip: 可选，APP和网页支付提交用户端ip，Native支付填调用微信支付API的机器IP
        :param openid: 可选，用户在商户appid下的唯一标识。trade_type=JSAPI，此参数必传
        :param out_trade_no: 可选，商户订单号，默认自动生成
        :param detail: 可选，商品详情
        :param attach: 可选，附加数据，在查询API和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据
        :param fee_type: 可选，符合ISO 4217标准的三位字母代码，默认人民币：CNY
        :param time_start: 可选，订单生成时间，默认为当前时间
        :param time_expire: 可选，订单失效时间，默认为订单生成时间后两小时
        :param goods_tag: 可选，商品标记，代金券或立减优惠功能的参数
        :param product_id: 可选，trade_type=NATIVE，此参数必传。此id为二维码中包含的商品ID，商户自行定义
        :param device_info: 可选，终端设备号(门店号或收银设备ID)，注意：PC网页或公众号内支付请传"WEB"
        :param spbill_create_ip: 调用接口的机器Ip地址
        :param limit_pay: 可选，指定支付方式，no_credit--指定不能使用信用卡支付
        :return: 返回的结果数据
        """

        _notify_url = notify_url or self.notify_url
        path = 'pay/unifiedorder'
        params = dict(
            body=body,                           # 商品描述
            total_fee=total_fee,                 # 总金额
            out_trade_no=out_trade_no,           # 商户订单号
            openid=openid,                       # 用户支付公众号openid(jsapi必须)
            fee_type=fee_type,                   # 货币类型
            spbill_create_ip=spbill_create_ip,   # 终端IP
            notify_url=_notify_url,              # 通知地址
            trade_type=trade_type,               # 交易类型
            device_info=device_info,             # 设备号
            detail=detail,                       # 商品详情
            attach=attach,                       # 附加数据
            time_start=time_start,               # 交易起始时间
            time_expire=time_expire,             # 交易结束时间
            goods_tag=goods_tag,                 # 商品标记
            product_id=product_id,               # 商品ID
            limit_pay=limit_pay,                 # 指定支付方式
        )
        method, url, kwargs = self.prepare_request('POST', path, params)
        return self.make_request(method, url, kwargs)

    def order_query(self, transaction_id='', out_trade_no=''):
        """
        订单查询接口
        https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_2
        :param out_trade_no: 可选，商户订单号，默认自动生成
        :param transaction_id: 可选，微信订单号 和out_trade_no 二选一
        :return: 返回的结果数据
        -----
        trade_state 订单状态
        SUCCESS—支付成功
        REFUND—转入退款
        NOTPAY—未支付
        CLOSED—已关闭
        REVOKED—已撤销（刷卡支付）
        USERPAYING--用户支付中
        PAYERROR--支付失败(其他原因，如银行返回失败)
        """
        path = 'pay/orderquery'
        params = dict(
            transaction_id=transaction_id,
            out_trade_no=out_trade_no
        )
        method, url, kwargs = self.prepare_request('POST', path, params)
        return self.make_request(method, url, kwargs)

    def order_close(self, out_trade_no):
        """
        订单关闭接口
        https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_3
        :param out_trade_no: 可选，商户订单号，默认自动生成
        :return: 返回的结果数据
        """
        path = 'pay/closeorder'
        params = dict(
            out_trade_no=out_trade_no
        )
        method, url, kwargs = self.prepare_request('POST', path, params)
        return self.make_request(method, url, kwargs)

    def refund(self, out_refund_no, total_fee, refund_fee, op_user_id,
               out_trade_no='', transaction_id='',
               device_info='', refund_fee_type='CNY'):
        """
        退款查询接口
        https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_4
        :param out_refund_no: 商户退款单号
        :param total_fee: 总金额
        :param refund_fee: 退款金额
        :param op_user_id: 操作员帐号, 默认为商户号
        :param transaction_id: 可选，商户订单号，默认自动生成
        :param out_trade_no: 可选，微信订单号 以上两个二选一
        :param refund_fee_type: 可选 货币类型，符合ISO 4217标准的三位字母代码，默认人民币：CNY
        :param device_info: 可选，终端设备号(门店号或收银设备ID)，注意：PC网页或公众号内支付请传"WEB"
        :return: 返回的结果数据
        """
        path = 'secapi/pay/refund'
        params = dict(
            out_refund_no=out_refund_no,
            total_fee=total_fee,
            refund_fee=refund_fee,
            op_user_id=op_user_id,
            transaction_id=transaction_id,
            out_trade_no=out_trade_no,
            refund_fee_type=refund_fee_type,
            device_info=device_info
        )
        method, url, kwargs = self.prepare_request('POST', path, params)
        return self.make_request(method, url, kwargs)

    def refundquery(self, out_trade_no='', transaction_id='',
                    out_refund_no='', refund_id='', device_info=''):
        """
        退款查询接口
        https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_5
        :param transaction_id: 可选，微信订单号
        :param out_trade_no: 可选，商户订单号，默认自动生成
        :param out_refund_no: 可选，商户退款单号
        :param refund_id: 可选，微信退款单号 以上四个四选一
        :param device_info: 可选，终端设备号(门店号或收银设备ID)，注意：PC网页或公众号内支付请传"WEB"
        :return: 返回的结果数据
        ----------
        退款状态：
        SUCCESS     退款成功
        FAIL        退款失败
        PROCESSING  退款处理中
        NOTSURE     未确定，需要商户原退款单号重新发起
        CHANGE      转入代发，退款到银行发现用户的卡作废或者冻结了，
                    导致原路退款银行卡失败，资金回流到商户的现金帐号，
                    需要商户人工干预，通过线下或者财付通转账的方式进行退款。
        """
        path = 'pay/refundquery'
        params = dict(
            out_trade_no=out_trade_no,
            transaction_id=transaction_id,
            out_refund_no=out_refund_no,
            refund_id=refund_id,
            device_info=device_info,
        )
        method, url, kwargs = self.prepare_request('POST', path, params)
        return self.make_request(method, url, kwargs)

    def make_request(self, method, url, kwargs):
        req = requests.request(method, url, timeout=TIMEOUT, **kwargs)
        # xml to dict
        result = xmltodict.parse(req.content)
        # 只需要返回数据
        return result.get('xml')


class WeixinAppPay(WeixinPay):
    '''
    微信移动APP支付
    '''

    BASE_URL = 'https://api.mch.weixin.qq.com/'

    def _full_url(self, path):
        if not path:
            return self.BASE_URL
        return '%s%s' % (self.BASE_URL, path)

    def get_base_params(self, is_app=False):
        params = {
            'appid': self.appid,                    # 公众账号ID
        }
        if is_app:
            params.update({
                'partnerid': self.mch_id,                  # 商户号
                'noncestr': generate_nonce_str(),      # 随机字符串
            })
        else:
            params.update({
                'mch_id': self.mch_id,                  # 商户号
                'nonce_str': generate_nonce_str(),      # 随机字符串
            })
        return params

    def prepare_request(self, method, path, params):
        kwargs = {}
        _params = self.get_base_params()
        params.update(_params)
        newparams, prestr = params_filter(params)
        sign = build_mysign(prestr, key=self.partner_key)
        # 将内容转化为unicode xmltodict 只支持unicode
        newparams = params_encoding(newparams)
        newparams['sign'] = sign
        xml_dict = {'xml': newparams}
        kwargs['data'] = smart_str(xmltodict.unparse(xml_dict))
        url = self._full_url(path)
        if self.mch_cert and self.mch_key:
            kwargs['cert'] = (self.mch_cert, self.mch_key)
        return method, url, kwargs

    # 统一下单
    # https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_1
    def unifiedorder(self, body='', out_trade_no='', total_fee='', openid='',
                     detail='', attach='', time_start='', time_expire='',
                     goods_tag='', product_id='', limit_pay='', device_info='',
                     fee_type='CNY', spbill_create_ip=SPBILL_CREATE_IP,
                     trade_type='JSAPI', notify_url=''):
        """
        统一下单接口
        https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_1
        :param trade_type: 交易类型，取值如下：JSAPI，NATIVE，APP，WAP, MWEB
        :param body: 商品描述
        :param total_fee: 总金额，单位分
        :param notify_url: 接收微信支付异步通知回调地址
        :param client_ip: 可选，APP和网页支付提交用户端ip，Native支付填调用微信支付API的机器IP
        :param openid: 可选，用户在商户appid下的唯一标识。trade_type=JSAPI，此参数必传
        :param out_trade_no: 可选，商户订单号，默认自动生成
        :param detail: 可选，商品详情
        :param attach: 可选，附加数据，在查询API和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据
        :param fee_type: 可选，符合ISO 4217标准的三位字母代码，默认人民币：CNY
        :param time_start: 可选，订单生成时间，默认为当前时间
        :param time_expire: 可选，订单失效时间，默认为订单生成时间后两小时
        :param goods_tag: 可选，商品标记，代金券或立减优惠功能的参数
        :param product_id: 可选，trade_type=NATIVE，此参数必传。此id为二维码中包含的商品ID，商户自行定义
        :param device_info: 可选，终端设备号(门店号或收银设备ID)，注意：PC网页或公众号内支付请传"WEB"
        :param spbill_create_ip: 调用接口的机器Ip地址
        :param limit_pay: 可选，指定支付方式，no_credit--指定不能使用信用卡支付
        :return: 返回的结果数据
        """

        _notify_url = notify_url or self.notify_url
        path = 'pay/unifiedorder'
        params = dict(
            body=body,                           # 商品描述
            total_fee=total_fee,                 # 总金额
            out_trade_no=out_trade_no,           # 商户订单号
            openid=openid,                       # 用户支付公众号openid(jsapi必须)
            fee_type=fee_type,                   # 货币类型
            spbill_create_ip=spbill_create_ip,   # 终端IP
            notify_url=_notify_url,              # 通知地址
            trade_type=trade_type,               # 交易类型
            device_info=device_info,             # 设备号
            detail=detail,                       # 商品详情
            attach=attach,                       # 附加数据
            time_start=time_start,               # 交易起始时间
            time_expire=time_expire,             # 交易结束时间
            goods_tag=goods_tag,                 # 商品标记
            product_id=product_id,               # 商品ID
            limit_pay=limit_pay,                 # 指定支付方式
        )
        method, url, kwargs = self.prepare_request('POST', path, params)
        result = self.make_request(method, url, kwargs)
        app_params = self.build_app_sign(result.get('prepay_id'))
        result.update({
            'sign': app_params.get('sign'),
            'nonce_str': app_params.get('noncestr'),
            'time_stamp': app_params.get('timestamp'),
        })
        return result

    def build_app_sign(self, prepay_id, package='Sign=WXPay'):
        params = dict(
            prepayid=prepay_id,
            timestamp=int(time.time()),
            package=package,
        )
        _params = self.get_base_params(is_app=True)
        params.update(_params)
        newparams, prestr = params_filter(params)
        sign = build_mysign(prestr, key=self.partner_key)
        params['sign'] = sign
        return params


class WXAppPay(WeixinPay):
    '''
    微信小程序支付
    '''

    BASE_URL = 'https://api.mch.weixin.qq.com/'
    PAY_SOURCE = 'wxapp'

    def _full_url(self, path):
        if not path:
            return self.BASE_URL
        return '%s%s' % (self.BASE_URL, path)

    # 统一下单
    # https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_1
    def unifiedorder(self, body='', out_trade_no='', total_fee='', openid='',
                     detail='', attach='', time_start='', time_expire='',
                     goods_tag='', product_id='', limit_pay='', device_info='',
                     fee_type='CNY', spbill_create_ip=SPBILL_CREATE_IP,
                     trade_type='JSAPI', notify_url=''):
        """
        统一下单接口
        https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_1
        :param trade_type: 交易类型，取值如下：JSAPI，NATIVE，APP，WAP, MWEB
        :param body: 商品描述
        :param total_fee: 总金额，单位分
        :param notify_url: 接收微信支付异步通知回调地址
        :param client_ip: 可选，APP和网页支付提交用户端ip，Native支付填调用微信支付API的机器IP
        :param openid: 可选，用户在商户appid下的唯一标识。trade_type=JSAPI，此参数必传
        :param out_trade_no: 可选，商户订单号，默认自动生成
        :param detail: 可选，商品详情
        :param attach: 可选，附加数据，在查询API和支付通知中原样返回，该字段主要用于商户携带订单的自定义数据
        :param fee_type: 可选，符合ISO 4217标准的三位字母代码，默认人民币：CNY
        :param time_start: 可选，订单生成时间，默认为当前时间
        :param time_expire: 可选，订单失效时间，默认为订单生成时间后两小时
        :param goods_tag: 可选，商品标记，代金券或立减优惠功能的参数
        :param product_id: 可选，trade_type=NATIVE，此参数必传。此id为二维码中包含的商品ID，商户自行定义
        :param device_info: 可选，终端设备号(门店号或收银设备ID)，注意：PC网页或公众号内支付请传"WEB"
        :param spbill_create_ip: 调用接口的机器Ip地址
        :param limit_pay: 可选，指定支付方式，no_credit--指定不能使用信用卡支付
        :return: 返回的结果数据
        """

        _notify_url = notify_url or self.notify_url
        path = 'pay/unifiedorder'
        params = dict(
            body=body,                           # 商品描述
            total_fee=total_fee,                 # 总金额
            out_trade_no=out_trade_no,           # 商户订单号
            openid=openid,                       # 用户支付公众号openid(jsapi必须)
            fee_type=fee_type,                   # 货币类型
            spbill_create_ip=spbill_create_ip,   # 终端IP
            notify_url=_notify_url,               # 通知地址
            trade_type=trade_type,               # 交易类型
            device_info=device_info,             # 设备号
            detail=detail,                       # 商品详情
            attach=attach,                       # 附加数据
            time_start=time_start,               # 交易起始时间
            time_expire=time_expire,             # 交易结束时间
            goods_tag=goods_tag,                 # 商品标记
            product_id=product_id,               # 商品ID
            limit_pay=limit_pay,                 # 指定支付方式
        )
        method, url, kwargs = self.prepare_request('POST', path, params)
        result = self.make_request(method, url, kwargs)
        sign_params = self.build_wxapp_sign(result, trade_type)
        result.update({
            'sign': sign_params.get('sign'),
            'nonce_str': sign_params.get('nonceStr'),
            'time_stamp': sign_params.get('timeStamp'),
        })
        return result

    def build_wxapp_sign(self, result, trade_type):
        _params = self.get_base_params()
        params = {
            'timeStamp': int(time.time()),
            'nonceStr': result.get('nonce_str'),
            'signType': 'MD5',
            'package': 'prepay_id=' + result.get('prepay_id', ''),
            'appId': _params.get('appid')
        }
        newparams, prestr = params_filter(params)
        sign = build_mysign(prestr, key=self.partner_key)
        params['sign'] = sign
        return params


class WeixinEnterprisePay(WeixinPay):

    BASE_URL = 'https://api.mch.weixin.qq.com/'

    def get_base_params(self):
        params = {
            'mch_appid': self.appid,                # 公众账号ID
            'mchid': self.mch_id,                   # 商户号
            'nonce_str': generate_nonce_str(),      # 随机字符串
        }
        return params

    def transfers(self, partner_trade_no, openid, amount, desc,
                  spbill_create_ip=SPBILL_CREATE_IP, check_name='NO_CHECK',
                  re_user_name='', device_info=''):
        """
        企业付款接口
        https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=9_1
        :param partner_trade_no: 商户订单号，默认自动生成
        :param openid: 用户在商户appid下的唯一标识
        :param amount: 企业付款金额，单位为分
        :param desc: 企业付款操作说明信息。必填
        :param spbill_create_ip: 调用接口的机器Ip地址
        :param check_name: NO_CHECK：不校验真实姓名
                           FORCE_CHECK：强校验真实姓名（未实名认证的用户会校验失败，无法转账）
                           OPTION_CHECK：针对已实名认证的用户才校验真实姓名（未实名认证用户不校验，可以转账成功）
        :param re_user_name: 可选 收款用户真实姓名。如果check_name设置为FORCE_CHECK或OPTION_CHECK，则必填用户真实姓名
        :param device_info: 可选，终端设备号(门店号或收银设备ID)，注意：PC网页或公众号内支付请传"WEB"
        :return: 返回的结果数据
        """
        path = 'mmpaymkttransfers/promotion/transfers'
        params = dict(
            partner_trade_no=partner_trade_no,
            openid=openid,
            amount=amount,
            desc=desc,
            check_name=check_name,
            re_user_name=re_user_name,
            device_info=device_info,
            spbill_create_ip=spbill_create_ip,
        )
        method, url, kwargs = self.prepare_request('POST', path, params)
        return self.make_request(method, url, kwargs)


class WeixinEnterprisePayQuery(WeixinPay):

    BASE_URL = 'https://api.mch.weixin.qq.com/'

    def gettransferinfo(self, partner_trade_no):
        """
        企业付款查询
        https://pay.weixin.qq.com/wiki/doc/api/tools/mch_pay.php?chapter=14_3
        :param partner_trade_no: 商户订单号，默认自动生成
        :return: 返回的结果数据
        """
        path = 'mmpaymkttransfers/gettransferinfo'
        params = dict(partner_trade_no=partner_trade_no)
        method, url, kwargs = self.prepare_request('POST', path, params)
        return self.make_request(method, url, kwargs)


def wxpay_notify_verify(post_data, partner_key=None):
    # 验证--签名
    _, prestr = params_filter(post_data, excludes=['sign'])
    mysign = build_mysign(prestr, key=partner_key)
    if mysign != post_data.get('sign'):
        return False
    return True
