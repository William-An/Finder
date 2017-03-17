import requests
import time
import os
import sys
import web
import json
import sqlite3
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
cursor = database.cursor()
# Create table to store tokens
try:
    database.execute('''CREATE TABLE appid_token(appid text, current_token text, last_time real)''')
except sqlite3.OperationalError:
    pass

class token_acquirer:
    def __init__(self):
        """
        Log server's initialization
        Store debug log
        """
        msg = time.strftime("%Y-%m-%d %H:%M:%S")+"\tServer begins..."
        print(msg)
        with open(PATH+r"\..\Static\log","a") as log:
            log.writelines(msg)
            log.write("\n")
            log.flush()
            log.close()
    def GET(self):
        # What about multi reuse??? 多个服务器请求时怎么办 -> SQL
        credential = dict(web.input())
        print(credential["appid"])
        # Get elapse time to calculate expire_time -> time.time() store last record in sql, calculate with this request
        # SELECT expire_time FROM appid_token WHERE appid =
        # SQL hacking>
        try:
            self.last_time = cursor.execute("SELECT last_time FROM appid_token WHERE appid = ?",credential["appid"])
        except: # New appid?
            # INSERT INTO appid_token VALUES(appid, current_token, last_time)
            self.last_time = 0
            cursor.execute("INSERT INTO appid_token VALUES(?,?,?)",(credential["appid"],"",self.last_time))

        # Simplify this if clause?
        if time.time() - self.last_time > 7180: # If access_token is nearly invalid
            self.token = self.get_token(credential)
            if "ERROR" in self.token:
                return self.token
            # Update token and time
            # UPDATE Person SET current_token = , expire_time =  WHERE appid =
            cursor.execute("UPDATE appid_token SET current_token =? ,last_time =?  WHERE appid = ?",(self.token,time.time(),credential["appid"]))
            return self.token
        else:
            # find token in sql
            return cursor.execute("SELECT current_token,last_time FROM appid_token WHERE appid=?",credential["appid"])
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
                msg = time.strftime("%Y-%m-%d %H:%M:%S")+"\t[+]token:"+str(key["access_token"])
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
    def GET(self):
        try:
            appid = dict(web.input())["appid"]
        except Exception as err:
            return str(err)
    def log_finder(self,appid):
        pass
if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()

