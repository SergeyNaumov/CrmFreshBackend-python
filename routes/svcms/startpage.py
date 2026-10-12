# Стартовая страница клиентской админки svcmsmanager.
# Порт легаси legacy/client_manager (start.pl + API.pl + common.js + forms.html):
# карточка хостинга/домена/SSL и заявки на услуги письмом (send_mes).
import asyncio
import re
import smtplib
import ssl
import subprocess
from email.mime.text import MIMEText

from fastapi import APIRouter, Request

from config import config
from db import get_strateg_db

router = APIRouter()

# Базовые получатели заявок (как в легаси API.pl)
BASE_TO = [
  'svetlanakrash@digitalstrateg.ru',
  'ag@digitalstrateg.ru',
]
# Адрес отправителя (легаси: from => info@design-b2b.com)
FROM_ADDR = 'info@design-b2b.com'


def fmt_date(v):
  # 'YYYY-MM-DD' (или datetime) -> 'dd.mm.yyyy'; иначе None
  if not v:
    return None
  m = re.match(r'^(\d{4})-(\d{2})-(\d{2})', str(v))
  if m:
    return f'{m.group(3)}.{m.group(2)}.{m.group(1)}'
  return None


def whois_info(host):
  # paid-till / created из whois (аналог action=domain_info)
  result = {}
  if not host or not re.match(r'^[a-z0-9.\-]+$', host):
    return result
  try:
    out = subprocess.run(
      ['whois', host], capture_output=True, text=True, timeout=10
    ).stdout
  except Exception:
    return result
  attrs = {}
  for line in out.splitlines():
    m = re.match(r'^([^:]+?)\s*:\s*(.+)$', line)
    if m:
      attrs[m.group(1).strip().lower()] = m.group(2).strip()
  paid_till = fmt_date(attrs.get('paid-till'))
  created = fmt_date(attrs.get('created'))
  if paid_till:
    result['paid_till'] = paid_till
  if created:
    result['created'] = created
  return result


async def op_card_info(s, host, errors):
  # Карточка хостинга (svcms) + данные ОП (strateg). Аналог get_op_card_info().
  result = {}
  if not host:
    return result
  hosting = await s.db.query(
    query='''
      SELECT
        wt.born_date, wt.hosting_paid_to, wt.crm_id,
        d.is_ssl, if(d.is_adaptive=2,1,0) domain_adaptive
      FROM
        project_hosting wt
        JOIN domain d ON (wt.domain_id=d.domain_id AND d.domain=%s)
    ''',
    values=[host],
    onerow=1,
    errors=errors,
  )
  if not hosting:
    return result
  result['hosting_start'] = fmt_date(hosting.get('born_date'))
  result['hosting_end'] = fmt_date(hosting.get('hosting_paid_to'))
  result['domain_adaptive'] = hosting.get('domain_adaptive')
  result['is_ssl'] = hosting.get('is_ssl')
  crm_id = hosting.get('crm_id')
  if not crm_id:
    return result
  strateg = get_strateg_db()
  if not strateg or not strateg.pool:
    return result
  op = await strateg.query(
    query='''
      select
        u.id, u.firm, m.email manager_email, m.name manager_name,
        u.manager_id, ip.id ip_id, mip.email manager_ip_email
      from
        user u
        left join manager m ON (m.id=u.manager_id)
        left join internet_project ip ON (ip.id=u.id)
        left join manager mip ON (mip.id=ip.manager_id)
      where u.id=%s
    ''',
    values=[crm_id],
    onerow=1,
    errors=errors,
  )
  if op and op.get('id'):
    result['id'] = op.get('id')
    result['firm'] = op.get('firm') or ''
    result['manager_id'] = op.get('manager_id')
    result['manager_name'] = op.get('manager_name')
    result['manager_email'] = op.get('manager_email')
    result['manager_ip_email'] = op.get('manager_ip_email')
    result['link'] = (
      'https://crm.digitalstrateg.ru/edit_form.pl'
      f'?config=user&action=edit&id={op.get("id")}'
    )
  return result


