import datetime


from lib.core import cur_year,cur_date, cur_hour, first_day_in_mon, get_mon_name, get_triade, join_ids
from fastapi import APIRouter, Request
#from config import config
#from lib.engine import s
from lib.core_crm import get_role, get_manager, get_group_options, format_sec_to_hours

# Компоненты
from .components.get_unpaid_wins import process_get_unpaid_wins
from .components.get_week_traffic import process_get_week_traffic
from .components.bank import process_bank
from db import get_db

router = APIRouter()

async def get_email_list(manager_id):
  # учитываем роль
  #s = request.state.engine
  db = get_db()

  manager_id = await get_role(db, manager_id) # s.request.state.manager['id']

  return await db.query(
    query="select email from manager_email where manager_id=%s and email like %s",
    values=[manager_id, '%@%'],
    massive=1
  )


# Неплаченные победы на главной
@router.get('/unpaid_wins')
async def get_unpaid_wins(request: Request):
  return await process_get_unpaid_wins(request)



# Таблица с трафиком за последнюю неделю на главной
@router.get('/traffic')
async def get_week_traffic(request: Request):
 return await process_get_week_traffic(request)
  # body = "<h1>Трафик сотрудников</h1>"+\
  #        """<table class="tbl1 sm" style="width: 100%; margin-bottom: 20px;"> <tr><td>Сотрудник</td><td>Трафик</td></tr>"""
  # for obj in result:
  #   if obj['duration'] >= 7200:  # больше 2х часов
  #     duration = f"""<h4 style="background-color:green">{await format_sec_to_hours(obj['duration'])}</h4>"""
  #   else:
  #     duration = f"""<h4 style="background-color:red">{await format_sec_to_hours(obj['duration'])}</h4>"""
  #   body += f"""<tr><td>{obj['name']}</td><td>{duration}</td></tr>"""
  # body += '</table>'
  # return {'success':True, 'errors': [], 'result_type': '', 'list':[{"type": "html", "body": body}]}



# Дни рождения на главной странице
@router.get('/birthdays')
async def get_birthdays(request: Request):
  s = request.state.engine
  config=s.config
  manager_table=config["auth"]["manager_table"]
  _list=await s.db.query(
      query=f"select id,name, born_date date from {manager_table} where gone=0 and born_date<>''"
  )
  return {'success':True, 'list':_list}

# Уведомления на главной
@router.get('/notifications')
async def get_notifications(request: Request):
  s = request.state.engine
  _list=[]
  email_list=await get_email_list(request.state.manager['id'])

  if len(email_list):
    _list=await s.db.query(
      query="SELECT id, registered,subject,message, to_addr, readed FROM mail_send WHERE to_addr in ('"+"','".join(email_list)+"') and registered>=now() - interval 2 day order by registered desc limit 100",
    )
  return {'success':True,'list':_list}

# Получение новых сообщений
@router.get('/notifications/update/{max_id}')
async def new_notifications(max_id: int, request: Request):
  s = request.state.engine
  _list=[]
  email_list=await get_email_list(request.state.manager['id'])
  if len(email_list):
    #return email_list
    _list=await s.db.query(
      query=f"SELECT * FROM mail_send WHERE id>{max_id} and to_addr in ('"+"','".join(email_list)+"') and registered >= ( now() - interval 2 day ) order by registered", #
      #values=[max_id],
#     debug=1
    )

  return {'success':True, 'list':_list}


@router.get('/notifications/set-readed/{_id}/{v}')
async def set_readed(_id:int, v:int, request: Request):
  s = request.state.engine
  if v:
    v=1
  else:
    v=0
  email_list=await get_email_list(request.state.manager['id'])
  if len(email_list):
    await s.db.query(
      query="UPDATE mail_send set readed=%s where id=%s and to_addr in ('"+"','".join(email_list)+"')" ,
      values=[v,_id]
    )

  return {'success':True}


@router.get('/manager-load/save/{percent}')
async def save_manager_load(percent: int, request:Request):
  s = request.state.engine
  manager_id = await get_role(s.db, request.state.manager['id'])
  h=cur_hour()
  if h>=11:
    return {'success':False,'errors':['разрешено вносить данные до 11 часов']}

  
  d=cur_date()
  exists=await s.db.query(
    query="SELECT * manager_load FROM where manager_id=%s and date=%s",
    values=[manager_id,d],
    onerow=1
  )
  if exists:
    return {'success':False,'errors':[f"Вы уже вносили данные по эффективности"]}

  if percent>=1 and percent<=100:
    await s.db.save(
      table='manager_load',
      data={
        'manager_id':manager_id,
        'percent':percent,
        'date':d
      },
      #debug=1
    )
    return {'success':True}

