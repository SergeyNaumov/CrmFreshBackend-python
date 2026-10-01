import os
import re
import asyncio
import subprocess


# Легаси domain.pl: whois выполняется перед выводом поля whois.
# Команда и разбор -- по аналогии с легаси.
def _whois_command(domain):
  if re.search(r'[a-zA-Z0-9\-.]\.msk\.ru', domain):
    return ['whois', '-h', 'WHOIS.REGISTRY.NIC.MOSCOW', domain]
  m = re.search(r'([^.]+\.[^.]+)$', domain)
  if m:
    d = m.group(1)
    if re.search(r'sts\.msk\.ru', d) or re.search(r'^[a-zA-Z0-9\-.]+\.(moscow|msk\.ru)$', d):
      return ['whois', '-h', 'WHOIS.REGISTRY.NIC.MOSCOW', d]
    if re.search(r'^[a-zA-Z0-9\-.]+$', d):
      return ['whois', d]
  return None


def _run_whois(domain):
  cmd = _whois_command(domain)
  if not cmd:
    return None, ''
  try:
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=25)
    return ' '.join(cmd), (r.stdout or '')
  except Exception as e:
    return ' '.join(cmd), f'ошибка выполнения whois: {e}'


async def whois_before_code(form, field):
  domain = (form.values or {}).get('domain') or ''
  domain = re.sub(r'\s+', '', domain)
  if not domain:
    field['html'] = ''
    return

  command, raw = await asyncio.to_thread(_run_whois, domain)
  if not command:
    field['html'] = ''
    return

  lines = [
    line for line in raw.split('\n')
    if re.search(r'(name server|nserver|(Primary|Secondary) server[\.:]+)', line, re.I)
  ]
  result = '<br>'.join(lines)
  other_ns = not re.search(r'\S+(\.design-b2b\.com\.su)', result, re.I)

  html = (
    '<hr><b>результат выполнения:</b><br>'
    f'{command}:<br><br>'
    f'<div style="display: block; border: 1px solid gray;">{result}</div><br>'
  )
  if other_ns:
    html += (
      '<div style="color: red;">Внимание! Если здесь указаны ns-серверы, '
      'отличные от: design-b2b.com, то необходимо указать правильные NS-серверы '
      'у регистратора</div>'
    )
  field['html'] = html


# Легаси domain.pl: этапы Lets Encrypt под полем SSL.
# cur_step берётся из domain.lets_encrypt_status (0..5).
LETS_ENCRYPT_ADDR = '178.57.220.192'


async def ssl_steps_before_code(form, field):
  v = form.values or {}
  domain = re.sub(r'\s+', '', str(v.get('domain') or ''))
  if not form.id or not re.match(r'^[a-zA-Z0-9\.\-\_]+$', domain):
    field['html'] = ''
    return
  try:
    cur_step = int(v.get('lets_encrypt_status') or 0)
  except (TypeError, ValueError):
    cur_step = 0
  tmpl = os.path.join(os.path.dirname(__file__), 'lets_encrypt_steps.html')
  field['html'] = form.template(
    tmpl,
    form_id=form.id,
    domain=domain.lower(),
    addr=LETS_ENCRYPT_ADDR,
    cur_step=cur_step,
  )


# Легаси domain.before_code: project_id из GET-параметра при создании
async def project_id_before_code(form, field):
  if form.action == 'new':
    project_id = form.request.query_params.get('project_id')
    if project_id and project_id.isdigit():
      field['value'] = project_id


# Легаси domain.filter_code для проекта
async def project_id_filter_code(form, field, row):
  project_id = row.get('wt__project_id') or ''
  header = row.get('p__header') or ''
  return (
    f'<a href="edit_form.pl?config=project&action=edit&id={project_id}"'
    f' target="_blank">{header}</a>'
  )


# Легаси domain.filter_code для домена: ссылка + подсветка недопустимых символов
async def domain_filter_code(form, field, row):
  value = row.get('wt__domain') or ''
  if not value:
    return ''
  label = re.sub(
    r'([^a-zA-Z0-9\-\.]+)',
    r'<span style="color: red;">\1</span>',
    value,
  )
  return f'<a href="http://{value}" target="_blank">{label}</a>'


events = {
  'project_id': {
    'before_code': project_id_before_code,
    'filter_code': project_id_filter_code,
  },
  'domain': {
    'filter_code': domain_filter_code,
  },
  'whois': {
    'before_code': whois_before_code,
  },
  'ssl_steps': {
    'before_code': ssl_steps_before_code,
  },
}
