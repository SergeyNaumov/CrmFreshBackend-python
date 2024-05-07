from lib.core import exists_arg
#from .create_ofp_card import *
from .find_inn_doubles import prepare_filters_for_find_inn_doubles

async def permissions(form):
    R=form.R
    # превращаем инструмент в "поиск по ИНН"
    inn=exists_arg('cgi_params;find_inn_doubles',R)
    if inn:
      prepare_filters_for_find_inn_doubles(form,inn)

  
events={
  'permissions':permissions
}