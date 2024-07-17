#from celery import Celery
#from fastapi import BackgroundTasks
from time import sleep
import smtplib, socket
#import email.message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

#celery=Celery('tasks',broker="redis://localhost:6379")

# @celery.task
# def send_mes_background(opt):
#   sleep(5)
#   print('opt:',opt)
#   return
#   msg = MIMEMultipart('related')
#   #MIMEMultipart('alternative')
  
#   if 'from_addr' in opt:
#     opt['from']=opt['from_addr']
#     #print(opt['from'])
#     #quit()
    
#   # from по умолчанию
#   if not ('from' in opt): 
#     opt['from']='info@anna.nov.ru'
  
  
#   msg['From'] = opt['from']
#   to_list = opt['to'].split(',')
  
  
#   need_copyes=False
#   if not('not_copyes' in opt):
#     need_copyes=True
#   elif not(opt['not_copyes']):
    
#     need_copyes=True

#   if need_copyes:    
#     to_list.append('orlova@digitalstrateg.ru')
#     to_list.append('oooanna136@gmail.com')
#     to_list.append('webadmin@digitalstrateg.ru')

#   msg['Subject'] = opt['subject']
  
#   msg_body = MIMEMultipart('alternative')
#   msg_body.add_header('Content-Type', 'text/html; charset=utf-8')
#   #msg.set_payload(opt['message'])
#   html_part= MIMEText(opt['message'], 'html')
#   msg_body.attach(html_part)
#   msg.attach(msg_body)
#   #print(msg['From'], [ msg['To'] ], msg.as_string())
  
#   if 'images' in opt:
#     for i in opt['images']:
#       with open(i['file'], 'rb') as fp:
#         img = MIMEImage(fp.read(),'png')
#         #print('i:',i)
#         img.add_header('Content-ID', f'<{i["cid"]}>')
#         msg.attach(img)



#   for to_addr in to_list:
#     try: 
#       server=smtplib.SMTP()
#       server.connect('localhost')
#       #server.starttls()
#       print(f"send: {to_addr}")
#       #server.set_debuglevel(2)
#       server.sendmail(msg['From'], [ to_addr ], msg.as_string())
#     except ConnectionRefusedError as e:
#       print("\033[31m {}" .format('ошибка при отправке почты:'),e,"\033[0m")
#     except smtplib.SMTPRecipientsRefused as e:
#       print('SMTPRecipientsRefused: ', e)


def send_mes(**opt):
  send_mes_background.delay(opt)