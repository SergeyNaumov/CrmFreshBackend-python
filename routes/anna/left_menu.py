from lib.engine import s
from config import config
def left_menu():
  errors=[]
  manager=None
  manager_menu_table=None
  left_menu=[]

  manager=s.db.query(
    query='select id,name,type from manager where login=%s',
    values=[s.login],
    onerow=1,
  )
  where='1'
  if manager['type']==1: # Менеджер АннА
    where='out_manager_anna=1'
  elif manager['type']==2: # Юридическое лицо
    where='out_ur_lico=1'
  elif manager['type']==3: # Аптека
    where='out_apteka=1'
  elif manager['type']==4: # Аптека
    where='out_pharm=1'

  left_menu=s.db.query(
    query=f"""
      SELECT
        mm.*
      from
        manager_menu mm
      where
        {where}
      ORDER BY mm.sort
    """,
    errors=errors,
    tree_use=1
  )

  return {
    'left_menu':left_menu,
    'manager':manager,
    'errors':errors,
    'success': not len(errors),
  }
  return {'success':1,'left_menu':left_menu}