from lib.engine import s
from config import config

def get_banners():
  banners={
    'desktop':[
      {'show':True,'list':[]},
      {'show':True,'list':[]},
      {'show':True,'list':[]},
      {'show':True,'list':[]}
    ],
    'mobile':[
      {'show':True,'list':[]},{'show':True,'list':[]}
    ]
  }
  all_banners=s.db.query(
    query='select url,attach file, type, type_mobile from banner where enabled=1'
  )
  for b in all_banners:
    if b['file']:
      b['file']=f"/files/bfiles/{b['file']}"
      if b['type']:
        idx=b['type']-1
        banners['desktop'][idx]['list'].append(b)

      if b['type_mobile']:
        idx=b['type_mobile']-1
        banners['mobile'][idx]['list'].append(b)
  return banners
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
    ur_lico_ids=s.db.query(
        query="select ur_lico_id from ur_lico_manager where manager_id=%s",
        values=[manager['id']],
        massive=1
    )
    
    where='out_ur_lico=1'

    if len(ur_lico_ids)>1:
      where+=' OR out_ur_lico_multi=1'

    
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
    'banners':get_banners(),
    'manager':manager,
    'errors':errors,
    'success': not len(errors),
  }
  return {'success':1,'left_menu':left_menu}