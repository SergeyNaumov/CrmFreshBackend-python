from lib.engine import s
def get_anna_manager():
  
  return s.db.query(
    query="""
      SELECT
        am.id, concat(am.name_f,' ',am.name_i,' ',am.name_o) fio, am.login email
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
    print('x')
    return None
  

  return s.db.query(
    query='SELECT * from ur_lico where id=%s',
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
    debug=1
  )
  return e


def password_ok(p):
    return s.db.query(
        query="select count(*) from manager where id=%s and password=sha2(%s,256)",
        values=[s.manager['id'],p],
        onevalue=1
    )
def get_manager_data(errors=[]):
    return s.db.query(
        query="""
            SELECT
                wt.id,wt.login,wt.name_f,wt.name_i,wt.name_o,wt.name,wt.phone,wt.type,
                ma.id ma_id, ma.name_f ma_name_f,  ma.name_i ma_name_i, ma.name_o ma_name_o, ma.email ma_email, ma.phone ma_phone
            FROM 
                manager wt
                LEFT JOIN manager ma ON wt.anna_manager_id=ma.id
            WHERE wt.id=%s
        """,
        values=[s.manager['id']],
        onerow=1

    )


  
