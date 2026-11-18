# -*- coding: utf-8 -*-
"""Картинки блоков проекта (block-images) — менеджерская сторона.

Та же папка и те же правила, что у конструктора страниц
(routes/svcmsadmin/page_constructor/__init__.py): файлы лежат в
<engine_files>/project_<id>/block-images[/<folder>]/ и рендерятся движком
сайта по относительному пути block-images/… (см. block/about.html).

Нужно для режима блоков «Текстовых блоков»: в /manager фото блока
выбирается и загружается оттуда же, откуда его берёт конструктор, поэтому
картинка остаётся общей для обеих сторон.
"""

import io
import os
import re

from config import config as sysconfig

# Транслит для имён загружаемых картинок (рус. → латиница).
_TRANSLIT = {
  'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e',
  'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
  'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
  'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '',
  'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
}

_RASTER_EXT = {'jpg', 'jpeg', 'png', 'webp', 'gif', 'bmp', 'tif', 'tiff'}


def _paths():
  return sysconfig.get('paths') or {}


def files_root():
  """Корень файлов проектов (у движка: sites/files)."""
  return _paths().get('engine_files') or './files'


def files_url():
  """URL-префикс файлов проектов (nginx отдаёт /files/...)."""
  return (_paths().get('engine_files_url') or '/files').rstrip('/')


def folder_slug(folder):
  """Санитайз подпапки block-images: только [a-z0-9_-]."""
  return re.sub(r'[^a-z0-9_-]', '', (folder or '').lower()).strip('-_')


def slugify_filename(name):
  """Имя файла: латиница/цифры/.-_, пробелы и кириллица → транслит/дефис."""
  name = (name or '').strip()
  base, dot, ext = name.rpartition('.')
  if not dot:
    base, ext = name, ''
  out = []
  for ch in base.lower():
    if ch in _TRANSLIT:
      out.append(_TRANSLIT[ch])
    elif re.match(r'[a-z0-9._-]', ch):
      out.append(ch)
    else:
      out.append('-')
  slug = re.sub(r'-+', '-', ''.join(out)).strip('-_.') or 'image'
  return slug + (('.' + ext.lower()) if ext else '')


def images_dir(project_id, folder=''):
  d = os.path.join(files_root(), 'project_%s' % project_id, 'block-images')
  sub = folder_slug(folder)
  if sub:
    d = os.path.join(d, sub)
  os.makedirs(d, exist_ok=True)
  return d


def list_images(project_id, folder=''):
  """Список картинок проекта: {success, errors, filesBase, folder, files}."""
  sub = folder_slug(folder)
  d = images_dir(project_id, sub)
  prefix = 'block-images/' + (sub + '/' if sub else '')
  base = '%s/project_%s/%s' % (files_url(), project_id, prefix)
  files = []
  for name in sorted(os.listdir(d)):
    if name.startswith('.') or not os.path.isfile(os.path.join(d, name)):
      continue
    files.append({'name': name, 'path': prefix + name, 'url': base + name})
  return {
    'success': True, 'errors': [],
    'filesBase': '%s/project_%s/' % (files_url(), project_id),
    'folder': sub,
    'files': files,
  }


def optimize_to_webp(content):
  """Растровую картинку → webp: exif-поворот, альфа, даунскейл, качество."""
  from PIL import Image, ImageOps

  img = Image.open(io.BytesIO(content))
  try:
    img = ImageOps.exif_transpose(img)
  except Exception:
    pass
  has_alpha = img.mode in ('RGBA', 'LA') or (
    img.mode == 'P' and 'transparency' in img.info)
  img = img.convert('RGBA' if has_alpha else 'RGB')
  max_side = int(_paths().get('block_images_max_side') or 1920)
  quality = int(_paths().get('block_images_quality') or 82)
  w, h = img.size
  m = max(w, h)
  if max_side and m > max_side:  # только уменьшаем
    scale = max_side / float(m)
    img = img.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
  buf = io.BytesIO()
  img.save(buf, format='WEBP', quality=quality, method=6)
  return buf.getvalue()


def save_image(project_id, folder, filename, raw):
  """Сохранить загруженную картинку: {success, errors, name, path, url}."""
  orig = filename or 'file'
  ext = orig.rsplit('.', 1)[-1].lower() if '.' in orig else ''
  if ext == 'svg':
    content, out_ext = raw, 'svg'
  elif ext in _RASTER_EXT:
    try:
      content, out_ext = optimize_to_webp(raw), 'webp'
    except Exception:
      return {'success': False, 'errors': ['не удалось обработать изображение']}
  else:
    return {'success': False,
            'errors': ['поддерживаются jpg, png, webp, gif, bmp, svg']}

  sub = folder_slug(folder)
  d = images_dir(project_id, sub)
  base_name = slugify_filename(orig).rsplit('.', 1)[0] or 'image'
  target = os.path.join(d, base_name + '.' + out_ext)
  i = 1
  while os.path.exists(target):
    target = os.path.join(d, '%s-%d.%s' % (base_name, i, out_ext))
    i += 1

  with open(target, 'wb') as f:
    f.write(content)

  fname = os.path.basename(target)
  prefix = 'block-images/' + (sub + '/' if sub else '')
  return {
    'success': True, 'errors': [],
    'name': fname,
    'path': prefix + fname,
    'url': '%s/project_%s/%s%s' % (files_url(), project_id, prefix, fname),
  }
