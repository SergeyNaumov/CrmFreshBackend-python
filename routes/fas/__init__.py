#from fastapi import FastAPI, APIRouter
from fastapi import APIRouter
from lib.engine import s
#from lib.send_mes import send_mes
#from lib.form_control import check_rules, is_email, is_phone
from .api import router as router_api
from .left_menu import left_menu
from routes.docpack_routes.num_to_text import num_to_text
from routes.docpack_routes.response_doc import response_doc
import os

router = APIRouter()



#@router.get('/download/action_plan')
#def x():
#    return {'ok':1}
router.include_router(router_api, prefix="/api")

@router.get('/left-menu')
async def controller_left_menu():
    return await left_menu()

@router.get('/download-act/{ur_lico_id}/{act_id}/{ext}/{need_print}')
async def download_act(ur_lico_id:int, act_id:int, ext:str, need_print:int):
    a=await s.db.query(

        query="""
            SELECT
                act2.number act_number, DATE_FORMAT(act2.dat,%s) act_from,
                act2.summa act_summ, act2.service, concat('№',d.number,' от ',DATE_FORMAT(d.registered,%s),' г.') osnovanie,
                ul.firm ur_lico_firm, ul.inn ur_lico_inn, ul.address ur_lico_address,
                ul.rs ur_lico_rs, ul.ks ur_lico_ks, ul.bik ur_lico_bik, ul.bank ur_lico_bank,
                ul.gendir_podp ur_lico_gendir_podp, ul.attach_pechat ur_lico_attach_pechat,
                ul.buh_podp ur_lico_buh_podp, ul.gen_dir_f_in ur_lico_gen_dir_f_in,
                u.firm, u.inn, act2.docpack_id

            FROM
                act2
                JOIN docpack dp ON dp.id=act2.docpack_id
                JOIN dogovor d ON d.docpack_id=dp.id
                LEFT JOIN ur_lico ul ON ul.id=dp.ur_lico_id
                LEFT JOIN user u ON u.id=dp.user_id
            WHERE
                act2.id=%s and act2.ur_lico_id=%s
        """,
        values=['%e %M %Y', '%e.%m.%Y', act_id, ur_lico_id],
        onerow=1

    )
    if not(a):
        return 'акт не найден'
    if not(a['docpack_id']):
        return 'не найдена связь с пакетом документов (пакет документов отсутствует для акта)'

    a['act_summ_prop']=num_to_text(a['act_summ'])
    blank=f"./files/blank_act2.docx"
    if not os.path.exists(blank):
        return "не найден бланк акта /files/blank_act2.docx"

    empty='./routes/docpack_routes/img/empty.png'

    if not(need_print):
        a['ur_lico_gendir_podp']=empty
        a['ur_lico_attach_pechat']=empty

    for f in ('ur_lico_gendir_podp', 'ur_lico_buh_podp', 'ur_lico_attach_pechat'):
        if a[f]: a[f]=f'./files/ur_lico/{a[f]}'

    replace_images=[
        ['ur_lico_gendir_podp',a['ur_lico_gendir_podp'] ],
        ['ur_lico_attach_pechat',a['ur_lico_attach_pechat'] ]
    ]
    output_filename=f"Акт №{a['act_number']}"
    #a['osnovanie']=f"№{a['dogovor_number']} от {a['dogovor_registered']}г."
    #return a
    return response_doc(blank, output_filename, ext, a, replace_images) # images_list



