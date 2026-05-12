import json
from datetime import datetime

from .config import celery_app
from .utils import get_email, get_email_async
from pathlib import Path

import sys

base_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(base_dir))

from db import get_db
from lib.send_mes import send_mes_task
from lib.diadoc.diadoc_tools import DiadocEdoStatStatus
from lib.diadoc.diadoc_handler import DiadocHandler
from lib.diadoc.diadoc_services import get_data_for_post_message, get_info_by_doc_number

from config import config

crm_write = config['connects']['crm_write']
diadoc_table = 'diadoc_edo_stat'


def send_edo_status_notification(diadoc_handler, diadoc_stat_obj, new_status, manager_email):
    if manager_email:
        doc_number = diadoc_stat_obj['number'] if diadoc_stat_obj['doc_type'] == 'dogovor' else diadoc_stat_obj['doc_object_id']
        text = f'{diadoc_handler.doc_titles(diadoc_stat_obj["doc_type"])} №{doc_number} - изменен статус ЭДО на "{new_status.label}"'
        send_mes_task.delay({
            'from_addr': 'no-reply@fascrm.ru',
            'to': manager_email,
            'subject': 'ЭДО - изменение статуса',
            'message': text,
        })


@celery_app.task()
def diadoc_check_counteragent_invitation_requests():
    db = get_db(sync=1)
    diadoc_stat_objs = db.query(
        query=f"""
            select * 
            from diadoc_edo_stat des 
            left join ur_lico ul on ul.id=des.ur_lico_id
            where des.status='request_invitation_sent'
        """
    )
    for diadoc_stat_obj in diadoc_stat_objs:
        diadoc_handler = DiadocHandler(diadoc_stat_obj)
        status_code, res = diadoc_handler.get_invitation_counteragent_status(diadoc_stat_obj)
        if status_code == 204:  # операция еще не завершена.
            continue
        manager_email = get_email(db, diadoc_stat_obj['manager_id'])
        if status_code != 200:
            db.save(
                table=diadoc_table, update=1, where=f"id={diadoc_stat_obj['id']}",
                data={
                    'status': DiadocEdoStatStatus.INVITATION_FAILED.value
                },
            )
            send_edo_status_notification(diadoc_handler, diadoc_stat_obj, DiadocEdoStatStatus.INVITATION_FAILED.value, manager_email)
            continue

        db.save(
            table=diadoc_table, update=1, where=f"id={diadoc_stat_obj['id']}",
            data={
                'status': DiadocEdoStatStatus.INVITATION_SENT.value,
                'counteragent_box_id': res.BoxId
            },
        )
        send_edo_status_notification(diadoc_handler, diadoc_stat_obj, DiadocEdoStatStatus.INVITATION_SENT.value, manager_email)


@celery_app.task()
def diadoc_check_counteragent_sent_invitations():
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_check())


