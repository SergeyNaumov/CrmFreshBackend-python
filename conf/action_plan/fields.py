from lib.engine import s
#from lib.core import exists_arg, date_to_rus
#from .header_before_code import header_before_code
#from .good_categories import good_categories
#from .good_categories2 import good_categories2 
from .pr_bonus import pr_bonus
def get_fields():
    return [ 
    {
      'name':'header',
      'description':'Данные по прогнозному бонусу',
      'type':'code',
      'code':pr_bonus,
      'read_only':1,
      'filter_on':1,
      'tab':'main',
    },
]