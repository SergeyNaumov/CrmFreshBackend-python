import os
import random
import time

from docxtpl import DocxTemplate
from subprocess import PIPE, run

from .diadoc_tools import num_to_text

empty = './routes/docpack_routes/img/empty.png'


def gen_tmpl_prefix():
    return str(int(time.time())) + '_' + ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUV0123456780') for i in range(5))


def response_doc(template_file, data, replace_images):
    doc = DocxTemplate(template_file)

    for i in replace_images:
        try:
            doc.replace_pic(i[0], i[1])
        except Exception as e:
            print(e)

    doc.render(data)
    file_prefix = gen_tmpl_prefix()
    tmp_dir = './tmp/docpack'
    docx_file = f'{tmp_dir}/{file_prefix}.docx'

    try:
        doc.save(docx_file)
    except Exception as e:
        return f'Внутренняя ошибка генерации документа: {e}'

    pdf_file = f'{tmp_dir}/{file_prefix}.pdf'
    convert_command = f"soffice --convert-to pdf {docx_file} --outdir {tmp_dir} --headless"
    print(f'{convert_command=}')
    run(convert_command, stdout=PIPE, stderr=PIPE, universal_newlines=True, shell=True)
    os.remove(docx_file)
    return pdf_file


async def prepare_dp(dp):
    for a in ('ur_lico_gendir_podp', 'ur_lico_buh_podp', 'ur_lico_attach_pechat'):
        if dp[a]:
            dp[a] = f'./files/ur_lico/{dp[a]}'
    dp['ur_lico_gendir_podp'] = empty
    dp['ur_lico_attach_pechat'] = empty
    replace_images = [['ur_lico_gendir_podp', dp['ur_lico_gendir_podp']], ['ur_lico_attach_pechat', dp['ur_lico_attach_pechat']]]

    for a in ('ur_lico_gendir_podp', 'ur_lico_buh_podp', 'ur_lico_attach_pechat'):
        if dp[a]: dp[a]=f'./files/ur_lico/{dp[a]}'
    return dp, replace_images


async def load_dogovor(db, info):
    buhgalter_card_id = info.get('buhgalter_card_requisits_id', 0)
    if not buhgalter_card_id:
        buhgalter_card_id = await db.query(query="select id from buhgalter_card_requisits where user_id=%s", values=[info['user_id']], onevalue=1) or 0

    dp = await db.query(query=f'''
        SELECT
            bcr.*,
            m.name manager_name,
            t.header tarif_name,
            t.summ tarif_summ, t.cnt_orders tarif_cnt_orders,
            t.count_days tarif_count_days, t.percent_pob, t.comment tarif_comment,
            b_dog.header b_dog_header, 
            b_dog.ur_lico_attach_pechat img_replace_ur_lico_attach_pechat,
            b_dog.ur_lico_buh_podp img_replace_ur_lico_gendir_podp,

            b_dog.attach dogovor_blank, b_dog.id b_dog_id,
            dp.registered dp_registered, dp.id dp_id, dp.tarif_id,
            ur_lico.firm ur_lico_firm, ur_lico.gen_dir_fio_im ur_lico_gen_dir_fio_im, ur_lico.gen_dir_fio_rod ur_lico_gen_dir_fio_rod,
            ur_lico.buh_fio_im ur_lico_buh_fio_im, ur_lico.buh_fio_rod ur_lico_buh_fio_rod, ur_lico.inn ur_lico_inn, ur_lico.ogrn ur_lico_ogrn,
            ur_lico.kpp ur_lico_kpp, ur_lico.rs ur_lico_rs, ur_lico.ks ur_lico_ks, ur_lico.bik ur_lico_bik, ur_lico.bank ur_lico_bank,
            ur_lico.attach ur_lico_attach, ur_lico.ur_address ur_lico_ur_address, ur_lico.address ur_lico_address,
            ur_lico.attach_pechat ur_lico_attach_pechat,ur_lico.gendir_podp ur_lico_gendir_podp, ur_lico.buh_podp ur_lico_buh_podp,
            ur_lico.gen_dir_f_in ur_lico_gen_dir_f_in, dogovor.number dogovor_number, 
            dogovor.registered dogovor_registered, dp.ur_lico_id,
            DATE_FORMAT(dogovor.registered,%s) dogovor_from
        FROM
            user u 
            LEFT JOIN buhgalter_card_requisits bcr ON bcr.user_id = u.id and bcr.id={buhgalter_card_id}
            LEFT JOIN manager m ON (u.manager_id =m.id)
            JOIN docpack dp ON dp.user_id = u.id
            LEFT JOIN dogovor  ON (dp.id=dogovor.docpack_id)
            LEFT JOIN tarif t ON (t.id = dp.tarif_id)
            LEFT JOIN blank_document b_dog ON (b_dog.id = t.blank_dogovor_id)
            LEFT JOIN ur_lico ON (ur_lico.id=dp.ur_lico_id)
        WHERE dp.id = %s LIMIT 1
    ''',
        values=['%e %M %Y', info['docpack_id']], onerow=1
    )

    if not dp['dogovor_blank']:
        return False, {'error': f'не найден бланк документа'}

    dp['dogovor_blank'] = f"./files/blank_document/{dp['dogovor_blank']}"
    if not os.path.exists(dp['dogovor_blank']):
        message = f'''<div style="color: red;">Бланк документа не найден: {dp['dogovor_blank']}!</div><br>
            Возможно, он был удалён<br><br>
    
            Подробности:
                Тариф: <a href="/edit_form/tarif/{dp['tarif_id']}">{dp['tarif_name']}</a><br>
                tarif_id: {dp['tarif_name']}<br>
                Бланк договора: <a href="/edit_form/blank_document/{dp['b_dog_id']}">{dp['b_dog_header']}</a><br>
        '''
        return False, message
    dp, replace_images = await prepare_dp(dp)
    return True, response_doc(dp['dogovor_blank'], dp, replace_images)


