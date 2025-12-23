from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def login():
    user = request.args.get("user", "")
    pwd = request.args.get("pwd", "")

    
    # 階段一：無防護 (為了展示 WAF 偵測功能，我們先讓它 Success)
    #if "or" in user.lower() or "'" in user:
    #    return "Login Success (SQLi bypass)"
    

    # 階段二：應用層關鍵字過濾
    # 這裡我們手動檢查關鍵字，並回傳 403 狀態碼
    if "or" in user.lower() or "'" in user:
        return "<h1>403 Forbidden: 應用層安全攔截 (SQLi Detected)</h1>", 403

    if user == "admin" and pwd == "admin":
        return "Login Success"

    return "Login Failed"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)



#攻擊指令
#docker exec -it client1 curl -v "http://172.20.0.254:8080/?user='OR'1'='1"