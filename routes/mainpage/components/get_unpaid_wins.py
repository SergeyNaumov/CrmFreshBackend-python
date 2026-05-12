from decimal import Decimal
from lib.core import get_triade,join_ids # cur_year,cur_date, cur_hour, first_day_in_mon, get_mon_name, ,
from lib.core_crm import get_role, get_manager
#from lib.engine import s

# НЕОПЛАЧЕННЫЕ ПОБЕДЫ
async def process_get_unpaid_wins(request):
  s = request.state.engine
  manager = await get_manager(id=request.state.manager['id'], db=s.db, options_hash=True, child_groups=True)
  manager_id = await get_role(s.db, manager['id'])
  if manager_id and manager_id != manager['id']:
    manager = await get_manager(id=manager_id, db=s.db, options_hash=True, child_groups=True)

  values = []
  if manager['options'].get('mainwidget_nopaidwin_show_all'):
    where = ''
  elif manager['owner'] and manager['CHILD_GROUPS']:
    where = f" and m.group_id in ({join_ids(manager['CHILD_GROUPS'])})"
  else:
    where = f' and m.id=%s'
    values.append(manager['id'])

  result = await s.db.query(
    query=f"""
          select wt.number, wt.summ, u.firm, u.id user_id
          from bill wt
          left join manager m on m.id=wt.manager_id
          left join manager_group mg on m.group_id=mg.id
          LEFT JOIN dogovor_app da ON da.id=wt.dogovor_app_id
          LEFT JOIN service s ON s.id=da.service_id
          LEFT JOIN teamwork_ofp tof ON tof.teamwork_ofp_id=da.card_id
          join docpack dp on wt.docpack_id=dp.id
          join user u on dp.user_id=u.id
          where m.gone=0 and s.type=1 and wt.paid=0 and tof.win_status=1 and wt.summ>0 {where}
          order by wt.summ desc
          limit 100
      """,
    values=values
  )
  data = []
  total_summ = Decimal(0)
  for obj in result:
    total_summ += obj['summ']
    data.append({
      'user': f'<a href="/edit_form/user/{obj["user_id"]}" target="_blank">{obj["firm"]}</a>',
      'bill': f"{get_triade(obj['summ'])} ({obj['number']})"
    })
  _list = [
    #{'type': 'html', 'body': f'<h3 style="margin: 20px 0px;">Итого: {get_triade(total_summ)}</h3>'},
    {
      'type': 'data_table',
      'sort': 'name',
      'headers': [
        {'text': 'Название компании', 'value': 'user'},
        {'text': 'Счет', 'value': 'bill'},
      ],
      'data': data
    }
  ]
  return {'title':f"Неоплаченные победы&nbsp;<small>(итого: {get_triade(total_summ)})</small>",'success': True, 'errors': [], 'result_type': '', 'list': _list}