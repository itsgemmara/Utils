import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_html_file(filename):
    with open(filename, 'r') as file: 
        html_as_string = file.read()
    return html_as_string


def email_html(html, recipient_email, sender):
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    sender = sender
    msg['Subject'] = "html file"
    msg['From'] = sender
    msg['To'] = recipient_email

    # Create the body of the message (a plain-text and an HTML version).

    # Record the MIME types of both parts - text/plain and text/html.
    p = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(p)

    # Send the message via local SMTP server.
    s = smtplib.SMTP('localhost')
    # sendmail function takes 3 arguments: sender's address, recipient's address
    # and message to send - here it is sent as one string.
    s.sendmail(sender, recipient_email, msg.as_string())
    s.quit()

