def before_code_type(**arg):
  form=arg['form']
  field=arg['field']
  if not field['value']:
    field['value']='vue'


fields=[ 
      {
          'description':'Наименование пункта меню',
          'type':'text',
          'name':'header',
          'tab':'main'
      },
      {
        'description':'Тип элемента',
        'type':'select_values',
        'name':'type',
        # before_code':sub{
        #   my $e=shift;
        #   $e->{value}='vue' if(!$e->{value} && $form->{action}=~m/^(new|edit)$/); 
        # },
        'values':[
          {'v':'','d':'не выбрано'},
          {'v':'vue','d':'VUE'},
          {'v':'src','d':'internal_prog'},
          {'v':'link','d':'link'},
          {'v':'newtab','d':'newtab'},
        ],
        'tab':'main',
        'before_code':before_code_type

      },
      {
        'description':'Значение',
        'type':'text',
        'name':'value',
        'after_html':'<div>admin-table<br>admin-tree<br>const<br>parser-excel<br></div>',
        'values':[
          {'v':'admin-table','d':'admin-table'},
          {'v':'admin-tree','d':'admin-tree'},
          {'v':'const','d':'const'},
          {'v':'parser-excel','d':'parser-excel'},
          {'v':'documentation','d':'documentation'},
        ],
        'tab':'main'
      },
      {
        'description':'Иконка',
        'name':'icon',
        'type':'font-awesome',
        'tab':'advanced'
      },
      {
        'description':'Параметры запуска',
        'name':'params',
        'type':'textarea',
        # before_code':sub{
        #   my $e=shift;
        #   unless($e->{value}){
        #     $e->{value}=qq{{"config":""}}
        #   }
        # },
        'add_description':'для типа vue например: {"config":"manager"}',
        'tab':'advanced'
      },
      {
        'name': 'permissions',
        'description ': 'Права доступа',
        'type': '1_to_m',
        'table': 'manager_menu_permissions',
        'table_id': 'id',
        'foreign_key': 'menu_id',
        'tab':'advanced',
        'fields ':
        [
          {
            'description':'Право доступа',
            'name':'permission_id',
            'type':'select_from_table',
            'order':'sort',
            #'tree_use':1,
            'table':'permissions',
            'value_field':'id',
            'header_field':'header',
          },
          {
            'description':'Если включено, то',
            'name':'denied',
            'type':'select_values',
            'values':[
              {'v':0,'d':'давать доступ'},
              {'v':1,'d':'запрещать доступ'}
            ]
          },
        ]
      },
]