from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, login_required,LoginManager,  logout_user
from flask_bcrypt import Bcrypt
from validate import validate_password

app = Flask(__name__)
app.secret_key = "username"
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

@app.route('/index')
@login_required
def index():
    if "user" in session:
        username = session["user"]
        user = User.query.filter_by(username=username).first()
        allowance = session.get("allowance", "Not Set")
        return render_template('index.html', user=user.username, allowance=allowance)
    return redirect(url_for("login"))


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method== "POST":
        current_user = request.form.get("username")
        password = request.form.get("password")
        if current_user and password:
            user = User.query.filter_by(username=current_user).first()
            if not user:
                #User does not exist
                return "Incorrect username!", 400
            if not bcrypt.check_password_hash(user.password, password):
                # Incorrect password
                return "Incorrect password!", 400
            login_user(user)
            session["user"]= user.username
            return redirect(url_for("index"))

        return "Username and password is required!", 400
    else:
        if "user" in session:
            return redirect(url_for("index"))
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method== "POST":
        user = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        validate_result, status_code = validate_password(password, email, confirm_password)
        if status_code != 200:
            return (validate_result, status_code)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=user, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        session["new_user"]= new_user.username
        if new_user:
            return redirect(url_for("index"))
        else:
            return "Username is required!", 400
    else:
        if "new_user" in session:
            return redirect(url_for("index"))
        return render_template('signup.html')

@app.route('/submit_allowance', methods=["POST", "GET"])
def submit_allowance():
    if request.method== "POST":
        allowance = request.form.get('allowance')
        if allowance:
            session["allowance"] = allowance
            return redirect(url_for("index"))
    return "Allowance not submitted!", 400

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop("user", None)
    return redirect(url_for("login"))




if __name__ == '__main__':
    app.run(debug=True)
