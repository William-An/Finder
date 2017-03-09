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
            token = ""
            list = [token,time,nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update,list)
            hashcode = sha1.hexdigest()
            print("index/GET Func:", hashcode," ", sign)
            if hashcode == sign:
                return echo
            else:
                return ""
        except Exception as Argument:
            return str(Argument)
if __name__ == "__main__":
    app = web.application(urls,globals())
    app.run()
