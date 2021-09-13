import pymysql
import json
import re
from .transform import tree_use_transform, massive_transform
from lib.core import print_console_error
def rez_to_str(rez):
  if rez:
    for k in rez:
      rez[k]=str(rez[k])
    
def exists_arg(key,dict):
  if (key in dict) and dict[key]:
    return True
  return False

def get_func(value):

  if value and isinstance(value,str):
    rez=re.search('func:\((.+)\)',value)
    if not rez:
      rez=re.search('func:(.+)',value)
    if rez: return rez[1]
  return ''



def out_error(self,error,arg):
  self.err_str=error
  if 'error' in arg:
    if(type(arg['error']) == type([])): # type is list
        arg['error'].append(error)
    else: # type is str
        arg['error']=error
  else:
    print(error)
    print("\nQUERY:\n"+arg['query'])
    if ('values' in arg) and len(arg['values']):
      print(arg['values'])
    #quit()


def get_query(self,arg): # для get и getrow
  self.error_str=''
  sf=''
  if not exists_arg('select_fields',arg):
    sf='*'
  else:
    sf=arg['select_fields']

  if not exists_arg('table',arg):
    out_error(self,"FreshDB::"+arg['method']+" not set attr table",arg)
    return ''
    
  
  query='select '+sf+' FROM '+arg['table']+' wt'
  
  # join-ы
  if 'tables' in arg:
    for table in arg['tables']:
      if ('lj' in table ) and (table['lj']) :
        query += ' LEFT '

      query += ' JOIN '
      query += table['t']

      if ('a' in table) and (table['a']):
        query += ' '+ table['a']

      if ('l' in table) and (table['l']):
        query += ' ON '+ table['l']


  if exists_arg('where',arg):
    query += ' WHERE '+arg['where']
  if exists_arg('order',arg):
    query += ' ORDER BY '+arg['order']
  
  if arg['method'] == 'getrow':
    arg['limit'] = 1
 
  if exists_arg('perpage',arg) and exists_arg('table',arg):
    arg['perpage']=int(arg['perpage'])
    if not(exists_arg('page',arg)):
      arg['page']=1

    query_count='SELECT CEILING(count(*) / ' + str(arg['perpage'])+') FROM '+arg['table'];

    if exists_arg('where',arg): query_count +=' WHERE '+arg['where']
    
    if exists_arg('group',arg): query_count +=' GROUP BY ' + arg['group']
    
    if not exists_arg('values',arg): arg['values']=[]

    arg['maxpage']=self.query(query=query_count,onevalue=1,values=arg['values'])

    limit1=(arg['page']-1) * arg['perpage'];
    arg['limit']=str(limit1)+','+str(arg['perpage']);


  if exists_arg('limit',arg):
    query += ' LIMIT ' + str(arg['limit'])
  return query

def to_json(data):
    return json.dumps(data, ensure_ascii=False) # ,separators=(',', ': ') sort_keys=False,indent=0,


