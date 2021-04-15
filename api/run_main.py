
import os
import re
import logging
from common.operate_ini import Openate_Ini
import requests
import json
import time
from common.sign import sha256,md5
from common.public import check_value,save_value,handle_body
from common.operate_excel import save_result
openate_ini=Openate_Ini()

def run_main(case,result_file,row):

    logging.info("用例开始之前，先把配置文件中的[body]删除")
    openate_ini.delect()

    save_value_list=[]
    #要保存的列表
    #is_pass=case['ispass']

    is_run=case['isrun']
    case_id=case['id']
    is_pass = case['ispass']
    case_model=case['model']
    case_name=case['name']
    save_value_list.append(is_run)
    save_value_list.append(case_id)
    save_value_list.append(is_pass)
    save_value_list.append(case_model)
    save_value_list.append(case_name)

    #传入的是整个用例，包括多个接口和校验等
    #分割
    steps = dict((key, value) for key, value in case.items() if 'step' in key)
    urls=dict((key,value) for key,value in case.items() if 'url' in key)
    bodys=dict((key,value) for key,value in case.items() if 'body' in key)
    methonds=dict((key,value) for key,value in case.items() if 'methond' in key)
    versions=dict((key,value) for key,value in case.items() if 'version' in key)
    verifys=dict((key,value) for key,value in case.items() if 'verify' in key)
    checks=dict((key,value) for key,value in case.items() if 'check' in key)
    get_values=dict((key,value) for key,value in case.items() if 'get_value' in key)
    real_txt=dict((key,value) for key,value in case.items() if 'real_response' in key)
    ispass=dict((key,value) for key,value in case.items() if 'ispass' in key)
    fail_reason=dict((key,value) for key,value in case.items() if 'fail_reason' in key)

    Flag=True

    for i in range(1,8):
        #循环次数和Excel表头、Excel接口数量一致
        print("------------------"+str(i)+"+++++++++++++++++++")
        tmp_step='step'+str(i)
        if steps[tmp_step]:
            tmp_url='url'+str(i)
            tmp_body='body'+str(i)
            tmp_methond='methond'+str(i)
            tmp_version='version'+str(i)
            tmp_verify="verify"+str(i)
            tmp_check="check"+str(i)
            tmp_get_value="get_value" +str(i)

            step=steps[tmp_step]
            url=urls[tmp_url]
            body=bodys[tmp_body]
            method=methonds[tmp_methond]
            version=versions[tmp_version]
            verify=verifys[tmp_verify]
            check=checks[tmp_check]
            get_value=get_values[tmp_get_value]
            logging.info("+++++++++++++++++++++++++")
            logging.info("分割case")
            logging.info("step: ")
            logging.info(step)
            logging.info("url: ")
            logging.info(url)
            logging.info("body: ")
            logging.info(body)
            logging.info("method: ")
            logging.info(method)
            logging.info("version: ")
            logging.info(version)
            logging.info("verify")
            logging.info(verify)
            logging.info("check")
            logging.info(check)
            logging.info("step: ")
            logging.info(step)
            logging.info("get_value: ")
            logging.info(get_value)

            # logging.info("case分割")
            logging.info("+++++++++++++++++++++++++")
            logging.info('\n')
            logging.info('\n')
            logging.info('\n')
            run_url=Run_Url(step,url,body,method,version,verify,check,get_value)
            if Flag:
                realtxt,flag,failreason=run_url.run()
                Flag=flag
            else:
                realtxt=""
                flag=""
                failreason=""
            save_value_list.append(step)
            save_value_list.append(url)
            save_value_list.append(body)
            save_value_list.append(method)
            save_value_list.append(version)
            save_value_list.append(verify)
            save_value_list.append(check)
            save_value_list.append(get_value)
            save_value_list.append(realtxt)
            save_value_list.append(flag)
            save_value_list.append(failreason)
    save_result(result_file,row,save_value_list)


