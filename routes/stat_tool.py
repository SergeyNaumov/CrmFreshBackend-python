from fastapi import APIRouter, Request #, File, UploadFile, Form, Depends
from fastapi.responses import StreamingResponse
from lib.all_configs import read_config
from lib.CRM.form.get_values_for_select_from_table import get_values_for_select_from_table
import traceback

router = APIRouter()
# Инициализация
@router.post('/{config}')
async def get_list(config: str, R:dict,request:Request): #
    form=await read_config(
        action='init',
        config=config,
        request=request,
        R=R,
        script='stat_tool'
    )
    if hasattr(form, 'response') and form.response:
        return form.response

    response={}
    success=True
    if not len(form.errors):
        #print('filters:',form.filters)
        filters=[]

        if hasattr(form, 'filters'):
            filters=form.filters
        elif hasattr(form,'fields'):
            filters=form.fields

        for f in filters:
            _type=f.get('type')

            if f.get('type')=='select_from_table':
                f['values']=await get_values_for_select_from_table(form, f)
                f['type']='select'

        response['title']=form.title
        response['filters']=filters
    else:
        success=False

    response['errors']=form.errors
    response['success']=success
    if(hasattr(form,'log')):
        response['log']=form.log
    else:
        response['log']=[]

    if(hasattr(form,'javascript')):
        response['javascript']=form.javascript
    
    return response

    # insert into const()

# Поиск
@router.post('/{config}/search')
async def search(config: str, R: dict, request: Request):
    form=await read_config(
        request=request,
        action='search',
        config=config,    
        script='stat_tool',
        R=R
    )



    if len(form.errors):
        return {'success':False, 'errors': form.errors}
    func=form.events['search']

    if func:
        try:
            #return await func(form, R)
            result = await func(form, R)

            # Проверяем, является ли результат StreamingResponse
            if isinstance(result, StreamingResponse):
                return result
            else:
                return result
        except Exception as e:
            error_info = traceback.format_exc()
            return {'success':False, 'errors':[f'ошибка приложения при выполнении события {search} ({e}) {error_info}']}
    else:
        return {'success':False, 'errors':[f'ошибка приложения при выполнении события {search} ({e})']}


# from conf.manager_employee.get_stat_dates_excel import save_excel
# @router.get('/test-xlsx')
# async def test_excel():

#     # form=await read_config(
#     #     request=request,
#     #     action='search',
#     #     config=config,
#     #     script='stat_tool',
#     #     R=R
#     # )
#     return await save_excel()
