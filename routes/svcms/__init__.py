#from fastapi import FastAPI, APIRouter
from fastapi import APIRouter
from lib.engine import s
#from lib.send_mes import send_mes
#from lib.form_control import check_rules, is_email, is_phone
#from lib.core import exists_arg

from .left_menu import left_menu




router = APIRouter()



#@router.get('/download/action_plan')
#def x():
#    return {'ok':1}

@router.get('/left-menu')
def controller_left_menu():
    return left_menu()



