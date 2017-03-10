#coding=utf-8
import web
import hashlib
urls = (
    '/','index'
)
class index:
    def GET(selfself):
        try:
            data = web.input()
            if len(data) == 0:
                return "HI"
            sign = data.signature
            time = data.timestamp
            nonce = data.nonce
            echo = data.echostr
            token = "helloworld"
            list = [token,time,nonce]
            list.sort()
            sha1 = hashlib.sha1()
            print(list)
            for i in list: # 3.5 & 2.7
                sha1.update(i.encode())
            hashcode = sha1.hexdigest()
            print("index/GET Func:", hashcode, sign)
            print("Token",token )
            if hashcode == sign:
                return echo
            else:
                return ""
        except Exception as Argument:
            return str(Argument)
if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()
