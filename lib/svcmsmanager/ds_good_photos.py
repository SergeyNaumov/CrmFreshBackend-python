# Фоновая обработка изображений после импорта товаров ds_good.
#
# Задачу (config='ds_good_import', action='process_photos') ставит в очередь
# crm_background конфиг configs/svcmsmanager/ds_good_import. Здесь скачиваем
# (или копируем локально) фото, конвертируем в webp, делаем миниатюры и
# создаём записи в ds_good_galery.
#
# Модуль импортируется из routes/parser_excel/__init__.py -- регистрация
# обработчика должна произойти в каждом процессе uvicorn при старте.

import os
import re
import shutil
import asyncio
import importlib

from lib.background import register_task
from lib.core import get_name_and_ext, random_filename
from lib.resize import resize_one, convert_to_webp, out_ext_for, is_raster_ext

MAX_BYTES = 15 * 1024 * 1024
DOWNLOAD_TIMEOUT = 20
ALLOWED_EXTS = {'jpg', 'jpeg', 'png', 'webp', 'gif'}

# Фолбэк, если конфиг ds_good недоступен (должен совпадать с полем photos).
DEFAULT_FIELD = {
  'name': 'photo',
  'filedir': './files/project_[project_id]/good_galery',
  'to_webp': True,
  'resize': [
    {'file': '<%filename_without_ext%>_mini1.<%ext%>', 'size': '200x200', 'quality': '85'},
    {'file': '<%filename_without_ext%>_mini2.<%ext%>', 'size': '320x320', 'quality': '85'},
    {'file': '<%filename_without_ext%>_mini3.<%ext%>', 'size': '600x600', 'quality': '84'},
  ],
}


def _photo_field(project_id):
  # Конфиг поля "Фотографии товара" из ds_good -- единый источник resize/filedir.
  field = None
  try:
    mod = importlib.import_module('configs.svcmsmanager.ds_good')
    for f in mod.form.get('fields', []):
      if f.get('name') == 'photos':
        for child in f.get('fields', []):
          if child.get('name') == 'photo':
            field = dict(child)
            break
        break
  except Exception:
    field = None

  if not field:
    field = dict(DEFAULT_FIELD)

  filedir = str(field.get('filedir') or DEFAULT_FIELD['filedir'])
  field['filedir'] = filedir.replace('[project_id]', str(project_id))
  return field


def _local_path(url, project_id):
  # Ссылка на файл этого же проекта -> локальный путь (сеть не нужна).
  m = re.search(r'/files/project_%d/([^?#\s]+)' % project_id, url)
  if not m:
    return None
  rel = m.group(1)
  if '..' in rel or not re.match(r'^[a-zA-Z0-9_\-/\.]+$', rel):
    return None
  return f'./files/project_{project_id}/{rel}'


def _url_ext(url, content_type=None):
  ext = os.path.splitext(url.split('?')[0].split('#')[0])[1].lower().lstrip('.')
  if ext in ALLOWED_EXTS:
    return ext
  ct = (content_type or '').lower()
  if 'webp' in ct: return 'webp'
  if 'png' in ct: return 'png'
  if 'gif' in ct: return 'gif'
  if 'jpeg' in ct or 'jpg' in ct: return 'jpg'
  return None


async def _download(url):
  # requests в отдельном потоке: на проде Python 3.8 и нет aiohttp.
  def fetch():
    import requests
    try:
      resp = requests.get(url, timeout=DOWNLOAD_TIMEOUT, stream=True)
    except Exception:
      return None, None
    if resp.status_code != 200:
      return None, None
    chunks = []
    size = 0
    for chunk in resp.iter_content(65536):
      size += len(chunk)
      if size > MAX_BYTES:
        return None, None
      chunks.append(chunk)
    return b''.join(chunks), resp.headers.get('Content-Type')

  try:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, fetch)
  except Exception:
    return None, None


def _unique_name(filedir, base, ext):
  name = f'{base}.{ext}'
  i = 0
  while os.path.exists(f'{filedir}/{name}'):
    i += 1
    name = f'{base}_{i}.{ext}'
  return name


