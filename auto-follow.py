#!/usr/bin/env python
#! -*- coding:utf-8 -*-

import requests
import json
import re

#在这里配置你的登录email和密码
myemail = 'xxx'
mypasswd = 'xxx'
myname = 'yyy'

#用emaail和密码登录支护, requests会保存cookie。
s = requests.session()
login_data = {'email':myemail, 'password':mypasswd}
s.post('http://www.zhihu.com/login', login_data)

header_info={
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Host':'www.zhihu.com',
    'Origin':'http://www.zhihu.com',
    'Referer':'http://www.zhihu.com/people/jixin/followees',
    'Connection':'keep-alive',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With':'XMLHttpRequest'
}


data_id_all=[]
r = s.get('http://www.zhihu.com/people/%s/followers' % (myname))

raw_data_id = re.findall('data-id(.*)', r.text)
for x in raw_data_id:
    data_id_all.append(x[2:34])

raw_hash_id = re.findall('hash_id(.*)', r.text)
hash_id = raw_hash_id[0][14:46]
raw_xsrf = re.findall('xsrf(.*)', r.text)
_xsrf = raw_xsrf[0][9:-3]
offsets=20
params = json.dumps({"hash_id":hash_id, "order_by":"created", "offset":offsets,})
payload={"method":"next", "params":params, "_xsrf":_xsrf,}
click_url = 'http://www.zhihu.com/node/ProfileFollowersListV2'

#获取所有关注你的知乎帐号
while True:
    r = s.post(click_url, data=payload, headers=header_info).text[13:-3]
    if len(r) == 0:
        break
    raw_data_id = re.findall('data-id(.*)', r)
    for x in raw_data_id:
        data_id_all.append(x[2:34])

header_info = {
    "Accept":"*/*",
    "Accept-Encoding":"gzip,deflate,sdch",
    "Accept-Language":"zh-CN,zh;q=0.8",
    "Connection":"keep-alive",
    "Content-Length":"127",
    "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
    "DNT":"1",
    "Host":"www.zhihu.com",
    "Origin":"http://www.zhihu.com",
    "Referer":"http://www.zhihu.com/people/shisu/followers",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest",
}

#关注他们
click_url = 'http://www.zhihu.com/node/MemberFollowBaseV2'
for x in data_id_all:
    params = json.dumps({"hash_id":x})
    payload={"method":"follow_member", "params":params, "_xsrf":_xsrf,}
    s.post(click_url, data=payload, headers=header_info)
