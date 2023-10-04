def zakaz_info_before_code (form,field):
    if form.id:
        zakaz=form.db.query(
            query='select *, 0 total_price from zakaz where id=%s and shop_id',
            values=[form.id],
            onerow=1
        )
        
        if zakaz:
            user=None
            if zakaz['user_id']:
                user=form.db.query(
                    query='select * from user where id=%s',
                    values=[zakaz['user_id']],
                    onerow=1
                )

            zakaz_info= form.db.query(
                query='''
                    select
                        zi.cnt, zi.price,
                        g.header
                    from

                        zakaz_info zi
                        LEFT JOIN good g ON g.id=zi.good_id
                    where zi.zakaz_id=%s
                ''',
                values=[form.id],
                #onerow=1
            )
            
            if zakaz_info:
                for g in zakaz_info:
                    g['summ']=g['price']*g['cnt']
                    zakaz['total_price']+=g['summ']
            else:
                zakaz_info=[]
            #orm.pre(form.s)
            delivery=None
            if zakaz['delivery_id']:
                delivery=form.db.query(
                    query='select * from delivery where id=%s',
                    values=[zakaz['delivery_id']],
                    onerow=1

                )
            #form.pre(delivery)
            field['after_html']=form.template(
                './conf/zakaz/zakaz_info.html',
                zakaz=zakaz, 
                delivery=delivery,
                
                zakaz_info=zakaz_info,
                user=user
            )
        else:
            return 'нет данных о заказе'

def user_id_filter_code(form,field, row):
    #form.pre(row)
    return f"{row['u__first_name']} {row['u__last_name']} {row['u__phone']}"
events={
    #'photos':{
    #    'before_code':photos_before_code
    #},
    'zakaz_info':{
       'before_code':zakaz_info_before_code 
    },
    'user_id':{
        'filter_code':user_id_filter_code
    }
}