from flask_mail import Mail, Message
from flask import current_app
from config import Config 

mail = Mail()

def init_mail(app):
    mail.init_app(app)

def send_email(subject, recipient, body):
    msg = Message(
        subject = subject
        recipient = recipient
        body = body
        sender = "officialwarerecovery@gmail.com"
    )

    mail.send(msg)

def reset_password_email():
    subject = 'CORE Account Password Reset'
    recipient = 'tang@unr.edu'
    body = "Test Email"
    send_email()