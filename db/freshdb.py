import aiomysql, asyncio
from .functions import *


loop = asyncio.get_event_loop()

class FreshDB():
    def __init__(self,settings):
        self.settings = settings ; self.error_str='' ; self.pool = None

    async def create_pool(self, **arg):
        settings=self.settings
        self.pool = await aiomysql.create_pool(
            minsize=settings.get('min_size_pool',2),
            maxsize=settings.get('max_size_pool',20),
            host=settings.get('host'),
            port=settings.get('port', 3306),
            user=settings.get('user'),
            password=settings.get('password',''),
            db=settings['dbname'],
            loop=loop,
            autocommit=settings.get('autocommit',True)
        )

    async def close_pool(self):
        if self.pool:
            self.pool.close()
            #await self.pool.await_closed()



    async def desc(self,**arg):
        self.error_str=''
        arg['method']='desc' ; table=arg.get('table')
        if not(table):
            out_error(self,"FreshDB::desc not set attr table",arg)
            return {}
        else:
            result = {}
            errors=[]
            fields = await self.query(query=f"desc {table}", errors=errors)
            if self.error_str:

                if 'errors' in arg:
                    arg['errors']+=errors
                return {}

            for f in fields:
                result[ f['Field'] ] = f

            return result

    async def query(self, **arg):

        self.error_str=''
        query=arg.get('query') ; values=arg.get('values',[])

        def get_cursor(conn):
            if arg.get('onevalue'):
                return conn.cursor()
            return conn.cursor(aiomysql.DictCursor)

        async with self.pool.acquire() as conn:
            async with get_cursor(conn) as cur:
                # out debug
                if(arg.get('debug')):
                    print(arg['query'])
                    if arg.get('values'):
                        print(arg['values'])
                result = None
                try:
                    await cur.execute(query, values)

                    if arg.get('onevalue'):
                        result = await cur.fetchone()
                        if result:
                            result=result[0]

                    elif arg.get('onerow'):
                        result = await cur.fetchone()
                    else:
                        #result = await cur.fetchone()
                        result = await cur.fetchall()

                    if arg.get('massive'):
                        result=massive_transform(result)

                    elif arg.get('tree_use'):
                        result=tree_use_transform(result)


                    if arg.get('str'):
                        result = [str(x) for x in result]
                    #    return ['585', '1347', '7576', '8311', '10653', '11691', '11709', '11836', '11928', '12060', '12066', '12068']
                    if arg.get('debug'):
                        print('RESULT:',result)
                    #return result
                except Exception as e:
                    print('Exception')
                    out_error(self,e,arg)
                    return


                return result
    async def get(self, **arg):
        arg['query']=get_query(self,arg)

        result=await self.query(query=arg['query'],values=arg.get('values',[]))
        if arg.get('massive'):
            result=massive_transform(result)
        elif arg.get('tree_use'):
            result=tree_use_transform(result)

        if arg.get('str'):
            rez_to_str(result)
        return result
    async def getrow(self, **arg):
        self.error_str=''
        arg['method']='getrow'
        query=get_query(self,arg)
        #print('query:',query)
        if self.error_str:
            return {}

        return await self.query(
            query=query,
            limit=1,
            onerow=1,
            debug=arg.get('debug',0),
            values=arg.get('values',[])
        )

    async def save(self, **arg):
        self.error_str=''
        table=arg.get('table') ; data=arg.get('data')
        if not(table):
            out_error(self,"FreshDB::save not set attr table",arg)
            return

        if not(data) or not(len(data)):
            out_error(self,"FreshDB::save not set attr data",arg)
            return
        errors=[]
        if 'errors' in arg:
            errors=arg['errors']
        exists_fields=await self.desc(table=arg['table'],errors=errors )

        if self.error_str:
          #if 'errors' in arg:
            #arg['errors']+=arg['e'](self.error_str)
            #print('Error_str errors:',arg['errors'])
          print('FreshDB::save after desc:',self.error_str)

          return

        insert_fields=[] ; insert_vopr=[] ; insert_values=[] ; update_names=[]
        for name in data:
            if name in exists_fields:
                if func:=get_func(data[name]):
                  insert_fields.append('`'+name+'`')
                  insert_vopr.append(func)
                  update_names.append('`'+name+'`='+func)
                else:
                  insert_fields.append('`'+name+'`')
                  insert_vopr.append('%s')
                  insert_values.append(data[name])
                  update_names.append('`'+name+'`=%s')

        query=''
        if arg.get('update'):
            if not(arg.get('where')):
                out_error(self,"FreshDB::save not set attr where",arg)
                return False
            query=f"UPDATE {arg['table']} SET {','.join(update_names)} WHERE {arg['where']}"

        else:
            if arg.get('replace'):
                query='REPLACE'
            else:
                query='INSERT'

            if arg.get('ignore'):
                query+=' IGNORE'

            query+=f" INTO {arg['table']}({','.join(insert_fields)}) VALUES({','.join(insert_vopr)})"

        arg['values']=insert_values

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                try:
                    await cur.execute(query, insert_values)
                    return cur.lastrowid
                except Exception as e:
                    out_error(self,e,arg)
                    return False




