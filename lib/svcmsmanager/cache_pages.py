import pickle
from pymemcache.client.base import Client
from pymemcache import serde
# Данный модуль нужен для сброса кэша сайта

client = Client(('127.0.0.1',11211),
    serializer=serde.python_memcache_serializer,
    deserializer=serde.python_memcache_deserializer
)

def url_ok(url):
    if '{{' in url or url in ['/capcha']:
        return False
    return True

def get_cache_word(domain,url,query_string):
    cache_word=domain+':'+url
    if query_string:
        cache_word+='?'+str(query_string)
    return cache_word


def clear_cache_for_domain(domain):
# Очищаем кэш для домена
    
    key_for_keylist='__keylist:'+domain
    try:
        print('Clear_cache_for_domain')
        #print('clear_cache_for_domain')
        key_for_keylist='__keylist:'+domain
        keylist=client.get(key_for_keylist)
        #print('keylist:',keylist)
        if keylist:
            for k in keylist:
                client.delete(k)
        
        # Обновляем keylist:
        client.set(key_for_keylist,{})

    except ConnectionRefusedError as e:
        print('not connected to memcached')

def pages_for_domain(domain):
    key_for_keylist='__keylist:'+domain
    keylist=client.get(key_for_keylist)
    res=[]
    if keylist:
        for k in keylist: res.append(k)
    return res
