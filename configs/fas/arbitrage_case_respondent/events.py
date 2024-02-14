from .get_values import get_values
from .after_search import after_search
from .permissions import permissions

def after_save(form):
    pass
    # form.nv=get_values(form)
    # #print('nv:',form.nv)

def before_search(form):
  qs=form.query_search
  qs['SELECT_FIELDS'].append('group_concat(pl.name) plaintiff_names')
  qs['SELECT_FIELDS'].append('group_concat(distinct email.email) email, group_concat(distinct phone.phone) phone')
  #, group_concat(distinct email.email) email, group_concat(distinct phone.phone) phone, ')

events={
  'permissions':[
      permissions,
      
  ],
  'before_search':before_search,
  'after_search':after_search
  #'before_delete':before_delete,
  #'before_code':events_before_code
}