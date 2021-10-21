import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from os.path import join, dirname
from dotenv import load_dotenv

'''
Code adapted from https://www.tutorialspoint.com/send-mail-from-your-gmail-account-using-python
'''


def send_change_email(addressTo, link, i):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)
    
    f1 = "./page/v{idx}".format(idx=i)
    f2 = "./page/v{idx}".format(idx=i-1)
    diff = os.popen('diff {path1} {path2}'.format(path1=f1, path2=f2)).read()

    # The mail addresses and password
    sender_address = os.environ.get("FROM")
    sender_pass = os.environ.get("PASS")
    receiver_address = addressTo

    mail_content = f'A change has been detected on {link}\n\n\n {diff}'

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    # The subject line
    message['Subject'] = 'A change was noticed on the website you\'re tracking!'
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    # login with mail_id and password
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')


def send_reminder_email(addressTo, link):
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    # The mail addresses and password
    sender_address = os.environ.get("FROM")
    sender_pass = os.environ.get("PASS")
    receiver_address = addressTo

    mail_content = f'A reminder that crawly is still tracking changes on {link}'

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    # The subject line
    message['Subject'] = 'A reminder that crawly is still tracking the website'
    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    # login with mail_id and password
    session.login(sender_address, sender_pass)
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
