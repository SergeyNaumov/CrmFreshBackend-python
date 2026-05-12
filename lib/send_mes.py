import os
import smtplib, ssl, socket
from email import encoders
from email.mime.base import MIMEBase
#import email.message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formatdate, make_msgid
from lib.celery_conf.config import celery_app
from lib.core_crm import get_email_list_from_manager_id
from config import config, PRODUCTION
from db import get_db
import re

@celery_app.task(autoretry_on=True, max_retries=3, queue='notifications')
def send_mes_task(opt):
    try:
        msg = MIMEMultipart('alternative')

        # ОБЯЗАТЕЛЬНЫЕ ЗАГОЛОВКИ
        msg['From'] = 'no-reply@fascrm.ru'
        msg['To'] = opt['to']
        msg['Subject'] = opt['subject']
        msg['Date'] = formatdate(localtime=True)
        msg['Message-ID'] = make_msgid(domain='fascrm.ru')

        # Текстовая версия
        plain_text = re.sub(r'<[^>]+>', '', opt['message'])
        plain_text = re.sub(r'\s+', ' ', plain_text).strip()
        msg.attach(MIMEText(plain_text, 'plain', 'utf-8'))

        # HTML версия
        msg.attach(MIMEText(opt['message'], 'html', 'utf-8'))

        # Изображения
        if 'images' in opt:
            msg_related = MIMEMultipart('related')
            msg_related.attach(msg)
            msg = msg_related
            for i in opt['images']:
                with open(i['file'], 'rb') as fp:
                    img = MIMEImage(fp.read(), 'png')
                    img.add_header('Content-ID', f'<{i["cid"]}>')
                    img.add_header('Content-Disposition', 'inline')
                    msg.attach(img)

        # Вложения
        if 'attachment' in opt:
            with open(opt['attachment'], 'rb') as attachment:
                f = MIMEBase('application', 'octet-stream')
                f.set_payload(attachment.read())
            encoders.encode_base64(f)
            f.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(opt["attachment"])}"')
            msg.attach(f)

        # Отправка
        config_mail = config['mail']
        mail_conf_sect = config_mail['no-reply@fascrm.ru']
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)

        with smtplib.SMTP(mail_conf_sect['server'], mail_conf_sect['port']) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(mail_conf_sect['user'], mail_conf_sect['password'])

            to_list_checked = [e.strip() for e in opt['to'].split(',') if e.strip() and '@' in e]

            if to_list_checked:
                server.sendmail(msg['From'], to_list_checked, msg.as_string())
                print(f"Отправлено: {msg['From']} -> {to_list_checked}")

    except smtplib.SMTPRecipientsRefused as e:
        # Ошибка с получателями - неавторетрей
        failed_recipients = list(e.recipients.keys())
        print(f"❌ Ошибка: получатели не найдены: {failed_recipients}")
        # Здесь можно записать в лог или БД, но не ретраить
        return {"status": "failed", "recipients": failed_recipients, "error": str(e)}

    except smtplib.SMTPAuthenticationError as e:
        # Ошибка аутентификации - неавторетрей
        print(f"❌ Ошибка аутентификации SMTP: {e}")
        return {"status": "failed", "error": "authentication_failed"}

    except (ConnectionRefusedError, smtplib.SMTPServerDisconnected) as e:
        # Ошибки соединения - авторетрей сработает
        print(f"⚠️ Ошибка соединения: {e}")
        raise  # Пробрасываем для авторетрея

    except Exception as e:
        # Другие ошибки
        print(f"❌ Неожиданная ошибка: {e}")
        return {"status": "failed", "error": str(e)}

  # return
  # db = get_db(sync=1)
  # msg = MIMEMultipart('related')
  # # MIMEMultipart('alternative')
  # opt['from_addr'] = 'no-reply@fascrm.ru'
  # config_mail = config['mail']

  # # from по умолчанию

  # if 'from_addr' in opt:
  #   opt['from'] = opt['from_addr']
  #   # print(opt['from'])
  #   # quit()

  # # from по умолчанию
  # if not ('from' in opt):
  #   opt['from'] = config_mail['default_from_addr']

  # if not (opt['from'] in config_mail):
  #   print(f"адрес {opt['from']} отсутствует в config['mail']")

  # mail_conf_sect = config_mail[opt['from']]
  # msg['From'] = 'no-reply@fascrm.ru'
  # # msg['From'] = opt['from']
  # to_list = opt['to'].split(',')

  # # to_list.append('svcomplex@yandex.ru')
  # # print(f'send_mes: {opt["subject"]} ',to_list)
  # need_copyes = False
  # if not ('not_copyes' in opt):
  #   need_copyes = True
  # elif not (opt['not_copyes']):
  #   need_copyes = True

  # msg['Subject'] = opt['subject']

  # msg_body = MIMEMultipart('alternative')
  # msg_body.add_header('Content-Type', 'text/html; charset=utf-8')
  # # msg.set_payload(opt['message'])
  # html_part = MIMEText(opt['message'], 'html')
  # msg_body.attach(html_part)
  # msg.attach(msg_body)
  # # print(msg['From'], [ msg['To'] ], msg.as_string())

  # if 'images' in opt:
  #   for i in opt['images']:
  #     with open(i['file'], 'rb') as fp:
  #       img = MIMEImage(fp.read(), 'png')
  #       # print('i:',i)
  #       img.add_header('Content-ID', f'<{i["cid"]}>')
  #       msg.attach(img)
  # if 'attachment' in opt:
  #   output_filename = opt['attachment']
  #   filename = os.path.basename(output_filename)
  #   with open(output_filename, 'rb') as attachment:
  #     f = MIMEBase('application', 'octet-stream')
  #     f.set_payload(attachment.read())
  #   encoders.encode_base64(f)
  #   f.add_header(
  #     'Content-Disposition',
  #     f'attachment; filename={filename}'
  #   )
  #   msg.attach(f)

  # context = ssl.SSLContext(ssl.PROTOCOL_TLS)
  # # print('server:',mail_conf_sect['server'], ' port:',mail_conf_sect['port'])
  # with smtplib.SMTP(mail_conf_sect['server'], mail_conf_sect['port']) as server:
  #   # for to_addr in to_list:
  #   try:
  #     server.ehlo()  # Can be omitted
  #     server.starttls(context=context)
  #     server.ehlo()  # Can be omitted

  #     server.login(mail_conf_sect['user'], mail_conf_sect['password'])
  #     to_list_checked = []
  #     for e in to_list:
  #       if e and '@' in e:
  #         to_list_checked.append(e)
  #     print(f"FROM: {msg['From']} user: {mail_conf_sect['user']}, to: {to_list_checked}")
  #     if len(to_list_checked):
  #       msg['From'] = 'no-reply@fascrm.ru'
  #       server.sendmail(msg['From'], to_list_checked, msg.as_string())
  #       # print(f"from: {msg['From']} to_list: {to_list_checked}")
  #     # Записываем в журнал отправки
  #     for t in to_list:
  #         db.save(
  #           table='mail_send',
  #           data={
  #             'to_addr':t,
  #             'subject':opt['subject'],
  #             'message':opt['message']
  #           }
  #         )

  #   except ConnectionRefusedError as e:
  #     print("\033[31m {}".format('ошибка при отправке почты:'), e, "\033[0m")
  #   except smtplib.SMTPRecipientsRefused as e:
  #     print('SMTPRecipientsRefused: ', e)

  #   # server.quit()




