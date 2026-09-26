fields_for_inline=[
    {
        'description':'Название кнопки',
        'name':'header',
        'type':'text',
    },
    {
        'description':'Действие при нажатии на кнопку',
        'type':'select_values',
        'name':'action',
        'values':[
            {'v':'3','d':'переход по ссылке'},
            {'v':'1','d':'переход по ссылке в web-app'},
            {'v':'2','d':'выполнить команду бота'},
        ]
    },
    {
        'description':'Ссылка на web-приложение / команда бота',
        'name':'url',
        'type':'text',
    },
]

fields_for_reply=[
    {
        'description':'Название кнопки',
        'name':'header',
        'type':'text',
    },
    {
        'description':'Запросить контакт',
        'type':'checkbox',
        'name':'request_contact'
    },
]

def ajax_keyboard_type(form, values):
    result=[]
    #
    keyboard_type=values['keyboard_type']
    # 1 - inline
    # 2 - reply
    #print('kt:',keyboard_type)

    if keyboard_type=='1':
        result.append('keyboard')
        result.append({'fields':fields_for_inline})

        result.append('one_time_keyboard')
        result.append({'hide':True})

        result.append('resize_keyboard')
        result.append({'hide':True})

    if keyboard_type=='2':
        result.append('keyboard')
        result.append({'fields':fields_for_reply})

        result.append('one_time_keyboard')
        result.append({'hide':False})

        result.append('resize_keyboard')
        result.append({'hide':False})


    print('result:',result)
    return result

ajax={
    'keyboard_type': ajax_keyboard_type
}