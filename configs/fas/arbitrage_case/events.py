from .get_values import get_values
from .after_search import after_search
from .permissions import permissions

def after_save(form):
    pass
    # form.nv=get_values(form)
    # #print('nv:',form.nv)

events={
  'permissions':[
      permissions,
      
  ],
  'after_search':after_search
  #'before_delete':before_delete,
  #'before_code':events_before_code
}