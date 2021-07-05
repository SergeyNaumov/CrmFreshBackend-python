



def get_fields():
    return [ 
    {
      'name':'attach',
      'description':'Файл',
      'filedir':'./files/bonus_order',
      'type':'file',
      #'read_only':1,
      'filter_on':1,
    },
    {
      'name':'ur_lico_id',
      'type':'select_from_table',
      'table':'ur_lico',
      'header_field':'header',
      'value_field':'value'
    }

]
