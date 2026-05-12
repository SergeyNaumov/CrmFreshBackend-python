from lib.core import get_mon_name,get_triade, first_day_in_mon # cur_year,cur_date, cur_hour, first_day_in_mon, , get_triade, join_ids
#from lib.engine import s
from jinja2 import Template



async def process_bank(manager, s):
  begin_date = first_day_in_mon()
  arr=begin_date.split('-')
  mon_name=get_mon_name(int(arr[1])-1)+f'`{int(arr[0])-2000}'

  #title=f"Банк&nbsp;<small>(за {get_mon_name(int(arr[1])-1)} {arr[0]})</small>"
  permissions = manager['options']

  _list = await s.db.query(
    query="""
      select * from (
      SELECT
        m.name, sum(b.paid_summ) bank, m.group_id, m.id, if(mp.id, 1, 0) not_show
      FROM
        bill b
      join manager m ON b.manager_id=m.id
      LEFT JOIN manager_permissions mp on mp.manager_id=m.id and mp.permissions_id=241
      WHERE b.paid_date>=%s group by m.id ORDER BY m.name
      ) x order by bank desc
    """,
    values=[begin_date]
  )
  data=[]
  total_summ=0
  st=[0,0,0]
  j=0
  mainwidget_bank_show_all_perm = permissions.get('mainwidget_bank_show_all')
  for l in _list:
    if l['not_show']:
      continue
    total_summ+=l['bank']
    if j in (0,1,2):
      st[j]=get_triade(int(l['bank']))
    j += 1
    l['bank'] = get_triade(l['bank'])

    if mainwidget_bank_show_all_perm:
      data.append(l)
    elif (manager['owner'] and l['group_id'] in manager['CHILD_GROUPS']) or manager['id']==l['id']:
      data.append(l)

  html = open("routes/mainpage/components/bank/template.html").read()
  t=Template(html)
  body=t.render(st=st)

  #body=templates.TemplateResponse('template.html', st=st)
  

  _list=[
    {'type':'html','body':body},
    {
      'type':'data_table',
      'sort':'name',
      'headers':[
        {'text':'Сотрудник','value':'name'},
        {'text':'Банк','value':'bank'},
      ],
      'data':data
    }
  ]
  if manager['login'] in ('pzm','akulov','sed'):
    title=f"Банк&nbsp;<small>(итого: {get_triade(total_summ) }) / {mon_name} </small>"
  else:
    title=f"Банк&nbsp;<small>({mon_name})</small>"

  return {'title':title, 'success':True, 'errors': [], 'result_type': '', 'list':_list}
