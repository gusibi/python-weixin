# -*- coding: utf-8 -*-

from weixin.helper import smart_bytes
from weixin.pay import WeixinPay

APPID = 'appid'
MCH_ID = 'mchid'

create_pay_info = {
    'body': smart_bytes("这里写点啥呢？"),
    'out_trade_no': '20181206130823938475',
    'total_fee': 1,
    'trade_type': "JSAPI",
    'openid': 'ol9GscXefkyakBnRV4s',
}

wxpay = WeixinPay(
    APPID, MCH_ID,
    partner_key='partner key',
    notify_url='http://www.qq.com/pay/notify')
order = wxpay.unifiedorder(**create_pay_info)

print(order)