async def load_bill(db, info):
    buhgalter_card_id = info.get('buhgalter_card_requisits_id', 0)
    if not buhgalter_card_id:
        buhgalter_card_id = await db.query(query="select id from buhgalter_card_requisits where user_id=%s", values=[info['user_id']], onevalue=1) or 0

    dp = await db.query(
        query=f'''
            SELECT
                bcr.*,
                m.name manager_name,
                t.header tarif_name,
                t.summ tarif_summ, t.cnt_orders tarif_cnt_orders,
                t.count_days tarif_count_days, t.percent_pob, t.comment tarif_comment,
                b_bill.header b_bill_header,
                b_bill.attach bill_blank, b_bill.id b_bill_id,
            
                dp.registered dp_registered, dp.id dp_id, dp.tarif_id,
                ur_lico.firm ur_lico_firm, ur_lico.gen_dir_fio_im ur_lico_gen_dir_fio_im, ur_lico.gen_dir_fio_rod ur_lico_gen_dir_fio_rod,
                ur_lico.buh_fio_im ur_lico_buh_fio_im, ur_lico.buh_fio_rod ur_lico_buh_fio_rod, ur_lico.inn ur_lico_inn, ur_lico.ogrn ur_lico_ogrn,
                ur_lico.kpp ur_lico_kpp, ur_lico.rs ur_lico_rs, ur_lico.ks ur_lico_ks, ur_lico.bik ur_lico_bik, ur_lico.bank ur_lico_bank,
                ur_lico.attach ur_lico_attach, ur_lico.ur_address ur_lico_ur_address, ur_lico.address ur_lico_address,
                ur_lico.attach_pechat ur_lico_attach_pechat,ur_lico.gendir_podp ur_lico_gendir_podp, ur_lico.buh_podp ur_lico_buh_podp,
                ur_lico.gen_dir_f_in ur_lico_gen_dir_f_in, dogovor.number dogovor_number, 
                dogovor.registered dogovor_registered, dp.ur_lico_id,
                DATE_FORMAT(dogovor.registered,%s) dogovor_from,
                b.number bill_number, 
                DATE_FORMAT(b.registered,%s) bill_from, b.summ bill_summ
            FROM
                user u 
                LEFT JOIN buhgalter_card_requisits bcr ON bcr.user_id = u.id and bcr.id={buhgalter_card_id}
                LEFT JOIN manager m ON (u.manager_id =m.id)
                JOIN docpack dp ON dp.user_id = u.id
                JOIN bill b ON b.docpack_id = dp.id
                LEFT JOIN dogovor  ON (dp.id=dogovor.docpack_id)
                LEFT JOIN tarif t ON (t.id = dp.tarif_id)
                LEFT JOIN blank_document b_bill ON (b_bill.id = t.blank_bill_id)
                LEFT JOIN ur_lico ON (ur_lico.id=dp.ur_lico_id)
            WHERE dp.id = %s and b.id=%s LIMIT 1
        ''',
        values=['%e %M %Y', '%e %M %Y', info['docpack_id'], info['bill_id']], onerow=1
    )

    if not dp['bill_blank']:
        return False, {'error': f'не найден бланк счёта'}

    dp['dogovor_blank'] = f"./files/blank_document/{dp['bill_blank']}"
    if not os.path.exists(dp['dogovor_blank']):
        message = f'''<div style="color: red;">Бланк документа не найден: {dp['dogovor_blank']}!</div><br>
            Возможно, он был удалён<br><br>
    
            Подробности:
                Тариф: <a href="/edit_form/tarif/{dp['tarif_id']}">{dp['tarif_name']}</a><br>
                tarif_id: {dp['tarif_name']}<br>
                Бланк счёта: <a href="/edit_form/blank_document/{dp['b_bill_id']}">{dp['b_bill_header']}</a><br>
        '''
        return False, message
    dp, replace_images = await prepare_dp(dp)
    dp['bill_summ_prop'] = num_to_text(dp['bill_summ'])
    return True, response_doc(dp['dogovor_blank'], dp, replace_images)