def request_to_list(op):
  # Получатели: базовые + менеджер ОП + менеджер интернет-проекта
  to_list = list(BASE_TO)
  if op.get('manager_email'):
    to_list.append(op['manager_email'])
  if op.get('manager_ip_email'):
    to_list.append(op['manager_ip_email'])
  return to_list


def send_mail(subject, message, to_list):
  # Синхронная отправка (вызывается в отдельном потоке). Без SMTP-конфига -- лог.
  mail = config.get('mail', {})
  server = mail.get('server')
  if not server:
    print(f'[svcms-manager-start] mail не настроен, письмо не отправлено: {subject}')
    return False
  msg = MIMEText(message, 'html', 'utf-8')
  msg['From'] = FROM_ADDR
  msg['Subject'] = subject
  with smtplib.SMTP(server, mail.get('port', 587)) as srv:
    srv.ehlo()
    srv.starttls(context=ssl.create_default_context())
    srv.ehlo()
    srv.login(mail.get('user', ''), mail.get('password', ''))
    srv.sendmail(FROM_ADDR, to_list, msg.as_string())
  return True


async def deliver(s, subject, message, to_list):
  # В debug-режиме письма не отправляем (см. lib/engine.py: s.debug_mode)
  if getattr(s, 'debug_mode', False):
    print(f'[svcms-manager-start] debug: письмо не отправлено: {subject}')
    return
  try:
    await asyncio.to_thread(send_mail, subject, message, to_list)
  except Exception as e:
    print(f'[svcms-manager-start] ошибка отправки письма: {e}')


@router.get('/startpage/user-info')
async def startpage_user_info(request: Request):
  s = request.state.engine
  errors = list(s.errors)
  manager = getattr(request.state, 'manager', None) or {}
  host = manager.get('host') or s.env.get('host', '')
  login = manager.get('login', '')

  op = await op_card_info(s, host, errors)
  user = {
    'loaded': 1,
    'id': op.get('id', 0),
    'firm': op.get('firm', login),
    'is_ssl': op.get('is_ssl', 0),
    'hosting_start': op.get('hosting_start'),
    'hosting_end': op.get('hosting_end'),
    'domain_adaptive': op.get('domain_adaptive', 1),
  }
  domain_info = await asyncio.to_thread(whois_info, host)
  return {
    'success': not len(errors),
    'host': host,
    'user': user,
    'domain_info': domain_info,
    'errors': errors,
  }


