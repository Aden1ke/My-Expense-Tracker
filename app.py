from flask import Flask, render_template, request, url_for, redirect, session

app = Flask(__name__)
app.secret_key = "username"

@app.route('/index')
def index():
    if "user" in session:
        user = session["user"]
        allowance = session.get("allowance", "Not Set")
        return render_template('index.html', user=user, allowance=allowance)
    return redirect(url_for("login"))

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method== "POST":
        user = request.form.get("username")
        session["user"]= user
        if user:
            return redirect(url_for("index"))
        else:
            return "Username is required!", 400
    else:
        if "user" in session:
            return redirect(url_for("index"))
        return render_template('login.html')

@app.route('/submit_allowance', methods=["POST", "GET"])
def submit_allowance():
    if request.method== "POST":
        allowance = request.form.get('allowance')
    if allowance:
        session["allowance"] = allowance
        return redirect(url_for("index"))

@app.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))




if __name__ == '__main__':
    app.run(debug=True)
