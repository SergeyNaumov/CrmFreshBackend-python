from .dp.get_bills import get_bills
from .dp.get_acts import get_acts
from .dp.ur_lico_list import ur_lico_list
from .dp.number_rules import *


# def get_acts(form,field,R):
#     return [
#             {
#                 'id':1,
#                 'link':f'/edit_form/act/1',
#                 'header':'Акт №П008/191223 от 10.12.2023 (25000 руб)'
#             }
#     ]


fields=[{
  'type':'docpack',
  'name':'docpack',
  'tab':'docpack',
  'not_filter':1,
  'docpack_foreign_key':'user_id',
  'dogovor_number_rule':dogovor_number_rule,
  'bill_number_rule':bill_number_rule,
  'act_number_rule':act_number_rule,
  'ur_lico_list': ur_lico_list,
  'get_bills':get_bills,
  'get_acts': get_acts

}]