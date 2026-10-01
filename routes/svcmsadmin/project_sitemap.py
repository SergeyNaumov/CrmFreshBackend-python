import os
from xml.sax.saxutils import escape

from fastapi import APIRouter, Request
from pydantic import BaseModel

from lib.background import enqueue, register_task


router = APIRouter()


class SitemapStart(BaseModel):
  project_id: int


# Фоновая генерация sitemap.xml для проекта.
# Файл кладём в files/project_<id>/sitemap.xml (каталог files смонтирован во фронт).
# При даче реального ТЗ путь/набор URL легко уточнить -- каркас от этого не зависит.
async def run_project_sitemap(ctx):
  pid = int(ctx.params.get('project_id') or 0)
  if not pid:
    raise ValueError('не указан project_id')

  await ctx.progress(10, 'Читаем домены проекта')
  domains = await ctx.db.query(
    query='SELECT domain, our_domain, is_ssl FROM domain WHERE project_id=%s ORDER BY our_domain DESC, domain',
    values=[pid],
    errors=[],
  )
  if not domains:
    raise ValueError(f'у проекта {pid} нет доменов')

  await ctx.progress(40, 'Собираем адреса')
  urls = []
  for d in domains:
    scheme = 'https' if d.get('is_ssl') else 'http'
    host = (d.get('domain') or '').strip()
    if host:
      urls.append(f'{scheme}://{host}/')

  menus = await ctx.db.query(
    query="SELECT url FROM project_menu WHERE project_id=%s AND url NOT LIKE '.%%' AND url<>''",
    values=[pid],
    errors=[],
  )
  primary = urls[0].rstrip('/') if urls else ''
  for m in menus:
    u = (m.get('url') or '').strip()
    if u and not u.startswith(('http://', 'https://', '/manager')):
      urls.append(f'{primary}/{u.lstrip("/")}')

  await ctx.progress(70, 'Формируем sitemap.xml')
  body = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  ]
  for u in urls:
    body.append(f'  <url><loc>{escape(u)}</loc></url>')
  body.append('</urlset>')
  content = '\n'.join(body)

  target_dir = os.path.join(os.getcwd(), 'files', f'project_{pid}')
  os.makedirs(target_dir, exist_ok=True)
  target = os.path.join(target_dir, 'sitemap.xml')
  with open(target, 'w', encoding='utf-8') as f:
    f.write(content)

  await ctx.progress(100, 'Готово')
  return {'file': f'files/project_{pid}/sitemap.xml', 'urls': len(urls)}


register_task('svcmsadmin', 'project_sitemap', run_project_sitemap)


@router.post('/project/sitemap/start')
async def project_sitemap_start(request: Request, r: SitemapStart):
  manager = request.state.manager or {}
  task_id = await enqueue(
    config='svcmsadmin',
    action='project_sitemap',
    params={'project_id': r.project_id},
    admin_id=manager.get('id'),
    project_id=r.project_id,
  )
  return {'success': True, 'errors': [], 'task_id': task_id}
