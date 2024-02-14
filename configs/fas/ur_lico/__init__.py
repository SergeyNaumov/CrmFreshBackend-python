ur_lico_filedir='files/ur_lico'

form={
    'work_table':'ur_lico',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Юридические лица',
    'sort':True,
    'tree_use':True,
    'explain':False,
    'header_field':'url',
    'default_find_filter':'header',
    'cols':[
        [
            {'description':'Реквизиты','name':'main','hide':False}
        ],
        [
            {'description':'Настройки','name':'addon','hide':False},
            #{'description':'Дополнительные соглашения','name':'dop_sogl'},
        ],
    ],
    
    'fields': [ 
    {
      'description':'Доступно всем',
      'name':'for_all',
      'type':'checkbox',
      'tab':'addon'
    },
    {
      'description':'Префикс для документов',
      'type':'text',
      'name':'prefix',
      'regexp_rules':[
          '/^.+?$/i','Необходимо указать префикс',
      ],
      'tab':'main'
    },
    {
      'description':'Могут выставлять только',
      'type':'1_to_m',
      'name':'ur_lico_access_only',
      'table':'ur_lico_access_only',
      'table_id':'id',
      
      'foreign_key':'ur_lico_id',
      'fields':[
        {
          'description':'Сотрудник',
          'type':'select_from_table',
          'table':'manager',
          'header_field':'name',
          'value_field':'id',
          #'autocomplete':1,
          'name':'manager_id'
        }
      ],
      'tab':'addon'
    },
    # {
    #   'description':'Нумерация в связке с ',
    #   'name':'order_num_ur_lico',
    #   'type':'select_from_table',
    #   'table':'ur_lico',
    #   'header_field':'firm',
    #   'value_field':'id',
    #   not_filter=>1,
    #   'tab':'addon'
    # },
    # {
    #   'description':'Прежние реквизиты',
    #   'type':'1_to_m',
    #   'name':'ur_lico_old_owner',
    #   'table':'ur_lico_old_owner',
    #   'table_id':'id',
    #   'foreign_key':'ur_lico_id',
    #   'view_type':'list',
    #   'fields':[
    #         {
    #           'description':'С','name':'from_date','type':'date'
    #         },
    #         {
    #           'description':'По','name':'to_date','type':'date'
    #         },
    #         {
    #           'description':'ФИО ген. дир (в именительном падеже)',
    #           'name':'gen_dir_fio_im',
    #           'type':'text'
    #         },
    #         {
    #           'description':'ФИО ген. дир (в родительном падеже)',
    #           'name':'gen_dir_fio_rod',
    #           'type':'text'
    #         },

    #         {
    #           'description':'ФИО гл.буха (в именит. падеже)',
    #           'name':'buh_fio_im',
    #           'type':'text'
    #         },
    #         {
    #           'description':'ФИО гл.буха (в род. падеже)',
    #           'name':'buh_fio_rod',
    #           'type':'text'
    #         },
    #         {
    #           'description':'Печать+подпись',
    #           'name':'attach',
    #           'type':'file',
    #           'filedir':'./files/ur_lico'
    #         },
    #         {
    #           'description':'Печать',
    #           'name':'attach_pechat',
    #           'type':'file',
    #           'filedir':'./files/ur_lico'
    #         },
    #         {
    #           'description':'Подпись ген. директора',
    #           'name':'gendir_podp',
    #           'type':'file',
    #           'filedir':'./files/ur_lico'
    #         },
    #         {
    #           'description':'Подпись гл. бухгалтера',
    #           'name':'buh_podp',
    #           'type':'file',
    #           'filedir':'./files/ur_lico'
    #         },
    #   ],
    #   'tab':'main'
    # },
    # {
    #   name => 'header',
    #   description => 'Название в списке юрлиц',
    #   type => 'text',
    #   'filter_on':1
    # },
    {
        'name':'firm',
        'description':'Название организации',
        'type':'text',
        'filter_on':1,
        'tab':'main'
    },
    {
      'description':'Комментарий',
      'name':'comment',
      'type':'text',
      'filter_on':1,
      'tab':'addon'
    },
    {
      'description':'Сообщение в бланке счёта',
      'name':'warn_for_bill',
      'type':'text',
      'filter_on':1,
      'tab':'addon'

    },
    {
      'description':'С НДС',
      'name':'with_nds',
      'type':'checkbox',
      'tab':'addon'
    },
    {
      'description':'Размер НДС в %',
      'add_description':'для детализации',
      'name':'nds',
      'type':'text',
      #regexp=>'\d+',
      'tab':'main'
    },
    {
      'description':'Без НДС с',
      'name':'without_nds_dat',
      'type':'date',
      # code=>sub{
      #   my $e=shift;
      #   $e->{field}.=q{
      #     <p><small>
      #       В случае, если не включена галочка "С НДС" -- всегда считается, что компания без НДС.<br>
      #       Если включена галочка "С НДС" и выбрана дата "Без НДС с", тогда компания считается как без НДС-ная, начиная с указанной даты<br>
      #       (счёт-фактура выводится только для актов, которые были выставлены ранее чем дата "Без НДС с")
      #     </small></p>
      #   }
      # },
      'tab':'addon'
    },
    {
      'description':'Адрес',
      'name':'address',
      'type':'textarea',
      'tab':'main'
    },
    {
      'description':'Юр.Адрес',
      'name':'ur_address',
      'type':'textarea',
      'tab':'main'
    },
    {
      'description':'ФИО ген. дир (в именительном падеже)',
      'name':'gen_dir_fio_im',
      'type':'text',
      'tab':'main'
    },
    {
      'description':'ФИО ген. дир (в родительном падеже)',
      'name':'gen_dir_fio_rod',
      'type':'text',
      'tab':'main'
    },
    {
      'description':'Фамилия И. О. Фамилия директора (кратко)',
      'name':'gen_dir_f_in',
      'type':'text',
      'tab':'main'
    },
    {
      'description':'ФИО гл.буха (в именит. падеже)',
      'name':'buh_fio_im',
      'type':'text',
      'tab':'main'
    },
    {
      'description':'ФИО гл.буха (в род. падеже)',
      'name':'buh_fio_rod',
      'type':'text',
      'tab':'main'
    },
    {
      'description':'ИНН',
      'name':'inn',
      'type':'text',
      'tab':'main'
    },

    {
      'description':'ОГРН',
      'name':'ogrn',
      'type':'text',
      'tab':'main'
    },
    {
      'description':'КПП',
      'name':'kpp',
      'type':'text',
      'tab':'main'
      
    },
    {
      'description':'р/с',
      'name':'rs',
      'type':'text',
      'tab':'main'
      
    },
    {
      'description':'к/с',
      'name':'ks',
      'type':'text',
      'tab':'main'
    },
    {
      'description':'БИК',
      'name':'bik',
      'type':'text',
      'tab':'main'
    },
    {
      'description':'Банк',
      'name':'bank',
      'type':'text',
      'tab':'main'
    },
    {
      'description':'Печать+подпись',
      'name':'attach',
      'type':'file',
      'filedir':'./files/ur_lico',
      'tab':'main'
    },
    {
      'description':'Печать',
      'name':'attach_pechat',
      'type':'file',
      'filedir':'./files/ur_lico',
      'tab':'main'
    },
    {
      'description':'Подпись ген. директора',
      'name':'gendir_podp',
      'type':'file',
      'filedir':'./files/ur_lico',
      'tab':'main'
    },
    {
      'description':'Подпись гл. бухгалтера',
      'name':'buh_podp',
      'type':'file',
      'filedir':'./files/ur_lico',
      'tab':'main'
    },
    {
      #'before_code': permissions_before_code,
      'description':'Доступно только для брендов',
      'type':'multiconnect',
      #'tree_use':1,
      'cols':2,
      'tree_table':'brand',
      'name':'for_brands',
      'tablename':'p',
      'relation_table':'brand',
      'relation_save_table':'ur_lico_brand',
      'relation_table_header':'header',
      'relation_save_table_header':'header',
      'relation_table_id':'id',
      'relation_save_table_id_worktable':'ur_lico_id',
      'relation_save_table_id_relation':'brand_id',
      'tab':'addon',
      #'not_order':1,
      #'read_only':1
    },
    #{
    #  'name':'edo_id',
    #  'description':'ЭДО',
    #  'type':'checkbox',
    #  'tab':'addon'
    #},
    # { # Доп. соглашения
    #   'description':'',
    #   'name':'dop_sogl',
    #   'table':'ur_lico_dop_sogl',
    #   'type':'1_to_m',
    #   'table_id':'id',
    #   'foreign_key':'ur_lico_id',
    #   'fields':[
    #     {
    #       'description':'Название',
    #       'type':'text',
    #       'name':'header'
    #     },
    #     {
    #       'description':'Номер внутри юр. лица',
    #       'type':'text',
    #       'name':'num'
    #     },
    #     {
    #       'description':'Шаблон',
    #       'type':'file',
    #       'name':'attach',
    #       'filedir':'./files/ur_lico'
    #     }
    #   ],
    #   'tab':'dop_sogl'

    # }
    ]  
    
}
      


