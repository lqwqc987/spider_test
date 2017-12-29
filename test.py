import requests;
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

#url = "https://www.zhihu.com/api/v4/members/wu-qing-cheng-92/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=0&limit=20"
url = "https://www.zhihu.com/api/v4/members/wu-qing-cheng-92/followers?" \
      "include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics" \
      "&offset=0" \
      "&limit=20";
headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0',
           'authorization' : 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'}

def sendRequest(url) :
    return requests.get(url=url,headers=headers).content;

i = 0;
while True :
    content = sendRequest(url);
    i = i+1;
    print i ;
    print content;
