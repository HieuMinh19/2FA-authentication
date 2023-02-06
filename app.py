# importing needed libraries
from flask import *
from flask_bootstrap import Bootstrap
import pyotp

# configuring flask application
app = Flask(__name__)
app.config["SECRET_KEY"] = "APP_SECRET_KEY"
Bootstrap(app)

# homepage route
@app.route("/")
def index():
    return "<h1>Welcome to Type For Life Channel!</h1>"

# login page route
@app.route("/login/")
def login():
    return render_template("login.html")

# login form route
@app.route("/login/", methods=["POST"])
def login_form():
    demoCreds = {"username": "felix", "password": "password"}

    # getting form data
    username = request.form.get("username")
    password = request.form.get("password")

    # authenticating submitted demoCreds with demo demoCreds
    if username == demoCreds["username"] and password == demoCreds["password"]:
        flash("The credentials provided are valid", "success")
        return redirect(url_for("login_2fa"))
    else:
        flash("Invalid login credentials!", "danger")
        return redirect(url_for("login"))

# 2FA page route
@app.route("/login/2fa/")
def login_2fa():
    secret = pyotp.random_base32()
    return render_template("login_2fa.html", secret=secret)

@app.route("/login/2fa/", methods=["POST"])
def login_2fa_form():

    secret = request.form.get("secret")
    otp = int(request.form.get("otp"))

    # verifying submitted OTP with PyOTP
    if pyotp.TOTP(secret).verify(otp):
        flash("The TOTP 2FA token is valid", "success")
        return redirect(url_for("login_2fa"))
    else:
        # OTP is invalid
        flash("You have supplied an invalid 2FA token!", "danger")
        return redirect(url_for("login_2fa"))

# running flask server
if __name__ == "__main__":
    app.run(debug=True)

