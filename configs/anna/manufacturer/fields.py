



def get_fields():
    return [ 

    {
      'name':'header',
      'description':'Наименование',
      'type':'text',
      'filter_on':1
    }, 
    {
      'name':'contractor_id',
      'description':'Поставщик',
      'type':'select_from_table',
      'table':'contractor',
      'header_field':'header',
      'value_field':'id',
      'tablename':'c',
      'default_off':1,
      'filter_on':1
    },


]