async def _check():
    db = get_db()
    await db.create_pool()
    diadoc_stat_objs = await db.query(
        query=f"""
            select des.*, ul.*, bcr.diadoc_box_id user_diadoc_box_id, bcr.inn user_inn, bcr.diadoc_org_id user_diadoc_org_id
            from diadoc_edo_stat des 
            left join ur_lico ul on ul.id=des.ur_lico_id
            left join buhgalter_card_requisits bcr on bcr.id=des.buhgalter_card_requisits_id
            where des.status='invitation_sent'
        """
    )
    for diadoc_stat_obj in diadoc_stat_objs:
        diadoc_handler = DiadocHandler(diadoc_stat_obj)
        current_status = diadoc_handler.get_current_counteragent_status(box_id=diadoc_stat_obj['user_diadoc_box_id'])
        if current_status == 3:
            continue
        manager_email = await get_email_async(db, diadoc_stat_obj['manager_id'])
        if current_status != 1:
            await db.save(
                table=diadoc_table, update=1, where=f"id={diadoc_stat_obj['id']}",
                data={
                    'status': DiadocEdoStatStatus.INVITATION_REFUSED.value
                },
            )
            send_edo_status_notification(diadoc_handler, diadoc_stat_obj, DiadocEdoStatStatus.INVITATION_REFUSED.value, manager_email)
            continue
        doc_number = diadoc_stat_obj['number'] if diadoc_stat_obj['doc_type'] == 'dogovor' else diadoc_stat_obj['doc_object_id']

        info = await get_info_by_doc_number(db, diadoc_stat_obj['doc_type'], doc_number)
        st, data = await get_data_for_post_message(diadoc_handler, info, diadoc_stat_obj['doc_type'], db)
        if not st:
            print('diadoc_check_counteragent_sent_invitations error', data)
            continue
        info_for_meta = data['info_for_meta']
        name_on_shelf = data['name_on_shelf']
        user = {
            'diadoc_org_id': diadoc_stat_obj['user_diadoc_org_id'],
            'diadoc_box_id': diadoc_stat_obj['user_diadoc_box_id'],
            'inn': diadoc_stat_obj['user_inn'],
        }
        status, message = diadoc_handler.post_message(user, name_on_shelf, diadoc_stat_obj['doc_type'], info_for_meta)
        if not status:
            print('diadoc_check_counteragent_sent_invitations error2', message)
            continue

        entity_id = None
        for entity in message.Entities:
            entity_id = entity.EntityId
            break
        meta_data = json.loads(diadoc_stat_obj['meta_data'])
        meta_data |= info_for_meta
        await db.save(
            table=diadoc_table, update=1, where=f"id={diadoc_stat_obj['id']}",
            data={
                'entity_id': entity_id,
                'status': DiadocEdoStatStatus.CREATED.value,
                'name_on_shelf': name_on_shelf,
                'message_id': message.MessageId,
                'meta_data': json.dumps(meta_data)
            }
        )

        send_edo_status_notification(diadoc_handler, diadoc_stat_obj, DiadocEdoStatStatus.CREATED.value, manager_email)


# @celery_app.task()
# def diadoc_set_document_signed(diadoc_stat_obj_id):
#     diadoc_stat_obj = DiadocEdoStat.objects.select_related('self_details').get(id=diadoc_stat_obj_id)
#     self_details = diadoc_stat_obj.self_details
#     diadoc_handler = DiadocHandler(self_details)
#
#     if diadoc_stat_obj.doc_type == 'bill':
#         diadoc_stat_obj.is_scan_downloaded = True
#         diadoc_stat_obj.save(update_fields=['is_scan_downloaded'])
#         return False, 'bill'
#
#     st, response = diadoc_handler.get_document_signed_print_form(diadoc_stat_obj)
#     if not st:
#         return st, response
#     content_disposition = response.headers.get("Content-Disposition")
#
#     filename = "document.pdf"
#     if content_disposition:
#         parts = content_disposition.split("filename=")
#         if len(parts) > 1:
#             filename = parts[1].strip().strip('"')
#
#     doc_obj = diadoc_stat_obj.doc_object
#     doc_obj.pdf_scan.save(filename, ContentFile(response.content), save=True)
#     diadoc_stat_obj.is_scan_downloaded = True
#     diadoc_stat_obj.save(update_fields=['is_scan_downloaded'])


@celery_app.task()
def diadoc_check_sign():
    db = get_db(sync=1)
    diadoc_stat_objs = db.query(
        query=f"""
            select des.*, ul.*, bcr.diadoc_box_id user_diadoc_box_id
            from diadoc_edo_stat des 
            left join ur_lico ul on ul.id=des.ur_lico_id
            left join buhgalter_card_requisits bcr on bcr.id=des.buhgalter_card_requisits_id
            where des.status in ('required_to_sign','created','in_process')
        """
    )

    for diadoc_stat_obj in diadoc_stat_objs:
        diadoc_handler = DiadocHandler(diadoc_stat_obj)
        st, new_status = diadoc_handler.check_sign_status(diadoc_stat_obj)
        if not st:
            continue
        if not new_status or new_status == diadoc_stat_obj['status']:
            continue

        data = {'status': new_status}
        if new_status == DiadocEdoStatStatus.SUCCEED.value:
            data['sign_time'] = datetime.now()

        db.save(table=diadoc_table, update=1, where=f"id={diadoc_stat_obj['id']}", data=data)
        # if new_status == DiadocEdoStatStatus.SUCCEED.value:
        #     diadoc_set_document_signed.delay(diadoc_stat_obj.id)
        manager_email = get_email(db, diadoc_stat_obj['manager_id'])
        send_edo_status_notification(diadoc_handler, diadoc_stat_obj, new_status, manager_email)
