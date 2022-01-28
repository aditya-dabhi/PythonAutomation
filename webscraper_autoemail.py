from urllib import request, response
import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import datetime

now = datetime.datetime.now()

# email content placeholder
content = ''

#Extracting from website

def extract_news(url):
    print('Extracting Hacker News Stories ...')
    cnt = ''
    cnt += ('<b>HN Top Stories:</b>\n'+'<br>'+'-'*50+'<br>')
    response = requests.get(url)
    content = response.content
    soup = BeautifulSoup(content, 'html.parser')
    for i, tag in enumerate(soup.find_all('td',attrs={'class':'title','valign':''})):
        cnt += ((str(i+1)+' :: '+tag.text+"\n"+ '<br>') if tag.text!='More' else '')
    return cnt

cnt = extract_news('https://news.ycombinator.com/')
content += cnt
content += ('<br>-------<br>')
content += ('<br><br>End of Message')

#Sending the mail

print('Composing Email...')

SERVER = 'smtp.gmail.com' #smtp server
PORT = 587
FROM = '' #Enter the sender's emailid
TO = '' #Enter receiver's email id --- can be a list
PASS = '' #Enter password of sender's emailid

msg = MIMEMultipart()

msg['Subject'] = 'Top News Stories HN [Automated Email]' + ' '+ str(now.day) + '-' + str(now.month) + '-' + str(now.year)
msg['From'] = FROM
msg['To'] = TO

msg.attach(MIMEText(content, 'html'))

print('Initiating Server...')

server = smtplib.SMTP(SERVER,PORT)
server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(FROM,PASS)
server.sendmail(FROM, TO, msg.as_string())

print('Email Sent...')

server.quit()