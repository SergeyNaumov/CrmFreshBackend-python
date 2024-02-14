def permissions(form):
    form.ov=None
    
    if form.id:
        ov=form.db.query(
            query=f'''
                SELECT 
                  u.id,u.firm, m.name m__name,mg.header mg__header,
                  if(bc.id is not null,1,0) exists_card
                from
                  user u
                  left join buhgalter_card bc ON (bc.id=u.id)
                  left join manager m ON (m.id=u.manager_id)
                  left join manager_group mg ON (m.group_id=mg.id)
                where u.id={form.id}
            ''',
            onerow=1
        )
        if ov and not(ov['exists_card']):
            form.db.save(
                table='buhgalter_card',
                data={'id':form.id}
            )
        form.ov=ov
        #form.pre(form.ov)




events={
  'permissions':[
      permissions,
      
  ],
  #'before_delete':before_delete,
  #'before_code':events_before_code
}