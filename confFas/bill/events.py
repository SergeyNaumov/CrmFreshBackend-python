from .get_values import get_values

def permissions(form):
    form.ov=None
    form.is_admin=True

    perm=form.manager['permissions']
    #form.pre(perm)
    if perm['admin_paids']:
        form.is_admin=True
        form.read_only=False
        form.make_delete=True
    
    if form.id:
        form.ov=get_values(form)

        if form.ov:
            form.title=f"Счёт №{form.ov['number']} от {form.ov['registered']}"

def before_search(form):
    # BEFORE SEARCH
    qs=form.query_search
    on_filters_hash=qs.get('on_filters_hash')
    if on_filters_hash and on_filters_hash.get('summ'):
        tables="\n".join(qs['TABLES'])
        where=''
        if len(qs['WHERE']):
            where='WHERE ' + ' AND '.join(qs['WHERE'])
        query=f"SELECT sum(wt.summ) from {tables} {where} GROUP BY wt.id"
        #form.pre(qs)
        #form.pre(query)
        bank=form.db.query(
            query=query,
            values=qs['VALUES'],
            onevalue=1
        )
        form.out_before_search.append(f"Итого: {bank} рублей")
        #form.pre({'bank':bank})



def after_save(form):
    form.nv=get_values(form)

    #print('nv:',form.nv)

events={
  'permissions':[
      permissions,
      
  ],
  'before_search':before_search,
  'after_save':after_save
  #'before_delete':before_delete,
  #'before_code':events_before_code
}