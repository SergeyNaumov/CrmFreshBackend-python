#from decimal import Decimal
import datetime
from collections import defaultdict

from lib.core import get_triade, join_ids
from lib.core_crm import get_role, get_manager, format_sec_to_hours
#from lib.engine import s

async def process_get_week_traffic(request):
  s = request.state.engine
  manager = await get_manager(id=request.state.manager['id'], db=s.db, child_groups=True, options_hash=True)
  manager_id = await get_role(s.db, manager['id']) # s.request.state.manager['id']
  if manager_id and manager_id!=manager['id']:
    manager = await get_manager(id=manager_id, db=s.db, options_hash=True, child_groups=True)


  values=[]
  if manager['options'].get('mainwidget_traffic_show_all'):
    where = ''
  elif manager['owner'] and manager['CHILD_GROUPS']:
    where = f" and m.group_id in ({join_ids(manager['CHILD_GROUPS'])})"
  else:
    where = f' and m.id=%s'
    values.append(manager['id'])

  week_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).replace(hour=0, minute=0)
  result=await s.db.query(
      query=f"""
          select br2.duration duration, m.name, date(br2.start_date) date
          from beeline_records_2 br2
          left join manager m on m.id=br2.manager_id
          where m.gone=0 and start_date >= '{week_ago.strftime('%Y-%m-%d %H:%M:%S')}' and duration>0 {where}
      """,
      values=values
  )
  date_headers = []
  start_date = week_ago.date()
  while start_date <= datetime.datetime.now().date():
    start_date_str = start_date.strftime("%Y-%m-%d")
    date_headers.append({'text': start_date_str, 'value': start_date_str})
    start_date += datetime.timedelta(days=1)

  grouped_data = defaultdict(lambda: defaultdict(int))

  for obj in result:
    date_str = obj['date'].strftime("%Y-%m-%d")
    grouped_data[obj['name']][date_str] += obj['duration']

  data = []
  for name, calls in grouped_data.items():
    row = {'name': name}
    existing_dates = set(calls.keys())
    for date_info in date_headers:
      date_str = date_info['value']
      if date_str in existing_dates:
        duration = calls[date_str]
        color = 'green' if duration >= 7200 else 'red'
        row[date_str] = f"<div style='display: inline-block; width: 10px; height: 10px; margin-right: 5px; border-radius: 5px; background-color: {color};'></div>{await format_sec_to_hours(duration)}"
      else:
        row[date_str] = "-"
    data.append(row)

  _list=[
    {
      'type':'data_table',
      'sort':'name',
      'headers':[
        {'text':'Сотрудник','value':'name'},
        *date_headers
      ],
      'data':data
    }
  ]
  return {'success':True, 'errors': [], 'result_type': '', 'list':_list}