class FreshDB():
    def go_connect(self,arg):
      #self.connect = pymysql.connect(arg['host'], arg['user'], arg['password'], arg['dbname'])
      self.connect = pymysql.connect(user=arg['user'], password=arg['password'], host=arg['host'], database=arg['dbname'])
      self.connect.ping(reconnect=True)


    def __init__(self, **arg):
      self.tmpl_saver = None;
      self.error_str=''
      if not exists_arg('host',arg):
        arg['host']='localhost'

      if not exists_arg('password',arg):
        arg['password']=''

      if exists_arg('tmpl_saver',arg):
        self.tmpl_saver=arg['tmpl_saver']
      
      self.go_connect(arg)
      # , cursorclass=pymysql.cursors.DictCursor
    def set_tmpl_saver(self,tmpl_saver):
      self.tmpl_saver=tmpl_saver

    def execute(self,cur,arg):
      self.connect.ping()  # reconnecting mysql

      if ('debug' in arg) and (arg['debug']):
        print(arg['query'])
        if exists_arg('values',arg): print(arg['values'])
      
      if not exists_arg('values',arg):
        arg['values']=[]

      try:
        cur.execute(arg['query'],arg['values'])
        self.connect.commit()
      except pymysql.err.ProgrammingError as err:
        if 'errors' in arg: arg['errors'].append(str(err))

      except pymysql.err.DataError as err:
        if 'errors' in arg: arg['errors'].append(str(err))
        #self.error_str = str(err)

      # except pymysql.err.IntegrityError as e2:
      #     out_error(self,str(e2),arg)
      #     self.error_str=e2

      except pymysql.err.InternalError as err:
          if 'errors' in arg: arg['errors'].append(str(err))
          #out_error(self,str(err),arg)
          self.error_str = str(err)
          


    def desc(self, **arg):
      self.connect.ping()  # reconnecting mysql
      cur = pymysql.cursors.DictCursor(self.connect)
      
      if not('method' in arg) :
        self.error_str=''
        arg['method']='desc'
      
      if not exists_arg('table',arg):
        out_error(self,"FreshDB::"+arg['method']+" not set attr table",arg)
        return 

      arg['query']='desc '+arg['table']

      
      self.execute(cur, arg)
      
      
      result={}
      if self.error_str: 
        return {}
      try:
        fields=cur.fetchall()

        
        for f in fields:
          result[ f['Field'] ]=f
      except pymysql.err.ProgrammingError as err:
        self.error_str = str(err)

      return result

    def getvalue(self, **arg):
      self.connect.ping()  # reconnecting mysql
      cur = self.connect.cursor()
      #print('arg:',arg)
      arg['method']='getvalue'
      arg['query']=get_query(self,arg)
      #print(arg)
      
      if self.error_str:
        return None
      self.execute(cur,arg)
      
      rez=cur.fetchone()
      #print('rez',rez)
      if not rez: rez=''
      else: rez=rez[0]
      
      return self.prepare_result(rez,arg)

    def getrow(self, **arg):
      self.connect.ping()  # reconnecting mysql
      self.error_str=''
      cur = pymysql.cursors.DictCursor(self.connect)
      arg['method']='getrow'
      arg['query']=get_query(self,arg)

      if self.error_str:
        return {}

      self.execute(cur,arg)
      if self.error_str: return {}
      try:
        rez=cur.fetchone()
        if exists_arg('str',arg):
          rez_to_str(rez)

      except pymysql.err.ProgrammingError as err:
        
        self.error_str = str(err)
        return None
      
      if exists_arg('to_json',arg):
        return to_json(rez)
      #if not(rez):
      #  rez=False

      return self.prepare_result(rez,arg) 
    def prepare_result(self,rez,arg): # подготавливает и возвращает результат
      
      if exists_arg('to_json',arg):
        rez=to_json(rez)

      if exists_arg('to_tmpl',arg):
          if self.tmpl_saver :
            self.tmpl_saver(name=arg['to_tmpl'],value=rez)
            if exists_arg('perpage',arg) & exists_arg('maxpage',arg):
              return int(arg['maxpage'])
            else:
              return True

      if exists_arg('perpage',arg) & exists_arg('maxpage',arg):

        return int(arg['maxpage']),rez

      return rez
    def get(self, **arg):
      self.connect.ping()  # reconnecting mysql
      self.error_str=''

      if exists_arg('onerow',arg):
        return self.getrow(**arg)

      cur = pymysql.cursors.DictCursor(self.connect)
      arg['method']='get'
      arg['query']=get_query(self,arg)

      if self.error_str:
        return []

      self.execute(cur,arg)

      if self.error_str:
        rez=[]
      else:
        try:
          rez=cur.fetchall()
        except pymysql.err.ProgrammingError as err:
          return []

      return self.prepare_result(rez,arg)



    def query(self, **arg):
      self.error_str=''
      self.connect.ping()  # reconnecting mysql
      
      if exists_arg('onevalue',arg):
        cur = self.connect.cursor()
      else:
        cur = pymysql.cursors.DictCursor(self.connect)
      
      arg['method']='query'
      if not exists_arg('query',arg):
        out_error(self,'FreshDB::query: not exists attribute query',arg)
      #print('arg:',arg)
      if self.error_str : return []
      try:
        self.execute(cur,arg)
      except pymysql.err.OperationalError as err:
        
        if 'errors' in arg:
          arg['errors'].append(f"error query: {arg['query']} {str(err)}")
        else:
          print_console_error("err1 query:\n"+arg['query']+"\n"+str(err))
        return []

      rez=''
      if exists_arg('onevalue',arg):
        try:
          rez = cur.fetchone()
        except pymysql.err.ProgrammingError as err:
          if 'errors' in arg:
            arg['errors'].append(f"error query: {arg['query']} {str(err)}")
          else:
            print_console_error("err2 query:\n"+arg['query']+"\n"+str(err))

          return []
        if rez: rez=rez[0]
      else:
          if exists_arg('onerow',arg):
            try:
              rez=cur.fetchone()
            except pymysql.err.ProgrammingError as err:
              print('err3: ',err )
              print_console_error(err)
              print(arg['query'],)
              return []

          else:
            try:
              rez=cur.fetchall()
              if exists_arg('massive',arg):
                rez=massive_transform(rez)
                if exists_arg('str',arg):
                  rez = [str(item) for item in rez]
              else:
                if exists_arg('tree_use',arg): rez=tree_use_transform(rez)



            except pymysql.err.ProgrammingError as err:
              print_console_error('freshdb query error:')
              print('ERR:',err,arg['query'])
              
              if exists_arg('errors',arg): arg['errors'].append(err)
              return []

      
      if exists_arg('to_json',arg): rez=to_json(rez)

      #if exists_arg('to_tmpl',arg):
      #  self.tmpl_vars[arg['to_tmpl']]=rez

      #if exists_arg('perpage',arg) & exists_arg('maxpage',arg):return arg['maxpage']
      return rez

      #print("query:")
      #print({'arg':arg})


    def save(self, **arg):
        self.connect.ping()  # reconnecting mysql
        self.error_str=''
        arg['method']='save'
        if not exists_arg('table',arg):
          out_error(self,"FreshDB::"+arg['method']+" not set attr table",arg)
          return 
        
        if not exists_arg('data',arg):
          out_error(self,"FreshDB::"+arg['method']+" not set attr data",arg)
          return 

        
        exists_fields=self.desc(table=arg['table'])
        data=arg['data']
        if self.error_str :
          print('after desc:',self.error_str)
          return 
        
        

        insert_fields=[]
        insert_vopr=[]
        insert_values=[]

        update_names=[]
        for name in data.keys():
          if name in exists_fields:
            func=get_func(data[name])
            if func:
              insert_fields.append('`'+name+'`')
              #insert_values.append(func)
              update_names.append('`'+name+'`='+func)
            else:
              insert_fields.append(name)
              insert_vopr.append('%s')
              insert_values.append(data[name])
              update_names.append('`'+name+'`=%s')

        
        if exists_arg('update',arg):
              if not exists_arg('where',arg):
                out_error(self,"FreshDB::"+arg['method']+" not set attr where",arg)
                return False
              
              arg['query']='UPDATE '+arg['table']+' SET '+','.join(update_names) + ' WHERE '+arg['where']
        else:
              q=''
              if exists_arg('replace',arg):
                q='REPLACE'
              else:
                q='INSERT'
              if exists_arg('ignore',arg):
                q+=' IGNORE'
                
              q +=' INTO '+arg['table'] +'(' + ','.join(insert_fields)+') VALUES (' + ','.join(insert_vopr) + ')'
              arg['query']=q

        arg['values']=insert_values

        cur = pymysql.cursors.DictCursor(self.connect)
      
        try:
          self.execute(cur,arg)
        except pymysql.err.IntegrityError as err:
          if 'errors' in arg: arg['errors'].append(str(err))
          out_error(self,"FreshDB::"+str(err),arg)
        return cur.lastrowid