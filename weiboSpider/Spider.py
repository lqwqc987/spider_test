# -*- coding: utf-8 -*-
import requests, re, json, hashlib, base64, rsa, binascii;

class request() :

    def __init__(self):
        self.username = '17816893901';
        self.password = 'wqc8866785520';

        self.s = requests.session();
       #  if (s == None)
        self.headers = {'content-type': 'application/x-www-form-urlencoded',
                        'Connection': 'keep-alive',
                        'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'};

        self.loginData= {
            'entry': 'weibo',
            'gateway': '1',
            'from': '',
            'savestate': '7',
            'qrcode_flag': False,
            'userticket': '1',
            'pagerefer' : 'https://login.sina.com.cn/crossdomain2.php?action=logout&r=https%3A%2F%2Fweibo.com%2Flogout.php%3Fbackurl%3D%252F',
            'vsnf': '1',
            'su': '',
            'service': 'miniblog',
            'servertime': '',
            'nonce': '',
            'pwencode': 'rsa2',
            'rsakv' : '1330428213',
            'sp': '',
            'sr':'1366*768',
            'encoding': 'UTF-8',
            'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        };
    def send(self, url, data=None):
        return unicode(self.s.get(url, headers=self.headers, params= data).content, 'gbk')

    def login(self):
        url = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
        try:
            servertime, nonce, pubkey, rsakv  = self.get_servertime();
        except:
            return

        self.loginData['servertime'] = servertime
        self.loginData['nonce'] = nonce
        self.loginData['rsakv'] = rsakv
        self.loginData['su'] = self.get_user()
        self.loginData['sp'] = self.get_pwd(servertime, nonce, pubkey)

        text = self.send(url, data=self.loginData);
        # print text
        p= re.compile('location\.replace\((\"|\')(.*?)(\"|\')\)')

        try:
            login_url = p.search(text).group(2);
            print login_url;
            self.send(login_url);
            print "登录成功!"
        except:
            print 'Login error!'


    # 获取servertime, nonce 用于登录
    def get_servertime(self):
        url = 'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.19)&_=1523515128316';
        data = self.send(url);
        p = re.compile('\((.*)\)')
        try:
            json_data = p.search(data).group(1)
            data = json.loads(json_data)
            servertime = str(data['servertime'])
            nonce      = data['nonce']
            pubkey     = data['pubkey']
            rsakv      = data['rsakv']
            return servertime, nonce, pubkey, rsakv
        except:
            print 'Get severtime error!'
            return None

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

    def get_user(self):
        return base64.encodestring(self.username)[:-1];


r = request();
r.login();
#url = 'https://rm.api.weibo.com/2/remind/push_count.json?trim_null=1&with_dm_group=0&with_settings=1&exclude_attitude=1&with_common_cmt=1&with_comment_attitude=1&with_common_attitude=1&with_moments=1&with_dm_unread=1&msgbox=true&with_page_group=1&with_chat_group=1&with_chat_group_notice=1&_pid=1&count=16&source=351354573&status_type=0&callback=STK_152352060148762'
url = 'https://weibo.com/aj/account/watermark?ajwvr=6&_t=0&__rnd=1523525488085';
#print unicode(r.send(url), 'gbk')
print r.s.cookies
print  r.send(url)