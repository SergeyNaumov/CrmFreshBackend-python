import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

import requests
from dotenv import load_dotenv

from .config import celery_app, get_redis_client
from .utils import *

import sys
base_dir = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(base_dir))

from db import get_db
load_dotenv()


@celery_app.task()
def user_transfere_task(data):
    db = get_db(sync=1)
    where = data['where']
    contact_date = data['contact_date']
    manager_from = data['manager_from']
    manager_to = data['manager_to']
    contact_date_to = data['contact_date_to']
    any_date=data.get('any_date',False)

    user_transferred = db.query(query=f"SELECT * FROM user {where}", values=contact_date)
    for user in user_transferred:
        for k, v in user.items():
            if isinstance(v, datetime):
                user[k] = v.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(v, date):
                user[k] = v.strftime("%Y-%m-%d")

        user_history_data = {
            'user_id': user['id'],
            'manager_id': data['manager_id'],
            'changed_fields': json.dumps(user)
        }
        db.save(table='user_history', data=user_history_data)

    query = f"""UPDATE user SET manager_id = %s{data['contact_date_to_q']} {where};"""
    db.query(query=query, values=data['query_values'])
    if len(user_transferred) > 0:
        transfere_data = {
            'manager_id': data['manager_id'],
            'move_params': json.dumps({
                'manager_from': manager_from,
                'manager_to': manager_to,
                'contact_date': contact_date,
                'contact_date_to': contact_date_to,
                'any_date':any_date
            })
        }
        user_transfere_id = db.save(table='user_transfere', data=transfere_data)
        values = ", ".join(
            f"({user['id']}, {user_transfere_id})"
            for user in user_transferred
        )
        db.query(query=f"INSERT INTO user_transfere_records(user_id, user_transfere_id) VALUES {values}")


@celery_app.task()
def tpass_sync_users(data):
    db = get_db(sync=1)
    exists_manager = db.query(
        query=f"""
            select id from manager m where m.tpass_id=%s
        """,
        values=[data['tpass_id']], onevalue=1
    )
    if exists_manager:
        data_to_update = {}
        if data['phone']:
            data_to_update['phone'] = data['phone']
        if data['name']:
            data_to_update['name'] = data['name']
        if data['login']:
            data_to_update['login'] = data['login']
        db.save(
            table='manager',
            data=data_to_update,
            update=1,
            where=f'id={exists_manager}'
        )
        exists_email = db.query(
            query=f"select email from manager_email where email=%s and manager_id=%s",
            values=[data['email'], exists_manager], onevalue=1
        )
        if not exists_email and data['email']:
            db.save(
                table='manager_email',
                data={
                    'email': data['email'],
                    'manager_id': exists_manager
                }
            )
    else:
        email = data.pop('email')
        new_manager = db.save(
            table='manager',
            data=data,
        )
        if email:
            db.save(
                table='manager_email',
                data={
                    'email': email,
                    'manager_id': new_manager,
                    'main': 1
                }
            )


def fill_br2_phone_from_logs():
    db = get_db(sync=1)
    empty_calls = db.query(query="select id, externalId from beeline_records_2 where phone = '' and externalId <> ''")
    print(f'empty: {len(empty_calls)}')
    total_cnt = 0
    for call in empty_calls:
        ext_id = call['externalId']
        full_query = f"""select call_data from beeline_records_2_logs where call_data like %s"""

        call_data = db.query(query=full_query, values=[f'%"{ext_id}"%'], massive=1)
        for obj in call_data:
            event_data = json.loads(obj).get('xsi:eventData')
            ed_call = event_data.get('xsi:call')
            if ed_call:
                ext_tracking_id = ed_call.get('xsi:extTrackingId')
                client_phone = get_client_phone_from_remote_party(ed_call.get('xsi:remoteParty'))
                if ext_id == ext_tracking_id and client_phone:
                    db.query(query=f"update beeline_records_2 set phone=%s where id={call['id']}", values=[client_phone])
                    total_cnt += 1
                    break
    print(f'total added: {total_cnt}')
