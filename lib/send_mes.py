import smtplib, socket
#import email.message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_mes(**opt):
  msg = MIMEMultipart('alternative')
  
  # from по умолчанию
  if not ('from' in opt): 
    opt['from']='info@design-b2b.com'
  
  
  msg['From'] = opt['from']
  to_list = opt['to'].split(',')

  to_list.append('tk@digitalstrateg.ru')

  msg['Subject'] = opt['subject']
  

  msg.add_header('Content-Type', 'text/html; charset=utf-8')
  #msg.set_payload(opt['message'])
  message_part= MIMEText(opt['message'], 'html')
  msg.attach(message_part)    
  #print(msg['From'], [ msg['To'] ], msg.as_string())
  for to_addr in to_list:
    try: 
      server=smtplib.SMTP()
      server.connect('localhost')
      #server.starttls()
      #server.set_debuglevel(2)
      server.sendmail(msg['From'], [ to_addr ], msg.as_string())
    except ConnectionRefusedError as e:
      print("\033[31m {}" .format('ошибка при отправке почты:'),e,"\033[0m")
    except smtplib.SMTPRecipientsRefused as e:
      print('SMTPRecipientsRefused: ', e)