async def load_act(db, info):
    buhgalter_card_id = info.get('buhgalter_card_requisits_id', 0)
    if not buhgalter_card_id:
        buhgalter_card_id = await db.query(query="select id from buhgalter_card_requisits where user_id=%s", values=[info['user_id']], onevalue=1) or 0
    dp = await db.query(
        query=f'''
            SELECT
                bcr.*,

                m.name manager_name,
                t.header tarif_name,t.id tarif_id,
                t.summ tarif_summ, t.cnt_orders tarif_cnt_orders,
                t.count_days tarif_count_days, t.percent_pob, t.comment tarif_comment,
                b_act.header b_act_header,
                b_act.attach act_blank, b_act.id b_act_id,

                dp.registered dp_registered, dp.id dp_id, dp.tarif_id,
                ur_lico.firm ur_lico_firm, ur_lico.gen_dir_fio_im ur_lico_gen_dir_fio_im, ur_lico.gen_dir_fio_rod ur_lico_gen_dir_fio_rod,
                ur_lico.buh_fio_im ur_lico_buh_fio_im, ur_lico.buh_fio_rod ur_lico_buh_fio_rod, ur_lico.inn ur_lico_inn, ur_lico.ogrn ur_lico_ogrn,
                ur_lico.kpp ur_lico_kpp, ur_lico.rs ur_lico_rs, ur_lico.ks ur_lico_ks, ur_lico.bik ur_lico_bik, ur_lico.bank ur_lico_bank,
                ur_lico.attach ur_lico_attach, ur_lico.ur_address ur_lico_ur_address, ur_lico.address ur_lico_address,
                ur_lico.attach_pechat ur_lico_attach_pechat,ur_lico.gendir_podp ur_lico_gendir_podp, ur_lico.buh_podp ur_lico_buh_podp,
                ur_lico.gen_dir_f_in ur_lico_gen_dir_f_in, dogovor.number dogovor_number,
                dogovor.registered dogovor_registered, dp.ur_lico_id,
                DATE_FORMAT(dogovor.registered,%s) dogovor_from,
                b.number bill_number,
                a.number act_number, DATE_FORMAT(a.registered,%s) act_from, a.summ act_summ,
                DATE_FORMAT(b.registered,%s) bill_from, b.summ bill_summ
            FROM
                user u
                LEFT JOIN buhgalter_card_requisits bcr ON bcr.user_id = u.id and bcr.id={buhgalter_card_id}
                LEFT JOIN manager m ON (u.manager_id =m.id)
                JOIN docpack dp ON dp.user_id = u.id
                JOIN bill b ON b.docpack_id = dp.id
                JOIN act a ON a.bill_id=b.id
                LEFT JOIN dogovor  ON (dp.id=dogovor.docpack_id)
                LEFT JOIN tarif t ON (t.id = dp.tarif_id)
                LEFT JOIN blank_document b_act ON (b_act.id = t.blank_act_id)
                LEFT JOIN ur_lico ON (ur_lico.id=dp.ur_lico_id)
            WHERE a.id=%s GROUP BY u.id LIMIT 1
        ''',
        values=['%e %M %Y', '%e %M %Y', '%e %M %Y', info['act_id']],onerow=1
    )
    blank=''
    if dp['act_blank']:
        blank=f"./files/blank_document/{dp['act_blank']}"

    if not blank:
        return False, {'error': f'не найден бланк для акта (тариф: {dp["tarif_name"]}, id={dp["tarif_id"]})'}

    if not os.path.exists(blank):
        message=f'''
        <div style="color: red;">Бланк документа не найден: {blank}!</div><br>
        Возможно, он был удалён<br><br>

        Подробности:
            Тариф: <a href="/edit_form/tarif/{dp['tarif_id']}">{dp['tarif_name']}</a><br>
            tarif_id: {dp['tarif_name']}<br>
            Бланк счёта: <a href="/edit_form/blank_document/{dp['b_bill_id']}">{dp['b_bill_header']}</a><br>
        '''
        return False, message
    dp, replace_images = await prepare_dp(dp)
    dp['act_summ_prop'] = num_to_text(dp['act_summ'])
    return response_doc(blank, dp, replace_images)

