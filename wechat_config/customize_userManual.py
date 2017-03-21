import requests
import os
import sys # provide option
PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
token_url = "https://api.weixin.qq.com/cgi-bin/token" # Change to control server
create_interface = "https://api.weixin.qq.com/cgi-bin/menu/create"

class userInterface:
    token = ""
    key = dict()
    @staticmethod
    def init():
        # Initialization: acquire access_token from control server
        with open(PATH+r"\..\Static\accesskey_token.json","r") as credential_file:
            credential = eval("".join([i.strip() for i in credential_file.readlines()]))
            # print(credential)
            credential_file.close()
        try:
            userInterface.key = requests.get(url=token_url,params=credential).json()
            userInterface.token = userInterface.key["access_token"]
        except Exception as err:
            if "errcode" in userInterface.key:
                print("ERROR: errcode:%\t%",(userInterface.key["errcode"],userInterface.key["errmsg"]))
            else:
                print("ERROR: "+str(err))
            exit()
    @staticmethod
    def createManual():
        with open(PATH+r"\..\Static\userInterface.json","rb") as config_file:
            try:
                # print([ i.decode() for i in config_file.readlines()])
                config = eval("".join([i.strip().decode() for i in config_file.readlines()]))
            except Exception as err:
                print(str(err))
                exit()
            credential = {'access_token':userInterface.token}
            response = requests.post(create_interface,params=credential,data=config).json()
            print("Result\nerrcode:",response["errcode"],response["errmsg"])
    """
    @staticmethod
    def delInterface():
    @staticmethod
    def viewInterface():
    """
if __name__ == "__main__":
    # Process different function through options
    userInterface.init()
    userInterface.createManual()
    # Some methods
    exit()
