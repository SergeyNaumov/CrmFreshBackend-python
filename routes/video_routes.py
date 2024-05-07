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
    rec_id= await form.db.save(
      table=form.table_stat_open,
      data={
        'manager_id':form.manager['id'],
        'video_id':R['id'],
        'ts':'func:(now())'
      },
      #debug=1
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
async def get_videos(config:str, limit: int = 0): # 
  
  form= await read_config(
    action='',
    config=config,
    #id=id,
    #values=values,
    script='video_list'
  )
  errors=form.errors
  data_list=[]

  if not len(errors):
    if limit:
      data_list= await form.db.query(
        query=f'select * from {config} where parent_id is not null order by id desc limit {limit}'
      )
    else:
      data_list= await form.db.query(
        query=f'select * from {config} order by concat( if(parent_id is null,0,parent_id),"-",sort )' ,
        #debug=1,
        #table=config,
        #order='sort',
        #where='parent_id is null',
        
        errors=errors,
        tree_use=1
      )

  #for d in data_list:

  return {
    'title':form.title,
    'log':form.log,
    'errors':form.errors,
    'success':1,
    'list':data_list,
    'links':form.links,
    #'links':form.links
  }

  