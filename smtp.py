import getpass
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

smtp_server = 'smtp.gmail.com'
smtp_port = 587

def sendMail(sender, receiver):
    msg = MIMEMultipart()
    msg['To'] = receiver
    msg['From'] = sender
    msg['Subject'] = input("Enter the subject: ")
    message = input("Enter the message: ")
    part = MIMEText('text', 'plain')
    part.set_payload(message)
    msg.attach(part)
    session = smtplib.SMTP(smtp_server, smtp_port)
    session.ehlo()
    session.starttls()
    session.ehlo
    password = getpass.getpass(prompt = "Enter your password: ")
    session.login(sender, password)
    session.sendmail(sender, receiver, msg.as_string())
    print("Mail sent to {}".format(receiver))
    session.quit()

sender = input("Enter your email address: ")
receiver = input("Enter the receipient mail address: ")
sendMail(sender, receiver)