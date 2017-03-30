import requests
import os
import sys # provide option
import argparse # parse options
import json

PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
token_url = "https://api.weixin.qq.com/cgi-bin/token" # Change to control server
create_interface = "https://api.weixin.qq.com/cgi-bin/menu/create"
get_Allinterface = "https://api.weixin.qq.com/cgi-bin/menu/get"
get_Currentinterface = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info"
del_interface = "https://api.weixin.qq.com/cgi-bin/menu/delete"

# del, getall, getcurrent could be merge into one method by changing params

class userInterface:
    credential = dict()
    @staticmethod
    def init():
        # Initialization: acquire access_token from control server
        with open(PATH+r"\..\Static\accesskey_token.json","r") as credential_file:
            credential = eval("".join([i.strip() for i in credential_file.readlines()]))
            #print(credential)
            credential_file.close()
        try:
            key = requests.get(url=token_url,params=credential).json()
            token = key["access_token"]
            userInterface.credential.update([("access_token",token)])
            #print(token)
        except Exception as err:
            if "errcode" in key:
                print("ERROR: errcode:%\t%",(key["errcode"],key["errmsg"]))
            else:
                print("ERROR: "+str(err))
            exit()
    @staticmethod
    def createManual(file_addr):
        with open(file_addr,"rb") as config_file:
            try:
                # print([ i.decode() for i in config_file.readlines()])
                config = eval("".join([i.strip().decode() for i in config_file.readlines()]))
                # print(config)
            except Exception as err:
                print(str(err))
                exit()
            response = requests.post(create_interface,params=userInterface.credential,data=json.dumps(config)).json() # Must use json
            print("Result\nerrcode:",response["errcode"],response["errmsg"])
    @staticmethod
    def delInterface():
        # Write into function? paras are url and credential?
        response = requests.get(del_interface,params=userInterface.credential).json()
        print("Result\nerrcode:",response["errcode"],response["errmsg"])
    @staticmethod
    def viewAllInterface():
        response = requests.get(get_Allinterface,params=userInterface.credential).json()
        if "errcode" in response:
            print("Result\nerrcode:",response["errcode"],response["errmsg"])
        else:
            print(response)
    @staticmethod
    def viewCurrentInterface():
        response = requests.get(get_Currentinterface,params=userInterface.credential).json()
        if "errcode" in response:
            print("Result\nerrcode:",response["errcode"],response["errmsg"])
        else:
            print(response)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Provide access to modify/view wechat customized usermanual")
    parser.add_argument('-d','--delete',action='store_true',help='Delete ALL interfaces')
    parser.add_argument('-l','--list',action="store_true",help="List all userinterfaces")
    parser.add_argument('-i','--inspect',action="store_true",help="List current userinterface")
    parser.add_argument('-c','--config',help="upload the userinterface configuration")
    option=parser.parse_args()
    userInterface.init()
    if option.delete:
        userInterface.delInterface()
    elif option.list:
        userInterface.viewAllInterface()
    elif option.inspect:
        userInterface.viewCurrentInterface()
    elif option.config:
        userInterface.createManual(option.config)
    exit()