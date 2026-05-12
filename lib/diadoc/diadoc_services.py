import json
import os

from lib.diadoc.diadoc_handler import DiadocHandler
from lib.diadoc.diadoc_tools import DiadocEdoStatStatus, is_ur_lico_available_for_diadoc
from lib.diadoc.file_generation import get_file


async def get_info_by_doc_number(db, doc_type, doc_number):
    if doc_type == 'dogovor':
        query = f"""
            select ul.*, d.number, d.registered, bcr.diadoc_box_id user_diadoc_box_id, bcr.diadoc_org_id user_diadoc_org_id, bcr.id bcr_id, bcr.inn user_inn,
            dp.id docpack_id, dp.buhgalter_card_requisits_id, dp.user_id
            from docpack dp 
            left join ur_lico ul on ul.id=dp.ur_lico_id 
            left join buhgalter_card_requisits bcr on bcr.id=dp.buhgalter_card_requisits_id 
            right join dogovor d on dp.id=d.docpack_id 
            where d.number=%s
        """
    elif doc_type == 'bill':
        query = f"""
            select ul.*, b.id doc_object_id, b.number, b.registered, b.summ, b.id bill_id,
            bcr.diadoc_box_id user_diadoc_box_id, bcr.diadoc_org_id user_diadoc_org_id, bcr.id bcr_id, bcr.inn user_inn, dp.id docpack_id,
            dp.buhgalter_card_requisits_id, dp.user_id
            from docpack dp 
            left join ur_lico ul on ul.id=dp.ur_lico_id 
            left join buhgalter_card_requisits bcr on bcr.id=dp.buhgalter_card_requisits_id 
            right join bill b on dp.id=b.docpack_id
            where b.number=%s
        """
    elif doc_type == 'act':
        query = f"""
            select ul.*, a.id doc_object_id, a.number, a.registered, a.summ, a.id act_id,
            bcr.diadoc_box_id user_diadoc_box_id, bcr.diadoc_org_id user_diadoc_org_id, bcr.id bcr_id, bcr.inn user_inn, dp.id docpack_id,
            dp.buhgalter_card_requisits_id, dp.user_id
            from docpack dp 
            left join ur_lico ul on ul.id=dp.ur_lico_id 
            left join buhgalter_card_requisits bcr on bcr.id=dp.buhgalter_card_requisits_id 
            right join bill b on dp.id=b.docpack_id
            right join act a on a.bill_id=b.id
            where a.number=%s
        """
    else:  # dogovor_app
        query = f"""
            select ul.*, da.id doc_object_id, da.registered, da.num_of_dogovor, d.number, d.registered dogovor_registered, da.id app_id,
            bcr.diadoc_box_id user_diadoc_box_id, bcr.diadoc_org_id user_diadoc_org_id, bcr.id bcr_id, bcr.inn user_inn, dp.id docpack_id,
            dp.buhgalter_card_requisits_id, dp.user_id
            from docpack dp 
            left join ur_lico ul on ul.id=dp.ur_lico_id 
            left join buhgalter_card_requisits bcr on bcr.id=dp.buhgalter_card_requisits_id 
            left join dogovor d on d.docpack_id=dp.id
            right join dogovor_app da on da.dogovor_id=dp.id
            where da.id=%s
        """
    return await db.query(query=query, values=[doc_number], onerow=1)


async def get_company_or_detail_info_from_diadoc(form, user_id, buhgalter_card_requisits_id, ur_lico=None):
    requisits = await form.db.query(
        query=f"""select * from buhgalter_card_requisits where user_id=%s and id=%s""",
        values=[user_id, buhgalter_card_requisits_id], onerow=1
    )
    if not ur_lico:
        ur_lico = await form.db.query(query="""select * from ur_lico where inn='9721188281' and kpp='772301001'""", onerow=1)

    if not is_ur_lico_available_for_diadoc(ur_lico):
        return False, f'Невозможно получить данные от юр. лица {ur_lico["firm"]}. Не заполнены данные для Диадока'

    diadoc_handler = DiadocHandler(ur_lico)
    res, info = diadoc_handler.get_organizations_info_id_by_inn_kpp(requisits['inn'], requisits['kpp'])
    if not res or not info:
        return res, info

    existing_org_ids = await form.db.query(
        query=f"""select diadoc_org_id from buhgalter_card_requisits where diadoc_org_id<>'' and user_id=%s""",
        values=[user_id], massive=1
    )
    existing_box_ids = await form.db.query(
        query=f"""select diadoc_box_id from buhgalter_card_requisits where diadoc_box_id<>'' and user_id=%s""",
        values=[user_id], massive=1
    )
    organizations_data = []
    for org in info['Organizations']:
        obj = {
            'org_id': org['OrgId'],
            'inn': org.get('Inn', ''),
            'kpp': org.get('Kpp', ''),
            'full_name': org.get('FullName', ''),
        }
        for box in org['Boxes']:
            if org['OrgId'] in existing_org_ids and box['BoxId'] in existing_box_ids:
                obj['is_checked'] = True
            else:
                obj['is_checked'] = False
            obj['box_id'] = box['BoxId']
            try:
                current_status = diadoc_handler.get_current_counteragent_status(box_id=box['BoxId'])
            except Exception:
                current_status = None
            obj['counteragent_status'] = diadoc_handler.counteragent_statuses(current_status)
            organizations_data.append(obj)
    return res, organizations_data