@router.post('/startpage/request')
async def startpage_request(R: dict, request: Request):
  s = request.state.engine
  errors = []
  manager = getattr(request.state, 'manager', None) or {}
  host = manager.get('host') or s.env.get('host', '')
  login = manager.get('login', '')
  R = R or {}
  action = R.get('action', '')

  op = await op_card_info(s, host, errors)
  link = op.get('link', '')
  to_list = request_to_list(op)
  subject = ''
  message = ''
  response = {}

  if action == 'prog_request':
    subject = f'Задан вопрос из админки по сайту {host}'
    message = (
      f'{link}<br>'
      f'Логин клиента: {login}<br>'
      f'Имя: {R.get("name", "")}<br>'
      f'Телефон: {R.get("phone", "")}<br>'
      f'<hr>{R.get("question", "")}'
    )
    response['success_header'] = 'Запрос успешно отправлен'
    response['success_text'] = 'Наш специалист свяжется в Вами'
  elif action == 'interest':
    v = R.get('v', '')
    subject = f'Клиент заинтересовался услугой {v}'
    message = (
      f'{link}<br>'
      f'Клиент нажал кнопку "Заказать {v}" в админке сайта {host}<br>'
      f'Логин клиента: {login}'
    )
  elif action in ('long_host', 'long_domain'):
    what = 'хостинга' if action == 'long_host' else 'домена'
    subject = f'Запрос из админки на продление {what} {host}'
    message = (
      f'{link}<br>'
      f'Логин клиента: {login}<br>'
      f'Сайт: {host}<br>'
      f'Имя: {R.get("name", "")}<br>'
      f'Телефон: {R.get("phone", "")}<br>'
      f'Email: {R.get("email", "")}'
    )
    if action == 'long_host':
      response['success_header'] = 'Запрос на продление хостинга отправлен'
  elif action == 'inner_optimize':
    subject = f'Запрос из админки на внутреннюю оптимизацию сайта {host}'
    message = f'Логин клиента: {login}<br>Сайт: {host}'
  elif action == 'optimize':
    subject = f'Запрос из админки на оптимизацию сайта {host}'
    message = (
      'Оптимизация сайта в соответствии с требованиями поисковых систем<br>'
      f'Логин клиента: {login}<br>Сайт: {host}'
    )
  elif action == 'adaptive_design':
    subject = f'Запрос из админки на адаптивный дизайн {host}'
    message = f'{link}<br>Логин клиента: {login}<br>Сайт: {host}'
  elif action == 'audit_site':
    subject = f'Запрос из админки на аудит сайта {host}'
    message = f'{link}<br>Логин клиента: {login}<br>Сайт: {host}'
  elif action == 'rule_fill':
    subject = f'Запрос из админки на наполнение {host}'
    message = f'{link}<br>Логин клиента: {login}<br>Сайт: {host}'
  elif action == 'context':
    subject = f'Запрос из админки на контекстную рекламу {host}'
    message = f'{link}<br>Логин клиента: {login}<br>Сайт: {host}'
  elif action == 'schema':
    subject = f'Запрос из админки на настройку микроразметки schema.org {host}'
    message = f'{link}<br>Логин клиента: {login}<br>Сайт: {host}'
  elif action == 'site_rework':
    subject = f'Запрос из админки на доработку сайта {host}'
    message = f'{link}<br>Логин клиента: {login}<br>Сайт: {host}'
  elif action == 'redesign':
    subject = f'Запрос из админки на обновление дизайна {host}'
    message = f'{link}<br>Логин клиента: {login}<br>Сайт: {host}'
  elif action == 'ii_show':
    subject = f'Запрос из админки на Улучшение видимости в нейросетях {host}'
    message = f'{link}<br>Логин клиента: {login}<br>Сайт: {host}'
  elif action == 'base_support':
    subject = f'Запрос из админки на Базовую поддержку сайта {host}'
    message = f'{link}<br>Логин клиента: {login}<br>Сайт: {host}'
  elif action == 'get_ssl':
    subject = f'Запрос из админки (SSL) {host}'
    message = (
      f'{link}<br>'
      f'Логин клиента: {login}<br>'
      f'Сайт: {host}<hr>'
      'Клиент отправил запрос на добавление ssl-сертификата'
    )
  elif action == 'add_section':
    sect_list = R.get('sect_list') or []
    sect_list_txt = ''.join(f'<li>{x}</li>' for x in sect_list)
    custom = R.get('custom_section', '')
    custom_txt = f'<br>введено вручную: <b>{custom}</b>' if custom else ''
    subject = f'Запрос из админки на подключение разделов у сайта {host}'
    message = (
      f'{link}<br>'
      f'Логин клиента: {login}<br>'
      f'Сайт: {host}<hr>'
      f'Желаемые секции сайта:<ul>{sect_list_txt}</ul>{custom_txt}'
    )
  elif action == 'start_promo':
    subject = f'Запрос из админки на наполнение {host}'
    message = f'{link}<br>Логин клиента: {login}<br>Сайт: {host}<hr>'
  else:
    errors.append('запрос не отправлен')

  if not len(errors):
    await deliver(s, subject, message, to_list)

  response['success'] = not len(errors)
  response['errors'] = errors
  return response
