import requests
import sqlite3
import web
import time
import os
import sys

# 加密？-> 出租服务器
"""
Using two server to provide wechat subscription service,
one for acquring token, one for processing request
"""
PATH = os.path.abspath(os.path.dirname(sys.argv[0])) # The path of this file
timer=os.times()

web.config.debug = False # Set true to open debug output
accesskey_url = "https://api.weixin.qq.com/cgi-bin/token"
urls=(
    "/access_token", "token_acquirer",
    "/log", "log_replyier"
)

database = sqlite3.connect(PATH+r"\..\Static\appid.db") # Initializing database
#database_dir = PATH+r"\..\Static\appid.db"
#database = web.database(dbn="sqlite",db=database_dir)
# Create table to store tokens
try:
    database.execute('''CREATE TABLE appid_token(appid text, current_token text, last_time real)''')
except:
    del database

class token_acquirer:
    db=None
    def __init__(self):
        """
        Log server's initialization
        Store debug log
        """
        # Initialize database
        # Class attribute?
        token_acquirer.db = web.database(dbn="sqlite",db=PATH+r"\..\Static\appid.db")
        self.last_time = 0
        msg = time.strftime("%Y-%m-%d %H:%M:%S")+"\tProcessing request..."
        print(msg)
        with open(PATH+r"\..\Static\log","a") as log:
            log.writelines(msg)
            log.write("\n")
            log.flush()
            log.close()
    def GET(self):
        # What about multi reuse??? 多个服务器请求时怎么办 -> SQL
        # print(web.ctx.ip)
        credential = dict(web.input())
        # print(credential["appid"])
        # Get elapse time to calculate expire_time -> time.time() store last record in sql, calculate with this request
        # SELECT expire_time FROM appid_token WHERE appid =
        try:
            # Using db.query to process regular sql code
            self.last_time = token_acquirer.db.query("SELECT last_time FROM appid_token WHERE appid = $appid",vars= {"appid":credential["appid"]})["last_time"]
            # print(self.last_time)
        except: # New appid?
            # INSERT INTO appid_token VALUES(appid, current_token, last_time)
            token_acquirer.db.query("INSERT INTO appid_token VALUES($appid,$current_token,$last_time)",vars={"appid":credential["appid"],"current_token":"", "last_time":self.last_time})
            # print(token_acquirer.db.select('appid_token')[0])
        # Simplify this if clause?
        if time.time() - self.last_time > 7180: # If access_token is nearly invalid
            self.token = self.get_token(credential)
            print(self.token)
            if "ERROR" in self.token:
                return self.token
            # Update token and time
            # UPDATE appid_token SET current_token = , expire_time =  WHERE appid =
            # print(token_acquirer.db.select('appid_token')[0])
            token_acquirer.db.query("UPDATE appid_token SET current_token =$current_token , last_time= $last_time WHERE appid = $appid",vars={"appid":credential["appid"],"current_token":self.token, "last_time":time.time()})
            # print(token_acquirer.db.select('appid_token')[0])
            return self.token
        else:
            # find token in sql
            return token_acquirer.db.select('appid_token',id,what="current_token",where="appid = "+credential["appid"])["current_token"]
    def get_token(self,credential):
        with open(PATH+r"\..\Static\log","a") as log:
            for i in range(5): # Try 5 times
                try:
                    key = requests.get(accesskey_url,params=credential).json()
                except Exception as err:
                    # Change to use string format: "%",var
                    msg = time.strftime("%Y-%m-%d %H:%M:%S")+"\t[-] ID:"+credential["appid"]+"\tError in get:"+str(err)#+"\t Usually inapporpriate GET input"
                    # Write a function?
                    log.writelines(msg+"\n")
                    log.flush()
                    print(msg)
                    #time.sleep(1)
                    continue
                if "errcode" in key:
                    msg = time.strftime("%Y-%m-%d %H:%M:%S")+"\t[-] ID:"+credential["appid"]+"\tUnable to acquire access_token:"+str(key["errcode"])+"\t"+key["errmsg"]
                    log.writelines(msg+"\n")
                    log.flush()
                    print(msg)
                    #time.sleep(1)
                    continue
                    # Send email?
                msg = time.strftime("%Y-%m-%d %H:%M:%S")+"\t[+] ID:"+credential["appid"]+"\ttoken:"+str(key["access_token"])
                log.writelines(msg+"\n")
                log.flush() # Save output
                print(msg)
                log.close()
                return key["access_token"]#, key["expires_in"]
            else:
                print(msg)
                log.close()
                return "ERROR:"+msg#,0 # Read the last 5 lines and print
class log_replyier():
    # Adding authentication? APP secret?
    log_dir = PATH+r"\..\Static\log"
    #def __init__(self):

    def GET(self):
        try:
            request_appid = dict(web.input())["appid"]
            return log_replyier.log_finder(request_appid) # Have to use position vars?
        except Exception as err:
            return str(err)
    @staticmethod
    def log_finder(appid):
        with open(log_replyier.log_dir,"r") as log_file:
            msg = "".join([i for i in log_file.readlines() if appid in i ])
            print(msg)
            return msg


if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()

