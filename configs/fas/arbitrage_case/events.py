from .get_values import get_values
from .after_search import after_search
from .permissions import permissions


events={
  'permissions':[
      permissions,
      
  ],
  'after_search':after_search
  #'before_delete':before_delete,
  #'before_code':events_before_code
}