from lib.core import cur_date, exists_arg

# получаем комментарии для списка
async def get_comments(form,lst):
    ids=[]
    for u in lst: ids.append(str(u['id']))
    #print('ids:',ids)
    comments={}

    if len(ids):
        comments_list=await form.db.query(
                query=f"""
                    SELECT
                        memo.user_id, memo.registered ts, m.name, memo.body 
                    FROM
                        user_memo memo
                        LEFT JOIN manager m ON memo.manager_id = m.id
                    WHERE memo.user_id in ({ ','.join(ids)  })
                    ORDER BY memo.registered desc
                """
        )
        #print('comments_list:',comments_list)
        for c in comments_list:
            
            if not(c['user_id'] in comments):
                comments[c['user_id']]=[]

            comments[c['user_id']].append({'ts':c['ts'], 'name': c['name'], 'body': c['body']})
        
        for u in lst:
            #print(f"u: {u}\ncomments: { comments[u['id']] }\n\n")
            u['comment']=form.template(
                './conf/transfere_result/template/comments.html',
                list=comments[u['id']]
            )
        
    
    else:
        return ''


# Возвращает таблицу компаний для менеджера
async def get_table_for_manager(form, _type, manager_id, ts):
    lst=await form.db.query(
        query=f"""
            SELECT
                u.id, u.firm, u.inn, c.name city, u.contact_date,
                '' comment, r.header region
            FROM
                transfere_result tr
                JOIN user u ON tr.user_id = u.id
                LEFT JOIN region r ON r.region_id=u.region_id
                LEFT JOIN city c ON c.city_id = u.city_id
            WHERE
                tr.type=%s and tr.ts>=%s and tr.ts<=%s and tr.manager_id=%s
        """,
        values=[_type, f"{ts} 00:00:00",f"{ts} 23:59:59",manager_id],

    )
    await get_comments(form, lst)
    #print('lst:',lst)
    

    return form.template('./conf/transfere_result/template/table.html',list=lst)
async def search(form, R):
    #R['cgi_params']['type']='43'
    try:
        _type=int(exists_arg('cgi_params;type',R))
    except Exception as e:
        return {'success':False,'errors':[str(e)]}
    if _type>=5 and _type<=24:
        where=[f""]
        ts=exists_arg('filters;ts',R)

        
        lst=await form.db.query(
            query="""SELECT
                m.id, m.name, sum(if(tr.is_double=0,1,0)) new, sum(if(tr.is_double,1,0)) doubles
            FROM
                transfere_result tr
                LEFT JOIN manager m ON m.id=tr.manager_id
            WHERE
                tr.type=%s and tr.ts>=%s and tr.ts<=%s
            GROUP BY tr.manager_id
            ORDER BY m.name""",
            values=[_type, f"{ts} 00:00:00",f"{ts} 23:59:59",],
            #debug=1,
            #error=form.errors
        )
        #print(query)
        accordion_data=[]
        total_leads=0
        for m in lst:
            total_leads+=m['doubles']+m['new']
            accordion_data.append({
                "header":form.template(
                    filename='./conf/transfere_result/template/accordion_header.html', **m
                ),
                #"header_links":[{'url':'sasa','style':'','header':'link1'}],
                'not_container':True,
                "content":[
                    {
                        'type':'html',

                        'body': await get_table_for_manager(form, _type,  m['id'], ts)
                    }
                ]
            })
            #print('accordion_data:',accordion_data)

        result_list=[]
        if len(accordion_data):
            if total_leads:
                result_list.append({
                    'type':'html',
                    'body':f"<p><b>Всего лидов:</b> {total_leads}</p>"}
                )
            result_list.append(
                { # раскрывающийся блок
                    'type':'accordion',
                    'data': accordion_data
                    # [
                    #     {
                    #         'header':"""
                                
                    #         """,
                    #         'header_links':[
                    #             # {'url':'sasa','style':'','header':'link1'},
                    #             # {'url':'sasa','style':'','header':'link2'},
                    #             # {'url':'sasa','style':'','header':'link3'},
                    #         ],
                    #         'content':[
                    #             {
                    #                 'type':'html',
                    #                 'body':form.template('./confFas/transfere_result/template/table.html')
                    #             },
                    #             {
                    #                 'type':'html',
                    #                 'body':'hello2'
                    #             },
                    #         ]
                    #     }
                    # ]


                },
            )
        return {
            'success':True,
            'errors':[],
            'list':result_list
        }
    else:
        return {'success':False, 'errors':['Ошибка при поиске (неверный type)']}
    

async def permissions(form):
    
    _type=exists_arg('cgi_params;type',form.R)
    if _type.isnumeric():
        _type=int(_type)
        #print('R:',form.R)
        if(_type==6):
            form.title='Статистика по уклонениям (РегРФ)'
        elif(_type==5):
            form.title='Статистика по расторжениям (РегРФ)'

        elif(_type==8):
            form.title='Статистика по расторжениям (Ревизор)'
        elif(_type==9):
            form.title='Статистика по уклонениям (Ревизор)'
        elif(_type==10):
            form.title='Статистика РНП (Ревизор)'
        elif(_type==11):
            form.title='Статистика по ответчикам (РегРФ)'
        elif(_type==12):
            form.title='Статистика по ответчикам (Ревизор)'
        elif(_type==13):
            form.title='Статистика по ответчикам (BzInfo)'
        elif(_type==14):
            form.title='Статистика по расторжениям (BzInfo)'
        elif(_type==15):
            form.title='Статистика по уклонениям (BzInfo)'
        elif(_type==16):
            form.title='Статистика РНП (BzInfo)'

        elif(_type==17):
            form.title='Статистика по уклонениям (ФАС-сервис)'
        elif(_type==18):
            form.title='Статистика по расторжениям (ФАС-сервис)'

        elif(_type==7):
            form.title='Статистика РНП (РегРФ)'


        elif(_type==19):
            form.title='Статистика РНП (ФАС-сервис)'
        elif(_type==20):
            form.title='Статистика по ответчикам (ФАС-сервис)'
        elif(_type==21):
            form.title='Статистика по уклонениям (AUZ)'
        elif(_type==22):
            form.title='Статистика по расторжениям (AUZ)'
        elif(_type==23):
            form.title='Статистика РНП (АУЗ)'
        elif(_type==24):
            form.title='Статистика ответчикам (АУЗ)'
        for f in form.filters:
            if f['name']=='ts':
                f['value']=cur_date()
    else:
        form.errors.append('неизвестный type')
    

form={
    'title':'Отчёт расторжения',
    'filters':[
      {
        'description':'Дата распределения',
        'type':'date',
        'name':'ts', 
        'value':''
      }
    ],
    'events':{
        'permissions':permissions,
        'search':search
    }
    
}
      


