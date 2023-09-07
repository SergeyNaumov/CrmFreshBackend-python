from lib.core import cur_year,cur_date, exists_arg
from fastapi import FastAPI, APIRouter
#from lib.engine import s

#import re
#from lib.send_mes import send_mes
from lib.all_configs import read_config


#valid_email=re.compile(r"^[a-zA-Z0-9\-_\.]+@[a-zA-Z0-9\-_\.]+\.[a-zA-Z0-9\-_\.]+$")
#valid_phone=re.compile(r"")
router = APIRouter()

# изменение пароля
@router.post('/ajax/{config}/{ajax_name}')
async def ajax(config:str,ajax_name:str,R: dict):
  success=1
  errors=[]
  form=read_config(
    script='ajax', config=config,
    R=R,
    id=R['id']
  )
  result=[];
  
  if exists_arg(ajax_name,form.ajax):
    result = form.ajax[ajax_name](form,R['values'])
  else:
    errors.append(f'не найден ajax-контроллер с именем: {ajax_name} обратитесь к разработчику')
  
  if len(errors):
    success=0
  return  {'success':success,'errors':errors,'result':result}
        

      
    
  
