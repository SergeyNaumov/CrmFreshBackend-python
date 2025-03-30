fields=[
    # {
    #   'description':'Юридическое лицо',
    #   'name':'ur_lico_id',
    #   'type':'select_from_table',
    #   'table':'ur_lico',
    #   'tablename':'ul',
    #   'header_field':'firm',
    #   'value_field':'id',
    #   'tab':'hr',
    # },
    {
      'description':'Должность',
      'type':'text',
      'name':'position',
      'tab':'hr'
    },
    # {
    #   'description':'День и месяц рождения',
    #   'add_description':'в формате DD/MM',
    #   'type':'text',
    #   'name':'born_date',
    #   'regexp_rules':[
    #       '/^(\d{2}\/\d{2})?$/i','в формате DD/MM',
    #   ],
    #   'replace_rules':[
    #       '/[^0-9\/]/', '',
    #       '/^(\d{2})(\d)/','$1/$2'
    #   ],
    #   'tab':'hr'
    # },
]