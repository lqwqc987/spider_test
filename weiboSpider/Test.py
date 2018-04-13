# -*-coding:utf-8-*-
import requests
from bs4 import BeautifulSoup
import time
import json
import os
import base64
import urllib
import hashlib
import re
import rsa
import binascii

head = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'http://weibo.com',
        "Referer": "http://weibo.com/",
        'User-Agent': 'Mozilla/5.0(Windows NT 6.1;WOW64;Trident/7.0;rv:11.0)like Gecko',
        'Host': 'login.sina.com.cn'}

data = {
    "entry": "weibo",
    "gateway": "1",
    "savestate": "7",
    "useticket": "1",
    "pagerefer": "https://www.baidu.com/link?url=3YSdEuAbjIWO9udn3LjIow1nWKq68fuNgSft3DzFvJu&wd=&eqid=91465358014ef6870000000356b9ac4e",
    "vsnf": "1",
    "su": "",
    "service": "miniblog",
    "servicetime": "",
    "nonce": "",
    "pwencode": "rsa2",
    "rsakv": "",
    "sp": "",
    "sr": "1366*768",
    "encoding": "UTF-8",
    "prelt": "76",
    "url": "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
    "returntype": "META"
}

if __name__ == '__main__':
    email = "17816893901"
    password = "wqc8866785520"
    pre_url = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=emhlZGFwYXQlNDAxNjMuY29t&rsakt=mod&client=ssologi"
    s = requests.session()
    res = s.get(pre_url)
    res = res.text.encode('utf-8').split('(')[-1].split(')')[0]
    pre_json = json.loads(res)
    print pre_json
    servertime = pre_json['servertime']
    nonce = pre_json['nonce']
    rsakv = pre_json['rsakv']
    pubkey = pre_json['pubkey']
    # urllib.quote()是进行url编码
    # su是经过一次base64加密之后的账号
    su = base64.encodestring(urllib.quote(email))[:-1]
    print "su:%s" % su
    # rsa2计算sp
    rsaPubkey = int(pubkey, 16)
    key = rsa.PublicKey(rsaPubkey, 65537)
    message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)
    sp = rsa.encrypt(message, key)
    sp = binascii.b2a_hex(sp)
    print "sp:%s" % sp
    data['servertime'] = servertime
    data['nonce'] = nonce
    data['rsakv'] = rsakv
    data['su'] = su
    data['sp'] = sp

    #
    post_url = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&wsseretry=servertime_error"
    res = s.post(post_url, data=data)
    print res.text

    #p = re.compile('location\.replace\"(.∗?)\"')
    p = re.compile('location\.replace\((\"|\')(.*?)(\"|\')\)')
    final_url = p.search(res.text.encode('utf-8')).group(2)
    print final_url
    res = s.get(final_url)
   # print res.text
    res = res.text.encode('utf-8').split('(')[-1].split(')')[0]
    user_json = json.loads(res)
    uniqueid = user_json['userinfo']['uniqueid'].encode('utf-8')
    print user_json['userinfo']['uniqueid']

    main_url = "http://weibo.com/u/%s/home" % uniqueid
    res = s.get(main_url)
   # print res.text;
    print '登录成功'