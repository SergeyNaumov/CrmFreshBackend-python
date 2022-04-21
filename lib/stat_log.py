# Данный модуль нужен для ведение статистики скриптов
def scriptToLog(script):
    return not(script in ('autocomplete','anna','NewsList','VideoList','wysiwyg','multiconnect'))
    
    
def notRecord(r,script,config):
    qs=r['query_string'].decode('ascii')
    if( (r['path']=='/table/conference_table') and (qs=='limit=6') ):
        print('TRUE')
        return True
    print('FALSE')
    return False
    

def stat_log_record(s,request):
  if not(s.config['stat_log']):
      return
  
  
  r=dict(request)
  if 'path' in r:
    path=str(r['path'])
    arr=path.split('/')
    method=str(r['method'])
    if method=='POST':
        #print('REQUEST:',r)
        pass
    script=''
    config=''
    if len(arr)>=3 and scriptToLog(arr[1]):
        script=arr[1]
        config=arr[2]
    elif arr[1] in ('startpage'):
        script=arr[1]
    
    
    if script:
        if notRecord(r,script,config):
            return        
        s.db.save(
            table='stat_log',
            data={
                'script':script,
                'config':config,
                'manager_id':s.manager['id']
            }
        )

        
