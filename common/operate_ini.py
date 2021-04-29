import configparser
import os
import shutil
import logging
# my_path=os.path.abspath(os.getcwd())
# inifile=my_path+'/config/config.ini'
# print(inifile)

#当前文件的路径
# pwd = os.getcwd()
# #当前文件的父路径
# father_path=os.path.abspath(os.path.dirname(pwd)+os.path.sep+".")
# print(father_path)
father_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
#print(father_path)

# #当前文件的前两级目录
# grader_father=os.path.abspath(os.path.dirname(pwd)+os.path.sep+"..")
# print(grader_father)

class Openate_Ini():
    def __init__(self):
        self.inipath=father_path+'/config/config.ini'
        self.inipath_new=father_path+'/config/config_new.ini'
        logging.info("ini的路径---------------------")
        logging.info(self.inipath)
        # self.config=configparser.ConfigParser()
        # #self.config=configparser.RawConfigParser()
        # self.config.read(self.inipath)
        # print("iniPath: "+str(self.inipath))

    def read_ini(self,session,key):
        try:
            config = configparser.ConfigParser()
            # self.config=configparser.RawConfigParser()
            config.read(self.inipath)
            logging.info("iniPath: " + str(self.inipath))
            res=config.get(session,key)
            return res
        except Exception as e:
            logging.error("读取ini文件失败，失败信息如下：")
            logging.error(e)
            logging.error("返回个空吧")
            return ''
        #print(res)
    def modify(self,session,key,value):
        # with open()
        #
        try:
            config = configparser.ConfigParser()
            # self.config=configparser.RawConfigParser()
            config.read(self.inipath)
            logging.info("iniPath: " + str(self.inipath))

            logging.info("修改保存ini")
            logging.info(session)
            logging.info(key)
            logging.info(value)
            config.set(session,key,value)
            config.write(open(self.inipath,"r+"))
        except Exception as e:
            logging.error("修改ini文件失败")
            logging.error("那就什么都不做吧，加个异常处理，防止程序中断")
    def add_section(self,section):
        #添加指定的节点
        config = configparser.ConfigParser()
        #config.add_section(section)
        sections=config.sections()
        logging.info(sections)
        #print(config.items())
        config.write(open(self.inipath, "a"))


        # sections=config.sections()
        # print(sections)
        # if section in sections:
        #     return
        # else:
        #     config.add_section(section)

    def remove_section(self,section):
        #删除节点
        config = configparser.ConfigParser()
        return config.remove_section(section)

    def sections(self):
        #返回文件中所有的sections
        config = configparser.ConfigParser()
        return config.sections()

    def delect(self):
        with open(self.inipath,'r') as f:
            with open(self.inipath_new,'w') as g:
                for line in f.readlines():
                    g.write(line)
                    if '[body]' in line:
                        break
        shutil.move(self.inipath_new,self.inipath)


#
if __name__=="__main__":
    op=Openate_Ini()
    op.delect()
    # res=op.read_ini('body','familyname')
    # print(res)

    # op.remove_section('body')
    # print(op.sections())
    # print("===========")
    # op.add_section('body')

    # body
    # familyId
    # '648139833036000000', '331188556991000001'
    # op.modify('body',"familyname","x11xx")
    # #res = op.read_ini('section1', 'key2')
    # print(res)

