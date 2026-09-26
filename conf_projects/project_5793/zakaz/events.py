
#from lib.CRM.plugins.InExtUrl import InExtUrl
        
def permissions(form):
    if hasattr(form.s, 'project_id'):
        project_id=form.s.project_id

        form.work_table=f'struct_{project_id}_zakaz'
        print('zakaz/work_table: ',form.work_table )
        form.QUERY_SEARCH_TABLES=[
            {'t':form.work_table,'a':'wt'},
            {'t':'bot_user','a':'u','l':'wt.user_id=u.id','lj':1},
            {'t':f'struct_{project_id}_delivery','a':'d','l':'d.id=wt.delivery_id','lj':1},
            {'t':f'struct_{project_id}_paid','a':'p','l':'p.id=wt.paid_id','lj':1},
        ]
        delivery_field=form.get_field('delivery_id')
        delivery_field['table']=f'struct_{project_id}_delivery'

        paid_field=form.get_field('paid_id')
        paid_field['table']=f'struct_{project_id}_paid'

        form.bot=form.db.query(
            query=f"select * from bot where project_id={project_id}",
            values=[],
            onerow=1,
            debug=1
        )

    else:
        form.errors('Ошибка! неизвестный project_id')


        
        
    if form.script=='edit_form' and form.id:
        form.ov=form.db.query(
            query=f"select * from {form.work_table} where {form.work_table_id}={form.id}",
            onerow=1
        )
        #form.pre(ov)

    # if form.script in ('admin_table','find_objects'):
    #     form.fields.append({
    #         'description':'Дата заказа',
    #         'type':'date',
    #         'read_only':1,
    #         'name':'registered',
    #         'filter_on':1
    #     })
            


events={
    'permissions':permissions
}