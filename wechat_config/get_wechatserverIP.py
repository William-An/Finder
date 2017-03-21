import requests
import os
import sys # provide option
PATH = os.path.abspath(os.path.dirname(sys.argv[0]))
token_url = "https://api.weixin.qq.com/cgi-bin/token" # Change to control server
getip_url = "https://api.weixin.qq.com/cgi-bin/getcallbackip"
def getip(token_url=token_url):
    with open(PATH+r"\..\Static\accesskey_token.json","r") as credential_file:
        credential = eval("".join([i.strip() for i in credential_file.readlines()]))
        # print(credential)
        credential_file.close()
    try:
        key = requests.get(url=token_url,params=credential).json()
        token = key["access_token"]
    except Exception as err:
        if "errcode" in key:
            print("ERROR: errcode:%\t%",(key["errcode"],key["errmsg"]))
        else:
            print("ERROR: "+str(err))
            return str(err)
        exit()
    try:
        response = requests.get(getip_url,params={'access_token':token}).json()
        ip_list = response["ip_list"]
        return ip_list
    except Exception as err:
        if "errcode" in response:
            print("ERROR: errcode:%\t%",(key["errcode"],key["errmsg"]))
        else:
            print("ERROR: "+str(err))
        return None
    exit()
if __name__ == "__main__":
    print(getip(token_url))
