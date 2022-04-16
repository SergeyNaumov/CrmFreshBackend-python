#def pre(d):
#    form.pre(d)
#from lib.CRM.plugins.search.xlsx import go as init_search_plugin
from lib.core import exists_arg, date_to_rus

def events_permissions(form):
    
    if form.manager['type']==1:
      form.is_admin=1
      form.read_only=0
      form.not_create=0
      #init_search_plugin(form)
      
    else:
      form.is_admin=0
      form.make_delete=0
      form.not_create=True
      form.read_only=1
      for field in form.fields:
        if not(field['name'] in ('header','anons','body')):
          form.remove_field(field['name'])
      
    
    if form.script=='table':
        form.data=form.db.query(
            query='''
              select
                id,header,registered,anons
              from
                news
              where enabled=1
            ''',
            log=form.log,
            errors=form.errors,
            arrays=1
        )
        print('data:',form.data)
        for d in form.data:
            d['registered']=date_to_rus(d['registered'])
            if d['header']:
                #Формируем объект-dialog
                d['header']={
                    'header':d['header'],
                    'type':'url',
                    'url':f"/page/news/{d['id']}",
                    
                }
                # d['header']={
                #     'header':d['header'],
                #     'type':'dialog',
                #     'dialog_html':form.template('./conf/conference_table/templates/dialog.html',d=d),
                #     #'url':f"/table/{form.config}/ajax-dialog/{d['id']}"
                # }
                
                del d['id']
                #f"""<a href="" target="_blank">{d['header']}</a>"""
            # if d['link']:
            #     d['link']=f"""<a href="{d['link']}" target="_blank">{d['link']}</a>"""

        if form.manager['type']==1:
            form.links=[
                {
                    'type':'url',
                    'link':'/admin_table/news',
                    'description':'Редактирование новостей'
                },
            ]

    
    if form.script=='page' and form.id:
        d=form.db.query(
            query='select header,body,DATE_FORMAT(registered, %s) registered from news where id=%s',
            values=['%d.%m.%Y',form.id],
            onerow=1
        )
        #d['start']=date_to_rus(d['start'])
        form.title=d['header']
        form.blocks=[
            {'type':'html','body':form.template('./conf/news/templates/dialog.html',d=d)},
            
        ]



      

def before_search(form):
  pass

def events_before_code(form):
    pass

def before_delete(form,opt):
    pass

events={
  'permissions':[
      events_permissions
    
  ],
  'before_search':before_search,
  'before_delete':before_delete,
  'before_code':events_before_code
}