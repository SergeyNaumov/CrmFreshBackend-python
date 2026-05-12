#from lib.engine import s
from lib.core import get_name_and_ext, gen_pas
import re, os
from base64 import b64decode
from time import time
from .go_parse import go_parse

def error(e):
    return { 'success':0, 'errors':[e] }
    
async def preload(parser, R):
    orig_name=R.get('orig_name','')
    src=R.get('src','')

    name, ext = get_name_and_ext(orig_name)
    if name and ext and src:
        rez = re.search(r'^data:(.+?);base64,(.+)',src)
        if rez:
            mime=rez[1]
            filename=f"{int(time())}_{gen_pas(3)}.{ext}" #time().'_'.substr(rand(),3,3).'.'.$ext;
            tmp_dir=parser.get('tmp_dir')
            if not(tmp_dir):
                return error('не указан tmp_dir')

            if not os.path.isdir(tmp_dir):
                try:
                  os.mkdir(tmp_dir)
                except FileExistsError:
                  return error(f'не удалось создать директорию {tmp_dir}')



            fullname=f"{tmp_dir}/{filename}"

            try:
                _bytes = b64decode(rez[2], validate=True)
                with open(fullname, "wb") as file:
                    file.write(_bytes)

            except Exception as e:
                return error(f"произошла ошибка при записи в {fullname}: {str(e)}")

            return await go_parse(
                filename=filename,
                tmp_dir=tmp_dir,
                limit=30
            )
        else:
            return error('отсутствует параметр src, либо он не соответствует base64')

    return error('не корректный параметр orig_name')
