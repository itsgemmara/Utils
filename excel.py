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


def create_highlight_style(df):
    c1 = 'background-color: #CDCDCD'
    c2 = '' 
    rows_count = len(df.index)
    colored = list()
    for i in range(rows_count):
        if i % 2 != 0:
            colored.append(i)
    columns = df.columns
    m = df[df.index%2 != 0]
    df1 = pd.DataFrame(c2, index=df.index, columns=columns)
    for i in colored:
        df1.loc[i] = c1
    return df1


def save_excel_with_style(df, output_filename, sheet_name):
    df.reset_index(drop=True, inplace=True)
    writer = pd.ExcelWriter(output_filename, engine='xlsxwriter')
    df.style.apply(create_highlight_style,axis=None).to_excel(writer, sheet_name=sheet_name, index=False)
    workbook  = writer.book
    formater = workbook.add_format({'border':1})

    worksheet = writer.sheets[sheet_name]
    worksheet.set_column(0, 0, 18, formater)
    worksheet.set_column(1, 1, 10, formater)
    worksheet.set_column(2, 2, 26, formater)
    worksheet.set_column(3, 3, 6, formater)
    worksheet.set_column(4, 4, 6, formater)
    worksheet.set_column(5, 5, 6, formater)
    worksheet.set_column(6, 6, 10, formater)
    worksheet.set_column(7, 7, 10, formater)
    worksheet.set_column(8, 8, 10, formater)
    worksheet.set_paper(9)
    worksheet.set_margins(left=0.19, right=0.19, top=0.5, bottom=0)
    time = str(jdt.now()).split()[0]
    worksheet.set_header(header=f"{time}/{sheet_name}", margin=0)
    worksheet.set_footer(footer="&CPage &P of &N", margin=0)
    worksheet.set_zoom(90)
    writer.save()

