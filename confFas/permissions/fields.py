def get_fields():
    return [ 
          {
              'description':'Наименование',
              'name':'header',
              'type':'text',
              'filter_on':1
          },
          {
              'description':'Ключевое название',
              'name':'pname',
              'type':'text',
              'filter_on':1,
              'uniquew':1,

          }
      ]