from lib.core import cur_year,cur_date, cur_hour
from fastapi import APIRouter
#from config import config
from lib.engine import s
from lib.core_crm import get_role, get_manager, get_group_options

router = APIRouter()

async def get_email_list():
  # учитываем роль

  manager_id = await get_role(s.db, s.request.state.manager['id'])

  return await s.db.query(
    query="select email from manager_email where manager_id=%s and email like %s",
    values=[manager_id, '%@%'],
    massive=1
  )

# Дни рождения на главной странице
@router.get('/birthdays')
async def get_birthdays():

  config=s.config
  manager_table=config["auth"]["manager_table"]
  _list=await s.db.query(
      query=f"select id,name, born_date date from {manager_table} where born_date<>''"
  )
  return {'success':True, 'list':_list}

# Уведомления на главной
@router.get('/notifications')
async def get_notifications():
  _list=[]

  email_list=await get_email_list()

  if len(email_list):
    #return email_list
    _list=await s.db.query(
      query="SELECT id, registered,subject,message, to_addr, readed FROM mail_send WHERE to_addr in ('"+"','".join(email_list)+"') and registered>=now() - interval 2 day order by registered desc limit 100",
      debug=1
    )
  return {'success':True,'list':_list}

# Получение новых сообщений
@router.get('/notifications/update/{max_id}')
async def new_notifications(max_id: int):
  _list=[]
  email_list=await get_email_list()
  if len(email_list):
    #return email_list
    _list=await s.db.query(
      query=f"SELECT * FROM mail_send WHERE id>{max_id} and to_addr in ('"+"','".join(email_list)+"') and registered >= ( now() - interval 2 day ) order by registered", #
      #values=[max_id],
#     debug=1
    )

  return {'success':True, 'list':_list}


@router.get('/notifications/set-readed/{_id}/{v}')
async def set_readed(_id:int, v:int):
  if v:
    v=1
  else:
    v=0
  email_list=await get_email_list()
  if len(email_list):
    await s.db.query(
      query="UPDATE mail_send set readed=%s where id=%s and to_addr in ('"+"','".join(email_list)+"')" ,
      values=[v,_id]
    )

  return {'success':True}


@router.get('/manager-load/save/{percent}')
async def save_manager_load(percent: int):
  manager_id = await get_role(s.db, s.request.state.manager['id'])
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

# Инициализация компонента manager-load (загрузка менеджера)
@router.get('/manager-load/init')
async def init_manager_load():
  
  manager_id = await get_role(s.db, s.request.state.manager['id'])
  #print('MANAGER_ID:',manager_id)
  #return {'manager_id':manager_id}
  manager = await get_manager(id=manager_id,options_hash=True, db=s.db)
  group_options = await get_group_options(db=s.db, group_id=manager['group_id'])
  #print('group_options:',group_options)
  d=cur_date()
  exists=await s.db.query(
    query="SELECT * FROM manager_load where manager_id=%s and date=%s",
    values=[manager_id,d],
    onerow=1,
    debug=1
  )
  return {
    'success':True,
    'exists':exists,
    'need_view':group_options.get('lawer'),
    'group_options':group_options
  }

# Главная
@router.get('')
async def mainpage():
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
      values=[s.request.state.manager['id']],
      errors=response['errors'],
      str=1,
    )
    response['news_list']=[]
    #response['news_list']=s.db.query(
    #  query='SELECT header,DATE_FORMAT(registered, %s) registered, body from crm_news order by registered desc limit 5',
    #  values=["%e.%m.%y"]
    #)

  if not len(response['errors']) and not response['manager']:
    response['errors'].append('отсутствует запись с manager.id=='+str(s.request.state.manager['id']))

  if len(response['errors']):
    response['success']=0

  main_page_components=config.get('main_page_components')
  if not(main_page_components):
    main_page_components=[]

  response['main_page_components']=main_page_components
  return response

