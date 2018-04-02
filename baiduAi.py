# -*- coding: utf-8 -*-
from aip import AipFace
import os;
import time;
import json;
import shutil;

appId = '11034414';
appKey = 'nrBlF3oeWTt4rX0xAtdcNu8T';
secretKey = 'LItELH5OBAKTUA6KGMPWX5PZIWTImuOd';

client = AipFace(appId, appKey, secretKey);

#建立连接的超时时间
#client.setConnectionTimeoutInMillis()
#通过打开的连接传输数据的超时时间
#client.setSocketTimeoutInMillis()

""" 读取图片 """
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

def call_BaiduAi (image):
    options = {};
    options["max_face_num"] = 2;
    options["face_fields"] = "age,gender";
    print client.detect(image, options);
   #res = client.detect(image, options);
    res = json.loads(client.detect(image, options));
    for result in res['result'] :
        if result.gender == "female":
            return True;
        else :
            return False;


path = 'dowload/zhihuPic/';
for f1 in os.listdir(path):
    #f1 = '_zhao_xu_.jpg';
    tmp_path = os.path.join(path, f1);
    if not os.path.isdir(tmp_path):
        image = get_file_content(tmp_path);
        options = {};
        options["max_face_num"] = 2;
        options["face_fields"] = "age,gender";
        res = client.detect(image, options);
        json_string = json.dumps(res)
        res = json.loads(json_string);
        if res['result_num'] > 0 :
            for result in res['result']:
                if result['gender'] == "female":
                    shutil.copy(tmp_path, "dowload/famale/" + '/' + f1);
                    print f1 + " is female !";
                else:
                    print f1 + " is not female !";
        else :
            print f1 + ' undetected face !';
        time.sleep(2); # QBS限制2
