from fastapi import APIRouter #, File, UploadFile, Form, Depends
from lib.all_configs import read_config

router = APIRouter()


@router.post('/{config}')
async def post_actions(config:str, R:dict): # 
  action=''
  if 'action' in R:
    action=R['action']
  
  form = await read_config(
    action=action,
    config=config,
    #id=id,
    #values=values,
    script='video_list'
  )

  if form.action=='open_video' and form.table_stat_open:
    rec_id = await form.db.save(
      table=form.table_stat_open,
      data={
        'manager_id':form.manager['id'],
        'video_id':R['id'],
        'ts':'func:(now())'
      },
    )

    return {
      'success':1,'id':rec_id
    }
  if form.action=='update_open_video' and ('id' in R) and ('seconds' in R) and form.table_stat_open:
    await form.db.query(
      query=f"UPDATE {form.table_stat_open} SET sec_opened=%s where manager_id=%s and id=%s",
      values=[R['seconds'], form.manager['id'], R['id']],
      
    )
  return {
    'success':len(form.errors)==0,
    'errors':form.errors,
    'log':form.log,
    'R':R
  }

@router.get('/{config}')
async def news_videos(config:str, limit: int = 0): # 
  
  form = await read_config(
    action='',
    config=config,
    #id=id,
    #values=values,
    script='video_list'
  )
  errors=form.errors
  data_list=[]
  #form.pre(f'select * from {form.work_table} where enabled=1 order by registered desc limit {limit}')
  if not len(errors):
    if limit:
      data_list=await form.db.query(
        query=f'''
          select
            id,anons,body,header,registered reg, DATE_FORMAT(registered, %s) registered
          from
            {form.work_table}
          where
            enabled=1 and registered<=curdate() order by reg desc limit {limit}
        ''',
        values=['%d.%m.%Y'],
      )
    else:
      data_list = await form.db.query(
        query=f'select * from {form.work_table} order by registered desc' ,
        #table=config,
        #order='sort',
        #where='parent_id is null',        
        errors=errors,
      )

  #for d in data_list:

  return {
    'title':form.title,
    'log':form.log,
    'errors':form.errors,
    'success':1,
    'list':data_list,
    #'links':form.links,
    #'links':form.links
  }

  
