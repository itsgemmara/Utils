import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders


def send_pdf_by_email(recipient_email, pdf_file_name, smtp_usernam, smtp_password, sender, subject='PDF file',  ):

    # Email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    recipient = recipient_email
    body = 'Please find attached the PDF file.'

    # # Create a multipart message object
    # msg = MIMEMultipart()
    # msg['From'] = sender
    # msg['To'] = recipient
    # msg['Subject'] = subject

    # attach the PDF file
    pdf_file = f'{pdf_file_name}'
    pdf_attachment = open(pdf_file, 'rb')
    pdf_part = MIMEBase('application', 'octet-stream')
    pdf_part.set_payload((pdf_attachment).read())
    encoders.encode_base64(pdf_part)
    pdf_part.add_header('Content-Disposition', "attachment; filename= %s" % pdf_file)

    # create the email message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    msg.attach(pdf_part)


    # Convert the message object to a string and send it via SMTP
    smtp = smtplib.SMTP(smtp_server, smtp_port)
    smtp.starttls()
    smtp.login(smtp_username, smtp_password)
    smtp.sendmail(sender, [recipient], msg.as_string())
    smtp.quit()
