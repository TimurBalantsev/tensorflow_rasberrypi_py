import datetime
import smtplib

gmail_user = "tbalantsev@gmail.com"
gmail_app_password = "ojba rwvs ishb yjwa"
de = gmail_user
to = gmail_user



class sms:
    def __init__(self, reason, time):
        self.reason = reason
        self.time = time
    def __str__(self):
        return f"{self.reason} - {self.time}"

dernier_sms = sms("Aucun", "")

def send_email(subject, body):
    global dernier_sms
    original_subject = subject
    subject = f"URGENT {subject}"
    try:
        the_email = """\
From:%s
To:%s
Subject:%s

%s
    """% (de, to, subject, body)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_app_password)
        server.sendmail(de, to, the_email.encode('utf-8'))
        server.close()
        dernier_sms = sms(original_subject, datetime.datetime.now().strftime('%d %b %Y %H:%M:%S'))
    except Exception as exception:
        print("Error : ", exception)
