from lib.core import date_to_rus
from lib.core_crm import get_manager, get_owner
from lib.send_mes import send_mes

# Юр.Лицо
def c_ur_lico_id_before_code(form,field):
      if form.ov:
        comment=form.db.query(
          query='SELECT comment from ur_lico where id=%s',
          values=[form.ov['ur_lico_id']],
          onevalue=1
        );
        
        if comment:
          comment=f" ({comment})"
        
        field['after_html']=f'''<a href="/edit_form/ur_lico/{form.ov['ur_lico_id']}">{form.ov['ur_lico']}{comment}</a>'''


def firm_c_before_code(form,field):
  if form.ov:
    field['after_html']=f'''
      <a href="/edit_form/user/{form.ov['user_id']}" target="_blank">{form.ov['firm']}</a>
    '''

def tarif_before_code(form,field):
  if form.ov:
    field['after_html']=f'''
      <a href="/edit_form/tarif/{form.ov['tarif_id']}" target="_blank">{form.ov['tarif']}</a>
    '''
def d1_number_before_code(form,field):
  if form.id: field['after_html']=form.ov['d_number']


def not_ro_admin(form,field):
  if form.is_admin: field['read_only']=0


def paid_after_save(form,field):
  to={}
  ov=form.ov
  

  if ov and ov['m_id']:
    if True or ( not(form.ov['paid']) and field['value']):
      own=get_owner(
        db=form.db,
        cur_manager={
          'id': ov['m_id'],
          'group_path': ov['m_group_path'],
          'group_id': ov['m_group_id'],

        }

      )
      # отправляем менеджеру счёта
      if ov['m_email'] and ov['m_id']!=form.manager['id']:
        to[ form.manager['id'] ]=1

      # и его руководителю
      if own and own['email'] and own['id'] != form.manager['id']:
        to[ own['email'] ]=1

      if len(to.keys()):
        to_str=', '.join(to.keys())
        #print('to_str:',to_str)

        
        #send_mes(

        #)
        subject=f"{ov['firm']} счёт №{ov['number']} оплачен "
        

        message=f'''
          Для компании <a href="{form.s.config['system_url']}edit_form/user/{ov['user_id']}">{ov['firm']}</a><br>
          <a href="{form.s.config['system_url']}edit_form/bill/{form.id}">Счёт №{ov['number']}</a><br>
          Сумма: {form.new_values['summ']}<br>
          дата оплаты: {form.new_values['paid_date']}
        '''
        send_mes(
          from_addr='info@fascrm.ru',
          to=','.join(to.keys()),
          subject=subject,
          message=message
        )
        #print(message)
    
def paid_before_code(form,field):
  if form.is_admin: field['read_only']=0
  if form.ov and form.ov['avance_fact_number']:
    field['after_html']=f'''
      <hr>
      <b>Авансовая счёт-фактура №{ov['avance_fact_number']}</b><br>
      с печатями: <a href="/tools/load_document.pl?type=av_fact&bill_id={form.id}&format=doc">doc</a> | <a href="/tools/load_document.pl?type=av_fact&bill_id={form.id}&format=pdf">pdf</a><br>
      без печатей: <a href="/tools/load_document.pl?type=av_fact&bill_id={form.id}&format=doc&without_print=1">doc</a> | <a href="/tools/load_document.pl?type=av_fact&bill_id={form.id}&format=pdf&&without_print=1">pdf</a><br>
      <hr>
    '''
def paid_to_before_code(form,field):
  if form.is_admin: field['read_only']=0
  if form.ov:
    user_id=form.ov['user_id']
    max_paid_to=form.db.query(
      query='''
        SELECT
          paid_to
        FROM
          docpack dp
          join bill b ON b.docpack_id=dp.id
        where dp.user_id=%s order by paid_to desc limit 1
      ''',
      values=[user_id],
      onevalue=1
    )
    if max_paid_to:

      field['after_html']=f"максимальная дата оплаты для данной компании: <b>{date_to_rus(max_paid_to)}</b><hr>"

def act_before_code(form,field):
  if form.is_admin:
    field['make_delete']=1
  if form.is_admin or (form.ov and (form.ov['paid'] or form.ov['manager_id'] == form.manager['id']) ):
    field['not_create']=0
    field['read_only']=0
    field['link_add']=f'/edit_form/act?bill_id={form.id}'

events={
  'c_ur_lico_id': {
    'before_code': c_ur_lico_id_before_code
  },
  'firm_c':{
    'before_code': firm_c_before_code
  },
  'tarif':{
    'before_code': tarif_before_code
  },
  'd1_number': {
    'before_code': d1_number_before_code
  },
  'payment_order': {
    'before_code': not_ro_admin
  },
  'registered':{
    'before_code': not_ro_admin
  },
  'paid':{
    'before_code': paid_before_code,
    'after_save': paid_after_save
  },
  'paid_date':{
    'before_code': not_ro_admin,
  },
  'paid_to':{
    'before_code': paid_to_before_code,
  },
  'group_id':{
    'before_code': not_ro_admin,
  },
  'manager_id':{
    'before_code': not_ro_admin,
  },
  'act':{
    'before_code':act_before_code
  } 
}