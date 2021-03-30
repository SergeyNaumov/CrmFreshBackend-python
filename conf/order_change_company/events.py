from lib.send_mes import send_mes
from lib.core import gen_pas


def events_permissions(form):
    form.read_only=1
    if(form.action=='new'):
      form.values={}
      if('cgi_params' in form.R):
        params=form.R['cgi_params']

        if 'comp_id' in params:
          data=form.db.getrow(table="comp",where="id = %s",values=[params['comp_id']],str=1)

          # Компанию нашли
          if data:

            form.fields.append({'name':'comp_id','type':'hidden'})
            form.values['comp_id']=data['id']
            
            # Разрешаем создавать только тем, кто является представителем компании
            if data['manager_id'] == form.manager['id']:
              form.read_only=0
            for f in form.fields:
              if f['name'] in data:
                #form.log.append(f['name']+' => '+data[f['name']])
                #f['value']=data[f['name']]
                form.values[f['name']]=data[f['name']]

    if form.action=='insert':
      comp_id=form.R['values']['comp_id']
      if comp_id:
        data=form.db.getrow(table="comp",where="id = %s",values=[comp_id],str=1)
        if data['manager_id'] == form.manager['id']:
          form.read_only=0
          form.fields.append({'name':'comp_id','type':'hidden','value':comp_id})
          form.explain=1
      else:
        form.errors.append('Не указано ID-компании. Обратитесь к разработчику')
      
      

#def after_insert(form,opt):


def after_save(form,opt):
  form.log.append(form.values)  
  ov=form.values
  nv=form.new_values
  
  # Отключаем редактирование у вновь добавленной заявки
  if not (form.manager['login'] == 'admin'):
    form.read_only=1
  



  # if int(ov['accepted'])==0 and int(nv['accepted'])==1:
  #   print('Включили галку!')

#def events_before_code(form):
    


    #form.errors.append('Вам запрещено удалять!')

events={
  'permissions':[
      events_permissions
    
  ],
  #'after_insert':after_insert,
  'after_save':after_save,
  #'before_delete':before_delete,
#  'before_code':events_before_code
}