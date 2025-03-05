



def get_fields():
    return [ 
    {
      'name':'header',
      'description':'Наименование',
      'type':'text',
      'filter_on':1
    },
    {
      'description':'Каталог бренда',
      'name':'catalog',
      'type':'1_to_m',
      'table':'brand_catalog',
      'table_id':'id',
      'foreign_key':'brand_id',
      'fields':[
        {
          'description':'Наименование раздела',
          'type':'text',
          'name':'header'
        }
      ]
    }

]
