from lib.core import exists_arg
from .create_ofp_card import *
def permissions(form):
  
  R=form.R
  db=form.db

  # Смотрим, какой бренд у данного менеджера
  manager_group=db.query(
    query="select * from manager_group where id=%s",
    values=[381], # form.manager['group_id']
    onerow=1
  )
  manager_brand=None
  if manager_group and manager_group['brand_id']:
      manager_brand=manager_group['brand_id']
  
  
  perm=form.manager['permissions']

  if form.script=='edit_form':
    form.ov={}
    if form.id:

      form.ov=db.query(
        query=f"SELECT * from user where id={form.id}",
        onerow=1
      )
      if form.ov:
        form.title=form.ov['firm']
      # Создание карты ОФП
      #form.pre(exists_arg('cgi_params;action',R))
      if exists_arg('cgi_params;action',R) == 'create_ofp_card':
          create_ofp_card(form)
      
      
      # В карте выбран брэнд
      if form.ov['brand_id'] and not( perm.get('user_show_all_brand') ) and form.ov['brand_id'] != manager_brand:
        form.errors.append('Вам запрещено просматривать данную карту (Вы работаете в рамках другого бренда)')

      form.read_only=0
events={
  'permissions':permissions
}