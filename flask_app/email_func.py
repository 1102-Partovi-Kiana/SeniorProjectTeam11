from flask_mail import Mail, Message

mail = Mail()

def init_mail(app):
    mail.init_app(app)

def send_email(subject, recipients, body):
    msg = Message(subject = subject, sender = "officialwarerecovery@gmail.com", recipients = [recipients], body = body)
    mail.send(msg)

def reset_password_email():
    subject = 'CORE Account Password Reset'
    recipient = 'tang@unr.edu'
    body = "Test Email"
    send_email()