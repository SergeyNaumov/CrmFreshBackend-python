from fastapi import APIRouter
from lib.core import cur_year,cur_date, success, exists_arg
router = APIRouter()

# Форма редактирования
@router.get('/edit-form/{config}/{id}')
async def edit_form(config,id):
  return {'config':config,'id':id}

# форма добавления элемента
@router.get('/edit-form/{config}')
async def insert_form(config):
  return  {'config':config}