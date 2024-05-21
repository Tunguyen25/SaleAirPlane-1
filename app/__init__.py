import mail
from flask import Flask
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message
import pyotp, secrets
from twilio.rest import Client
import os

app = Flask(__name__)
app.secret_key = '18sdjksdgjs&%^&^(*@@*#&@#^@DGGHJHG'
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@Localhost/airplane?charset=utf8mb4" % quote(
    '0906079953@@')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)
login = LoginManager(app=app)

# app.config['MAIL_SERVER'] = 'smtp.example.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = '97.lethanhdanh.toky@gmail.com'
# app.config['MAIL_PASSWORD'] = '0902505949'
#
# mail = Mail(app)

# Cài đặt SID và Token của Twilio
account_sid = 'ACcb526a10653d357005fb8f53248101dd'
auth_token = '1db862c03f881e608d5f4ec29a9706f8'


# auth_token = os.environ["TWILIO_AUTH_TOKEN"]
verify_sid = "VA8d94666984ad86abe2fd1d3f59c0022c"
verified_number = "+840902505949"
client = Client(account_sid, auth_token)

# verification = client.verify.v2.services(verify_sid) \
#   .verifications \
#   .create(to=verified_number, channel="sms")
# print(verification.status)
# otp_code = input("Please enter the OTP:")
# verification_check = client.verify.v2.services(verify_sid) \
#   .verification_checks \
#   .create(to=verified_number, code=otp_code)
# print(verification_check.status)


def generate_random_otp(length=6):
    digits = "0123456789"
    otp = ''.join(secrets.choice(digits) for i in range(length))
    return otp


# def send_otp_email(email, otp):
#     msg = Message('Subject', recipients=[email])
#     msg.body = f'Your OTP is: {otp}'
#     mail.send(msg)
#
#
# def verify_otp(submitted_otp, generated_otp):
#     return submitted_otp == generated_otp


import cloudinary

cloudinary.config(
    cloud_name="dxxwcby8l",
    api_key="448651448423589",
    api_secret="ftGud0r1TTqp0CGp5tjwNmkAm-A"
)
if __name__ == '__main__':
    with app.app_context():
        msg = Message('Test Subject', recipients=['nguyenbaothaitu9a8@gmail.com'])
        msg.body = 'This is a test email.'
        mail.send(msg)
