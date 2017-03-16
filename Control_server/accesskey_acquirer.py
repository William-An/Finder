import requests
import time
import os
import sys
import web
import json
"""
Using two server to provide wechat subscription service,
one for acquring token, one for processing request
"""
PATH = os.path.abspath(os.path.dirname(sys.argv[0])) # The path of this file
accesskey_url = "https://api.weixin.qq.com/cgi-bin/token"
web.config.debug = False # Set true to open debug output
timer=os.times()
urls=(
    "/access_token","token_acquirer"
)
class token_acquirer:
    def __init__(self):
        """
        Log server's initialization
        Store debug log
        """
        self.expire_time = 0
        self.token = ""
        msg = time.strftime("%Y-%m-%d %H:%M:%S")+"\tServer begins..."
        print(msg)
        with open(PATH+r"\..\Static\log","a") as log:
            log.writelines(msg)
            log.write("\n")
            log.flush()
            log.close()
    def GET(self):
        # What about multi reuse??? 多个服务器请求时怎么办
        credential = dict(web.input())
        if self.expire_time < 120: # If access_token is not valid
            self.token, self.expire_time = self.get_token(credential)
            return self.token
        else:
            return self.token
    def get_token(self,credential):
        with open(PATH+r"\..\Static\log","a") as log:
            for i in range(5): # Try 5 times
                try:
                    key = requests.get(accesskey_url,params=credential).json()
                except json.decoder.JSONDecodeError as err:
                    msg = time.strftime("%Y-%m-%d %H:%M:%S")+"\t[-]Error in get:"+str(err)+"\t Usually inapporpriate GET input"
                    # Write a function?
                    log.writelines(msg+"\n")
                    log.flush()
                    print(msg)
                    #time.sleep(1)
                    continue
                if "errcode" in key:
                    msg = time.strftime("%Y-%m-%d %H:%M:%S")+"\t[-]Unable to acquire access_token:"+str(key["errcode"])+"\t"+key["errmsg"]
                    log.writelines(msg+"\n")
                    log.flush()
                    print(msg)
                    #time.sleep(1)
                    continue
                    # Send email?
                msg = time.strftime("%Y-%m-%d %H:%M:%S")+"\t[+]\ttoken:"+str(key["access_token"])
                log.writelines(msg+"\n")
                log.flush() # Save output
                print(msg)
                log.close()
                return key["access_token"], key["expires_in"]
            else:
                print(msg)
                log.close()
                return "ERROR:"+msg,0 # Read the last 5 lines and print
if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()

