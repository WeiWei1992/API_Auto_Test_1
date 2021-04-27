import logging
import re
from common.operate_ini import Openate_Ini

from configparser import NoOptionError
open_ini=Openate_Ini()

def befor_cheak_value(check_value):
    #该函数的功能是检查checn_value中是否有配置的参数
    #如果有的话就转成实际的参数
    logging.info("首先检查下校验值中是否有配置文件中的参数")
    if '**' in check_value:
        pattern = re.compile(r'"(\*\*.*?\*\*)"')  # 查找
        print(pattern)
        result = pattern.findall(check_value)
        print(result)

        #现在result是列表，需要转成字符串
        result = str(result)
        # print(result)
        # # print("---result[1:]---")
        # result = result[2:]
        # # print(result)
        # # print("---result[:-1]---")
        # result = result[:-2]
        # print(result)
        # logging.info(result)

        # result=result.replace("**","")
        #
        # print(result)
        #去点'' []
        result=result.replace("'",'')
        print(result)
        result=result.replace('[','')
        print(result)
        result = result.replace(']', '')
        print(result)

        value=get_inivalue(result)
        value_list=value.split(',')
        print("-------")
        print(value_list)

        realvalu=value_list[0].replace("'",'')
        #替换
        body1=check_value.replace(result,realvalu)
        print(body1)
        return body1
    else:
        return check_value


def check_value(res, check_values):
    check_values=befor_cheak_value(check_values)
    # resflag=False
    # flag = True
    flag=False
    fail_list = []
    failreason_code=''
    if res.status_code != 200:
        flag = False
        failreason_code = "status_code错误，不是200"
        logging.error(failreason_code)
        fail_list.append(failreason_code)
        logging.error(res.status_code)

    check_values_list=check_values.split('|')
    for check_value in check_values_list:
        check_value=str(check_value)
        check_value = check_value.strip()
        restext = res.text.strip()
        check_value_list = check_value.split(';')
        logging.info("-----------check_value_list--------------")
        logging.info(check_value_list)
        logging.info(len(check_value_list))
        logging.info("----------------restext-------------------------")
        logging.info(restext)
        flag_tmp=True
        for checkvalue in check_value_list:
            if checkvalue not in restext:
                flag_tmp = False
                failreason = '结果参数校验失败'
                logging.error(failreason)
                # fail_list.append(failreason)
                logging.error("期望参数")
                logging.error(checkvalue)
                logging.error("实际结果")
                logging.error(restext)
        if flag_tmp:
            flag=True


    if flag:
        logging.info("校验正确")
        fail_list.append("pass")
        return flag, fail_list
    else:
        logging.error("校验失败")
        fail_list.append("结果参数校验失败")
        return flag, fail_list



def save_value(res,get_value):
    # print("-----")
    # print(get_value)
    logging.info("保存需要保存的配置文件")
    logging.info(get_value)

    if get_value and "pattern" in get_value:
        try:
            logging.info("使用自定义的正则表达式提取内容")
            #logging.info("-------------------------")
            logging.info(res.text)
            get_value_list=get_value.split('--')
            logging.info("读入的需要提取的内容是：")
            logging.info(get_value_list)
            logging.info(type(get_value_list))
            tmp_pattern=get_value_list[1]
            pattern=re.compile(tmp_pattern)
            logging.info("正则表达式提取的正则是： "+str(pattern))
            result=pattern.findall(res.text)
            logging.info("正则提取到的内容是： ")
            logging.info(result)
            #print(result)
            logging.info(type(result))
            logging.info("转换成字符串形")
            result = str(result)
            logging.info("去点前后的[ ] ")
            result = result[1:]
            result = result[:-1]
            logging.info(result)
            open_ini = Openate_Ini()
            body_key=get_value_list[2]
            logging.info("读入的key")
            logging.info(body_key)
            open_ini.modify('body', body_key, str(result))
        except:
            logging.error("保存配置文件失败，可能是因为接口返回数据没有该数据")
        #pass
    elif get_value:
        res=res.text
        logging.info("请求返回的数据")
        logging.info(res)
        get_value_list=get_value.split(';')
        logging.info("需要保存的参数列表：")
        logging.info(get_value_list)
        print(get_value_list)
        for body_key in get_value_list:
            try:
                logging.info("获取")
                logging.info(body_key)
                pattern = re.compile(r'"'+body_key+'\":\"(.*?)\"')  #
                logging.info("提取的正则")
                logging.info(pattern)
                #print(res)
                result=pattern.findall(res)

                # print("======xxxxxxxx=========")
                # print(result)
                logging.info("本次保存的参数是： ")
                logging.info(body_key)
                logging.info("该参数的获取的值是： ")
                logging.info(result)
                logging.info("转换成字符串形")
                result=str(result)
                logging.info(result)

                logging.info("去点前后的[ ] ")
                #print("---result[1:]---")
                result=result[1:]
                # print(result)
                # print("---result[:-1]---")
                result=result[:-1]
                # print(result)
                logging.info(result)
                open_ini = Openate_Ini()
                open_ini.modify('body',body_key,str(result))
            except:
                logging.error("保存配置文件失败，可能是因为接口返回数据没有该数据")
                continue

    else:
        logging.info("get_value参数空，略过即可")



