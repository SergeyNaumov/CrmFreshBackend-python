from datetime import datetime

def memo_before_out_tags(form,data):
    #print('data:',data)
    today=datetime.now().date()
    manager_id=form.manager.get('id')
    for d in data:
        # Если комментарий сегодняшний, то разрешаем его менять или удалять
        #print
        if (d['user_id']==manager_id) and (today==d['date'].date()):
            d['make_edit']=True
            d['make_delete']=True
        #print('d:',d)
fields=[
      
        {
            'description':'Менеджер',
            'name':'manager_id',
            'type':'select_from_table',
            'table':'manager',
            'tablename':'m',
            'header_field':'name',
            'value_field':'id',
            'tab':'sale',
            'read_only':True,
            'filter_on':True
        },
        {
            'description':'Группы менеджеров',
            'type':'filter_extend_select_from_table',
            'name':'f_manager_group',
            'table':'manager_group',
            #'tree_use':True,
            'tablename':'mg',
            'header_field':'header',
            'value_field':'id'
        },
        {
            'description':'Дата контакта',
            'name':'contact_date',
            'type':'date',
            'tab':'sale',
        },
        { # Memo
            # Комментарий 
            'description':'Состояние',
            'name':'memo',
            'type':'memo',
            'memo_table':'user_memo',
            'memo_table_id':'id',
            'memo_table_comment':'body',
            'memo_table_auth_id':'manager_id',
            'memo_table_registered':'registered',
            'memo_table_foreign_key':'user_id',
            'auth_table':'manager',
            'auth_login_field':'login',
            'auth_id_field':'id',
            'auth_name_field':'name',
            'reverse':1,
            'memo_table_alias':'memo',
            'auth_table_alias':'m_memo',
            'make_delete':False,
            'make_edit':True,
            'tab':'sale',
            'before_out_tags':memo_before_out_tags,
            'show_type':'html'
        },
        {
            'description':'Состояние2',
            'name':'state2',
            'type':'textarea',
            'tab':'sale'
        },
        # {
        #     'description':'ОТК',
        #     'name':'otk',
        #     'type':'checkbox',
        #     'read_only':True,
        #     #'before_code':otk_before_code,
        #     'tab':'sale',
        # },
        # {
        #     'description':'ДТ2',
        #     'name':'dt2',
        #     'type':'checkbox',
        #     'read_only':True,
        #     #'before_code':dt2_before_code,
        #     'tab':'sale',
        # },
        {
            'description':'Презентация заявки',
            'name':'prez_order',
            'type':'checkbox',
            'tab':'sale',
        },
        {
            'description':'Презентация заявки, отмена',
            'name':'prez_order_cancel',
            'type':'checkbox',
            'tab':'sale',
        },
]