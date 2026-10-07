import inspect
from lib.core import cur_year,cur_date, exists_arg
from fastapi import FastAPI, APIRouter, Request
#from lib.engine import s

#import re
#from lib.send_mes import send_mes
from lib.all_configs import read_config


#valid_email=re.compile(r"^[a-zA-Z0-9\-_\.]+@[a-zA-Z0-9\-_\.]+\.[a-zA-Z0-9\-_\.]+$")
#valid_phone=re.compile(r"")
router = APIRouter()

# Контроллеры в конфигах бывают и sync, и async -- поддерживаем оба.
async def run_ajax(form,ajax_name):
  res=form.ajax[ajax_name](form,form.R.get('values'))
  if inspect.isawaitable(res):
    res=await res
  return res

@router.get('/ajax/{config}/{ajax_name}')
async def ajax_get(config:str,ajax_name:str,request: Request):
  success=True ; errors=[] ; result=[]
  form=await read_config(
    request=request,
    script='ajax', config=config,
  )

  if exists_arg(ajax_name,form.ajax):
    result = await run_ajax(form,ajax_name)
  else:
    errors.append(f'не найден ajax-контроллер с именем: {ajax_name} обратитесь к разработчику')

  if len(errors):
    success=False
  return  {'success':success,'errors':errors,'result':result}

# изменение пароля
@router.post('/ajax/{config}/{ajax_name}')
@router.get('/ajax/{config}/{ajax_name}')
async def ajax(config:str,ajax_name:str,R: dict, request: Request):
  success=1
  errors=[]
  form=await read_config(
    request=request,
    script='ajax', config=config,
    R=R,
    id=R.get('id')
  )
  result=[];
  
  if exists_arg(ajax_name,form.ajax):
    result = await run_ajax(form,ajax_name)
  else:
    errors.append(f'не найден ajax-контроллер с именем: {ajax_name} обратитесь к разработчику')
  
  if len(errors):
    success=0
  return  {'success':success,'errors':errors,'result':result}
        

      
    
  