def handle_body(body,seciton=None):
    if body==None:
        return '{}'
    #处理请求参数，如果里面有自定义的配置参数，需要在配置文件中读取
    #logging.info("处理body中还有配置文件情况")
    elif '**' in body:
        logging.info("处理body中还有配置文件情况")
        logging.info(body)
        pattern = re.compile(r'"(\*\*.*?\*\*)"')  # 查找
        print(pattern)
        result = pattern.findall(body)



        logging.info("提取到的配置文件中body的值")
        logging.info(result)
        i=1
        for result_tmp in result:
            try:
                logging.info("处理body中的第 " +str(i)+" 个配置文件 "+str(result_tmp)+"的值 ")
                value_tmp=get_inivalue(result_tmp,seciton)
                logging.info("通过该配置文件，查询配置文件得到的值是： ")
                logging.info(value_tmp)
                # realvalue_tmp=value_tmp[0].replace("'","")
                #logging.info("从配置文件中获取到的内容去掉引号，因为他是字符串类型")
                logging.info(value_tmp)
                result_tmp_list=value_tmp.split(',')
                logging.info("从配置文件中获取到的内容转成列表形式")
                logging.info(result_tmp_list)
                realvalue=result_tmp_list[0]
                logging.info("提取列表中的第一个值进行替换")
                logging.info(realvalue)
                realvalue=realvalue.replace("'","")
                logging.info("配置文件中获取到的值去点引号后的值是")
                logging.info(realvalue)
                body=body.replace(result_tmp,realvalue)
                i=i+1
            except:
                logging.error("配置文件中读取body配置文件出错，没有读到该值，该值直接赋值空")
                body=body.replace(result_tmp,"")
        logging.info("配置文件替换完后的body")
        logging.info(body)
        return body



        # value=get_inivalue(result)
        # value_list=value.split(',')
        # print("-------")
        # print(value_list)
        #
        # realvalu=value_list[0].replace("'",'')
        # #替换
        # body1=body.replace(result,realvalu)

        #print(body1)
        # logging.info("处理完body中含有配置文件后的数据")
        # logging.info(body1)
        # return body1
    else:
        return body

def get_inivalue(key,seciton=None):
    #去掉**
    key=key[2:]
    key=key[:-2]
    if seciton=="user":
        value=open_ini.read_ini('user',key)
    else:
        value = open_ini.read_ini('body', key)
    return value



if __name__=="__main__":
    check_value1='"retCode":"00000";"retInfo":"操作成功";"roomId":"**roomId**"'
    check_value1=befor_cheak_value(check_value1)

    print(check_value)
    #save_value('res','familyId')

    # tmp='{"retCode":"00000","retInfo":"操作成功","data":{"createfamilies":[{"createTime":"2019-11-29 09:10:36","familyMembers":null,"familyOwner":"36427446","appId":"MB-UZHSH-0000","familyOwnerInfo":null,"familyId":"648139833036000000","familyName":"魏艾辰","familyPosition":"青岛 城阳","locationChangeFlag":false,"familyDeviceCount":"0","familyUserCount":"2","familyVirtUserCount":"0","familyLocation":{"longitude":120.37,"latitude":36.3,"cityCode":"370214"},"rooms":null,"isDefault":0},{"createTime":"2021-03-30 15:49:52","familyMembers":null,"familyOwner":"36427446","appId":"MB-UZHSH-0000","familyOwnerInfo":null,"familyId":"331188556991000001","familyName":"陈明霞","familyPosition":"临沂 费县","locationChangeFlag":false,"familyDeviceCount":"0","familyUserCount":"1","familyVirtUserCount":"0","familyLocation":{"longitude":117.98584,"latitude":35.25497,"cityCode":"371325"},"rooms":null,"isDefault":1}],"joinfamilies":[]}}'
    # save_value(tmp,'familyId;familyName;familyPosition')

    # body='{"roomName": "新增的房间的名称","familyId": "**familyId**"}'
    # handle_body(body)
