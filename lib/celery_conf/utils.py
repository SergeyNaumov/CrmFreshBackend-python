import os
import re
import stat
from datetime import datetime, date, timedelta

import requests


def get_manager_phone_from_id(id='none'):
    is_sip = False
    try:
        raw_phone = id.split('@')[0]
        if 'SIP' in raw_phone:
            is_sip = True
            return is_sip, raw_phone
        # if len(raw_phone) == 10:
        #     phone = '+7 ({}{}{}) {}{}{}-{}{}-{}{}'.format(*raw_phone)
        return is_sip, raw_phone
    except:
        return is_sip, None


def get_phone_from_user_dn(user_dn):
    phone = user_dn.get('xsi:userDN')
    if not phone:
        phone = user_dn.get('#text')
    if not phone:
        return None
    clean_phone = re.search(r"tel:(\+\d+)", phone)
    if not clean_phone:
        return None
    return clean_phone.group(1)


def get_client_phone_from_remote_party(remote_party):
    address = remote_party.get('xsi:address')
    if isinstance(address, str):
        phone = address.replace('tel:', '')
        if len(phone) < 10:
            if user_dn := remote_party.get('xsi:userDN'):
                phone = get_phone_from_user_dn(user_dn)
        return phone
    else:
        phone = address.get('#text')
        if phone:
            phone = phone.replace('tel:', '')
        if not phone or len(phone) < 10:
            if user_dn := remote_party.get('xsi:userDN'):
                phone = get_phone_from_user_dn(user_dn)
        return phone


def get_call_direction(personality):
    personality = personality.lower()
    if personality == 'terminator':
        return 'INBOUND'
    if personality == 'originator':
        return 'OUTBOUND'
    return 'NONE'


def get_call_by_call_id(db, call_data):
    _id, _phone, created, error = None, None, True, None
    external_id = call_data['externalId']
    try:
        _id = db.save(
            table='beeline_records_2',
            ignore=1,
            data={
                'externalId': external_id,
                'beeline_abonent_id': call_data['beeline_abonent_id'],
                'api_key_number': call_data['api_key_number'],
            }
        )

        if not _id:
            call_obj = db.query(
                query="select id, phone from beeline_records_2 where externalId=%s",
                values=[external_id],
                onerow=1
            )
            _id, _phone = call_obj['id'], call_obj['phone']
            created = False
    except Exception as e:
        error = str(e)
    return _id, _phone, created, error


def parse_date(value):
    if value == '0000-00-00 00:00:00':
        return datetime.min
    if isinstance(value, datetime):
        return value
    elif isinstance(value, date):
        return datetime.combine(value, datetime.min.time())
    elif value is None:
        return datetime.min
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")


def parse_phone(p):
    p = p.strip()
    p = re.sub(r'\s+', ' ', p)
    p = re.sub(r'^\+7', '8', p)
    p = re.sub(r'[^\d]', '', p)
    if len(p) >= 10:
        p = re.sub(r'^8', '+7', p)
    return p


def format_phones(phone_string):
    result = []
    for p in re.split(r'[,;\.]', phone_string):
        if p := parse_phone(p):
            result.append(p)
    return result


def clean_phone_number(phone):
    if 'SIP' in phone:
        return phone
    phone = re.sub(r'^\+7', '', phone)
    phone = re.sub(r'\D', '', phone)
    return phone


def get_manager_dict(db):
    _list = db.query(query="""select id,phone,phone2 from manager where (phone<>'' or phone2<>'') and gone=0""")
    _list_sip = db.query(query="""select id,sip_number phone from manager where sip_number<>'' and gone=0""")
    manager_dict = {}
    for m in _list:
        if m['phone']:
            phone = clean_phone_number(m['phone'])
            manager_dict[phone] = m['id']
        if m['phone2']:
            phone2 = clean_phone_number(m['phone2'])
            manager_dict[phone2] = m['id']
    for m in _list_sip:
        manager_dict[m['phone']] = m['id']
    return manager_dict


def process_response(response, out_errors=True):
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        if out_errors:
            print(f'Error: {response.status_code}')
        return None


abonents_dict = {}


