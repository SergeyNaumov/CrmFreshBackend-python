from lib.core import exists_arg
from .create_ofp_card import *
def permissions(form):
  
  R=form.R
  db=form.db

  
  
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
      
      form.read_only=0
events={
  'permissions':permissions
}