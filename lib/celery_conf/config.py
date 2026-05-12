import os

from celery import Celery
from celery.schedules import crontab
from redis import Redis
from dotenv import load_dotenv
from kombu import Queue, Exchange


REDIS_HOST = os.getenv("REDIS_HOST", 'localhost')
load_dotenv()
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
CELERY_BROKER = f'redis://default:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0'


SUB_KEY = "CLOUD_PBX_BEELINE_SUB_ID"
SUB_KEY_2 = "CLOUD_PBX_BEELINE_SUB_ID_2"
SUB_KEY_3 = "CLOUD_PBX_BEELINE_SUB_ID_3"

BL_API_KEYS = {
    1: os.getenv("CLOUD_PBX_BEELINE_API_KEY", '403648d8-06fd-4a99-953a-71bb73077fa7'),
    2: os.getenv("CLOUD_PBX_BEELINE_API_KEY_2", 'a521ced8-d1f2-43c5-a18a-2b369de279c6'),
    3: os.getenv("CLOUD_PBX_BEELINE_API_KEY_3", 'f2547ad6-a61d-44e2-8298-40867ebdef2b')
}
BL_URLS = {
    1: 'https://fas.crm-dev.ru/backend/beeline/1/subscription',
    2: 'https://fas.crm-dev.ru/backend/beeline/2/subscription',
    3: 'https://fas.crm-dev.ru/backend/beeline/3/subscription'
}

celery_app = Celery('fas')
celery_app.conf.broker_url = CELERY_BROKER
celery_app.conf.result_backend = CELERY_BROKER


class CeleryConfig:
    enable_utc = True
    timezone = 'Europe/Moscow'
    task_queues = (
        Queue('celery', Exchange('celery'), routing_key='celery'),
        Queue('notifications', Exchange('notifications'), routing_key='notifications'),
    )
    task_default_queue = 'celery'
    task_default_exchange = 'celery'
    task_default_routing_key = 'celery'


celery_app.config_from_object(CeleryConfig)

celery_app.conf.beat_schedule = {
    "check_xsi_sub": {
        "task": "lib.celery_conf.tasks.check_xsi_sub",
        "schedule": crontab(minute="*/1"),
        "args": (SUB_KEY, BL_API_KEYS[1], BL_URLS[1]),
    },
    "renew_xsi_sub": {
        "task": "lib.celery_conf.tasks.renew_xsi_sub",
        "schedule": crontab(hour=3, minute=0),
        "args": (SUB_KEY, BL_API_KEYS[1], BL_URLS[1]),
    },
    "check_xsi_sub_2": {
        "task": "lib.celery_conf.tasks.check_xsi_sub",
        "schedule": crontab(minute="*/1"),
        "args": (SUB_KEY_2, BL_API_KEYS[2], BL_URLS[2]),
    },
    "renew_xsi_sub_2": {
        "task": "lib.celery_conf.tasks.renew_xsi_sub",
        "schedule": crontab(hour=3, minute=0),
        "args": (SUB_KEY_2, BL_API_KEYS[2], BL_URLS[2]),
    },
    "check_xsi_sub_3": {
        "task": "lib.celery_conf.tasks.check_xsi_sub",
        "schedule": crontab(minute="*/1"),
        "args": (SUB_KEY_3, BL_API_KEYS[3], BL_URLS[3]),
    },
    "renew_xsi_sub_3": {
        "task": "lib.celery_conf.tasks.renew_xsi_sub",
        "schedule": crontab(hour=3, minute=0),
        "args": (SUB_KEY_3, BL_API_KEYS[3], BL_URLS[3]),
    },
    "search_records": {
        "task": "lib.celery_conf.tasks.search_records",
        "schedule": crontab(minute=0, hour="*/1"),
        "args": ([BL_API_KEYS[1], BL_API_KEYS[2], BL_API_KEYS[3]],),
    },
    "delete_old_records": {
        "task": "lib.celery_conf.tasks.delete_old_records",
        "schedule": crontab(hour=2, minute=0),
    },
    "user_contact_clean": {
        "task": "lib.celery_conf.tasks.user_contact_clean",
        "schedule": crontab(hour=1, minute=0),
    },
    "clear_mail_send_table": {
        "task": "lib.celery_conf.tasks.clear_mail_send_table",
        "schedule": crontab(hour=2, minute=0),
    },
    "check_user_input_work": {
        "task": "lib.celery_conf.tasks.check_user_input_work",
        "schedule": crontab(minute=0, hour="*/1"),
    },
    "generate_xlsx_with_unused_phones": {
        "task": "lib.celery_conf.tasks.generate_xlsx_with_unused_phones",
        "schedule": crontab(hour=8, minute=10),
    },
    "check_phones_in_identifiers": {
        "task": "lib.celery_conf.tasks.check_phones_in_identifiers",
        "schedule": crontab(hour=2, minute=10),
    },
    "teamwork_ofp_wins_send": {
        "task": "lib.celery_conf.tasks.teamwork_ofp_wins_send",
        "schedule": crontab(hour=7, minute=0, day_of_week="mon-fri"),
    },
    "send_current_kpi_traffic_notifications_11_00": {
        "task": "lib.celery_conf.tasks.send_current_kpi_traffic_notifications",
        "schedule": crontab(hour=11, minute=0),
    },
    "send_current_kpi_traffic_notifications_12_30": {
        "task": "lib.celery_conf.tasks.send_current_kpi_traffic_notifications",
        "schedule": crontab(hour=12, minute=30),
    },
    "send_current_kpi_traffic_notifications_16_00": {
        "task": "lib.celery_conf.tasks.send_current_kpi_traffic_notifications",
        "schedule": crontab(hour=16, minute=0),
    },
    "send_current_kpi_traffic_notifications_18_00": {
        "task": "lib.celery_conf.tasks.send_current_kpi_traffic_notifications",
        "schedule": crontab(hour=18, minute=0),
    },
    "sync_abonents_task": {
        "task": "lib.celery_conf.tasks.sync_abonents_task",
        "schedule": crontab(minute=0, hour="*/1"),
    },
    "teamwork_ofp_week_wins_send": {
        "task": "lib.celery_conf.tasks.teamwork_ofp_week_wins_send",
        "schedule": crontab(hour=7, minute=10, day_of_week="mon"),
    },
    "add_info_to_sip_calls": {
        "task": "lib.celery_conf.tasks.add_info_to_sip_calls",
        "schedule": crontab(minute="*/30"),
    },
}

celery_app.autodiscover_tasks([
    'lib.celery_conf.tasks', # 'lib.celery_conf.parser_excel_tasks', 
    'lib.send_mes', 'lib.celery_conf.services', 'lib.celery_conf.diadoc_tasks'
])


def get_redis_client():
    return Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=0)
