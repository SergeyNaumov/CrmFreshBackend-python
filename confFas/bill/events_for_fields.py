from lib.core import date_to_rus, cur_date, get_triade
from lib.core_crm import get_manager, get_owner, get_email_list_from_manager_id
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
    if  not(form.ov['paid']) and form.nv['paid']:
      paid_date=cur_date()
      #print(f"ov: {form.ov['paid']} // nv: {form.nv['paid']}")
      form.db.query(
        query="UPDATE bill set paid_date=%s where id=%s",
        values=[paid_date,form.id]
      )

      own=get_owner(
        db=form.db,
        cur_manager={
          'id': ov['m_id'],
          'group_path': ov['m_group_path'],
          'group_id': ov['m_group_id'],

        }
      )
      #print('owner:',own)
      # отправляем менеджеру счёта
      to_ids={7576:1}

      #print(f"email: {ov['m_email']}")

      if  ov['m_id']!=form.manager['id']:
        #to[ ov['m_email'] ]=1
        to_ids[ov['m_id']]=1

      # и его руководителю
      if own and own['id'] != form.manager['id']:
        #to[ own['email'] ]=1
        to_ids[own['id']]=1

      if len(to_ids.keys()):
        #to_str=', '.join(to.keys())
        #print('to_str:',to_str)

        
        #send_mes(

        #)
        subject=f"{ov['firm']} счёт №{ov['number']} оплачен "
        

        message=f'''
          Для компании <a href="{form.s.config['system_url']}edit_form/user/{ov['user_id']}">{ov['firm']}</a><br>
          <a href="{form.s.config['system_url']}edit_form/bill/{form.id}">Счёт №{ov['number']}</a><br>
          Сумма: {form.new_values['summ']}<br>
          дата оплаты: {cur_date}
        '''

        to=get_email_list_from_manager_id(form.db, to_ids)


        send_mes(
          from_addr='info@fascrm.ru',
          to=','.join(to.keys()),
          subject=subject,
          message=message
        )
        #print(message)
    
def paid_before_code(form,field):
  if form.is_admin or form.manager['permissions']['admin_paids']:
    field['read_only']=0
  # if form.ov and form.ov['avance_fact_number']:
  #   field['after_html']=f'''
  #     <hr>
  #     <b>Авансовая счёт-фактура №{ov['avance_fact_number']}</b><br>
  #     с печатями: <a href="/tools/load_document.pl?type=av_fact&bill_id={form.id}&format=doc">doc</a> | <a href="/tools/load_document.pl?type=av_fact&bill_id={form.id}&format=pdf">pdf</a><br>
  #     без печатей: <a href="/tools/load_document.pl?type=av_fact&bill_id={form.id}&format=doc&without_print=1">doc</a> | <a href="/tools/load_document.pl?type=av_fact&bill_id={form.id}&format=pdf&&without_print=1">pdf</a><br>
  #     <hr>
  #   '''

# Дата оплаты
def date_before_code(form,field):
  if form.script=='admin_table':
    field['value']=['2023-12-01']
  if form.id:
    if form.ov['paid']:
      field['hide']=False
    if form.is_admin or form.manager['permissions']['admin_paids']:
      field['read_only']=0

def paid_summ_before_code(form,field):
  if form.id:
    if(form.ov['paid']):
      field['hide']=False
    if form.is_admin or form.manager['permissions']['admin_paids']:
      field['read_only']=0

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

# Название компании
def firm_filter_code(form,field,row):
  if firm:=row.get('u__firm'):
    return f"<a href='/edit_form/user/{row['u__id']}' target='_blank'>{firm}</a>"
  return '-'

#def summ_before_code(form,field,row):

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
    'before_code': date_before_code,
  },
  'paid_to':{
    'before_code': paid_to_before_code,
  },
  'summ':{
    'filter_code': lambda form,field,row: get_triade(row['wt__summ'])
  },
  'paid_summ':{
    'before_code': paid_summ_before_code,
  },
  'group_id':{
    'before_code': not_ro_admin,
  },
  'manager_id':{
    'before_code': not_ro_admin,
  },
  'act':{
    'before_code':act_before_code
  },
  'firm':{
    'filter_code':firm_filter_code
  }
}