async def load_app(db, info):
    buhgalter_card_id = info.get('buhgalter_card_requisits_id', 0)
    if not buhgalter_card_id:
        buhgalter_card_id = await db.query(query="select id from buhgalter_card_requisits where user_id=%s", values=[info['user_id']], onevalue=1) or 0

    dp = await db.query(
        query=f'''
            SELECT
                bcr.*,
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
                LEFT JOIN buhgalter_card_requisits bcr ON bcr.user_id = u.id and bcr.id={buhgalter_card_id}
                LEFT JOIN manager m ON (u.manager_id =m.id)
                LEFT JOIN blank_document blank ON (blank.id = s.blank_id)
                LEFT JOIN ur_lico ON (ur_lico.id=dp.ur_lico_id)
            WHERE app.id=%s GROUP BY u.id LIMIT 1
        ''',
        values=['%e %M %Y', '%e %M %Y', info['app_id']],onerow=1
    )
    dp['app_fields']={}
    fields = await db.query(
        query=f"""
            SELECT
              sv.header name, wt.value
            FROM
              dogovor_app_values wt
              JOIN service_field sf ON sf.id=wt.field_id
              JOIN service_var sv ON sv.id=sf.service_var_id
            WHERE wt.dogovor_app_id={info['app_id']}
            ORDER BY sf.sort
        """
    )
    for f in fields:
        dp['app_fields'][f['name']]=f['value']

    blank=''
    if dp['app_blank']:
        blank=f"./files/blank_document/{dp['app_blank']}"

    if not blank:
        return False, {'error': f'не найден бланк для приложения (service_id: {dp["service_id"]})'}

    if not os.path.exists(blank):
        message=f'''
        <div style="color: red;">Бланк документа не найден: {blank}!</div><br>
        Возможно, он был удалён<br><br>

        Подробности:
            Тариф: <a href="/edit_form/tarif/{dp['tarif_id']}">{dp['tarif_name']}</a><br>
            tarif_id: {dp['tarif_name']}<br>
            Бланк счёта: <a href="/edit_form/blank_document/{dp['b_bill_id']}">{dp['b_bill_header']}</a><br>
        '''
        return False, message
    dp, replace_images = await prepare_dp(dp)
    dp['app_summ_prop']=num_to_text(dp['app_summ'])
    dp['app_summ_post_prop']=num_to_text(dp['app_summ_post'])
    return response_doc(blank, dp, replace_images)


async def get_file(db, doc_type, info):
    if doc_type == 'dogovor':
        st, res = await load_dogovor(db, info)
    elif doc_type == 'act':
        st, res = await load_act(db, info)
    elif doc_type == 'bill':
        st, res = await load_bill(db, info)
    else:
        st, res = await load_app(db, info)
    return st, res
