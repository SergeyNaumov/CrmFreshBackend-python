from lib.core import join_ids
async def action_list(form,field):
        #field=form.fields_hash[field_name]
        
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
                    dp.{field['docpack_foreign_key']}={form.id}
                ORDER BY dp.id desc
            """,
            errors=form.errors
        )
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
            'list':lst
        };
