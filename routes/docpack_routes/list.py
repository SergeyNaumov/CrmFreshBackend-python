from lib.core import join_ids, exists_arg
async def action_list(form,field):
        #field=form.fields_hash[field_name]
        form_id=form.R.get('form_id_alternative',form.id)

        lst_where=f"dp.{field['docpack_foreign_key']}=%s"
        lst_values=[form_id]

        if only_dogovor:=form.R.get('only_dogovor'):
            lst_where+=f" and dp.id=%s"
            lst_values.append(only_dogovor)

        lst=await form.db.query(
            query=f"""
                select
                    dp.id, dp.ur_lico_id, dp.tarif_id, t.header tarif, ul.firm ur_lico, dp.registered, m.name manager,
                    if(ul.for_all or a.id is not null,1,0) make_new_bill
                from
                    docpack dp
                    LEFT join tarif t ON dp.tarif_id=t.id
                    LEFT join ur_lico ul ON (dp.ur_lico_id=ul.id)
                    LEFT JOIN ur_lico_access_only a ON (a.ur_lico_id=ul.id and a.manager_id={form.manager['id']}) 
                    LEFT JOIN manager m ON (m.id=dp.manager_id)
                WHERE
                    {lst_where}
                ORDER BY dp.id desc
            """,
            values=lst_values,
            errors=form.errors
        )

        # Список услуг
        services=[]
        if service_table:=field.get('service_table'):
            serv_fields=[]
            services = await form.db.query(query=f"select id,header from {service_table} order by header")

            # доп. поля для услуг
            if field_table:=field.get('service_field_table'):
                serv_fields=await form.db.query(query=f"select * from {field_table} order by sort")

            for s in services:
                s['fields']=[]
                for f in serv_fields:
                    if s['id']==f['service_id']:
                        f['value']=''
                        s['fields'].append(f)



        #print(lst)
        id_list=[]
        for l in lst:
            id_list.append(l['id'])
        
        #print('id_list:',id_list)
        
        if len(id_list):
            
            query=f"select * from dogovor where docpack_id in ({join_ids(id_list)}) ORDER BY registered desc"
            
            dogovor_list = await form.db.query(
                query=f"select * from dogovor where docpack_id in ({join_ids(id_list)}) ORDER BY registered desc",
                #debug=1
            )
            #print('dogovor_list:',dogovor_list)
            
            for dp in lst:
                dp['cnt_bill'] = await form.db.query(
                    query='select count(*) from bill where docpack_id=%s',
                    values=[dp['id']],
                    errors=form.errors,
                    onevalue=1
                )
                #return {'dp':dp}
                dp['make_new_bill']=1
                dp['dogovor_list']=[]

                for d in dogovor_list:
                    d['show']=False
                    
                    if dp['id']==d['docpack_id']:
                        dp['dogovor_list'].append(d)

        #return {'ok':3}
        return {
            'success':form.success(),
            'errors':form.errors,
            'permissions':form.manager['permissions'],
            'list':lst,
            'services':services
        };
