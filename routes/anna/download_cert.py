from fastapi import APIRouter
from lib.engine import s
from config import config

router = APIRouter()


@router.get('/')
def download_cert(): 
  return [1,2]
