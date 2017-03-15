import requests
import time
import os
import sys
import web
"""
Using two server to provide wechat subscription service,
one for acquring token, one for processing request
"""
PATH = os.path.abspath(os.path.dirname(sys.argv[0])) # The path of this file
accesskey_url = "https://api.weixin.qq.com/cgi-bin/token"
token=""
expire_time=0
timer=os.times()
urls=(
    "/access_token","token_acquirer"
)
class token_acquirer:
    def __init__(self):
        self.token, self.expire_time= self.get_token()
    def GET(self):
        if expire_time < 120:
            self.get_token()
        else:
            return self.token
    def get_token(self):
        with open(PATH+r"\..\Static\log","w+") as log:
            with open(PATH+r"\..\Static\accesskey_token.json") as credential_file: # Use relative path to find the credential file
                credential = credential_file.readlines()
                credential = [i.strip() for i in credential]
                credential = eval("".join(credential)) # Catenate list to form json
                #print(credential)
                try:
                    key = requests.get(accesskey_url,params=credential).json()
                except Exception as err:
                    msg = time.strftime("%Y-%m-%d %H:%M:%S")+"\t[-]Error in get:"+err
                    log.writelines(msg)
                    log.flush()
                    print(msg)
                    return
                if "errcode" in key:
                    msg = time.strftime("%Y-%m-%d %H:%M:%S")+"\t[-]Unable to acquire access_token:"+key["errcode"]+"\t"+key["errmsg"]
                    log.writelines(msg)
                    log.flush()
                    print(msg)
                    time.sleep(10)
                    # Send email?
                msg = time.strftime("%Y-%m-%d %H:%M:%S")+"\t[+]\ttoken:"+key["access_token"]
                log.writelines(msg)
                log.flush() # Save output
                print(msg)
                return key["access_token"], key[""]