class Run_Url():
    def __init__(self,step,url,body,method,version,verify,check,get_value):
        self.step=step
        self.url=url
        self.body=body
        self.method=method
        self.version=version
        self.verify=verify
        self.check=check
        self.get_value=get_value
    def handle_login(self,res):
        #处理登录接口后的部分，主要是一些信息的提取与保存
        logging.info("处理登录接口，相关信息提取")
        logging.info("接口返回"+str(res))

        try:
            accesstoken=res['data']['tokenInfo']['uhomeAccessToken']
            logging.info("accesstoken:  "+accesstoken)
            openate_ini.modify('headers','accesstoken',accesstoken)
        except:
            logging.error("accesstoken提取失败，可能是因为接口返回错误，没有该数据")

        try:
            accounttoken=res['data']['tokenInfo']['accountToken']
            logging.info("提取到的accounttoken： "+accounttoken)
            openate_ini.modify('headers','accounttoken',accounttoken)
        except:
            logging.error("accounttoken提取失败，可能是因为接口返回错误，没有该数据")

        try:
            userId = res['data']['tokenInfo']['uhomeUserId']
            logging.info("提取到的userId是： " + str(userId))
            openate_ini.modify("headers","userId",str(userId))
        except:
            logging.error("userId提取失败，可能是因为接口返回错误，没有该数据")


        #pass

    def run(self):
        #时间戳
        currTimes = time.time()
        time_stamp = int(round(currTimes * 1000))

        openate_ini.modify('headers','timestamp',str(time_stamp))

        # headers = self.get_header(time_stamp)
        # logging.info("headers: " + str(headers))
        # print("---------------headers------------------------")
        # print(headers)
        # print(type(headers))
        allurl="http://"+openate_ini.read_ini('url','domain')+"/"+self.url
        #print("allurl:  ",allurl)
        logging.info("请求url: "+allurl)
        if "登录" == self.step:

            #登录接口较为特殊，需要特殊出来，已经保存token等信息
            logging.info("这个是登录接口")
            #res=self.send_login()
            logging.info("先处理下body,看里面是否有配置的参数")
            self.body=handle_body(self.body,'user')
            # print("--------------------------这个是对body进行转码操作----------")
            # self.body = self.body.encode("utf-8").decode("latin1")
            logging.info("处理后body后的body:: ")
            logging.info(self.body)

            headers = self.get_header(time_stamp,self.verify)
            res=requests.post(url=allurl,headers=headers,data=self.body)
            logging.info("接口请求返回的数据是： "+str(res.json()))
            self.handle_login(res.json())
            flag,fail_reason = check_value(res, self.check)
            if res.text:
                real_txt=res.text
            else:
                real_txt=''
            if fail_reason:
                fail_reason=fail_reason
            else:
                fail_reason=""
            return real_txt,flag,fail_reason

        elif self.method==None or self.method=='':
            return '','',''

        elif self.method.upper()=='POST':
            #请求方法是post
            logging.info(self.step+" 是个 POST 请求，现在要发送该请求")
            logging.info("请求的url: ")
            logging.info(allurl)
            logging.info("请求的data: ")
            logging.info(self.body)

            logging.info("先处理下body,看里面是否有配置的参数")
            self.body=handle_body(self.body)
            # print("--------------------------这个是对body进行转码操作----------")
            # self.body = self.body.encode("utf-8").decode("latin1")

            logging.info("处理后body后的body:: ")
            logging.info(self.body)
            # logging.info("请求的heders: ")
            # logging.info(headers)
            try:
                headers = self.get_header(time_stamp,self.verify)
                logging.info("请求的heders: ")
                logging.info(headers)
                res=requests.post(url=allurl,headers=headers,data=self.body)
            except UnicodeEncodeError:
                print("--------------------------------------")
                print(self.body)
                print(type(self.body))
                """
                    这个地方有个坑，对于中文参数，需要转码才能发送；
                    并且计算签名要在转码之前计算
                """
                headers = self.get_header(time_stamp,self.verify)
                self.body = self.body.encode("utf-8").decode("latin1")
                logging.info("请求的heders: ")
                logging.info(headers)
                print("++++++++++++++++++++")
                print(self.body)
                print(type(self.body))
                res=requests.post(url=allurl,headers=headers,data=self.body,verify=False)

            logging.info("这个地方要开始去进行校验结果了")
            # print(res.status_code)
            # print(res.text)
            logging.info("需要校验的内容")
            logging.info(self.check)
            logging.info("实际的返回")
            logging.info(res.text)
            flag,fail_reason=check_value(res,self.check)
            if flag:
                #检验通过才能去提要需要的内容
                #提取要提取的内容
                save_value(res,self.get_value)
            if res.text:
                real_txt=res.text
            else:
                real_txt=''
            if fail_reason:
                fail_reason=fail_reason
            else:
                fail_reason=""
            return real_txt,flag,fail_reason


        elif self.method.upper()=="GET":
            logging.info(self.step+" 是个 GET 请求，现在要发送该请求")
            logging.info("先处理下body,看里面是否有配置的参数")
            self.body = handle_body(self.body)
            try:
                headers = self.get_header(time_stamp,self.verify)
                logging.info("请求的heders: ")
                logging.info(headers)
                res=requests.post(url=allurl,headers=headers,data=self.body)
            except UnicodeEncodeError:
                print("--------------------------------------")
                print(self.body)
                """
                   这个地方有个坑，对于中文参数，需要转码才能发送；
                   并且计算签名要在转码之前计算
                """
                headers = self.get_header(time_stamp,self.verify)
                self.body = self.body.encode("utf-8").decode("latin1")
                logging.info("请求的heders: ")
                logging.info(headers)
                print("++++++++++++++++++++")
                print(self.body)
                print(type(self.body))
                res = requests.get(url=allurl, headers=headers, data=self.body, verify=False)
            logging.info("这个地方要开始去进行校验结果了")
            # print(res.status_code)
            # print(res.text)
            logging.info("需要校验的内容")
            logging.info(self.check)
            logging.info("实际的返回")
            logging.info(res.text)
            flag, fail_reason = check_value(res, self.check)
            # 提取要提取的内容
            save_value(res, self.get_value)
            if res.text:
                real_txt=res.text
            else:
                real_txt=''
            if fail_reason:
                fail_reason=fail_reason
            else:
                fail_reason=""
            return real_txt,flag,fail_reason

            # res=requests.get(url=allurl,headers=headers,data=self.body)
            # print(res.text)

        else:
            print("略过-------------")
            logging.info("在这里进行保存，先留个坑")
            return '','',''


    def get_header(self,timestamp,verify):
        headers={}
        headers['sign']=self.get_sign(timestamp,verify)
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
    def send_login(self):
        #先检查是否是登录接口，登录接口需要
        pass
    def get_sign(self,timestamp,verify):
        #verify用来标志是使用md5加密还是sha256加密
        if "md5" in str(verify).lower():
            Sign=md5(self.url,self.body,str(timestamp))
        elif "sha256" in str(verify).lower():
            Sign=sha256(self.url,self.body,str(timestamp))
        else:
            #默认使用sha256
            Sign = sha256(self.url, self.body, str(timestamp))
        return Sign.get_sign()

    def _handle_data(self, data):
        # 将请求携带参数里面的中文进行处理,data为字典格式
        for k, v in data.items():
            try:
            # 匹配出带有汉字的value
                hanzi = re.search(r'[\u4E00-\u9FA5]*', v).group()
                #  匹配到，则替换；未匹配到，不做任何处理
                if hanzi:
                    data[k] = hanzi.encode('utf-8').decode('latin1')
            except Exception as f:
                pass
        return data



    # def check_value(self,res,check_value):
    #     flag=True
    #     fail_list=[]
    #     if res.status_code!=200:
    #         flag=False
    #         failreason="status_code错误，不是200"
    #         logging.error(failreason)
    #         fail_list.append(failreason)
    #         logging.error(res.status_code)
    #     check_value=check_value.strip()
    #     restext=res.text.strip()
    #     check_value_list=check_value.split(';')
    #     logging.info("-----------check_value_list--------------")
    #     logging.info(check_value_list)
    #     logging.info(len(check_value_list))
    #     logging.info("----------------restext-------------------------")
    #     logging.info(restext)
    #     for checkvalue in check_value_list:
    #         if checkvalue not in restext:
    #             flag=False
    #             failreason='结果参数校验失败'
    #             logging.error(failreason)
    #             fail_list.append(failreason)
    #             logging.error("期望参数")
    #             logging.error(checkvalue)
    #             logging.error("实际结果")
    #             logging.error(restext)
    #
    #     if flag:
    #         logging.info("校验正确")
    #         fail_list.append("pass")
    #         return flag,fail_list
    #     else:
    #         logging.error("校验失败")
    #         return flag,fail_list







