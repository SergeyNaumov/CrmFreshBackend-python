#from .fields import get_fields
async def map_zoom_before_code(form,field):
    if form.script=='edit_form':
        if form.action=='new':
            field['value']='7'
        elif field['value']=='0' or not(field['value']):
            field['value']='7'


form={
    'work_table':'struct_5794_address_list',
    'work_table_id':'id',
    #'work_table_foreign_key':'project_id',
    #'work_table_foreign_key_value':4664,
    'title':'Адреса',
    'sort':1,
    'tree_use':False,
    'header_field':'header',
    'max_level':2,
    'default_find_filter':'header',
    'changed_in_tree':False, # Возможность изменять в дереве, не заходя в карточки
    'fields':[
        {
            'description':'Город',
            'type':'text',
            'name':'header',
        },
        {
            'description':'Адрес',
            'type':'text',
            'name':'address',
        },
        {
            'description':'Юр. Адрес',
            'type':'text',
            'name':'ur_address',
        },
        {
            'description':'Телефоны для списка в шапке',
            'type':'textarea',
            'after_html':'с переносом строк, например: <br>+7 (987) 907-80-45<br>+7 (987) 907-80-46<br>+7 (987) 907-80-47',
            'name':'phones',

        },
        {
            'description':'Телефоны в блоке "контакты"',
            'type':'wysiwyg',
            'name':'phones_contact_block',
            'values':[
                {
                    'd':'заполнить',
                    'v': '<div class="item"><a class="link" href="tel:+78463730712">(846) 373-07-12</a> отдел договоров</div>\n'+\
                         '<div class="item"><a class="link" href="tel:+78463730713">(846) 373-07-13</a> испытательная лаборатория</div>\n'+\
                         '<div class="item"><a class="link" href="tel:+79879078045">(987) 907-80-45</a></div>\n'+\
                         '<div class="item"><a class="link" href="tel:+78463730711">(846) 373-07-11</a> / 12</div>'
                }
            ]
        },
        {
            'description':'Ссылка на whatsapp',
            'after_html':'<i><small>например, https://wa.me/79109854595</small></i>',
            'type':'text',
            'name':'whatsapp',
        },
        {
            'description':'Ссылка на telegram',
            'after_html':'<i><small>например, https://t.me/9109854595</small></i>',
            'type':'text',
            'name':'telegram',
        },
        {
            'description':'Email в шапке',
            'type':'text',
            'name':'email'
        },
        {
            'description':'Email-ы',
            'type':'wysiwyg',
            'name':'email_block',
            'values':[
                {
                    'd':'заполнить',
                    'v':'<div class="item"><a class="link" href="mailto:sozvezdie-m2007@yandex.ru">sozvezdie-m2007@yandex.ru</a></div>\n'+
                    '<div class="item"><a class="link" href="mailto:info@yandex.ru">info@yandex.ru</a> к.л. Екатерина Иванова</div>'
                }
            ]

        },
        {
            'description':'Email для заказа',
            'type':'text',
            'name':'email_for_feedback'
        },
        {
            'description':'График работы',
            'type':'textarea',
            'name':'work_time',
            'values':[
                {'d':'пн-сб', 'v':"Пн. - Сб.: с 8:00 - 18:00\nОбед: с 12:00 до 13:00\nВс.: Выходной"},
                {'d':'без выходных', 'v':"Пн - Вс.: с 8:00 - 18:00\nОбед: с 12:00 до 13:00"},
            ],
        },
        {
            'description':'Координаты на странце "контакты" (широта,долгота)',
            'after_html':'''<i><small>строгий формат:, например: 48.475164,135.086209</small></i>''',
            'type':'text',
            'name':'map_center',
            'regexp_rules':[
                r'/^(\d+\.\d+,\d+\.\d+)$/', 'проверьте формат координат центра карты'
            ],
            'replace_rules':[
                r'/[^\d\.,]/', '',
                r'/\.,/', '.',
            ]
        },
        {
            'description':'Координаты в блоке "представительства" (широта,долгота)',
            'after_html':'''<i><small>строгий формат:, например: 48.475164,135.086209</small></i>''',
            'type':'text',
            'name':'map_center2',
            'regexp_rules':[
                r'/^(\d+\.\d+,\d+\.\d+)$/', 'проверьте формат координат центра карты'
            ],
            'replace_rules':[
                r'/[^\d\.,]/', '',
                r'/\.,/', '.',
            ]
        },
        {
            'description':'Координаты метки (широта,долгота)',
            'after_html':'''<i><small>строгий формат:, например: 48.475164,135.086209</small></i>''',
            'type':'text',
            'name':'placemark_center',
            'regexp_rules':[
                r'/^(\d+\.\d+,\d+\.\d+)$/', 'проверьте формат координат метки'
            ],
            'replace_rules':[
                r'/[^\d\.,]/', '',
                r'/\.,/', '.',
            ]
        },
        {
            'description':'Размер карты',
            'after_html':'<i><small>строгий формат:, 1..16</small></i>',
            'type':'text',

            'before_code':map_zoom_before_code,
            'name':'map_zoom',
            'regexp_rules':[
                r'/^([1][0-6]|\d)$/', 'неверное значение'
            ],
            'replace_rules':[
                #r'/[^\d]/g', '',
                #r'/^(\d).+/', '$1',
            ]
        },
        {
            'description':'Название метки на карте при наведении',
            'name':'label_header',
            'type':'text'
        },
        {
            'description':'Подпись метки на карте при клике',
            'name':'label_header2',
            'type':'text'
        },
        {
            'description':'Название организации',
            'type':'text',
            'name':'firm',
        },
        {
            'description':'Название банка',
            'type':'text',
            'name':'bankname',
        },
        {
            'description':'Файл с реквизитами',
            'type':'file',
            'filedir':'./files/project_5794/address_list',
            'name':'attach'

        },
       {
            'description':'ОКПО',
            'type':'text',
            'name':'okpo',
        },
        {
            'description':'ОКОГУ',
            'type':'text',
            'name':'okogu',
        },
        {
            'description':'ОКАТО',
            'type':'text',
            'name':'okato',
        },
        {
            'description':'ОКВЭД',
            'type':'text',
            'name':'okved',
        },
        {
            'description':'ОКФС',
            'type':'text',
            'name':'okfs',
        },
        {
            'description':'ОКОПФ',
            'type':'text',
            'name':'okopf',
        },
        {
            'description':'ИНН',
            'type':'text',
            'name':'inn',
        },
        {
            'description':'КПП',
            'type':'text',
            'name':'kpp',
        },
        {
            'description':'Кор. счёт',
            'type':'text',
            'name':'kor_sc',
        },
        {
            'description':'БИК',
            'type':'text',
            'name':'bik',
        },
        {
            'description':'Расчётный счёт',
            'type':'text',
            'name':'rs',
        },


    ]
}
      


