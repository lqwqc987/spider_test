# -*- coding: utf-8 -*-
import requests;
import json;
import os;
import sys
import threadpool;
import random
import time;
class SpiderZhihu(object) :
    def __init__(self):
        default_encoding = 'utf-8'
        if sys.getdefaultencoding() != default_encoding:
            reload(sys);
            sys.setdefaultencoding(default_encoding);

        self.headers = {'content-type': 'application/json',
               'authorization' : 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
               'keep-live':'false'};
        self.task_pool = threadpool.ThreadPool(10);

    def sendRequest(self, url=None, token=None) :
        if token is not None:
            url = "https://www.zhihu.com/api/v4/members/"+token+"/followers?" \
              "include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics" \
              "&offset=0" \
              "&limit=20";
            #status_code
        # 失败的重发三次, 三次失败则跳过
        for i in range(1,3):
            res = requests.get(url=url, headers=self.getHeaders());
            if res.status_code == 200:
                return res.content;
            else:
                print '请求错误, 正在重试第',i+1, '次'
        #time.sleep(500);
        return;

    def parseJson(self, str):
        rs = self.sendRequest(token=str);
        if rs is not None:
            obj = json.loads(rs);
            if obj['paging']['totals'] > 0 :
                # 下载当前页所有关注者的头像
                self.dowload_pic(obj['data']);
                # 如果有下一页 则继续调用函数下载
                if obj['paging']['is_end'] == False:
                    self.parseJson(self.sendRequest(url=obj['paging']['next']));

    def dowload_pic(self, list):
        default_addr = 'https://pic2.zhimg.com/da8e974dc_xl.jpg';
        user_list = [];
        for data in list:
            url_token = data['url_token'];
            user_list.append(url_token);
            pic_addr = data['avatar_url_template'].replace('{size}', 'xl');
            # 默认头像不保存
            if pic_addr != default_addr:
                path = 'dowload\\zhihuPic';
                pic_name = url_token + '.jpg';
                # 验证该图片是否已存在
                if os.path.exists(path + '\\' + pic_name) == False:
                    self.save_file(path, pic_name, self.sendRequest(pic_addr));
                else:
                    print pic_name + ' is existed！';
        #r2 = threadpool.makeRequests(self.parseJson, user_list);
        #[self.task_pool.putRequest(req) for req in r2];
        #self.task_pool.wait();

    def save_file(self,path,file_name,data):
        if data is not None :
            if not os.path.exists(path):
                os.makedirs(path);
            path = path+'\\'+file_name;
            with open(path,"wb") as f:
                f.write(data);
                f.flush();
            print 'dowload success:' + path;

    def start(self):
        self.parseJson('cai-ding-xian-96');

    def getUserAgent(self):
        list = ['Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0',
                'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;',
                'Mozilla/5.0 (iPhone; U; CPU iPhone OS 4_3_3 like Mac OS X; en-us) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8J2 Safari/6533.18.5',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11'];
        return list[random.randint(0, 3)];

    def getHeaders(self):
        headers = self.headers;
        headers['User-Agent'] = self.getUserAgent();
        return headers;

sz = SpiderZhihu();
sz.start();