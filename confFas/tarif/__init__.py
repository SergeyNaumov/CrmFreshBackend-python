ur_lico_filedir='files/tarif'

form={
    'work_table':'tarif',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Тарифы',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'fields': [ 
        {
          'description':'Вкл',
          'type':'checkbox',
          'name':'enabled',
          'value':1
        },
        {
          'description':'С НДС',
          'type':'checkbox',
          'name':'with_nds',
        },
        {
          'description':'Название тарифа',
          'name':'header',
          'type':'text',


        },
        {
          'description':'Кол-во дней',
          'name':'count_days',
          'type':'text'
        },
        {
          'description':'Кол-во заявок',
          'name':'cnt_orders',
          'type':'text'
        },
        {
          'description':'Бланк для договора',
          'table':'blank_document',
          'tablename':'bd_d',
          'type':'select_from_table',
          'header_field':'header',
          'value_field':'id',
          'name':'blank_dogovor_id',
          #regexp=>'^\d+$',
          'regexp_rules':[
            '/^\d+$/','Выберите бланк для договора',
          ],
        },
        {
          'description':'Бланк для счёта',
          'table':'blank_document',
          'tablename':'bd_b',
          'type':'select_from_table',
          'header_field':'header',
          'value_field':'id',
          'name':'blank_bill_id',
          'regexp_rules':[
            '/^\d+$/','Выберите бланк для счёта',
          ],

        },

        {
          'description':'Бланк для акта',
          'table':'blank_document',
          'tablename':'bd_a',
          'type':'select_from_table',
          'header_field':'header',
          'value_field':'id',
          'name':'blank_act_id',
          #'regexp_rules':[
          #  '/^\d+$/','Выберите бланк для акта',
          #],
        },
        {
          'description':'Бланк для счёт-фактуры',
          'table':'blank_document',
          'tablename':'bd_f',
          'type':'select_from_table',
          'header_field':'header',
          'value_field':'id',
          'name':'blank_billfact_id',
        },
        {
          'description':'Стоимость тарифа',
          'name':'summ',
          'type':'text',
        },
        {
          'name':'comment',
          'description':'Примечание к тарифу',
          'type':'textarea'
        },
  ]  
    
}
      


