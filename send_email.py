from email.mime.text import MIMEText       # standard package - enabling HTML content
import smtplib

def send_email(email, height):
    """Send email back from form """
    from_email = 'peterjenkin2019@gmail.com'
    from_password = 'P0s1t!ve'
    to_email = email

    subject = 'Height data'
    message = f'Hello, your height was recorded as <strong><em>{height}</em></strong>'

    message = MIMEText(message, 'html')     # MIME type of html in message header
    message['Subject'] = subject
    message['To'] = to_email
    message['From'] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com', 587)          # https://support.google.com/a/answer/176600?hl=en
    gmail.connect('smtp.gmail.com', 587)
    gmail.ehlo          # https://docs.python.org/2/library/smtplib.html
    gmail.starttls      # NB Transport Layer Security - gmail on port 587
    gmail.ehlo          # https://docs.python.org/2/library/smtplib.html
    gmail.login(from_email, from_password)
    gmail.send_message(message)
    # NB Allow less secure apps - Sign-in & security in gmail - as of 25/3/19 requiring G-Suite, for which there is a charge
    # REMmed out calling line in app.py
    # https://stackoverflow.com/a/27515833
    # https://myaccount.google.com/lesssecureapps
