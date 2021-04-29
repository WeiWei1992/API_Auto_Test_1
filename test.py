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

# text='"retCode":"00000";"retInfo":"操作成功"'
# text_list=text.split('|')
# print(text_list)
# print(type(text_list))
# print(len(text_list))
#
# import random
# #print(random.randint(0,9))
#
# def generate_random_str(randomlength=4):
#   """
#   生成一个指定长度的随机字符串
#   """
#   random_str = ''
#   base_str = 'ABCDEFGHIGKLMNOPQRSTUVWXYZabcdefghigklmnopqrstuvwxyz0123456789'
#   length = len(base_str) - 1
#   for i in range(randomlength):
#     random_str += base_str[random.randint(0, length)]
#   return random_str
#
# if __name__=="__main__":
#     f=generate_random_str()
#     print(f)

import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr,formataddr

def send_email():
    sender = 'zhangyan@haierubic.com'
    #receivers =['zhangyan@haierubic.com','daiyy@haierubic.com','liujf@haierubic.com','yaox@haierubic.com','mengzg@haierubic.com','liujw@haierubic.com']
    receivers =['weiwei.uh@haier.com']
    #创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] =  sender
    message['To'] = receivers
    subject = 'appserver接口测试结果'
    message['Subject'] = Header(subject, 'utf-8')

    #邮件正文内容
    message.attach(MIMEText('hi,all:\n    附件中是本次接口的自动化测试结果,请查收', 'plain', 'utf-8'))

    # 构造附件1，传送当前目录下的 test.txt 文件
    # att1 = MIMEText(open('D:/appserver.xlsx', 'rb').read(), 'base64', 'utf-8')
    # att1["Content-Type"] = 'application/octet-stream'
    # # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    # att1["Content-Disposition"] = 'attachment; filename="appserver.xlsx"'
    # message.attach(att1)
    try:
        smtpObj = smtplib.SMTP('mail.haierubic.com',25)
        smtpObj.set_debuglevel(1)
        #smtpObj.connect('mail.haierubic.com')
        smtpObj.login('zhangyan@haierubic.com','123qweasdzxc')
        smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except Exception as e:
        print("Error: 无法发送邮件")
        print(e)

if __name__=="__main__":
    send_email()