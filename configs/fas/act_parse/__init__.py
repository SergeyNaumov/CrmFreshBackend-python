from lib.engine import s
import re

def before_loopback(data):
  if dogovor_number:=data.get('dogovor_number'):
    data['dogovor_number']=re.sub(r"от .+$",'',dogovor_number.replace('№',''))
    data['dogovor_number']=re.sub(r"\s+$",'',data['dogovor_number'])
    data['dogovor_number']=re.sub(r"^\s+",'',data['dogovor_number'])
    docpack_id=s.db.query(
      query="select docpack_id from dogovor where number=%s",
      values=[data['dogovor_number']],
      onevalue=1
    )
    if docpack_id:
      data['docpack_id']=docpack_id

  if dat:=data.get('dat'):
    
    dat = re.sub(r'^(\d{2})\.(\d{2})\.(\d{2})$', r'20\3-\2-\1', dat)
    #dat = re.sub(r'^(\d{2})\.(\d{2})\.\d{4}$', '\3-\2-\1', dat)
    data['dat'] =dat

  if inn:=data.get('inn'):
    # в ИНН оставляем только цифры
    data['inn'] = re.sub(r'^\s*(\d+).+$', r'\1', inn)
  #print('data:',data)


parser={
  'title':'Парсер актов',
  'work_table':'act2',
  'work_table_id':'id',
  'tmp_dir':'./tmp/act_parse',
  'livetime_tmp':'3600',# время жизни временных файлов
  'before_loopback':before_loopback,
  'loopback':None, # собственная функция для сохранения

  'before_load_fields_message': 'для продолжения работы выберите юрлицо',
  
  'unique_fields':['number'],
  'before_load_fields':[
    {
      'description':'Выберите юридическое лицо',
      'name':'ur_lico_id',
      'type':'select',
      'values':s.db.query(query="select id v, firm d from ur_lico order by firm")
    }
  ],
  'fields':[

    {'name':'number','description':'Номер документа'},
    {'name':'dat','description':'Дата'},
    {'name':'inn','description':'ИНН'},
    {'name':'dogovor_number','description':'Договор'},
    {'name':'service','description':'Услуга'},
    {'name':'summa','description':'Сумма'},


  ]

}