from fastapi import APIRouter #, File, UploadFile, Form, Depends
from lib.all_configs import read_config
from lib.CRM.form.get_values_for_select_from_table import get_values_for_select_from_table
import traceback

router = APIRouter()
@router.post('/{config}')
async def get_list(config: str, R:dict): # 
    form=read_config(
        action='init',
        config=config,
        #id=exists_arg('id',arg),
        R=R,
        script='stat_tool'
    )
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
                f['values']=get_values_for_select_from_table(form, f)
                f['type']='select'

        response['title']=form.title
        response['filters']=filters
    else:
        success=False

    response['errors']=form.errors
    
    response['success']=success

    

    
    
    return response

    # insert into const()

# Поиск
@router.post('/{config}/search')
async def search(config: str, R: dict):
    form=read_config(
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
            """
                form.events.search возвращает блоки для вывода, которые выводятся на frontend-е
                success: True,
                list: [
                    { # раскрывающийся блок
                        'type':'accordion',
                        'data':[
                            {
                                'header':"
                                    Волков Павел Юрьевич
                                    <span style="color: green;">новых: 19</span> | <span style="color: red;">дублей: 6</span>
                                ",
                                'header_links':[
                                    # {'url':'sasa','style':'','header':'link1'},
                                    # {'url':'sasa','style':'','header':'link2'},
                                    # {'url':'sasa','style':'','header':'link3'},
                                ],
                                'content':[
                                    {
                                        'type':'html',
                                        'body':form.template('./confFas/transfere_result/template/table.html')
                                    },
                                    {
                                        'type':'html',
                                        'body':'hello2'
                                    },
                                ]
                            }
                        ]


                    },
                    {
                        'type':'html',
                        'body':'html-код для вывода'
                    },
                    {   # вложенный список (но это задел на будущее)
                        'type':'list',
                    }
                ]
            """
            return func(form, R)
        except Exception as e:
            error_info = traceback.format_exc()
            return {'success':False, 'errors':[f'ошибка приложения при выполнении события {search} ({e}) {error_info}']}
    else:
        return {'success':False, 'errors':[f'ошибка приложения при выполнении события {search} ({e})']}