def send_mes(**opt): # через t-pass
  if PRODUCTION == '1':
    send_mes_task.delay(opt)
  else:
    print(opt)


async def send_mes_email_managers(ids, subject, message):
  db=get_db()


  to_emails = await get_email_list_from_manager_id(db, ids)
  print(f'send_mes_email_managers: {to_emails} (ids: {ids})')
  if len(to_emails):
      send_mes(
          from_addr='info@fascrm.ru',
          to=','.join(to_emails.keys()),
          subject=subject,
          message=message
      )


def send_mes0(**opt): # локальная отправка
  #print(opt['from'])
  #print('opt:',opt)
  if 'from_addr' in opt:
    opt['from']=opt['from_addr']

  msg = MIMEMultipart('alternative')
  msg.add_header('Content-Type', 'text/html; charset=utf-8')
  html_part= MIMEText(opt['message'], 'html')
  msg.attach(html_part)
  to_list = opt['to'].split(',')
  #to_list.append('svcomplex@yandex.ru')
  msg['From'] = 'info@fas.crm-dev.ru' #opt['from']
  #msg['To'] = opt['to']
  msg['Subject'] = opt['subject']
  #print('msg:',msg)
  #msg.add_header('Content-Type', 'text/html; charset=utf-8')


  #if 'images' in opt:
  #  for i in opt['images']:
  #    with open(i['file'], 'rb') as fp:
  #      img = MIMEImage(fp.read(),'png')
        #print('i:',i)
  #      img.add_header('Content-ID', f'<{i["cid"]}>')
  #      msg.attach(img)
  #print(msg['From'], [ msg['To'] ], msg.as_string())

  #if not( msg.get('From') ):
  #  msg['From']='info@fas.crm-dev.ru'

  try:
    server=smtplib.SMTP()
    server.connect('localhost')
    #server.starttls()
    #server.set_debuglevel(2)
    server.sendmail(msg['From'], to_list, msg.as_string())
  except ConnectionRefusedError as e:
    print('ошибка при отправке почты: ', e)
  except smtplib.SMTPRecipientsRefused as e:
    print('SMTPRecipientsRefused: ', e)


def send_mes2(opt):
  #print(opt['from'])

  msg = MIMEMultipart('alternative')
  msg['From'] = opt['from']
  msg['To'] = opt['to']
  msg['Subject'] = opt['subject']


  msg.add_header('Content-Type', 'text/html; charset=utf-8')
  #msg.set_payload(opt['message'])
  message_part= MIMEText(opt['message'], 'html')
  msg.attach(message_part)
  #print(msg['From'], [ msg['To'] ], msg.as_string())

  if not( msg.get('From') ):
    msg['From']='info@beyeezy.ru'

  try:
    server=smtplib.SMTP()
    server.connect('localhost')
    #server.starttls()
    server.set_debuglevel(2)
    server.sendmail(msg['From'], [ msg['To'] ], msg.as_string())
  except ConnectionRefusedError as e:
    print('ошибка при отправке почты: ', e)
  except smtplib.SMTPRecipientsRefused as e:
    print('SMTPRecipientsRefused: ', e)