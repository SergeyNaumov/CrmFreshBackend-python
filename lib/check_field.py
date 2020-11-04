import re
# проверяет поле на ошибки:
#      from lib.check_field import check_field
#        check_field(form,field,value)
def check_field(form,field,value):

  if 'regexp_rules' in field:
    i=0
    
    regexp_rules=field['regexp_rules']
    while i<len(regexp_rules):
      pattern=regexp_rules[i]
      pattern_arr=re.search(r'^\/(.+)\/(.*)$',pattern)
      if pattern_arr:
        pattern=pattern_arr[1]
        modificators=pattern_arr[2]
        err=regexp_rules[i+1]
        if 'i' in modificators:
          pattern=re.compile(pattern, re.IGNORECASE|re.MULTILINE)
        else:
          pattern=re.compile(pattern,re.MULTILINE)
        
        if not re.match(pattern,value):
          form.errors.append(err)
      i+=2