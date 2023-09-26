from lib.core import exists_arg
def get_data(form,field):
    R=form.R
    values=exists_arg('values',R) or {}
    data={}
    foreign_key_value=None
    if 'foreign_key_value' in field:
      foreign_key_value=field['foreign_key_value']

    else:
      foreign_key_value=form.id

    data[field['foreign_key']]=foreign_key_value
    
    for f in field['fields']:
        
        if f['type'] in ['code','file','picture']: continue
        if exists_arg('read_only',f): continue

        v=exists_arg(f['name'],values)

        #if f['type'] in ['checkbox','switch']:
        #  print('checkbox:', v)
        if not v==None:
          #print(f'VALUE {f["name"]}', v)
          regexp_rules=exists_arg('regexp_rules',f) or ''
          
          # проверка регулярок
          if isinstance(regexp_rules,list):
            i=0
            _len=len(regexp_rules)

            while i < len(regexp_rules):
                reg=regexp_rules[i]
                err=regexp_rules[i+1]

                if not err:
                  err=f'поле {f["description"]} не заполнено или заполнено неверно'
                  # !!!! $reg=~s/^\///;
                  pattern=''
                  # if($reg=~m/\/([a-zA-Z]+)?$/){
                  #   $reg=~s/\/([a-zA-Z]+)?$//;
                  # }

                i+=2
          if f['type'] in ['checkbox','switch']:
            #print('checkbox:', v)
            if v=='true': v=1
            elif v=='false': v=0
          data[f['name']]=v

    return data




