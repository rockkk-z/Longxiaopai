from flask import Flask, render_template, request, redirect, url_for, session, jsonify

app = Flask(__name__)
app.secret_key = "secret_key"

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    name = data.get("name")
    who = data.get("who")
    where = data.get("where")
    plate = data.get("plate")   # 可能没有

    # 基本字段验证
    if not who or not where:
        return jsonify({"message": "信息不完整"}), 400

    # 对于需要车牌号的身份，验证 plate 存在且非空
    if who in ["客车", "货车", "邮政", "私家车"]:
        if not plate or not plate.strip():
            return jsonify({"message": "请填写车牌号"}), 400
    # 对于供货商，plate 可以不提供，我们将其设为空字符串存入session（或None）
    else:
        plate = ""

    # 保存登录信息
    session["name"] = name
    session["who"] = who
    session["where"] = where
    session["plate"] = plate

    return jsonify({
        "message": "登录成功",
        "who": who
    })

# 货主页面
@app.route("/shipper")
def shipper():
    if "who" not in session:
        return redirect(url_for("index"))
    return render_template("发订单.html", name=session["name"], who=session["who"], plate=session["plate"])

# 客车页面 (同时用于货车、邮政)
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

# 可选：监控后台
@app.route("/dashboard")
def dashboard():
    if "who" not in session:
        return redirect(url_for("index"))
    return render_template("dashboard.html", name=session["name"], who=session["who"], plate=session["plate"])

if __name__ == "__main__":
    app.run(debug=True)