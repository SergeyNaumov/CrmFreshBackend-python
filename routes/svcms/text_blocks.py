# API режима блоков сервиса «Текстовые блоки» (svcms manager).
#
#   GET  /svcms/text-block/block-images?folder=…   — картинки проекта
#   POST /svcms/text-block/block-images/upload     — загрузка картинки
#
# Папка и правила те же, что у конструктора страниц (block-images проекта):
# фото блока правится в /manager и читается движком сайта. Проект берём из
# менеджерской сессии (request.state.project), чужой проект недоступен.

from fastapi import APIRouter, File, Form, Request, UploadFile

from lib.svcmsmanager import block_images


router = APIRouter()


def _project_id(request):
  project = getattr(request.state, 'project', None) or {}
  try:
    return int(project.get('project_id') or 0)
  except (TypeError, ValueError):
    return 0


@router.get('/text-block/block-images')
async def block_images_list(request: Request, folder: str = ''):
  """Список картинок проекта для пикера редактора блока."""
  pid = _project_id(request)
  if not pid:
    return {'success': False, 'errors': ['не выбран проект'], 'files': []}
  return block_images.list_images(pid, folder)


@router.post('/text-block/block-images/upload')
async def block_images_upload(request: Request,
                              folder: str = Form(''),
                              file: UploadFile = File(...)):
  """Загрузка картинки в files/project_<id>/block-images[/<folder>]/."""
  pid = _project_id(request)
  if not pid:
    return {'success': False, 'errors': ['не выбран проект']}
  raw = await file.read()
  return block_images.save_image(pid, folder, file.filename or '', raw)
