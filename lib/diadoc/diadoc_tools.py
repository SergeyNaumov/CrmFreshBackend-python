import base64
import os
from enum import Enum
from cryptography.fernet import Fernet

DIADOC_SECRET_KEY = 'OEpSMEpVeUFMWnRCeWpic0cxTWE5a1F1QS1zVnE0TnVES2wxMFNaaE1pND0='


class DiadocEdoStatStatus(str, Enum):
    CREATED = "created"
    SUCCEED = "succeed"
    ERROR = "error"
    IN_PROCESS = "in_process"
    REQUIRED_TO_SIGN = "required_to_sign"
    REQUEST_INVITATION_SENT = "request_invitation_sent"
    INVITATION_SENT = "invitation_sent"
    INVITATION_FAILED = "invitation_failed"
    INVITATION_REFUSED = "invitation_refused"
    DELETED = "deleted"

    @property
    def label(self):
        labels = {
            self.CREATED: 'Сообщение с документом создано',
            self.SUCCEED: 'Успешно подписано',
            self.ERROR: 'Не удалось подписать',
            self.IN_PROCESS: 'В процессе',
            self.REQUIRED_TO_SIGN: 'Требуется подписать и отправить',
            self.REQUEST_INVITATION_SENT: 'Запрос на приглашение создан',
            self.INVITATION_SENT: 'Приглашение успешно отправлено',
            self.INVITATION_FAILED: 'Не удалось отправить приглашение',
            self.INVITATION_REFUSED: 'Приглашение отклонено или в неизвестном состоянии',
            self.DELETED: 'Удален',
        }
        return labels.get(self, self.value)


class DiadocEdoStatDocType(str, Enum):
    ACT = "act"
    BILL = "bill"
    DOGOVOR_APP = "dogovor_app"
    DOGOVOR = "dogovor"

    def label(self):
        labels = {
            self.ACT: 'Акт',
            self.BILL: 'Счет',
            self.DOGOVOR_APP: 'Доп. Соглашение',
            self.DOGOVOR: 'Договор',
        }
        return labels.get(self, self.value)


def save_diadoc_pass(db, ur_lico_id, raw_pass):
    cipher = Fernet(base64.urlsafe_b64decode(DIADOC_SECRET_KEY))
    db.save(
        table='ur_lico',
        data={
            'diadoc_pass': cipher.encrypt(raw_pass.encode()).decode(),
        },
        update=1,
        where=f"id={ur_lico_id}"
    )


def get_diadoc_pass(diadoc_pass):
    cipher = Fernet(base64.urlsafe_b64decode(DIADOC_SECRET_KEY))
    return cipher.decrypt(diadoc_pass.encode()).decode()


def is_ur_lico_available_for_diadoc(ur_lico):
    return all([ur_lico['diadoc_login'], ur_lico['diadoc_key'], ur_lico['diadoc_box_id'], ur_lico['diadoc_org_id'], ur_lico['diadoc_pass']])


