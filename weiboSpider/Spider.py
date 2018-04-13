# -*- coding: utf-8 -*-
import requests, re, json, hashlib, base64, rsa, binascii, urllib;

class request() :

    def __init__(self):
        self.username = '17816893901';
        self.password = 'wqc8866785520';

        self.POST = 1;
        self.GET  = 2;
        self.s = requests.session();
       #  if (s == None)
        self.headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Content-Type':'application/x-www-form-urlencoded',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Connection':'keep-alive',
            'Origin':'http://weibo.com',
            "Referer":"http://weibo.com/",
            'User-Agent':'Mozilla/5.0(Windows NT 6.1;WOW64;Trident/7.0;rv:11.0)like Gecko',
        };

        self.loginData= {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'userticket': '1',
            'pagerefer' : 'https://www.baidu.com/link?url=3YSdEuAbjIWO9udn3LjIow1nWKq68fuNgSft3DzFvJu&wd=&eqid=91465358014ef6870000000356b9ac4e',
            'vsnf': '1',
            'su': '',
            'service': 'miniblog',
            'servertime': '',
            'nonce': '',
            'pwencode': 'rsa2',
            'rsakv' : '',
            'sp': '',
            'sr':'1366*768',
            'encoding': 'UTF-8',
            "prelt": "76",
            'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        };

    # 发送请求
    def send(self, url, type=None, data=None):
        if type == self.POST :
            return self.s.post(url, headers=self.headers, data=data).content
        else :
            return self.s.get(url, headers=self.headers, params=data).content

    # 登录
    def login(self):
        url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&wsseretry=servertime_error'
        try:
            servertime, nonce, pubkey, rsakv  = self.get_servertime();
        except:
            return

        self.loginData['servertime'] = servertime
        self.loginData['nonce'] = nonce
        self.loginData['rsakv'] = rsakv
        self.loginData['su'] = self.get_user()
        self.loginData['sp'] = self.get_pwd(servertime, nonce, pubkey)

        # 登录
        text = self.send(url, self.POST,data= self.loginData);
        p= re.compile('location\.replace\((\"|\')(.*?)(\"|\')\)')

        # 请求两次才算真正的登录, 并获取用户uniqueid值
        text2 = self.send(p.search(text).group(2));
        text3 = self.send(p.search(text2).group(2))
        user_json = json.loads(text3.split('(')[-1].split(')')[0])
        uniqueid = user_json['userinfo']['uniqueid']

        main_url = "http://weibo.com/u/%s/home" % uniqueid
        self.send(main_url);
        print "登录成功!"

    # 获取servertime, nonce 用于登录
    def get_servertime(self):
        #url = 'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.18)&_=1523515128316';
        url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=emhlZGFwYXQlNDAxNjMuY29t&rsakt=mod&client=ssologi';
        data = self.send(url);
        p = re.compile('\((.*)\)')
        try:
            json_data = p.search(data).group(1)
            data = json.loads(json_data)
            servertime = str(data['servertime'])
            nonce      = str(data['nonce'])
            pubkey     = str(data['pubkey'])
            rsakv      = str(data['rsakv'])
            return servertime, nonce, pubkey, rsakv
        except:
            print 'Get severtime error!'
            return None

    # ras 加密密码
    def get_pwd(self, servertime, nonce, pubkey):
        # 新版加密方式
        rsaPublickey = int(pubkey, 16)
        key = rsa.PublicKey(rsaPublickey, 65537)
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(self.password)
        pwd3 = binascii.b2a_hex(rsa.encrypt(message.encode(encoding="utf-8"), key))

        #pwd1 = hashlib.sha1(self.password).hexdigest()
        #pwd2 = hashlib.sha1(pwd1).hexdigest()
        #pwd3_ = pwd2 + servertime + nonce
        #pwd3 = hashlib.sha1(pwd3_).hexdigest()
        return pwd3

    # base64 加密用户名
    def get_user(self):
        return base64.encodestring(urllib.quote(self.username))[:-1];

    # 点赞功能
    def praise(self):
        url = 'https://weibo.com/aj/v6/like/add?ajwvr=6&__rnd=1523604774184';

        data = {
            'location': 'v6_content_home',
            'version':'mini',
            'qid':'heart',
            'mid':'4227946187023105',
            'like_src':'1',
            'cuslike':'1'
        }

        res = self.send(url, type=self.POST, data = data);
        # res.data.is_del  1 -- 取消点赞  0 -- 赞
        print res


r = request();
r.login();
r.praise();
#url = 'https://rm.api.weibo.com/2/remind/push_count.json?trim_null=1&with_dm_group=0&with_settings=1&exclude_attitude=1&with_common_cmt=1&with_comment_attitude=1&with_common_attitude=1&with_moments=1&with_dm_unread=1&msgbox=true&with_page_group=1&with_chat_group=1&with_chat_group_notice=1&_pid=1&count=16&source=351354573&status_type=0&callback=STK_152352060148762'
#print unicode(r.send(url), 'gbk')
#print r.s.cookies
#print  r.send(url)