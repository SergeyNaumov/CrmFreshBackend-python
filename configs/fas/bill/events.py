from lib.core import get_triade, join_ids
from .get_values import get_values

async def permissions(form):
    form.ov=None
    form.is_admin=False

    perm=form.manager['permissions']
    #form.pre(perm)
    if perm['admin_paids']:
        form.is_admin=True
        form.read_only=False
        form.make_delete=True
    
    # if form.manager['login']=='buh':
    #     form.explain=True
    #     form.pre(form.manager)
    if form.id:
        form.ov=await get_values(form)

        if form.ov:
            form.title=f"Счёт №{form.ov['number']} от {form.ov['registered']}"


async def before_search(form):
    # BEFORE SEARCH
    qs=form.query_search
    manager=form.manager ; perm=manager['permissions']

    #form.pre(perm)
    on_filters_hash=qs.get('on_filters_hash')

    if not(perm.get('admin_paids') or perm.get('view_all_paids') or form.is_admin):
        
        # если это не менеджер платежей и не админ
        if manager['is_owner'] and len(manager['CHILD_GROUPS']):
            # Руководитель
            group_ids=join_ids(manager['CHILD_GROUPS'])
            qs['WHERE'].append(f"(m.group_id in ({group_ids}) )")

        else:
            # Менеджер
            manager_id=manager['id']
            qs['WHERE'].append(f"(wt.manager_id={manager_id})")

    #form.pre(qs)
    if on_filters_hash and 'paid_summ' in on_filters_hash:
        tables="\n".join(qs['TABLES'])
        where=''
        if len(qs['WHERE']):
            where='WHERE ' + ' AND '.join(qs['WHERE'])
        query=f"SELECT sum(wt.paid_summ) from {tables} {where}"
        #form.pre(qs)
        #form.pre(query)
        bank=await form.db.query(
            query=query,
            values=qs['VALUES'],
            onevalue=1
        )
        if bank or bank==0:
            form.out_before_search.append(f"Итого: {get_triade(bank)} рублей")
        #form.pre({'bank':bank})



async def after_save(form):
    form.nv=await get_values(form)

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