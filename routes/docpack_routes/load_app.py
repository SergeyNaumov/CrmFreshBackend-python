from db import db
import os.path 
from fastapi.responses import HTMLResponse
from .check_document_data import check_dogovor, out_debug
from .num_to_text import num_to_text
from .response_doc import response_doc

async def load_app(app_id,ext:str,need_print: int, debug=0):
    print('load app begin')
    dp = await db.query(
        query=f'''
            SELECT
                app.id, app.service_id, app.num_of_dogovor app_num_of_dogovor,
                app.summ app_summ, app.summ_post app_summ_post, DATE_FORMAT(app.registered,%s) app_from,
                m.name manager_name,
                t.header tarif_name,t.id tarif_id,
                t.summ tarif_summ, t.cnt_orders tarif_cnt_orders,
                t.count_days tarif_count_days, t.percent_pob, t.comment tarif_comment,
                dp.registered dp_registered, dp.id dp_id, dp.tarif_id,
                ur_lico.firm ur_lico_firm, ur_lico.gen_dir_fio_im ur_lico_gen_dir_fio_im, ur_lico.gen_dir_fio_rod ur_lico_gen_dir_fio_rod,
                ur_lico.buh_fio_im ur_lico_buh_fio_im, ur_lico.buh_fio_rod ur_lico_buh_fio_rod, ur_lico.inn ur_lico_inn, ur_lico.ogrn ur_lico_ogrn,
                ur_lico.kpp ur_lico_kpp, ur_lico.rs ur_lico_rs, ur_lico.ks ur_lico_ks, ur_lico.bik ur_lico_bik, ur_lico.bank ur_lico_bank,
                ur_lico.attach ur_lico_attach, ur_lico.ur_address ur_lico_ur_address, ur_lico.address ur_lico_address,
                ur_lico.attach_pechat ur_lico_attach_pechat,ur_lico.gendir_podp ur_lico_gendir_podp, ur_lico.buh_podp ur_lico_buh_podp,
                ur_lico.gen_dir_f_in ur_lico_gen_dir_f_in, d.number dogovor_number,
                d.registered dogovor_registered, dp.ur_lico_id,
                DATE_FORMAT(d.registered,%s) dogovor_from,
                app.num_of_dogovor app_num_of_dogovor,

                blank.attach app_blank

            FROM
                user u
                JOIN docpack dp ON dp.user_id = u.id
                JOIN dogovor d ON d.docpack_id=dp.id
                JOIN dogovor_app app ON app.dogovor_id=dp.id
                LEFT JOIN service s ON app.service_id=s.id
                LEFT JOIN tarif t ON (t.id = dp.tarif_id)
                LEFT JOIN buhgalter_card_requisits bcr ON bcr.user_id = u.id
                LEFT JOIN manager m ON (u.manager_id =m.id)


                LEFT JOIN blank_document blank ON (blank.id = s.blank_id)
                LEFT JOIN ur_lico ON (ur_lico.id=dp.ur_lico_id)
            WHERE app.id=%s GROUP BY u.id ORDER BY bcr.main LIMIT 1
        ''',
        #debug=1,
        values=['%e %M %Y', '%e %M %Y', app_id],onerow=1
        #values=['%e %M %Y', '%e %M %Y', '%e %M %Y', app_id],onerow=1
    )
    dp['app_fields']={}
    fields = await db.query(
        query=f"""
            SELECT
              sf.name, wt.value
            FROM
              dogovor_app_values wt
              JOIN service_field sf ON sf.id=wt.field_id
            WHERE wt.dogovor_app_id={app_id}
            ORDER BY sf.sort
        """
    )
    for f in fields:
        dp['app_fields'][f['name']]=f['value']



    #print('blank: ',blank)

    if not(dp):
        return {'error': f'пакет документов №{docpack_id} не найден'}

    blank=''
    if dp['app_blank']:
        blank=f"./files/blank_document/{dp['app_blank']}"

    if not(blank):
        return {'error': f'не найден бланк для приложения (service_id: {dp["service_id"]})'}



    #return dp

    # Проверка бланка
    if not os.path.exists(blank):
        message=f'''
        <div style="color: red;">Бланк документа не найден: {blank}!</div><br>
        Возможно, он был удалён<br><br>

        Подробности:
            Тариф: <a href="/edit_form/tarif/{dp['tarif_id']}">{dp['tarif_name']}</a><br>
            tarif_id: {dp['tarif_name']}<br>
            Бланк счёта: <a href="/edit_form/blank_document/{dp['b_bill_id']}">{dp['b_bill_header']}</a><br>
        '''
        return HTMLResponse(message)

    for a in ('ur_lico_gendir_podp', 'ur_lico_buh_podp', 'ur_lico_attach_pechat'):
        if dp[a]: dp[a]=f'./files/ur_lico/{dp[a]}'

    dp['app_summ_prop']=num_to_text(dp['app_summ'])
    dp['app_summ_post_prop']=num_to_text(dp['app_summ_post'])

    if debug:
        return out_debug(dp)



    empty='./routes/docpack_routes/img/empty.png'
    print('NEED PRINT:', need_print)
    if not(need_print):
        dp['ur_lico_gendir_podp']=empty
        dp['ur_lico_attach_pechat']=empty


    replace_images=[
        ['ur_lico_gendir_podp',dp['ur_lico_gendir_podp'] ],
        ['ur_lico_attach_pechat',dp['ur_lico_attach_pechat'] ]
    ]

    output_filename=f"Приложение к договору №{dp['dogovor_number']}"
    return response_doc(blank, output_filename, ext, dp, replace_images) # images_list

    #return dp
