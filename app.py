from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os

app = Flask(__name__)
app.secret_key = "your_secure_secret_key_123456"  # 生产环境务必修改

# 登录页
@app.route("/")
def index():
    return render_template("login.html")

# 登录处理
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    name = data.get("name")
    who = data.get("who")
    where = data.get("where")
    plate = data.get("plate")

    # 基本字段验证：身份必须存在
    if not who:
        return jsonify({"message": "身份类型不能为空"}), 400

    # 政府人员不强制要求定位，其他身份必须填写定位
    if who != "政府人员" and not where:
        return jsonify({"message": "请填写当前位置"}), 400

    # 车牌号验证：对于需要车牌的身份（客车、货车、邮政、私家车），plate不能为空
    if who in ["客车", "货车", "邮政", "私家车"]:
        if not plate or not plate.strip():
            return jsonify({"message": "请填写车牌号"}), 400
    # 其他身份（供货商、政府人员等）车牌号留空
    else:
        plate = ""

    # 保存登录信息
    session["name"] = name
    session["who"] = who
    session["where"] = where if who != "政府人员" else ""   # 政府人员定位置为空字符串，也可保留用户输入
    session["plate"] = plate

    return jsonify({"message": "登录成功", "who": who})

# 货主页面
@app.route("/shipper")
def shipper():
    if "who" not in session:
        return redirect(url_for("index"))
    return render_template("发订单.html", name=session["name"], who=session["who"], plate=session["plate"])

# 客车/货车/邮政页面
@app.route("/bus")
def bus():
    if "who" not in session:
        return redirect(url_for("index"))
    return render_template("客车中心2.html", name=session["name"], who=session["who"], plate=session["plate"])

# 社会车辆页面
@app.route("/car")
def car():
    if "who" not in session:
        return redirect(url_for("index"))
    return render_template("社会车辆5.html", name=session["name"], who=session["who"], plate=session["plate"])

# 监控中心页面（原 dashboard 改为此）
@app.route("/dashboard")
def dashboard():
    if "who" not in session:
        return redirect(url_for("index"))
    return render_template("监控中心.html", name=session["name"], who=session["who"], plate=session["plate"])

# Vercel 入口
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)), debug=False)

application = app