def get_abonent(abonent: dict, create_if_not_exists, db):
    exists_abonent = abonents_dict.get(abonent['userId'], None)
    if not exists_abonent:
        exists_abonent = db.query(
            query="select * from beeline_abonent where userId LIKE %s",
            values=[f"%{abonent['userId'].split('@')[0]}%"],
            onerow=1
        )

    if exists_abonent and (
            exists_abonent['firstName'] != abonent.get('firstName', '') or
            exists_abonent['lastName'] != abonent.get('lastName', '') or
            exists_abonent['extension'] != abonent.get('extension', '') or
            exists_abonent['department'] != abonent.get('department', '') or
            abonent.get('manager_id') and (exists_abonent['manager_id'] != abonent.get('manager_id', 0))
    ):
        manager_id = exists_abonent['manager_id']
        if new_manager_id := abonent.get('manager_id'):
            manager_id = new_manager_id
        data = {
            'userId': abonent['userId'],
            'firstName': abonent.get('firstName', ''),
            'lastName': abonent.get('lastName', ''),
            'department': abonent.get('department', ''),
            'extension': abonent.get('extension', ''),
            'manager_id': manager_id
        }
        if 'SIP' in abonent['userId']:
            data['sip_number'] = abonent['userId'].split('@')[0]
        else:
            data['phone'] = abonent['phone']
        db.save(
            table="beeline_abonent",
            update=1,
            debug=1,
            where=f"id={exists_abonent['id']}",
            data=data
        )
        exists_abonent['firstName'] = abonent.get('firstName', '')
        exists_abonent['lastName'] = abonent.get('lastName', '')
        exists_abonent['extension'] = abonent.get('extension', '')
        exists_abonent['department'] = abonent.get('department', '')

    if not exists_abonent and create_if_not_exists:
        data = {
            'userId': abonent['userId'],
            'firstName': abonent.get('firstName', ''),
            'lastName': abonent.get('lastName', ''),
            'department': abonent.get('department', ''),
            'extension': abonent.get('extension', ''),
            'manager_id': abonent.get('manager_id', '0'),
        }
        if 'SIP' in abonent['userId']:
            data['sip_number'] = abonent['userId'].split('@')[0]
        else:
            data['phone'] = abonent['phone']

        db.save(
            table="beeline_abonent",
            data=data,
        )
        exists_abonent = db.query(
            query="select * from beeline_abonent where userId=%s",
            values=[abonent['userId']],
            onerow=1
        )
        if exists_abonent:
            abonents_dict[abonent['userId']] = exists_abonent
    return exists_abonent


def sync_abonent(db, api_keys):
    for api_key in api_keys:
        manager_dict = get_manager_dict(db)
        headers = {'X-MPBX-API-AUTH-TOKEN': api_key}
        for phone in manager_dict:
            manager_id = manager_dict[phone]
            response = requests.get(f"https://cloudpbx.beeline.ru/apis/portal/abonents/{phone}", headers=headers)
            abonent = process_response(response, out_errors=False)
            if abonent:
                abonent['manager_id'] = manager_id
                get_abonent(abonent, True, db)


def get_beeline_abonent(db, manager_raw_phone_or_sip, is_sip):
    where = 'sip_number=%s' if is_sip else 'phone=%s'
    return db.query(
        query=f"SELECT id, manager_id FROM beeline_abonent WHERE {where}", onerow=1, values=[manager_raw_phone_or_sip]
    )


def set_group_writeable(path):
    # Получаем текущие права доступа
    current_permissions = os.stat(path).st_mode
    # Устанавливаем флаг "запись для группы"
    new_permissions = current_permissions | stat.S_IWGRP
    # Применяем новые права
    os.chmod(path, new_permissions)


def recursive_chmod(directory):
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            set_group_writeable(dir_path)
        for file_name in files:
            file_path = os.path.join(root, file_name)
            set_group_writeable(file_path)


def get_email(db, manager_id):
    email = db.query(
        query="select email from manager_email where manager_id=%s order by main desc limit 1", values=[manager_id], onevalue=1
    )
    if not email:
        email = ''
    return email


async def get_email_async(db, manager_id):
    email = await db.query(
        query="select email from manager_email where manager_id=%s order by main desc limit 1", values=[manager_id], onevalue=1
    )
    if not email:
        email = ''
    return email


def format_sec(decimal_seconds):
    total_seconds = int(decimal_seconds)
    minutes, seconds = divmod(total_seconds, 60)
    return f"{minutes} м. {seconds} с."

# =============================================================================

