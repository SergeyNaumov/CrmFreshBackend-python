import os, re
from fastapi import APIRouter
from fastapi.responses import FileResponse

# Скачивание временных файлов, сформированных серверными инструментами
# (экспорт в xlsx и т.п.). Авторизация -- общая, через middleware движка.
router = APIRouter()

TMP_DIR='files/tmp'


@router.get('/download_tmp/{filename}')
async def download_tmp(filename: str):
    if not(re.match(r'^[a-zA-Z0-9_\-\.]+$',filename)):
        return {'success':0,'errors':['некорректное имя файла']}
    full=f"{TMP_DIR}/{filename}"
    if not(os.path.isfile(full)):
        return {'success':0,'errors':['файл не найден']}
    return FileResponse(path=full, filename=filename)
