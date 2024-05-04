from .query_search_tables import get_query_search_tables
from lib.core import exists_arg

def permissions(form):
    form.QUERY_SEARCH_TABLES=get_query_search_tables()

    entity = exists_arg('cgi_params;entity',form.R)

    if entity=='11':
        form.title='Ответчики РегРФ'
    elif entity=='12':
        form.title='Ответчики НС "Ревизор"'
    elif entity=='13':
        form.title='Ответчики BzInfo'
    elif entity=='20':
        form.title='Ответчики FAS'
    elif entity=='24':
        form.title='Ответчики AUZ'
    else:
        entity=''

    if entity:
        login=form.manager['login']
        if login in ('akulov','pzm','sed','anna','admin'):
            form.search_links.append({
              'link':f"/vue/admin_table/assignment?entity={entity}",
              'description':"Менеджеры для распределения",
              'target':f'assignment{entity}'
            })


        add_qs=[
            {'t':'transfere_result','a':'tr', 'l':f'tr.parent_id = wt.id and tr.type={entity}','lj':1},
            {'t':'manager','a':'m','l':'tr.manager_id=m.id','lj':True},
            {'t':'user','a':'u','l':'tr.user_id=u.id','lj':True}
        ]
        for qs in add_qs:
            form.QUERY_SEARCH_TABLES.append(qs)



    # form.ov=None
    # form.is_admin=True

    # perm=form.manager['permissions']
    # #form.pre(perm)
    # if perm['admin_paids']:
    #     form.is_admin=True
    #     form.read_only=False
    #     form.make_delete=True

    # if form.id:
    #     form.ov=get_values(form)

    #     if form.ov:
    #         form.title=f"Акт №{form.ov['number']} от {form.ov['registered']}"