def update_self_detail_organization_info(db, ur_lico):
    diadoc_handler = DiadocHandler(ur_lico)
    res, organization_info = diadoc_handler.get_organization(ur_lico['inn'], ur_lico['kpp'])
    if not res:
        return res, organization_info

    set_part = []
    values = []
    if not ur_lico['diadoc_org_id']:
        set_part.append('diadoc_org_id=%s')
        values.append(organization_info.OrgId)
    if not ur_lico['diadoc_box_id']:
        for box in organization_info.Boxes:
            set_part.append('diadoc_box_id=%s')
            values.append(box.BoxId)
            break
    if set_part:
        values.append(ur_lico['id'])
        db.query(query=f"""update ur_lico set {','.join(set_part)} where id=%s""", values=values)
    return True, ur_lico


async def get_data_for_post_message(diadoc_handler, info, doc_type, db):
    res, file_path_or_error = await get_file(db, doc_type, info)
    if not res:
        return res, file_path_or_error
    res, name_on_shelf = diadoc_handler.upload_to_shelf(file_path_or_error, ".pdf")
    os.remove(file_path_or_error)
    if not res:
        return res, name_on_shelf
    doc_num = info['num_of_dogovor'] if doc_type == 'dogovor_app' else info['number']
    filename = f"{diadoc_handler.doc_titles(doc_type)} №{doc_num}"
    data = {
        'name_on_shelf': name_on_shelf,
        'info_for_meta': {
            'filename': filename.replace('/', '-'),
            'doc_date': info['registered'].strftime("%d.%m.%Y"),
            'doc_num': doc_num,
            'total_sum': float(info['summ']) if doc_type in ['bill', 'act'] else None,
            'contract_doc_num': info['number'] if doc_type == 'dogovor_app' else None,
            'contract_doc_date': info['dogovor_registered'].strftime("%d.%m.%Y") if doc_type == 'dogovor_app' else None,
        }
    }
    return True, data


async def send_document_via_diadoc(form, info, user, doc_type, manager_id):
    diadoc_handler = DiadocHandler(info)

    current_status = diadoc_handler.get_current_counteragent_status(user=user)
    if not current_status or current_status in [5, 6]:  # если не является контрагентом
        st, res = diadoc_handler.invite_counteragent(user)
        if st:
            data = {
                'status': DiadocEdoStatStatus.REQUEST_INVITATION_SENT.value,
                'meta_data': json.dumps({"task_id": res}),
                'manager_id': manager_id,
                'doc_type': doc_type,
                'buhgalter_card_requisits_id': info['bcr_id'],
                'ur_lico_id': info['id']
            }
            if doc_type == 'dogovor':
                data['number'] = info['number']
            else:
                data['doc_object_id'] = info['doc_object_id']

            await form.db.save(table='diadoc_edo_stat', data=data)
            res = DiadocEdoStatStatus.REQUEST_INVITATION_SENT.label
        return st, res
    if current_status != 1:
        return False, f'Невозможно отправить документ. Статус контрагента: {diadoc_handler.counteragent_statuses(current_status)}'

    st, res = await get_data_for_post_message(diadoc_handler, info, doc_type, form.db)
    if not st:
        return st, res
    info_for_meta = res['info_for_meta']
    name_on_shelf = res['name_on_shelf']
    status, message = diadoc_handler.post_message(user, name_on_shelf, doc_type, info_for_meta)
    if not status:
        return status, message

    entity_id = None
    for entity in message.Entities:
        entity_id = entity.EntityId
        break
    data = {
        'status': DiadocEdoStatStatus.REQUEST_INVITATION_SENT.value,
        'meta_data': json.dumps(info_for_meta),
        'manager_id': manager_id,
        'doc_type': doc_type,
        'buhgalter_card_requisits_id': info['bcr_id'],
        'ur_lico_id': info['id'],
        'name_on_shelf': name_on_shelf,
        'counteragent_box_id': message.ToBoxId,
        'message_id': message.MessageId,
        'entity_id': entity_id
    }
    if doc_type == 'dogovor':
        data['number'] = info['number']
    else:
        data['doc_object_id'] = info['doc_object_id']

    await form.db.save(table='diadoc_edo_stat', data=data)
    return True, DiadocEdoStatStatus.CREATED.label


async def check_and_prepare_upload(form, doc_number, org_id, box_id, doc_type):
    info = await get_info_by_doc_number(form.db, doc_type, doc_number)
    if not info['id']:
        return False, 'Не удалось найти юр. лицо по данным из набора документов'
    if not is_ur_lico_available_for_diadoc(info):
        return False, f'К сожалению, нельзя отправить в ЭДО документ от юридического лица {info["firm"]}. Не заполнены данные для Диадока'

    if not info['bcr_id']:
        return False, 'Не удалось найти получателя'

    set_part = []
    values = []
    if not info['user_diadoc_box_id']:
        set_part.append('diadoc_box_id=%s')
        values.append(box_id)
    if not info['user_diadoc_org_id']:
        set_part.append('diadoc_org_id=%s')
        values.append(org_id)
    if set_part:
        values.append(info['bcr_id'])
        await form.db.query(query=f"""update buhgalter_card_requisits set {','.join(set_part)} where id=%s""", values=values)
    user = {
        'diadoc_org_id': org_id,
        'diadoc_box_id': box_id,
        'inn': info['user_inn'],
    }
    st, res = await send_document_via_diadoc(form, info, user, doc_type, form.manager['id'])
    return st, res
