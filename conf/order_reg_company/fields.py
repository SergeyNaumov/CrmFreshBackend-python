
def accepted_before_code(**arg):
  form=arg['form']
  field=arg['field']
  #form.log.append(field)
  if field['value']=="0":
    field['after_html']="""
    <hr>
      <small ><strong style="color: red;">Внимание!</strong> После того, как Вы подтвердите заявку:<br>
      1. Создастся юридическое лицо (в случае отсутствия в базе юрлица с таким ИНН)<br>
      2. Создастся учётная запись для представителя данного юридического лица и отправится ему на почту<br>
      <b>3. Оменить подтверждение заявки простым снятием галочки будет нельзя</b>
    </small>
    <hr>
    """
  else:
    field['after_html']="""
      Заявка была подтверждена ранее
    """
    #field['read_only']=1

  #form.log.append(field)



def get_fields():
    return [ 
    {
      'name':'registered',
      'description':'Дата регистрации',
      'type':'date',
      'read_only':1,
      'filter_on':1
    },
    {
      'description':'Подтвердена',
      'name':'accepted',
      'type':'checkbox',
      #'before_code':accepted_before_code,
    },
    {
      'name':'firm',
      'description':'Наименование организации',
      'type':'text',
      'filter_on':1
    }, 
    {
      'name':'inn',
      'description':'ИНН',
      'type':'text',
      'filter_on':1
    },
    {
      'name':'ur_address',
      'description':'Юридический адрес',
      'type':'text',
      'filter_on':1
    },
    {
      'description':'Телефон',
      'type':'text',
      'name':'phone',
      'filter_on':1
    },
    {
      'description':'Имя',
      'type':'text',
      'name':'name',
      'filter_on':1
    }

]
