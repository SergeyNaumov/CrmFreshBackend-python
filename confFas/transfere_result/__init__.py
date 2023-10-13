from lib.core import cur_date, exists_arg

# получаем комментарии для списка
def get_comments(form,lst):
    ids=[]
    for u in lst: ids.append(str(u['id']))
    #print('ids:',ids)
    comments={}

    if len(ids):
        comments_list=form.db.query(
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
                './confFas/transfere_result/template/comments.html',
                list=comments[u['id']]
            )
        
    
    else:
        return ''


# Возвращает таблицу компаний для менеджера
def get_table_for_manager(form, _type, manager_id, ts):
    lst=form.db.query(
        query=f"""
            SELECT
                u.id, u.firm, u.inn, c.name city, u.contact_date,
                '' comment
            FROM
                transfere_result tr
                JOIN user u ON tr.user_id = u.id
                LEFT JOIN city c ON c.city_id = u.city_id
            WHERE
                tr.type=%s and tr.ts>=%s and tr.ts<=%s and tr.manager_id=%s
        """,
        values=[_type, f"{ts} 00:00:00",f"{ts} 23:59:59",manager_id],
        debug=1

    )
    get_comments(form, lst)
    #print('lst:',lst)
    

    return form.template('./confFas/transfere_result/template/table.html',list=lst)
def search(form, R):
    #R['cgi_params']['type']='43'
    try:
        _type=int(exists_arg('cgi_params;type',R))
    except Exception as e:
        return {'success':False,'errors':[str(e)]}
    if _type in (5,6):
        where=[f""]
        ts=exists_arg('filters;ts',R)

        
        lst=form.db.query(
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
        for m in lst:
            accordion_data.append({
                "header":form.template(
                    filename='./confFas/transfere_result/template/accordion_header.html', **m
                ),
                #"header_links":[{'url':'sasa','style':'','header':'link1'}],
                'not_container':True,
                "content":[
                    {
                        'type':'html',

                        'body': get_table_for_manager(form, _type,  m['id'], ts)
                    }
                ]
            })
            #print('accordion_data:',accordion_data)

        
        return {
            'success':True,
            'errors':[],
            'list':[

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
                # {
                #     'type':'html',
                #     'body':'html-код для вывода'
                # },

            ]
        }
    else:
        return {'success':False, 'errors':['Ошибка при поиске (неверный type)']}
    

def permissions(form):
    for f in form.filters:
        if f['name']=='ts':
            f['value']=cur_date()
    

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
      


