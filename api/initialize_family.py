import os
import re
import logging
from common.operate_ini import Openate_Ini
openate_ini=Openate_Ini()
import requests
import time
from common.public import handle_body
from common.sign import sha256,md5
class Initalize_Family():
    def __init__(self,userbody):
        self.userbody=userbody
    def get_sign(self,url,body,timestamp,verify):
        #versify指定是md5还是sha256

        logging.info("开始计算签名")

        #verify用来标志是使用md5加密还是sha256加密
        if "md5" in str(verify).lower():
            Sign=md5(url,body,str(timestamp))
        elif "sha256" in str(verify).lower():

            logging.info("创建sha256加密类")
            Sign=sha256(url,body,str(timestamp))
        else:
            #默认使用sha256
            Sign = sha256(url, body, str(timestamp))
        return Sign.get_sign()
    def get_header(self,url,body,timestamp,verify):
        headers={}
        headers['sign']=self.get_sign(url,body,timestamp,verify)
        headers['timestamp']=str(timestamp)
        headers['clientid']=openate_ini.read_ini('headers','clientid')
        headers['accesstoken']=openate_ini.read_ini('headers','accesstoken')
        headers['accounttoken']=openate_ini.read_ini('headers','accounttoken')
        headers['content-type']=openate_ini.read_ini('headers','content-type')
        headers['appid']=openate_ini.read_ini('headers','appid')
        headers['appkey']=openate_ini.read_ini('headers','appkey')
        headers['userid']=openate_ini.read_ini('headers','userid')
        headers['appversion']=openate_ini.read_ini('headers','appversion')

        return headers

    def get_allurl(self,url):
        #计算请求头的时间戳和组合请求的url
        currTimes = time.time()
        time_stamp = int(round(currTimes * 1000))
        openate_ini.modify('headers', 'timestamp', str(time_stamp))
        allurl = "http://" + openate_ini.read_ini('url', 'domain') + "/" + url
        logging.info("请求url: " + allurl)
        return allurl,time_stamp
    def login(self,loginurl):
        loginallurl,time_stamp=self.get_allurl(loginurl)
        headers=self.get_header(loginurl,self.userbody,time_stamp,'md5')
        try:
            res = requests.post(url=loginallurl, headers=headers, data=self.userbody)
        except Exception as e:
            logging.error("发送请求错误，错误类型是：")
            logging.error(e.__class__.__name__)
            logging.error("发送请求错误，错误明细：")
            logging.error(e)
            # real_txt, flag, fail_reason
            real_txt = '请求异常'
            flag = False
            fail_reason = '请求异常'
            return False,''
        else:
            if res.status_code==200:
                return True,res
            else:
                return False,''


    def get_familiy_list(self,url):
        #获取家庭列表
        allurl,time_stamp=self.get_allurl(url)
        body=''
        headers=self.get_header(url,str(body),time_stamp,'md5')
        try:
            res=requests.post(url=allurl,headers=headers,data=body)
        except Exception as e:
            logging.error("发送请求错误，错误类型是：")
            logging.error(e.__class__.__name__)
            logging.error("发送请求错误，错误明细：")
            logging.error(e)
            # real_txt, flag, fail_reason
            real_txt = '请求异常'
            flag = False
            fail_reason = '请求异常'
            return False, ''
        else:
            if res.status_code==200:
                return True,res
            else:
                return False,''


    def handle_family_list(self,res):
        # print(res)
        # print(type(res))
        res_dict=res.json()
        # print(res_dict)
        # print(type(res_dict))

        creatfamilys=res_dict['data']['createfamilies']
        # print(creatfamilys)
        # print(type(creatfamilys))
        lenfamilys=len(creatfamilys)
        # print(lenfamilys)
        family_list=[]
        for i in range(lenfamilys):
            tmp_family_list=[]
            # print(i)
            tmp_family=creatfamilys[i]
            # print(tmp_family)
            family_name=tmp_family['familyName']
            family_id=tmp_family['familyId']
            tmp_family_list.append(family_name)
            tmp_family_list.append(family_id)
            family_list.append(tmp_family_list)
        # print("-------------")
        # print(family_list)
        return family_list


        # res_text=res.text
        # print(res_text)
        # print(type(res_text))
    def my_append(self,mylist,res):
        try:
            res_text=res.text
        except Exception as e:
            logging.error("返回数据错误")
        else:
            mylist.append(res_text)
        return mylist
    def delete_family(self,family):
        #解散家庭
        url="/emuplus/family/v1/family/destroy"
        family_name=family[0]
        familyId=family[1]
        logging.info("要删除的房间是："+str(family_name))
        logging.info("要删除的房间id是： "+str(familyId))

        allurl, time_stamp = self.get_allurl(url)
        body ={"familyId":familyId}
        logging.info("body:  "+str(body))
        body=str(body)
        body=body.replace("'",'"')
        logging.info(body)

        headers = self.get_header(url, str(body), time_stamp, 'md5')
        try:
            res = requests.post(url=allurl, headers=headers, data=body)
            #print(res.text)
        except Exception as e:
            print(e)
            logging.error("删除房间发送请求错误，错误类型是：")
            logging.error(e.__class__.__name__)
            logging.error("发送请求错误，错误明细：")
            logging.error(e)
            real_txt = '请求异常'
            flag = False
            fail_reason = '请求异常'
            return False, ''
        else:
            if res.status_code == 200 and "00000" in res.text:
                logging.info(family_name+"删除成功")
                return True, res
            else:
                return False, ''



    def delete_family_list(self,family_list):
        logging.info("开始准备删除房间")
        res=[]
        print("开始准备删除房间")
        if family_list==None or len(family_list)==0 or family_list=="":
            logging.warning("没有要删除的房间，结束")
            # logging.info("没有要删除的房间，结束")
            return True,'no_family'
        else:

            for family in family_list:
                logging.info("账号下的账号列表： ")
                logging.info(family_list)
                logging.info("当前处理的家庭： ")
                logging.info(family)
                print(family[0])
                if "NewFamily" in family[0]:
                    logging.info("删除"+str(family[0]))
                    flag,res_tmp=self.delete_family(family)
                    if flag:
                        res.append(res_tmp.text)

                else:
                    logging.info("没有找到NewFamily房间")
                    res.append('no_delete_family')
                    logging.info(res)
            return True,res
        # print(res)
        # print(type(res))
        # return res


    def run_init_family(self):
        res=[]
        loginurl="/emuplus/secuag/account/v1.0/login"
        flaglogin,reslogin=self.login(loginurl)

        # print("========")
        # print(flaglogin)
        # print(type(flaglogin))

        if flaglogin:
            logging.info("登录成功")
            # print("登录成功")
            res=self.my_append(res,reslogin)
            get_familiy_url="/emuplus/family/v1/family/list"
            flag_family,res_family=self.get_familiy_list(get_familiy_url)
            if flag_family:
                logging.info("获取家庭列表成功")
                # print("获取家庭列表成功")
                res=self.my_append(res,res_family)
                try:
                    family_list=self.handle_family_list(res_family)
                except Exception as e:
                    logging.error("处理家庭列表的返回错误")
                    logging.error("错误类型是：")
                    logging.error(e.__class__.__name__)
                    logging.error("错误明细：")
                    logging.error(e)
                else:
                    logging.info("家庭列表处理完成，开始进行删除")
                    # print("家庭列表处理完成，开始进行删除")
                    flag,res_tmp=self.delete_family_list(family_list)
                    logging.info("删除方法调用结束  ")
                    # print(flag)
                    # print(res_tmp)
                    res.append(res_tmp)
        #             print(res)
        # print("+++++++++++++++++")
        # print(res)


        real_txt=str(res)
        flag=True
        fail_reason=''

        return real_txt, flag, fail_reason

if __name__=="__main__":
    userbody={
    "username": "15192727132",
    "password": "weiwei123",
    "captchaToken": "",
    "captchaAnswer": ""
}
    init_family=Initalize_Family(str(userbody))
    init_family.run_init_family()

