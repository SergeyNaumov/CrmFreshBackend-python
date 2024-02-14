search_multi_action_list=[
        {
            'description':'перенести всё в рубрику',
            'type':'set_all_value_field',
            'name':'category_id',
            'step':1, # состояние поля
       },
       {
            'description':'изменить цену',
            'type':'change_price',
            'name':'price',
            'step':1
       },
       # {
       #      'description':'выбрать цвет',
       #      'type':'set_all_value_field',
       #      'name':'color_id',
       #      'step':1, # состояние поля
       # },
       {
            'description':'удалить выбранные',
            'type':'delete',
       },
]