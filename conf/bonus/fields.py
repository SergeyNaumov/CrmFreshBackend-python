import os.path



def get_fields():
    return [ 
    {
      'name':'file',
      'description':'Файл',
      'type':'text',
      'read_only':1,
      'filter_on':1,
      'filter_code':file_filter_code
    },
    {
      'name':'number',
      'description':'Номер акта',
      'type':'text',
      'filter_on':1
    }, 
    {
      'name':'date_create',
      'description':'Дата выставления акта',
      'type':'date',
      'default_off':1,
      'filter_on':1
    },
    {
      'name':'accept',
      'description':'Подписан',
      'type':'checkbox',
      'filter_on':1
    },
    {
      'description':'Оплачен',
      'type':'checkbox',
      'name':'paid_status',
      'filter_on':1
    },
    {
      'description':'Сумма оплаты',
      'name':'summ',
      'type':'text',
      'filter_on':1

    },
    {
      'name':'paid_date',
      'description':'Дата оплаты',
      'type':'date',
      'default_off':1,
      'filter_on':1
    },
    {
      'name':'id',
      'description':'Поставщики',
      'type':'filter_extend_checkbox',
      
    }

]
def file_filter_code(form,field,row):
  if row['wt__file'] and os.path.exists('./files/Akt/'+row['wt__file']):
    return f'''
      <a href="{'/files/Akt/'+row['wt__file']}" target="_blank">{row['wt__file']}</a>
    '''
  else:
    return row['wt__file']+' <small>файл отсутствует</small>'
  