# Банк за текущий месяц
@router.get('/bank')
async def load_bank(request: Request):
  s = request.state.engine
  manager_id = await get_role(s.db, request.state.manager['id'])
  manager = await get_manager(id=manager_id,options_hash=True, child_groups=True, db=s.db)
  return await process_bank(manager, s)
  # begin_date = first_day_in_mon()
  # arr=begin_date.split('-')
  # title=f"Банк&nbsp;<small>(за {get_mon_name(int(arr[1])-1)} {arr[0]})</small>"

  # _list = await s.db.query(
  #   query="""
  #     SELECT
  #       m.name, sum(b.paid_summ) bank
  #     FROM
  #       bill b
  #       join manager m ON b.manager_id=m.id
  #     WHERE b.paid_date>=%s group by m.id ORDER BY m.name
  #   """,
  #   values=[begin_date]
  # )
  # data=[]

  # for l in _list:
  #   l['bank']=get_triade(l['bank'])
  #   data.append(l)

  # _list=[
  #   {
  #     'type':'data_table',
  #     'sort':'name',
  #     'headers':[
  #       {'text':'Сотрудник','value':'name'},
  #       {'text':'Банк','value':'bank'},
  #     ],
  #     'data':data
  #   }
  # ]
  # return {'title':title, 'success':True, 'errors': [], 'result_type': '', 'list':_list}


# Инициализация компонента manager-load (загрузка менеджера)
@router.get('/manager-load/init')
async def init_manager_load(request: Request):
  s = request.state.engine
  manager_id = await get_role(s.db, request.state.manager['id'])
  manager = await get_manager(id=manager_id,options_hash=True, db=s.db)
  group_options = await get_group_options(db=s.db, group_id=manager['group_id'])
  #print('group_options:',group_options)
  d=cur_date()
  exists=await s.db.query(
    query="SELECT * FROM manager_load where manager_id=%s and date=%s",
    values=[manager_id,d],
    onerow=1,
    #debug=1
  )
  return {
    'success':True,
    'exists':exists,
    'need_view':group_options.get('lawer'),
    'group_options':group_options
  }

# Главная
@router.get('')
async def mainpage(request: Request):
  s = request.state.engine
  config=s.config
  curdate=cur_date(format="%d.%m.%Y")
  response={'curdate':curdate,'errors':[],'success':1}
  if not('manager_table_id' in config['auth']):
    config["auth"]["manager_table_id"]='id'
  if s.project:
    response['manager']=await s.db.query(
      query=f'SELECT id,login,name,position, concat("/edit-form/project_manager/",{config["auth"]["manager_table_id"]}) link from project_manager where project_id=%s and id=%s',
      values=[s.project['id']],
      onerow=1
    )

    #response['news_list']=s.db.query(
    #  query='SELECT header,DATE_FORMAT(a.registered, "%e.%m.%y") registered,body from project_crm_news WHERE project_id=%s order by registered desc limit 5',
    #  values=[s.project['id']]
    #)
  else:

    response['manager']=await s.db.getrow(
      table=config['auth']['manager_table'],
      #select_fields=f' {config["auth"]["manager_table_id"]} id,login,name,"" position, concat("/edit-form/manager/",id) link',
      select_fields=f'{config["auth"]["manager_table_id"]} id,login, "" link',
      where=f'{config["auth"]["manager_table_id"]}=%s',
      values=[request.state.manager['id']],
      errors=response['errors'],
      str=1,
    )
    response['news_list']=[]
    #response['news_list']=s.db.query(
    #  query='SELECT header,DATE_FORMAT(registered, %s) registered, body from crm_news order by registered desc limit 5',
    #  values=["%e.%m.%y"]
    #)

  if not len(response['errors']) and not response['manager']:
    response['errors'].append('отсутствует запись с manager.id=='+str(request.state.manager['id']))

  if len(response['errors']):
    response['success']=0

  main_page_components=config.get('main_page_components')
  if not(main_page_components):
    main_page_components=[]

  response['main_page_components']=main_page_components
  return response

