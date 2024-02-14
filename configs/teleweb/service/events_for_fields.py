def photos_before_code(form,field):
    
    photo_fld=field['fields'][1]
    photo_fld['filedir']=f'./files/project_{form.s.shop_id}/good_photos'
    #form.pre(photo_fld)

def photos_after_save_code(form,field,data):
    #print("\n\nphotos_after_save_code")
    print("\n\n")
    print('id:',form.id)
    print('field:',field)
    print('data:',data)
    print('form.action:',form.action)
    print("\n\n")

    exists_main=form.db.query(
        query=f"select main from {field['table']} where {field['foreign_key']}=%s",
        values=[form.id],
        onevalue=1
    )

    if not exists_main:
        form.db.query(
            query=f"UPDATE {field['table']} SET main=1 where {field['foreign_key']}=%s order by sort limit 1",
            values=[form.id],
        )

    # делаем, чтобы основное фото было только одно
    
    if len(data)==1:
        d=data[0]
        if d['main']==1:
            form.db.query(
                query=f"UPDATE {field['table']} SET main=0 where {field['foreign_key']}=%s and id<>%s",
                values=[form.id,d['id']]
            )
events={
    'photos':{
        'before_code':photos_before_code,
        'after_save_code':photos_after_save_code
    },
}
