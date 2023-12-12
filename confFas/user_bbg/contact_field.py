def contacts_before_code(form,field):
  if form.id and form.ov['user_id']:
    field['foreign_key_value']=form.ov['user_id']
  else:
    field['foreign_key_value']=''
    field['read_only']=1
    field['after_html']='отображение контактов невозможно, поскольку данная карта не привязана к карте ОП'

contact_field={
            'description':'Контакты',
            'name':'contacts',
            'type':'1_to_m',
            'table':'user_contact',
            'foreign_key':'user_id',
            'table_id':'id',
            'view_type':'list',
            'before_code':contacts_before_code,
            'fields':[
                {
                    'description':'ФИО',
                    'name':'fio',
                    'type':'text',
                },
                {
                    'description':'Email',
                    'name':'email',
                    'type':'text',
                },
                {
                    'description':'Телефон',
                    'name':'phone',
                    'type':'text',
                    'subtype':'qr_call',
                    'replace_rules':[
                        '/^8/','+7',
                        '/^92/', '+792',
                        '/;/g',',',
                        '/,$/',', ',
                        '/\s+,/', ', ',
                        '/\s+,/g', ',',
                        '/[^\s,\d\+]/g','',
                        '/, 8/',', +7',
                    ],
                    'regexp_rules':[
                        '/^(\+\d{6,12})(,\s\+\d{6,12})*$/','Номер должен быть в формате: +[код]XXXXXXXXXX, например: +74951234567',
                       
                    ],
                },
                {
                    'description':'Должность',
                    'name':'position',
                    'type':'text',
                },
                {
                    'description':'Ответственный',
                    'name':'otv',
                    'type':'checkbox',
                },
                {
                    'description':'Комментарий',
                    'name':'comment',
                    'type':'text',
                },
            ],
            #'tab':'contacts',
}