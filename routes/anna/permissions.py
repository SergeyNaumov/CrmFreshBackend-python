from lib.engine import s
from lib.core import exists_arg
#from .get_reg_data import get_ur_lico_list_for_account

def get_anna_manager():
  
  return s.db.query(
    query="""
      SELECT
        am.id, concat(am.name_f,' ',am.name_i,' ',am.name_o) fio, if(am.email,am.email,am.login) email
      FROM
        manager wt
        join manager am ON am.id=wt.anna_manager_id
      WHERE wt.id=%s
    """,
    values=[s.manager['id']],
    onerow=1
  )

def get_ur_lico(ur_lico_id):
  if not ur_lico_id:
    #print('x')
    return None
  

  return s.db.query(
    query='''
      SELECT
        ul.*,
        ma.id ma_id, ma.name_f ma_name_f,  ma.name_i ma_name_i, ma.name_o ma_name_o, ma.login ma_email, ma.phone ma_phone
      from
        ur_lico ul
        LEFT JOIN manager ma ON ma.id=ul.anna_manager_id
      where ul.id=%s
    ''',
    values=[ur_lico_id],
    onerow=1
  )



def exist_login(login):
  # Проверяем заявку
  return s.db.getrow(
    table='order_reg_company',
    where='id<>%s and  login = %s',
    values=[s.manager['id'], login],
    onerow=1
  )

def exists_manager_login(login,manager_id=0):
  where='login=%s'
  if manager_id and str(manager_id).isdigit():
    where=where + " and id<>"+str(manager_id)
  
  e=s.db.query(
    query="select login from manager where "+where,
    values=[login],
    onevalue=1,
    #debug=1
  )
  return e


def password_ok(p):
    return s.db.query(
        query="select count(*) from manager where id=%s and password=sha2(%s,256)",
        values=[s.manager['id'],p],
        onevalue=1
    )

def get_manager_data(manager_id=0,errors=[]):
    if not manager_id:
      manager_id=s.manager['id']

    manager=s.db.query(
        query="""
            SELECT
                wt.id,wt.login,wt.name_f,wt.name_i,wt.name_o,wt.name,wt.phone,wt.type,
                ma.id ma_id, ma.name_f ma_name_f,  ma.name_i ma_name_i, ma.name_o ma_name_o, if(ma.email,ma.email,ma.login) ma_email, ma.phone ma_phone
                
            FROM 
                manager wt
                LEFT JOIN manager ma ON wt.anna_manager_id=ma.id
            WHERE wt.id=%s
        """,
        errors=errors,
        values=[manager_id],
        onerow=1,
    )
    
    

    if manager:
      manager['apteka']=None
      if manager['type']==3: # Если это аптека
          # если это аптека -- менеджер аптеки -- это менеджер юрлица
          manager['apteka']=s.db.query(
            query='''
              select
                a.*
              from
                apteka a
              where a.manager_id=%s
            ''',
            values=[manager_id],
            onerow=1
          )
        
          if manager['apteka'] and exists_arg('ur_lico_id',manager['apteka']):
            ur_lico=get_ur_lico(manager['apteka']['ur_lico_id'])
          
            # для аптеки менеджер AннA берётся из юрлица
            if exists_arg('ma_id',ur_lico):
              for attr in ['ma_id', 'ma_name_f', 'ma_name_i', 'ma_name_o', 'ma_email', 'ma_phone']:
                manager[attr]=ur_lico[attr]

              manager['ur_lico']=ur_lico

          

      if manager['type']==2:
        manager['ur_lico_list']=s.db.query(
          query="""
              SELECT
                  ul.id, ul.header
              from
                  ur_lico_manager ulm
                  join ur_lico ul ON ulm.ur_lico_id=ul.id
              WHERE ulm.manager_id=%s
          """,
          values=[manager_id],
        )
        ur_lico_hash={}
        for u in manager['ur_lico_list']:
          ur_lico_hash[u['id']]=1
        manager['ur_lico_hash']=ur_lico_hash

    return manager



    
#    manager={
#      ...
#       type:2,
#       apteka: 
#       ur_lico_list:[ ... ] список юрлиц
#    }

  
