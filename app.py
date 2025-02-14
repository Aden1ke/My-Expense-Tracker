from flask import Flask, render_template, request, url_for, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, login_required,LoginManager,  logout_user
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from validate import validate_password
from random import randint
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
import os


app = Flask(__name__)
load_dotenv()
app.secret_key = os.getenv('secret_key')
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
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'  # Store sessions in a file instead of memory

mail = Mail(app)

def generate_otp():
    """Generate a new OTP and store it in session with a timestamp."""
    new_otp = randint(100000, 999999)
    session["otp"] = {
            'value': new_otp,
            "timestamp": datetime.now(timezone.utc).isoformat()

            }
    return new_otp

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def user_loader(user_id):
    return db.session.get(User, int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    allowance = db.Column(db.Float, nullable=False, default=0)
    expenses = db.relationship('UserExpense', backref='user', lazy=True)

class UserExpense(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    expense_category = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)

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
    return render_template('login.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method== "POST":
        user = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        allowance = 0

        if not email or not user or not password or not confirm_password:
            return "All fields are required!", 400

        # Check if email exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email already exists.", 400

        validate_result, status_code = validate_password(password, email, confirm_password)
        if status_code != 200:
            return (validate_result, status_code)
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # Store user details in session instead of saving to DB
        session["new_user"]={
                "username": user,
                "email": email,
                "password":hashed_password
                }
        #new_user = User(username=user, password=hashed_password, email=email,)
        #db.session.add(new_user)
        #db.session.commit()
        #session["new_user"]= new_user.username
        session["email"] = email
        return redirect(url_for("verifyEmail"))

    return render_template('signup.html')

@app.route('/verifyEmail', methods=["POST", "GET"])
def verifyEmail():
    #email = request.form.get("email")
    email = session.get("email")
    if not email:
        return "Email is required!", 400  # Return error if email is missing
    # Generate OTP with timestamp
    new_otp = generate_otp()
    msg = Message('OTP Verification', sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f"Your OTP is {new_otp}. It expires in 1 minutes."
    try:
        mail.send(msg)
        return render_template("verifyEmail.html")
    except Exception as e:
        return f"Error sending email: {str(e)}", 500

@app.route('/validateEmail', methods=["POST"])
def validateEmail():
    user_otp = request.form.get('otp')
    if not user_otp:
        return "<h3>Failure, OTP does not match</h3>"

    stored_otp = session['otp']
    otp_value = stored_otp['value']
    otp_timestamp = datetime.fromisoformat(stored_otp['timestamp'])

    # Check if OTP is expired (valid for 1 minutes)
    otp_lifetime = timedelta(minutes=1)
    if datetime.now(timezone.utc) - otp_timestamp > otp_lifetime:
        new_otp = generate_otp()
        return f"<h3>Failure, OTP has expired. A new OTP has been sent.</h3>"

    if otp_value == int(user_otp):
        # Retrieve user details from session and save to DB
        new_user_data = session.get("new_user")
        if new_user_data:
            new_user = User(
                    username=new_user_data["username"],
                    password=new_user_data["password"],
                    email=new_user_data["email"]
                    )
            db.session.add(new_user)
            db.session.commit()

            # Clear session after successful registration
            session.pop("new_user", None)
            session.pop("otp", None)
            session["user"] = new_user.username  # Log the user in
            return redirect(url_for("index"))
    else:
        return "<h3>Failure, OTP does not match</h3>"

@app.route('/resend_otp', methods=["GET"])
def resend_otp():
    email = session.get("email")
    if not email:
        return "Email is required!", 400

    new_otp = generate_otp()
    msg = Message('New OTP Verification', sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f"Your OTP is {new_otp}. It expires in 1 minute."


    try:
        mail.send(msg)
        return "New OTP has been sent!", 200
    except Exception as e:
        return f"Error sending email: {str(e)}", 500



@app.route('/submit_allowance', methods=["POST", "GET"])
def submit_allowance():
    if request.method== "POST":
        allowance = request.form.get('allowance')
        if allowance:
            user = User.query.filter_by(username=session["user"]).first()
            user.allowance = float(allowance)
            db.session.commit()
            session["allowance"] = user.allowance
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
    session.clear()
    return redirect(url_for("login"))




if __name__ == '__main__':
    app.run(debug=True)
