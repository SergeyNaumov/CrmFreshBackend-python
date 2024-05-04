from lib.core import cur_date, exists_arg, join_ids
from fastapi.responses import FileResponse
import random, time
from openpyxl import Workbook
import os
def gen_tmpl_prefix():
    now=str(int(time.time()))
    return str(int(time.time())) + \
    '_' +  ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUV0123456780') for i in range(5))

def search(form, R):
    result_list=[]
    filters=R['filters']
    city=filters.get('city')



    #print('R:',city)
    body=''
    db=form.db ; where='' ; values=[] ; w=[]
    page=R.get('page') or 0
    if not(page) or not(page.isnumeric()):
        page=0

    perpage=20

    if city:


        city=city.strip()
        cityes=[]
        for city_id in db.query(
            query="select city_id from city where country_id=1 and name like %s",
            values=[city+'%'],massive=1 ):

            cityes.append(city_id)
        #print('city: ',city)

        #values.append(city+'%')
        if not len(cityes):
            cityes=[0]

        #print('cityes:',cityes)
        #if len(cityes):
        #   w.append(f"wt.city_id in ({join_ids(cityes)})")
        #   w.append(f"u.city_id in ({join_ids(cityes)})")

        where=' OR '.join(w)
        where=f"WHERE wt.product in (9,14,15) AND wt.win_status=1 and  (wt.city_id in ({join_ids(cityes)}) or u.city_id in ({join_ids(cityes)}) )"

    else:
        where="WHERE wt.product in (9,14,15) AND wt.win_status=1"


    query=f"""
        SELECT
            wt.teamwork_ofp_id id, wt.win_status, wt.firm, wt.inn, wt.regnumber,wt.pred_comm,
            if(me.id,me.name,'-') exhibitor,
            if(mf.id,mf.name,'-') manager,
            if(mt.id,mt.name,'-') manager_to,
            if(mt2.id,mt2.name,'-') manager_to2,
            if(m_oso.id,m_oso.name,'-') manager_oso,
            c.name city, c.name city2, wt.product,
            born
        FROM
            teamwork_ofp wt
            join user u ON u.id=wt.user_id
            LEFT join manager me ON wt.exhibitor_id=me.id
            LEFT JOIN manager mf ON wt.manager_from=mf.id
            LEFT JOIN manager mt ON wt.manager_to=mt.id
            LEFT JOIN manager mt2 ON wt.manager_to2=mt2.id
            LEFT JOIN manager m_oso ON wt.manager_oso=m_oso.id
            LEFT JOIN city c ON c.city_id=wt.city_id

        {where}
        order by teamwork_ofp_id desc

    """
    count=0
    saveto_xls= ( filters.get('format') == 2 )
    if saveto_xls:
        # Если мы сохраняем в xls

        # Готовим данные
        query+=' LIMIT 1000'
        data=[
            ['Компания','ИНН','Представитель','Юрист1','Юрист2','Юрист3','Город','Город заседания','Дата заседания','Вид продукта','Реестровый №','Председатель комиссии']
        ]
        for itt in db.query(query=query):

            if not(itt['born']):
                itt['born']=''
            itt['born']=str(itt['born'])

            d=[]
            for a in ('firm','inn','exhibitor','manager','manager_to','manager_to2','city','city2','born','product','regnumber','pred_comm'):
               if not itt[a]:
                itt[a]=''
               d.append(itt[a])

            data.append(d)

        #print(data)





        dirname='./files/tmp/win_our_clients/'
        if not os.path.exists(dirname):
            # создаём темповую директорию, если её нет
            os.makedirs(dirname)

        filename=f"{dirname}/{gen_tmpl_prefix()}.xlsx"

        wb = Workbook()
        ws = wb.active
        for d in data:
            ws.append(d)
        #ws[f'A1'] = 'hello'

        wb.save(filename)

        return {
            'success':True,
            'errors':[],
            'list':[
                {
                    'type':'html',
                    'body':f'Файл с отчётом Вы можете получить <a href="{filename.replace("./","/")}" download="Выгрузка_победы_наших_клиентов.xls">Здесь</a>'
                }
            ]
        }

    else:
        query+=f" LIMIT {page},{perpage}"

        query_count=f"SELECT count(*) from teamwork_ofp wt join user u ON u.id=wt.user_id {where}"
        count=db.query(
            query=query_count,
            values=values,
            onevalue=1

        )

        _list=db.query(
            query=query,
            #values=values
        )
        #print("template:",f"./{form.s.config['config_folder']}/{form.config}/template/table.html")
        body=form.template(
            #'confFas/win_our_clients/template/table.html',
            f"./{form.s.config['config_folder']}/{form.config}/template/table.html",
            list=_list,
            count=count
        )
        #print('body:',body)

        result_list.append({
            'type':'html',
            'body': body
        })
        return {
            'success':True,
            'errors':form.errors,
            'list':result_list
        }

    #R['cgi_params']['type']='43'
    # try:
    #     _type=int(exists_arg('cgi_params;type',R))
    # except Exception as e:
    #     return {'success':False,'errors':[str(e)]}
    # if _type in (5,6):
    #     where=[f""]
    #     ts=exists_arg('filters;ts',R)

        
    #     lst=form.db.query(
    #         query="""SELECT
    #             m.id, m.name, sum(if(tr.is_double=0,1,0)) new, sum(if(tr.is_double,1,0)) doubles
    #         FROM
    #             transfere_result tr
    #             LEFT JOIN manager m ON m.id=tr.manager_id
    #         WHERE
    #             tr.type=%s and tr.ts>=%s and tr.ts<=%s
    #         GROUP BY tr.manager_id
    #         ORDER BY m.name""",
    #         values=[_type, f"{ts} 00:00:00",f"{ts} 23:59:59",],
    #         #error=form.errors
    #     )
    #     #print(query)
    #     accordion_data=[]
    #     for m in lst:
    #         accordion_data.append({
    #             "header":form.template(
    #                 filename='./conf/transfere_result/template/accordion_header.html', **m
    #             ),
    #             #"header_links":[{'url':'sasa','style':'','header':'link1'}],
    #             'not_container':True,
    #             "content":[
    #                 {
    #                     'type':'html',

    #                     'body': get_table_for_manager(form, _type,  m['id'], ts)
    #                 }
    #             ]
    #         })
    #         #print('accordion_data:',accordion_data)

    #     result_list=[]
    #     if len(accordion_data):
    #         result_list.append(
    #             { # раскрывающийся блок
    #                 'type':'accordion',
    #                 'data': accordion_data
    #             },
    #         )

    

def permissions(form):
    ...

def city_autocomplete(form,field,R):
    term=R.get('term')
    print('term:',term)
    if term and len(term):
        return form.db.query(
            query='select name from city where name like %s order by name limit 20',
            values=[term+'%'],
            massive=1
        )
    else:
        return []


form={
    'title':'Победы наших клиентов',
    'work_table':'',
    'fields':[
      {
        'description':'Формат',
        'type':'select',
        'name':'format',
        'not_multiple':1,
        'values':[
            {'v':1,'d':'Показать результаты на экране'},
            {'v':2,'d':'Microsoft excel'},
        ],
        'value':1
      },
      {
        'description':'Город',
        'type':'text',
        'autocomplete':1,
        'name':'city',
        'ajax':{
            'autocomplete':city_autocomplete
        },
        'not_multiple':1,
        'value':''
      },
    ],

    'events':{
        'permissions':permissions,
        'search':search
    }
    
}
      


