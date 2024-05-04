def before_code_type(form,field):
  #print('form:',form)
  #print('field:',field)
  if not 'value' in field or not field['value']:
    field['value']='vue'

form={
    'work_table':'manager_menu',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Меню системы',
    'sort':True,
    'tree_use':True,
    'max_level':2,
    'explain':False,
    'fields': [ 
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
          #'after_html':'<div>admin-table<br>admin-tree<br>const<br>parser-excel<br></div>',
          'values':[
            {'v':'admin-table','d':'admin-table'},
            {'v':'admin-tree','d':'admin-tree'},
            {'v':'const','d':'const'},
            {'v':'parser-excel','d':'parser-excel'},
            {'v':'documentation','d':'documentation'},
            {'v':'stat-tool','d':'stat-tool'},
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
          'description': 'Права доступа',
          'type': '1_to_m',
          'table': 'manager_menu_permissions',
          'table_id': 'id',
          'foreign_key': 'menu_id',
          'tab':'advanced',
          'fields':
          [
            {
              'description':'Право доступа',
              'name':'permission_id',
              'type':'select_from_table',
              'order':'sort',
              'tree_use':1,
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
    
}
      

