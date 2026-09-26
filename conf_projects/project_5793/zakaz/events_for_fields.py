
def user_id_filter_code(form,field,row):

    if row['u__id']:
        #form.pre(row)
        return f"@{row['u__username']} {row['u__first_name']} {row['u__last_name']} {row['u__phone']}"
    else:
        return ''

def user_id_before_code(form,field):
    if hasattr(form, 'bot'):
        field['where']=f'bot_id={form.bot["id"]}'
    else:
        form.errors.append('к Вашему проекту не привязае бот')
    #if form.script=='find_results'
    if form.script=='find_objects':
        field['header_field']='username'

def goods_before_code(form,field):
    if not(form.script=='edit_form' and form.id):
        return

    project_id=form.s.project_id

    good_list=form.db.query(
        query=f"""
            SELECT 
                zg.*, g.header, g.artikul
            from
                struct_{project_id}_zakaz_good zg
                left JOIN struct_{project_id}_good g ON g.id=zg.good_id
            where zg.zakaz_id={form.id}
        """)
    total_price=0
    for g in good_list:
        total_price+=g['price']*g['cnt']
    

    field['after_html']=form.template(
        filename=f'conf_projects/project_{form.s.project_id}/zakaz/goods.html',
        good_list=good_list,
        total_price=total_price
    )

events={
    'user_id':{
        'before_code':user_id_before_code,
        'filter_code':user_id_filter_code,
    },
    'goods':{
        'before_code':goods_before_code,
    }
}