def _process_file(field, filedir, filename_without_ext, ext):
  # webp-конвертация + миниатюры. Возвращает имя файла для БД или None.
  if field.get('to_webp') and is_raster_ext(ext) and ext.lower() != 'webp':
    new_name = f'{filename_without_ext}.webp'
    if not convert_to_webp(f'{filedir}/{filename_without_ext}.{ext}',
                           f'{filedir}/{new_name}', quality=85):
      return None
    try:
      os.remove(f'{filedir}/{filename_without_ext}.{ext}')
    except OSError:
      pass
    ext = 'webp'

  if field.get('resize'):
    out_ext = out_ext_for(field, ext)
    for r in field['resize']:
      if not r.get('size'):
        continue
      width, height = r['size'].split('x')
      resize_filename = str(r['file']).replace(
        '<%filename_without_ext%>', filename_without_ext
      ).replace('<%ext%>', out_ext)
      resize_one(
        fr=f'{filedir}/{filename_without_ext}.{ext}',
        to=f'{filedir}/{resize_filename}',
        width=width,
        height=height,
        quality=r.get('quality'),
        to_webp=field.get('to_webp'),
      )

  return f'{filename_without_ext}.{ext}'


async def _add_photo(db, field, filedir, project_id, good_id, url):
  ext = None
  name = None

  local = _local_path(url, project_id)
  if local and os.path.isfile(local):
    ext = (get_name_and_ext(local)[1] or '').lower()
    if ext not in ALLOWED_EXTS:
      return None
    base = random_filename()
    name = _unique_name(filedir, base, ext)
    shutil.copyfile(local, f'{filedir}/{name}')
  else:
    data, content_type = await _download(url)
    if data is None:
      return None
    ext = _url_ext(url, content_type)
    if not ext:
      return None
    base = random_filename()
    name = _unique_name(filedir, base, ext)
    with open(f'{filedir}/{name}', 'wb') as fh:
      fh.write(data)

  filename_without_ext = os.path.splitext(name)[0]
  db_value = _process_file(field, filedir, filename_without_ext, ext)
  if not db_value:
    # битый/неподдерживаемый файл -- удаляем и пропускаем
    try:
      os.remove(f'{filedir}/{name}')
    except OSError:
      pass
    return None

  max_sort = await db.query(
    query='SELECT max(sort) FROM ds_good_galery WHERE good_id=%s',
    values=[good_id], onevalue=1, errors=[]) or 0

  new_id = await db.save(
    table='ds_good_galery',
    data={
      'project_id': project_id,
      'good_id': good_id,
      'header': os.path.basename(url.split('?')[0])[:255],
      'photo': db_value,
      'enabled': 1,
      'sort': int(max_sort) + 1,
    },
    errors=[])

  return db_value if new_id else None


async def run_import_photos(ctx):
  project_id = int(ctx.params.get('project_id') or ctx.project_id or 0)
  jobs = ctx.params.get('jobs') or []
  if not project_id:
    raise ValueError('не указан project_id')

  db = ctx.db
  field = _photo_field(project_id)
  filedir = field['filedir']
  os.makedirs(filedir, exist_ok=True)

  added = 0
  skipped = 0
  errors = []
  total = len(jobs) or 1

  for idx, job in enumerate(jobs):
    good_id = int(job.get('good_id') or 0)
    urls = job.get('urls') or []
    if not good_id:
      continue

    rows = await db.query(
      query='SELECT photo FROM ds_good_galery WHERE good_id=%s',
      values=[good_id], errors=[])
    existing = set()
    for r in (rows or []):
      photo = str(r.get('photo') or '').split(';')[0]
      if photo:
        existing.add(os.path.basename(photo))

    for url in urls:
      basename = os.path.basename(url.split('?')[0].split('#')[0])
      if basename and basename in existing:
        skipped += 1
        continue
      try:
        db_value = await _add_photo(db, field, filedir, project_id, good_id, url)
      except Exception as e:
        errors.append(f'товар {good_id}: {url}: {e}')
        continue
      if db_value:
        existing.add(os.path.basename(db_value))
        added += 1
      else:
        skipped += 1

    if idx % 5 == 0:
      await ctx.progress(int((idx + 1) * 100 / total), f'Фото: {idx + 1}/{total}')

  await ctx.progress(100, f'Добавлено фото: {added}, пропущено: {skipped}')
  return {'added': added, 'skipped': skipped, 'errors': errors[:50]}


register_task('ds_good_import', 'process_photos', run_import_photos)
