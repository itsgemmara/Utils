import pandas as pd
from .json import save_json
from django.http import HttpResponse
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE
from email import encoders


def read_excel(excel_path: str, target_file_name: str=None):
    print('in read excel')
    data = pd.read_excel(excel_path, sheet_name=None, engine='openpyxl')
    final_result = dict()
    for sheet_name in data:
        if str(sheet_name).strip() == '>>>راهنما<<<':
            continue
        final_result[sheet_name] = list()
        print('before pd')
        df = pd.DataFrame(data[sheet_name])
        print('after pd', data[sheet_name])
        columns = df.columns
        for row in df.itertuples():
            rows_dict = dict()
            c = 0
            for i in row:
                c += 1
                rows_dict[columns[c - 1]] = row[c]
                if c == len(columns):
                    break
            final_result[sheet_name].append(rows_dict)
    if target_file_name:
        save_json(final_result, f'{target_file_name}.json')
    return final_result


def sort_excel(excel_path, by: list, save_excel: bool = False):
    data = read_excel(excel_path)
    filename = str(excel_path).split('\\')[-1]
    full_data = list()
    for sheet in data:
        for item in data[sheet]:
            full_data.append(item)
    df = pd.DataFrame(full_data)
    df = df.sort_values(by)
    if save_excel:
        handler = pd.ExcelWriter(fr"=sorted_{filename}", engine='xlsxwriter')
        df.to_excel(handler, sheet_name="sorted_data", index=False)
        handler.save()
    return df


def return_excel_http_response(df: pd.DataFrame, file_name: str):

    with BytesIO() as b:
        # Use the StringIO object as the filehandle.
        writer = pd.ExcelWriter(b, engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
        # Set up the Http response.
        filename = f'{file_name}.xlsx'
        response = HttpResponse(
            b.getvalue(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response
    

def send_excel_by_email(
        recipient_email: str, 
        df: pd.DataFrame, 
        excel_file_name: str, 
        smtp_username: str, 
        smtp_password: str, 
        sender: str, 
        subject: str='Excel file'
        ):

    # Email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = smtp_username
    smtp_password = smtp_password 
    sender = sender
    recipient = recipient_email

    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject

    # Open the Excel file and attach it to the message object
    excel_file = f'/app/excels/{excel_file_name}.xlsx'
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    with open(excel_file, 'rb') as f:
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(f.read())
        encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition', f'attachment; filename="{excel_file}"')
        msg.attach(attachment)

    # Convert the message object to a string and send it via SMTP
    smtp = smtplib.SMTP(smtp_server, smtp_port)
    smtp.starttls()
    smtp.login(smtp_username, smtp_password)
    smtp.sendmail(sender, [recipient], msg.as_string())
    smtp.quit()