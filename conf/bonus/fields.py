import os.path



def get_fields():
    return [ 
    {
      'name':'file',
      'description':'Файл',
      'filedir':'./files/Akt',
      'type':'file',
      #'read_only':1,
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
      'filter_on':1,
      'filter_code':accept_filter_code
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
def accept_filter_code(form,field,row):
  if row['wt__accept']:
    return 'акт подписан'
  else:
    return {
      'before_html':'не подписан',
      'title':'Отправка акта',
      'id':row['wt__id'],
      'config':'bonus',
      'name':'file',
      'type':'form',
      'style':'margin-top: 20px;',

      'spoiler':'загрузить',
      'fields':[
        {
          'description':'Файл акта',
          'name':'attach',
          'filedir':'/files/bonus_order',
          'type':'file'
        },
        {
          'description':'Комментарий',
          'name':'comment',
          'type':'textarea'
        }
      ],
      # url заменить
      'url':f'/backend/anna/bonus/order/{row["wt__id"]}',
      'value':''
    }
def file_filter_code(form,field,row):
  arr=row['wt__file'].split('.')


  if len(arr)>1:
    #form.pre('len:'+str(len(arr)))
    #form.pre(arr)
    if row['wt__file'] and os.path.exists('./files/Akt/'+row['wt__file']):
      return f'''
        <a href="{'/files/Akt/'+row['wt__file']}" target="_blank">{row['wt__file']}</a>
      '''
    else: # Если не найден файл -- пробуем найти с другим расширением (файлы у нас только с расширением jpg и pdf)
      ext=arr[-1]
      if ext=='jpg':
        ext='pdf'
      elif ext=='pdf':
        ext='jpg'
      
      #form.pre(''.join(arr))
      del arr[-1]
      
      filename='.'.join(arr)+'.'+ext
      #form.pre(filename)
      if filename and os.path.exists('./files/Akt/'+filename):
        #form.pre('find changed'+filename)
        return f'''<a href="{'/files/Akt/'+filename}" target="_blank">{filename}</a>'''
      #form.pre(ext)

  #return row['wt__file']+' <small>файл отсутствует</small>'

    
  