if __name__=="__main__":
    #headers={}
    # # res=openate_ini.read_ini('headers', 'clientid')
    # # print(res)
    # # print(type(res))
    # # headers['id']=res
    # # print(headers)
    url="http://uhome.haier.net/emuplus/family/v1/family/list"
    # headers['clientid'] = '2014022801010'
    #headers['accessToken'] = 'TGT1N8CDW9QAHWY21YPYIM5GWHSRH0'
    # #headers['accounttoken'] = '06204e7ca80a4f70bb729e1535bf7dbf'
    # headers['Content-Type'] = 'application/json;charset = utf-8'
    # headers['appId'] = 'MB-UZHSH-0001'
    # headers['appkey'] = 'f50c76fbc8271d361e1f6b5973f54585'
    # headers['userid'] = '36427446'
    # headers['appversion'] = '5.2.0'
    #headers['clientId']='2014022801010'
    # headers['sign']='76aecf937a510f7d8c6cd10b4d53db1e'
    # headers['clientModel']='fdsafdfsadf'
    # headers['timestamp']='20160111141341'
    # headers['Host']='uhome.haier.net'

    #headers['appKey']='f50c76fbc8271d361e1f6b5973f54585'
    headers['clientId']='2014022801010'
    #headers['appVersion']='5.2.0'
    headers['appId']='MB-UZHSH-0000'
    #headers['Content-Type']='application/json;charset=utf-8'
    headers['accessToken']='TGT1N8CDW9QAHWY21YPYIM5GWHSRH0'
    headers['timestamp'] ='20160111141341'
    #headers['Host']='uhome.haier.net'
    #headers['clientModel']='fdsafdfsadf'
    headers['sign']='76aecf937a510f7d8c6cd10b4d53db1e'
    headers['accounttoken']='06204e7ca80a4f70bb729e1535bf7dbf'
    print(headers)
    print(type(headers))


    body={}
    res=requests.post(url=url,headers=headers,data=body)
    # res=requests.request("POST", url, headers=headers, data=body)
    print(res.status_code)
    print(res.text)

    sh=md5("/emuplus/family/v1/family/list",str(body),'20160111141341')
    print("计算签名")
    print(sh.get_sign())


    #url = "http://uhome.haier.net/emuplus/family/v1/family/list"
    payload = {}
    headers1 = {
        'appKey': 'f50c76fbc8271d361e1f6b5973f54585',
        'clientId': '2014022801010',
        'appVersion': '5.2.0',
        'appId': 'MB-UZHSH-0000',
        'Content-Type': 'application/json;charset=utf-8',
        'accessToken': 'TGT1N8CDW9QAHWY21YPYIM5GWHSRH0',
        'timestamp': '20160111141341',
        'Host': 'uhome.haier.net',
        'clientModel': 'fdsafdfsadf',
        'sign': '76aecf937a510f7d8c6cd10b4d53db1e'
    }
    print(headers1)
    print(type(headers1))

    response = requests.request("POST", url, headers=headers1, data=payload)

    print(response.text)

    currTimes=time.time()
    time_stamp=int(round(currTimes*1000))
    print(time_stamp)
