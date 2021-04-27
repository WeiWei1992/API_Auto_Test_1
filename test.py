# import requests
# import hashlib
# #1.实例化一个sha256对象
# sha256=hashlib.sha256()
#
# # #2.加密原始值-比如密码,需要将字符串转成bytes（字节）
# # sha256.update('111111'.encode('utf-8'))
# # print(sha256.hexdigest())
# # header={"Content-Type":"application/x-www-form-urlencoded","X-Requested-With":"XMLHttpRequest"}
# #
# # #3.发送登录接口信息
# # body={"userName":"sqqdcl","password":sha256.hexdigest()}
# # #body={"userName":"sqqdcl","password":'111111'}
# # resp=requests.post('http://47.96.181.17:8098/login',data=body,headers=header)
# # print(resp.text)
#
# mystr='/emuplus/secuag/account/v1.0/login{"username":"18161982838","password":"123456","captchaToken":"","captchaAnswer":""}MB-UZHSH-00015dfca8714eb26e3a776e58a8273c87521616047412445'
# sha256.update(mystr.encode('utf-8'))
# print(sha256.hexdigest())

import os
import re
# text='{"retCode":"00000","retInfo":"操作成功","data":{"qrcode":"http://uplusapp.cn/U/0005H?token=5afcecd943cc4d12b98060365607420c&content=uplus://joinFamily/5afcecd943cc4d12b98060365607420c"}}'
# mypattern='joinFamily/(.*)"'
# pattern=re.compile(mypattern)
# print(pattern)
# m=pattern.findall(text)
# print(m)
# print(type(m))

text='"retCode":"00000";"retInfo":"操作成功"'
text_list=text.split('|')
print(text_list)
print(type(text_list))
print(len(text_list))
