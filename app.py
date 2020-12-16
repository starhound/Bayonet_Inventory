import pandas as pd
import requests
import ssl
import smtplib
import base64
import html_generate
import html_save
import time
from flask import Flask, current_app, request, send_file, request
from random import randint
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.headerregistry import Address
from email.message import EmailMessage


app = Flask(__name__)


if __name__ == '__main__':
    html_generate.main()
    app.run(host='0.0.0.0', port=80, debug=True, use_debugger=True)


from_address_email = ""
from_address_password = ""
cc_address = ""
mail_server = ""

def create_email_message(from_address, to_address, subject, body, file, has_file):
    msg = EmailMessage()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['CC'] = cc_address
    msg['Subject'] = subject
    msg.set_content(body)
    if has_file:
        with open('/home/ubuntu/inv/emp/' + file, 'rb') as content_file:
            content = content_file.read()
            msg.add_attachment(content, maintype='application', subtype='xlsx', filename=file)
    return msg


def send_email(file, fileName, employee):
    msg = create_email_message(
        from_address=from_address_email,
        to_address=employee,
        subject='Bayonet Inventory Results - Excel File',
        body="Attached is the excel file generated from your inventory count.",
        file=fileName,
        has_file=True
    )
    smtp_server = smtplib.SMTP(mail_server, port=587)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.login(from_address_email, from_address_password)
    smtp_server.send_message(msg)
    smtp_server.quit()
    print("Confirmation email send to: " + employee + " -- file: " + fileName)


def send_email_link(employee, link):
    msg = create_email_message(
        from_address=from_address_email,
        to_address=employee,
        subject='Bayonet Inventory - Save Link',
        body="Your link to your saved inventory form: " + link,
        file=0,
        has_file=False
    )
    smtp_server = smtplib.SMTP(mail_server, port=587)
    smtp_server.ehlo()
    smtp_server.starttls()
    smtp_server.login(from_address_email, from_address_password)
    smtp_server.send_message(msg)
    smtp_server.quit()
    print('Save Email Sent for ' + employee + " -- url:" + link)


@app.route("/", methods=["GET"])
def home():
    return current_app.send_static_file('index.html')


@app.route("/hudson_main_group", methods=["GET"])
def hudson_main_group():
    return current_app.send_static_file('hudson_main_group.html')


@app.route("/hudson_service_group", methods=["GET"])
def hudson_service_group():
    return current_app.send_static_file('hudson_service_group.html')


@app.route("/tampa_group", methods=["GET"])
def tampa_group():
    return current_app.send_static_file('tampa_group.html')


@app.route("/dundee_group", methods=["GET"])
def dundee_group():
    return current_app.send_static_file('dundee_group.html')


@app.route("/clermont_group", methods=["GET"])
def clermont_group():
    return current_app.send_static_file('clermont_group.html')


@app.route("/inventory/<type>", methods=["GET"])
def inventory_page(type):
    return current_app.send_static_file('/inventory/' + type + '.html')


def serveFile(file):
    return current_app.send_file(file, as_attachment=True)


@app.route("/save/<type>/<employee>", methods=["GET"])
def download(employee, type):
    return current_app.send_static_file('save/' + type + "/" + employee + '.html')


def write_inventory_results(d, employee_email, do_email):
    user = employee_email.split('@')[0]
    timestr = time.strftime("%Y%m%d-%H%M%S")
    fileName = user + "_" + timestr + "_InventoryResults"
    d.pop("employeeName", None)
    keys = d.keys()
    values = d.values()
    df = pd.DataFrame({"ITEM CODE": keys, "COUNT": values})
    df.to_excel("emp/" + fileName + ".xlsx", index=False)
    if do_email:
        send_email("emp/" + fileName + ".xlsx", fileName + ".xlsx", employee_email)


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.form:
        if "save" in request.form:
            from_save = False
            url = request.referrer
            type = ''

            if "save" in url:
                from_save = True
                link = url.split("/")[6]
                type = link.split('.')[0]
            else:
                link = url.split("/")[5]
                type = link.split('.')[0]

            d = request.form.to_dict()

            code = randint(10000, 1000000)
            d.pop('save', None)
            email = d["employeeName"]

            if len(email) == 0:
                write_inventory_results(d, "NONE_ENTERED_FROM_SAVE", False)
                return current_app.send_static_file("error.html")

            save_url = html_save.save_employee_progress(d, email, code, type, from_save)

            print("SAVE URL GENERATED: " + save_url)
            send_email_link(email, save_url)
            return current_app.send_static_file('save.html')
        elif "submit" in request.form:
            d = request.form.to_dict()
            d.pop('submit', None)
            email = d["employeeName"]
            print("REPORT SUBMITTED FOR: " + email)
            if len(email) == 0:
                write_inventory_results(d, "NONE_ENTERED", False)
                return current_app.send_static_file("error.html")
            else:
                write_inventory_results(d, email, True)
                return current_app.send_static_file('submit.html')
                