import re
from lib.core import exists_arg
# Модуль для формирования ЧПУ

def to_translate(s):

   # Слоаврь с заменами
   d = {'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'e',
      'ж':'zh','з':'z','и':'i','й':'i','к':'k','л':'l','м':'m','н':'n',
      'о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f','х':'h',
      'ц':'c','ч':'cz','ш':'sh','щ':'scz','ъ':'','ы':'y','ь':'','э':'e',
      'ю':'u','я':'ja', 'А':'A','Б':'B','В':'V','Г':'G','Д':'D','Е':'E','Ё':'E',
      'Ж':'ZH','З':'Z','И':'I','Й':'I','К':'K','Л':'L','М':'M','Н':'N',
      'О':'O','П':'P','Р':'R','С':'S','Т':'T','У':'U','Ф':'F','Х':'H',
      'Ц':'C','Ч':'CZ','Ш':'SH','Щ':'SCH','Ъ':'','Ы':'y','Ь':'','Э':'E',
      'Ю':'U','Я':'YA',',':'','?':'',' ':'_','~':'','!':'','@':'','#':'',
      '$':'','%':'','^':'','&':'','*':'','(':'',')':'','-':'','=':'','+':'',
      ':':'',';':'','<':'','>':'','\'':'','"':'','\\':'','/':'','№':'',
      '[':'',']':'','{':'','}':'','ґ':'','ї':'', 'є':'','Ґ':'g','Ї':'i',
      'Є':'e', '—':''}
        
   # Циклически заменяем все буквы в строке
   for key in d:
      s = s.replace(key, d[key])
   return s

async def check_exists_url(form,url,opt,postfix=''):
    if not(url): return
    if postfix:
        url+=f'-{postfix}'

    where='ext_url=%s'
    if exists_arg('foreign_key', opt) and exists_arg('foreign_key_value', opt):
        where+=f' AND {opt["foreign_key"]}={opt["foreign_key_value"]}'
    if form.id:
        in_url=opt['in_url'].replace('<%id%>',str(form.id))
        where+=f' AND in_url<>"{in_url}"'

    exists=await form.db.query(
        query=f'select count(*) from in_ext_url where {where}',
        values=[url],
        #debug=1,
        onevalue=1
    )
    #print('exists:',exists)
    return exists

async def InExtUrl(form, opt):
    if not( exists_arg('dependence_field', opt) ):
        form.errors.append('Не указап параметр dependence_field при вызове модуля InExtUrl')
        return 
    
    dependence_field=opt['dependence_field']
    dep=form.get_field(dependence_field)
    dep['frontend']={
            'ajax':{
                'name':'in_ext_url'
            }
    }

    if not( exists_arg('in_url', opt) ):
        form.errors.append('Не указап параметр in_url при вызове модуля InExtUrl')
        return 

    in_ext_url_field={        
        'description':'url',
        'name':'in_ext_url',
        'type':'in_ext_url',
        'in_url':opt['in_url'],
        #'in_url':'/service/<%id%>',
        
    }
    
    if exists_arg('tab', opt):
        in_ext_url_field['tab']=opt['tab']
    
    if exists_arg('after_field', opt): #
        #pass
        form.add_field(in_ext_url_field, opt['after_field'])
        #form.pre(form.fields)
    else:
        form.fields.append(in_ext_url_field)

    if exists_arg('foreign_key', opt) and exists_arg('foreign_key_value', opt):
        in_ext_url_field['foreign_key']=opt['foreign_key']
        in_ext_url_field['foreign_key_value']=opt['foreign_key_value']

    async def ajax_in_ext_url(form,values):
        url=''
        if (dependence_field in values) and  values[dependence_field]:
            h=values[dependence_field].replace('/','-')
            url+=to_translate(h)
            # rewrite from perl to python:
            url=re.sub(r"[^a-zA-Z0-9\-]+","-",url)
            url=re.sub(r"--+","-",url)
            url=url.lower()
            if exists_arg('url_prefix', opt):
                url=opt['url_prefix']+url

            if await check_exists_url(form,url,opt):
                postfix=1
                while await check_exists_url(form, url, opt, postfix):
                    postfix+=1
                
                url=url+f'-{postfix}'
            
            return [
                'in_ext_url',
                {
                    #'instead_of_empty':url,
                    'value':url
                    #'url':url
                }
            ]
    
    if form.script in ('ajax','edit_form'):
        if not hasattr(form,'ajax'): form.ajax={}
        form.ajax['in_ext_url']=ajax_in_ext_url