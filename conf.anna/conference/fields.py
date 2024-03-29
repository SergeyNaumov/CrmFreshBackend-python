




def enabled_before_code(form,field):
  if form.script=='edit_form' and form.action=='new':
    field['value']=1

def link_filter_code(form,field,row):
  if row['wt__link']:
    return f"""<a href="{row['wt__link']}" target="_blank">{row['wt__link']}</a>"""

def get_fields():
  return [ 
      {
          'description':'Вкл',
          'type':'checkbox',
          'name':'enabled',
          'before_code':enabled_before_code
      },
      {
          'description':'Не выдавать сертификат',
          'type':'checkbox',
          'name':'not_cert',
      },
      {
          'description':'Название конференции',
          'type':'text',
          'name':'header',
          'filter_on':1,
      },
      {
          'description':'Название компании, проводящей конференцию',
          'type':'text',
          'name':'comp_name',
          'filter_on':1,
      },
      {
          'description':'Тема конференции',
          'type':'textarea',
          'name':'subject_conf',
          'filter_on':1,
      },
      {
          'description':'Название документа',
          'add_description':'"Сертификат", "Диплом" или иное',
          'type':'text',
          'name':'document_name',
          'filter_on':1,
      },
      {
          'description':'Дата и время начала',
          'type':'datetime',
          'name':'start',
          'filter_on':1,
      },

      {
        'description':'Ссылка на конференцию',
        'type':'text',
        'name':'link',
        'filter_code':link_filter_code,
        
      },
      {
        'description':'Идентификатор конференции',
        'type':'text',
        'name':'conf_id',
      },
      {
        'description':'Код доступа',
        'type':'text',
        'name':'access_code',
      },
      {
        'description':'Комментарий',
        'type':'wysiwyg',
        'name':'comment',
      },
  ]