def generate_time_intervals(hours):
    current_time = datetime.now()
    start_time = current_time - timedelta(hours=hours)
    intervals = []
    while start_time < current_time:
        end_time = start_time + timedelta(hours=2)
        intervals.append([start_time.strftime('%Y-%m-%dT%H:%M:%S.000Z'), end_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')])
        start_time = end_time
    return intervals
def utc_to_datetime(v):
    dt_object = datetime.utcfromtimestamp((v / 1000)) + timedelta(hours=3)
    formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date
def records_get(dateFrom, dateTo, api_key):
    headers = {'X-MPBX-API-AUTH-TOKEN': api_key}
    query = []
    if dateFrom:
        query.append(f"dateFrom={dateFrom}")
    if dateTo:
        query.append(f"dateTo={dateTo}")
    url = 'https://cloudpbx.beeline.ru/apis/portal/records'
    if len(query):
        url += '?' + '&'.join(query)
    response = requests.get(url, headers=headers)
    result = process_response(response)
    if result:
        for r in result:
            r['date'] = utc_to_datetime(r['date'])
    return result
def save_record(db, record, abonent_dict):
    abonent = get_abonent(record.get('abonent', ''), False, db)
    if abonent and abonent_dict.get(abonent['phone']):
        manager_id = abonent_dict.get(abonent['phone'])
        exists_record = db.query(
            query="SELECT id, duration from beeline_records_2 where externalId=%s",
            values=[record['externalId']], onerow=1
        )
        if not exists_record:
            if record['duration']:
                record['duration'] = record['duration'] / 1000
            db.save(
                table='beeline_records_2',
                data={
                    'externalId': record['externalId'],
                    'phone': record['phone'],
                    'direction': record['direction'],
                    'start_date': record['date'],
                    'duration': record['duration'],
                    'beeline_abonent_id': abonent['id'],
                    'manager_id': manager_id
                },
            )
        elif exists_record:
            if record['duration']:
                record['duration'] = record['duration'] / 1000
                if exists_record['duration'] == 0:
                    db.save(
                        table='beeline_records_2',
                        update=1,
                        data={
                            'duration': record['duration'],
                        },
                        where=f"id={exists_record['id']}"
                    )

def sync_records(db, api_keys, hours=72):
    abonent_dict = {}
    for a in db.query(query="select phone, manager_id from beeline_abonent where manager_id>0"):
        abonent_dict[a['phone']] = a['manager_id']
    for api_key in api_keys:
        for i in generate_time_intervals(hours):
            if _list := records_get(dateFrom=i[0], dateTo=i[1], api_key=api_key):
                for r in _list:
                    save_record(db, r, abonent_dict)

# from lib.celery_conf.utils import sync_records
# from db import get_db
# db = get_db(sync=1)
# sync_records(db, ['a521ced8-d1f2-43c5-a18a-2b369de279c6', '403648d8-06fd-4a99-953a-71bb73077fa7'], 240)


def add_info_to_sip_calls_from_date(db, abonents, api_keys, hours=24):
    abonent_data = {abonent['sip_number']: abonent for abonent in abonents}
    api_key_number = 0
    for api_key in api_keys:
        api_key_number += 1
        headers = {'X-MPBX-API-AUTH-TOKEN': api_key}
        intervals = generate_time_intervals(hours)
        for interval in intervals:
            url = f'https://cloudpbx.beeline.ru/apis/portal/records?dateFrom={interval[0]}&dateTo={interval[1]}'
            data = requests.get(url=url, headers=headers)
            for obj in data.json():
                if 'SIP' not in obj['abonent']['phone']:
                    continue
                manager_sip = obj['abonent']['phone']
                if manager_sip in abonent_data.keys():
                    manager = abonent_data[manager_sip]
                    client_phone = f'+7{obj["phone"]}'
                    dt_object = datetime.utcfromtimestamp((obj['date'] / 1000)) + timedelta(hours=3)
                    start_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
                    if call_obj := db.query(query=f"select * from beeline_records_2 where externalId=%s", values=[obj['externalId']], onerow=1):
                        if call_obj['phone']:
                            continue
                        db.save(table='beeline_records_2', data={'phone': client_phone}, update=1, where=f'id={call_obj["id"]}')
                        continue
                    db.save(
                        table='beeline_records_2',
                        data={
                            'phone': client_phone,
                            'direction': obj['direction'],
                            'manager_id': manager['id'],
                            'beeline_abonent_id': manager['beeline_abonent_id'],
                            'externalId': obj['externalId'],
                            'start_date': start_date,
                            'duration': obj['duration'] / 1000,
                            'api_key_number': api_key_number
                        }
                    )
