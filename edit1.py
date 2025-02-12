from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, login_required,LoginManager,  logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from random import randint
from validate import validate_password
import os

app = Flask(__name__)
app.secret_key = "My Chinchilla"
bcrypt = Bcrypt(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

# Configure Flask-Mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Use your SMTP server
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']
mail = Mail(app)

otp = randint(100000, 999999)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def user_loader(user_id):
    return db.session.get(User, int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class UserExpense(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    expense_category = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)

class SubmitAllowance(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    allowance = db.Column(db.Float, nullable=False)

@app.route('/index')
@login_required
def index():
    if "user" in session:
        username = session["user"]
        user = User.query.filter_by(username=username).first()
        allowance = session.get("allowance", "Not Set")
        amount = session.get("amount", "Not Set")
        date = session.get("date", "Not Set")
        expense_category = session.get("expense_category", "Not Set")
        return render_template('index.html', user=user.username, allowance=allowance, amount=amount, date=date, expense_category=expense_category)
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
        new_user = User(username=user, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        #session["new_user"]= new_user.username
        session["email"] = email
        if new_user:
            return redirect(url_for("verifyEmail"))
        else:
            return "Username is required!", 400
    else:
        if "new_user" in session:
            return redirect(url_for("index"))
        return render_template('signup.html')
@app.route('/verifyEmail', methods=["POST", "GET"])
def verifyEmail():
    print(f"Received {request.method} request")  # Log the received method
    #email = request.form.get("email")
    email = session.get("email")
    if not email:
        return "Email is required!", 400
        # If email is not in session, redirect back to signup
        #return redirect(url_for("signup"))
    # Automatically send OTP on GET requests
    #if request.method == "GET":
    #msg = Message('OTP Verification', sender=app.config['MAIL_DEFAULT_SENDER'], recipients=[email])
    msg = Message('OTP Verification', recipients=[email])
    msg.body = str(otp)
    try:
        mail.send(msg)
        return render_template("verifyEmail.html")
    except Exception as e:
        return f"Error sending email: {str(e)}", 500
    #return render_template("verifyEmail.html", otp_sent=True)
    #elif request.method == "POST":
     #   msg = Message('OTP Verification', recipients=[email])
      #  msg.body = str(otp)
       # try:
        #    mail.send(msg)
        #except Exception as e:
         #   return f"Error sending email: {str(e)}", 500
        # Render the page with a flag that OTP was sent (if needed)
        #return render_template("verifyEmail.html", otp_sent=True)
    #return render_template("verifyEmail.html")

@app.route('/validateEmail', methods=["POST"])
def validateEmail():
    user_otp = request.form.get('otp')
    if otp == int(user_otp):
        return "<h3>'Email verification successful'</h3>"
    else:
        return "<h3>'Failure, OTP does not match'</h3>"

@app.route('/submit_allowance', methods=["POST", "GET"])
def submit_allowance():
    if request.method== "POST":
        allowance = request.form.get('allowance')
        if allowance:
            user = User.query.filter_by(username=session["user"]).first()
            allowance_entry = SubmitAllowance(user_id=user.id, allowance=allowance)
            db.session.add(allowance_entry)
            db.session.commit()
            session["allowance"] = {
                    "allowance": allowance_entry.allowance
                    }
            return redirect(url_for("index"))
    return "Allowance not submitted!", 400

@app.route("/add_expense", methods=["POST", "GET"])
def add_expense():
    if request.method == "POST":
        date = request.form.get('date')
        expense_category = request.form.get('category')
        amount = request.form.get('amount')
        new_category = request.form.get('newCategory')  # Retrieve new category

        # Use new category if it was added
        if expense_category == "others" and new_category:
            expense_category = new_category

        if date and expense_category and amount:
            user = User.query.filter_by(username=session["user"]).first()
            expense_entry = UserExpense(user_id=user.id, date=date, expense_category=expense_category, amount=amount)
            db.session.add(expense_entry)
            db.session.commit()
            session["expense_entry"] = {
                    "amount": expense_entry.amount,
                    "date": expense_entry.date,
                    "expense_category": expense_entry.expense_category
                    }
            return redirect(url_for("index"))
        else:
            return "Expense category not submitted!", 400
    return "Invalid Request Method!", 400


@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop("user", None)
    return redirect(url_for("login"))




if __name__ == '__main__':
    app.run(debug=True)
