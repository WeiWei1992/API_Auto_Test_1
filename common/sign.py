import hashlib
import logging
from common.operate_ini import Openate_Ini
# opini=Openate_Ini()
print("===========")
# print(opini.inipath)
class sha256():
    #sha256签名算法
    #传入的参数包括url,body,timestamp(时间戳)，时间戳要传入，
    # 不能再这里生成，因为有的请求headers也需要时间戳，这样能保证两处的时间戳一致
    # 计算签名需要的参数是：url+body+appid+appkey+timestamp,appid和appkey从配置文件中读取
    def __init__(self,url,body,timestamp):
        self.opini=Openate_Ini()
        self.url=url
        self.body=body
        self.tiimestamp=timestamp
        self.appid=self.opini.read_ini('headers','appId')
        self.appkey=self.opini.read_ini('headers','appKey')
        print(self.appid)
        print(self.appkey)

    def get_sign(self):
        self.appkey=self.appkey.strip()  #去点字符串两边的空格

        if (self.body!=None):
            self.body=self.body.strip()

        if (self.body!=""):
            self.body=self.body.replace(" ","")
            self.body=self.body.replace("\t","")
            self.body=self.body.replace("\r","")
            self.body=self.body.replace("\n","")

        #sha256需要加上url,md5不需要加上url
        mystr=self.url+self.body+self.appid+self.appkey+self.tiimestamp
        #mystr =self.body + self.appid + self.appkey + self.tiimestamp
        logging.info("要加密的数据")
        logging.info(mystr)
        sha256 = hashlib.sha256()

        #mystr = '/emuplus/secuag/account/v1.0/login{"username":"18161982838","password":"123456","captchaToken":"","captchaAnswer":""}MB-UZHSH-00015dfca8714eb26e3a776e58a8273c87521616047412445'
        sha256.update(mystr.encode('utf-8'))
        return sha256.hexdigest()
    # def cut(self,input):
    #     tmp=input.strip()
    # def cut_appkey(self,inputkey):
    #     tmp=inputkey.strip()

class md5():
    # md5签名算法
    # 传入的参数包括url,body,timestamp(时间戳)，时间戳要传入，
    # 不能再这里生成时间戳，因为有的请求headers也需要时间戳，这样能保证两处的时间戳一致
    # 计算签名需要的参数是：url+body+appid+appkey+timestamp,appid和appkey从配置文件中读取
    def __init__(self, url, body, timestamp):
        self.opini = Openate_Ini()
        self.url = url
        self.body = body
        self.tiimestamp = timestamp
        self.appid = self.opini.read_ini('headers', 'appId')
        self.appkey = self.opini.read_ini('headers', 'appKey')
        print(self.appid)
        print(self.appkey)

    def get_sign(self):
        self.appkey = self.appkey.strip()  # 去点字符串两边的空格

        if (self.body != None):
            self.body = self.body.strip()

        if (self.body != "" and self.body!=None):
            self.body = self.body.replace(" ", "")
            self.body = self.body.replace("\t", "")
            self.body = self.body.replace("\r", "")
            self.body = self.body.replace("\n", "")

        # mystr=self.url+self.body+self.appid+self.appkey+self.tiimestamp
            mystr = self.body + self.appid + self.appkey + self.tiimestamp
            logging.info(mystr)
        else:
            mystr =self.appid + self.appkey + self.tiimestamp
            logging.info(mystr)

        md5_val = hashlib.md5(mystr.encode('utf-8')).hexdigest()
        return md5_val

        #去掉空格


if __name__=="__main__":
    # url = "/emuplus/family/v1/family/list"
    # body = ''
    # timestamp = '20160111141341'
    # op=sha256(url,body,timestamp)
    # res=op.get_sign()
    # print(res)

    # mystr="MB-UZHSH-0000f50c76fbc8271d361e1f6b5973f5458520160111141341"
    # sha256 = hashlib.sha256()

    mystr = '/emuplus/secuag/account/v1.0/login{"username":"18161982838","password":"123456","captchaToken":"","captchaAnswer":""}MB-UZHSH-00015dfca8714eb26e3a776e58a8273c87521616047412445'
    # sha256.update(mystr.encode('utf-8'))
    # print(sha256.hexdigest())

    print("计算md5")
    md5_val=hashlib.md5(mystr.encode('utf-8')).hexdigest()
    print(md5_val)

    # tep="nihao"
    # print(tep)
    # tep=tep.replace("ni",'wo')
    # print(tep)
