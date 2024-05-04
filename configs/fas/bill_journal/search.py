from lib.core import cur_date, exists_arg, join_ids
def search(form, R):
    #print('form:',form)
    col1=[]
    col2=[]
    filters=R['filters']
    city=filters.get('city')



    #print('R:',city)
    body=''
    db=form.db ; where='' ; values=[] ; w=['wt.paid=1']
    page=R.get('page') or 0
    if not(page) or not(page.isnumeric()):
        page=0

    perpage=20
    manager=form.manager
    perm=manager['permissions']
    if perm['admin_paids']:
        # для менеджера платажей нет ограничений
        ...
    elif manager.get('is_owner') and len(manager['CHILD_GROUPS']):
        # ограничение для руководителей
        w.append("m.group_id in ("+join_ids(manager['CHILD_GROUPS'])+")")

    else:
        # ограничение для менеджеров
        w.append("m.id=%s")
        values.append(manager['id'])


    period=exists_arg('filters;period',R)
    group_id_filter=exists_arg('filters;group_id',R)
    manager_id_filter=exists_arg('filters;manager_id',R)
    if group_id_filter and len(group_id_filter):
        w.append("m.group_id in ("+join_ids(group_id_filter)+")")

    if manager_id_filter and len(manager_id_filter):
        w.append("m.id in ("+join_ids(manager_id_filter)+")")

    if len(period)==2:
        if v:=period[0]:
            w.append('wt.paid_date>=%s')
            values.append(v)

        if v:=period[1]:
            w.append('wt.paid_date<=%s')
            values.append(v)

    if len(w):
        where='WHERE '+' AND '.join(w)

    query=f"""
        SELECT
            m.name, sum(wt.paid_summ) bank
        FROM
            bill wt
            join docpack dp ON wt.docpack_id = dp.id

            join manager m ON m.id=wt.manager_id


        {where}
        group by m.id
        order by m.name

    """
    count=0




    _list=db.query(
        query=query,
        #debug=1,
        values=values
    )
    total=0
    if len(_list):
        # Добавляем диаграмму в вывод
        chart_labels=[]
        chart_values=[]
        for l in _list:
            if l['bank']:
                total+=l['bank']
            chart_labels.append(f"{l['name']} - {l['bank']}" )
            chart_values.append(l['bank'])

        col1.append({
            'description':'Менеджеры',
            'width':500,
            'height':500,
            'legend_position':'bottom',
            'type':'chart',
            'subtype':'circle',
            'labels':chart_labels,
            'values':chart_values,
            'colors': [ '#E57373','#F06292','#9575CD', '#7986CB', '#64B5F6','#4FC3F7','#4FC3F7','#4DB6AC','#4DB6AC','#AED581']
        })
    #print("template:",f"./{form.s.config['config_folder']}/{form.config}/template/table.html")
    body=form.template(
        #'confFas/win_our_clients/template/table.html',
        f"./{form.s.config['config_folder']}/{form.config}/template/table.html",
        list=_list,
        total=total

    )
    #print('body:',body)


    col2.append(
        {
        'type':'html',
        'body': body
        }
    )

    return {
        'success':True,
        'errors':form.errors,
        'result_type':'columns',
        'columns':[col2,col1],
        'not_total_count': True
    }