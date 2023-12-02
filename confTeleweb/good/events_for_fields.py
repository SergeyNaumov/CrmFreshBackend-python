def photos_before_code(form,field):
    
    photo_fld=field['fields'][1]
    photo_fld['filedir']=f'./files/project_{form.s.shop_id}/good_photos'
    #form.pre(photo_fld)

def photos_after_save_code(form,field,data=None):
    #print("\n\nphotos_after_save_code")
    #print('id:',form.id)
    #print('field:',field)
    #print('data:',data)
    exists_main=form.db.query(
        query=f"select main from {field['table']} where {field['foreign_key']}=%s",
        values=[form.id],
        onevalue=1
    )
    #print('exists_main:',exists_main)
    if not exists_main:
        form.db.query(
            query=f"UPDATE {field['table']} SET main=1 where {field['foreign_key']}=%s order by sort limit 1",
            values=[form.id],
        )

    if data and len(data)==1:
        d=data[0]
        if d['main']==1:
            form.db.query(
                query=f"UPDATE {field['table']} SET main=0 where {field['foreign_key']}=%s and id<>%s",
                values=[form.id,d['id']]
            )

dict_catalog_path={}
dict_catalog_name={}
def catalog_id_filter_code(form,field,row):
    global dict_catalog_path
    if result:=dict_catalog_path.get(row['wt__catalog_id']):
        #form.pre('from cache')
        return result

    if row['wt__catalog_id']:

        if not(row['c__id'] in dict_catalog_name):
            dict_catalog_name[row['c__id']]=row['c__header']

        path=f"{row['c__path']}/{row['c__id']}"

        result=[]
        for catalog_id in path.split('/'):
            #form.pre({'catalog_id':catalog_id})
            if catalog_id.isdigit():

                header=''
                if catalog_id in dict_catalog_name:
                    header=dict_catalog_name[catalog_id]

                else:
                    header=form.db.query(query="SELECT header from catalog where id=%s",values=[catalog_id],debug=1, onevalue=1)

                    if header:
                        dict_catalog_name['catalog_id']=header

                if header:
                    result.append(f"<a href='/manager/edit_form/catalog/{catalog_id}' target='_blank'>{header}</a>")

        if len(result):
            dict_catalog_path[row['wt__catalog_id']]=' / '.join(result)

            return ' / '.join(result)

    return '-'

def header_filter_code(form,field,row):
    shop=form.s.shop
    return f"{row['wt__header']}<br><small><a href='https://{shop['domain']}/good/{row['wt__id']}'>на сайте</a></small>"

events={
    'photos':{
        'before_code':photos_before_code,
        'after_save_code':photos_after_save_code
    },
    'header':{
        'filter_code':header_filter_code
    },
    'catalog_id':{
        'filter_code':catalog_id_filter_code
    }
}