units = ('ноль', ('один', 'одна'), ('два', 'две'), 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять')
teens = ('десять', 'одиннадцать', 'двенадцать', 'тринадцать', 'четырнадцать', 'пятнадцать', 'шестнадцать', 'семнадцать', 'восемнадцать', 'девятнадцать')
tens = (teens, 'двадцать', 'тридцать', 'сорок', 'пятьдесят', 'шестьдесят', 'семьдесят', 'восемьдесят', 'девяносто')
hundreds = ('сто', 'двести', 'триста', 'четыреста', 'пятьсот', 'шестьсот', 'семьсот', 'восемьсот', 'девятьсот')
orders = ((('тысяча', 'тысячи', 'тысяч'), 'f'), (('миллион', 'миллиона', 'миллионов'), 'm'), (('миллиард', 'миллиарда', 'миллиардов'), 'm'),)


def thousand(rest, sex):
    """Converts numbers from 19 to 999"""
    prev = 0
    plural = 2
    name = []
    use_teens = 10 <= rest % 100 <= 19
    if not use_teens:
        data = ((units, 10), (tens, 100), (hundreds, 1000))
    else:
        data = ((teens, 10), (hundreds, 1000))
    for names, x in data:
        cur = int(((rest - prev) % x) * 10 / x)
        prev = rest % x
        if x == 10 and use_teens:
            plural = 2
            name.append(teens[cur])
        elif cur == 0:
            continue
        elif x == 10:
            name_ = names[cur]
            if isinstance(name_, tuple):
                name_ = name_[0 if sex == 'm' else 1]
            name.append(name_)
            if cur >= 2 and cur <= 4:
                plural = 1
            elif cur == 1:
                plural = 0
            else:
                plural = 2
        else:
            name.append(names[cur-1])
    return plural, name


def num_to_text(num, main_units=(('', '', ''), 'm')):
    _orders = (main_units,) + orders
    if num == 0:
        return ' '.join((units[0], _orders[0][0][2])).strip()  # ноль

    rest = abs(num)
    ord = 0
    name = []
    while rest > 0:
        plural, nme = thousand(rest % 1000, _orders[ord][1])
        if nme or ord == 0:
            name.append(_orders[ord][0][plural])
        name += nme
        rest = int(rest / 1000)
        ord += 1
    if num < 0:
        name.append('минус')
    name.reverse()
    return ' '.join(name).strip()


"""
CREATE TABLE diadoc_edo_stat (
  id int(10) unsigned NOT NULL AUTO_INCREMENT,
  counteragent_box_id varchar(100) NOT NULL DEFAULT '',
  message_id varchar(150) NOT NULL DEFAULT '',
  entity_id varchar(150) NOT NULL DEFAULT '',
  name_on_shelf varchar(100) NOT NULL DEFAULT '',
  doc_type varchar(30) NOT NULL DEFAULT '',
  ur_lico_id int unsigned NOT NULL,
  status varchar(30) NOT NULL DEFAULT '',
  meta_data JSON,
  manager_id int unsigned NOT NULL,
  buhgalter_card_requisits_id int unsigned NOT NULL,
  doc_object_id int unsigned NOT NULL,
  number varchar(50) NOT NULL DEFAULT ''
  sign_time timestamp,
  is_scan_downloaded tinyint unsigned NOT NULL DEFAULT '0',
  created_at timestamp NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (id)
)


alter table buhgalter_card_requisits add column diadoc_box_id varchar(100) not null default '';
alter table buhgalter_card_requisits add column diadoc_org_id varchar(150) not null default '';


alter table ur_lico add column diadoc_login varchar(100) not null default '';
alter table ur_lico add column diadoc_pass varchar(200) not null default '';
alter table ur_lico add column diadoc_key varchar(100) not null default '';
alter table ur_lico add column diadoc_dep varchar(100) not null default '';
alter table ur_lico add column diadoc_box_id varchar(100) not null default '';
alter table ur_lico add column diadoc_org_id varchar(150) not null default '';
alter table ur_lico add column diadoc_api_key varchar(400) not null default '';
alter table ur_lico add column diadoc_api_key_expiration timestamp;


update ur_lico set diadoc_login='buh1@t-pass.pro' where inn='9721188281';
update ur_lico set diadoc_key='api-456d198f-a7ce-44ff-896d-592f6c0eb102' where inn='9721188281';
update ur_lico set diadoc_box_id='8047e14c5b8c450cb379efcc645d07ee@diadoc.ru' where inn='9721188281';
update ur_lico set diadoc_org_id='0a70a312-d959-4cdb-99d6-055e97ab7c5d' where inn='9721188281';

if not is_ur_lico_available_for_diadoc(ur_lico):
    return False, f'К сожалению, нельзя отправить в ЭДО документ от юридического лица {ur_lico["firm"]}. Не заполнены данные для Диадока'
"""
"""
from lib.diadoc.diadoc_tools import save_diadoc_pass
from db import get_db
db = get_db(sync=1)
save_diadoc_pass(db, 27, 'msk-onlain24')
"""