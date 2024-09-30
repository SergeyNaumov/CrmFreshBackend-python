
from lib.core import exists_arg,date_to_rus

def process_bill_list(form, _list):

    perm=form.manager['permissions']

    for b in _list:
      # для редактирования на фронте
      b['old_summ']=b['summ']
      b['edit_sum']=False

      # тип счёта
      b['bill_type']=''
      if b['type']==1:
        b['type']='предоплата'
      elif b['type']==2:
        b['type']='постоплата'

      b['registered']=date_to_rus(b['registered'])

      # Разрешаем редактировать сумму счёта если:
      if perm.get('admin_paids'):
          # Если это менеджер платежей
          b['make_edit_summ']=True
      elif not(b['paid']) and (b['manager_id']==form.manager['id'] or form.manager['CHILD_GROUPS_HASH'].get(b['group_id']) ) :
          # или менеджер платежа
          # или руководитель менелжера платежа
          b['make_edit_summ']=True
      else:
          b['make_edit_summ']=False
async def get_bills(form,field, R):
  """
    Возвращает все счета и приложения к договору (с привязанными счетами)
  """
  R=form.R
  form_id=R.get('form_id_alternative') or form.id
  only_dogovor=R.get('only_dogovor')
  only_app=R.get('only_app')
  docpack_foreign_key=field['docpack_foreign_key'] ; lst=[] ; db=form.db
  if R.get('dogovor_id'):
      bill_list=[]
      bill_for_apps_dict={}

      lst_where=f"dp.{docpack_foreign_key}=%s and b.docpack_id=%s"
      lst_values=[form_id, R['dogovor_id']]

      if only_dogovor:
        lst_where+=f" and dp.id=%s"
        lst_values.append(only_dogovor)
      if only_app:
        lst_where+=' and dogovor_app_id=%s'
        lst_values.append(only_app)
      lst = await form.db.query(
        query=f"""
          SELECT
              b.*
          from
              docpack dp
              JOIN bill b ON b.docpack_id=dp.id
          where
              {lst_where}
          order by b.id desc
        """,
        #debug=1,
        values=lst_values
      )
      process_bill_list(form, lst)

      for b in lst:
        if b['dogovor_app_id']>0:
          if not(b['dogovor_app_id'] in bill_for_apps_dict):
            bill_for_apps_dict[b['dogovor_app_id']]=[]

          bill_for_apps_dict[b['dogovor_app_id']].append(b)
        else:
          bill_list.append(b)

      # Приложения к договору
      apps_list = await db.query(
        query="""
          select
            a.id, a.num_of_dogovor, date(a.registered) registered,
            a.card_id, s.type, s.header service,a.summ, a.summ_post,
            u.firm sr_name, u.id user_id, '' error
          from
            dogovor_app a
            LEFT JOIN service s ON s.id=a.service_id
            LEFT JOIN teamwork_ofp uc ON s.type=1 and uc.teamwork_ofp_id=a.card_id
            LEFT JOIN user_fin uf ON s.type=2 and uf.id=a.card_id
            LEFT JOIN user u ON u.id in (uf.user_id,uc.user_id)
          where a.dogovor_id=%s
        """,
        values=[R['dogovor_id']]
      )

      for a in apps_list:
        if a['sr_name'] and a['card_id']:
          if a['type']==1:
            a['sr_link']=f"/edit_form/teamwork_ofp/{a['card_id']}"
          elif a['type']==2:
            a['sr_link']=f"/edit_form/user_fin/{a['card_id']}"

        a['fields'] = await db.query(
          query=f"""
            SELECT
              wt.id, sf.header name, wt.value, '' edited
            FROM
              dogovor_app_values wt
              JOIN service_field sf ON sf.id=wt.field_id
            WHERE wt.dogovor_app_id={a['id']}
            ORDER BY sf.sort
          """
        )
        a['registered']=date_to_rus(a['registered'])
        a['bills']=bill_for_apps_dict.get(a['id'],[])


  else:
    form.errors.append('отсутствует параметр dogovor_id')
  return bill_list, apps_list

async def action_get_bills(form,field, R):
  bills,apps = await get_bills(form,field, R)
  return {'success':form.success(),'errors':form.errors, 'bills':bills,'apps':apps}