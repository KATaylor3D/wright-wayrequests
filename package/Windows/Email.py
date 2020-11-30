from getpass import getpass
from string import Template
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from Scraper import convert_animal_id_to_link
import datetime
import os


contact_email = input("Email to send new animals to:  ")
server_email = input("Gmail used as the smtp.gmail server:  ")
password = getpass("Smtp.gmail server password:  ")


# def get_documents_directory():
#     current_directory = os.getcwd()
#     doc_directory = current_directory.split('\\GitHubWrightWay')[0]
#     return doc_directory

# def get_email_credetials():
#     return_directory = os.getcwd()
#     os.chdir(get_documents_directory())
#     with open('credentials.txt', 'r') as file:
#         content = file.read()
#     content = content.split('\n')
#     os.chdir(return_directory)
#     return content[0], content[1], content[2]
  
# contact_email, server_email, password = get_email_credetials()




def convert_data_for_email(data_list):
    names = []
    ages = []
    colors = []
    breeds = []
    urls = []
    for data in data_list:
        names.append(data[1])
        ages.append(data[3])
        colors.append(data[9])
        breeds.append(data[6])
        urls.append(convert_animal_id_to_link(data[0]))
    return names, ages, colors, breeds, urls

def make_template(filename):
    with open(filename, 'r') as template_file:
        file_content = template_file.read()
    return Template(file_content)

def send_email(data):
    message_template = make_template('message.txt')
    names, ages, colors, breeds, urls = convert_data_for_email(data)
    s = smtplib.SMTP(host= 'smtp.gmail.com', port= 587)
    s.starttls()
    s.login(server_email, password)
    msg = MIMEMultipart()
    message = ''
    current_time = str(datetime.datetime.now())
    for name, age, color, breed, url in zip(names, ages, colors, breeds, urls):
        message_part = message_template.safe_substitute(DogName=name, Age=age, Color=color, Breed=breed, PageLink=url) + '\n'
        message += message_part

    msg['From'] = server_email
    msg['To'] = contact_email
    msg['Subject'] = "WrightWayRequests " + current_time
   
    msg.attach(MIMEText(message, 'plain'))
    s.send_message(msg)
    del msg
    s.quit()

if __name__ == '__main__':
    print("Not run directly")