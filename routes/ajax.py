from lib.core import cur_year,cur_date, exists_arg
from fastapi import FastAPI, APIRouter
#from lib.engine import s

#import re
#from lib.send_mes import send_mes
from lib.all_configs import read_config


#valid_email=re.compile(r"^[a-zA-Z0-9\-_\.]+@[a-zA-Z0-9\-_\.]+\.[a-zA-Z0-9\-_\.]+$")
#valid_phone=re.compile(r"")
router = APIRouter()

@router.get('/ajax/{config}/{ajax_name}')
async def ajax_get(config:str,ajax_name:str):
  success=True ; errors=[] ; result=[]
  form=read_config(
    script='ajax', config=config,
  )

  if exists_arg(ajax_name,form.ajax):
    result = form.ajax[ajax_name](form)
  else:
    errors.append(f'не найден ajax-контроллер с именем: {ajax_name} обратитесь к разработчику')

  if len(errors):
    success=False
  return  {'success':success,'errors':errors,'result':result}

# изменение пароля
@router.post('/ajax/{config}/{ajax_name}')
@router.get('/ajax/{config}/{ajax_name}')
async def ajax(config:str,ajax_name:str,R: dict):
  success=1
  errors=[]
  form=await read_config(
    script='ajax', config=config,
    R=R,
    id=R['id']
  )
  result=[];
  
  if exists_arg(ajax_name,form.ajax):
    result = await form.ajax[ajax_name](form,R.get('values'))
  else:
    errors.append(f'не найден ajax-контроллер с именем: {ajax_name} обратитесь к разработчику')
  
  if len(errors):
    success=0
  return  {'success':success,'errors':errors,'result':result}
        

      
    
  
