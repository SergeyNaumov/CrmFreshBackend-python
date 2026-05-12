import json
from datetime import timedelta, datetime

import requests
from google.protobuf.json_format import MessageToJson
from lib.diadoc import diadoc_pb2
from lib.diadoc.diadoc_tools import DiadocEdoStatStatus, get_diadoc_pass
from config import config
from db.freshdbs import FreshDB as FreshDBSync

crm_write = config['connects']['crm_write']

# from lib.diadoc.diadoc_handler import DiadocHandler
# from db import get_db
# db = get_db(sync=1)
# h = DiadocHandler()


class DiadocHandler:
    def __init__(self, ur_lico):
        self.url = 'https://diadoc-api.kontur.ru'
        self.full_headers = self._get_headers(ur_lico)
        self.cliend_id_headers = {"Authorization": f"DiadocAuth ddauth_api_client_id={ur_lico['diadoc_key']}"}
        self.ur_lico = ur_lico
        self.box_id = ur_lico['diadoc_box_id']
        # Роуминг -- это когда через диадок документы отправляются
        self.rouming_operators_hash = {
            '-': 1,  # Если 1, то не получаем каждый раз по API этот список роуминга
            '2BM': 'Диадок',
            '2lb': 'ЭТП ГПБ', '2ps': 'ЭДО.ПОТОК (Петер-Сервис Спецтехнологии)', '2hx': 'Криптэкс', '2md': 'ООО АЙТИКОМ',
            '2ee': 'ООО "Электронный Экспресс" («Экспресс Документ»)', '2ao': 'ООО УЦ АСКОМ', '2bf': 'Сервер-Центр',
            '2lp': 'ТЭК-Торг', '2jd': 'НИИАС', '2ad': 'ООО «Русь-Телеком» («Фельдъегерь: ЭДО»)', '2lg': 'БИФИТ ЭДО', '2jg': 'ООО СЗТЛС',
            '2al': 'Такском', '2bh': 'Аргос', '2lt': 'ЭДО-Лайт', '2cn': 'ГИС', '2ld': 'Э-КОМ',
            '2gt': 'Центр информационной безопасности', '2be': 'Тензор', '2vo': 'Платформа ЭДО (ООО «Эвотор ОФД»)',
            '2lj': 'Финтендер-Крипто (Fintender-eds)', '2ij': 'Edisoft', '2ah': 'ИнфоТеКС', '2ak': 'ТаксНет', '2hu': 'ЗАО "НУЦ"',
            '2ae': 'Калуга Астрал', '2jm': 'CISLink', '2kv': 'ООО УЦ СОЮЗ', '2ci': 'ООО "Электронный Экспресс" (Гарант)', '2ba': 'НТЦ СТЭК',
            '2lq': 'Сберключ (Сбербанк-АСТ)', '2kl': 'Сервионика', '2bk': 'Корус', '2lh': 'ЛераДата',
            '2mb': 'ДиСтэйт', '2rt': 'Ростелеком', '2ig': 'Synerdocs', '2ky': 'МТС'
        }

    def _get_api_key(self, ur_lico):
        login_password = diadoc_pb2.LoginPassword()
        login_password.login = ur_lico['diadoc_login']
        login_password.password = get_diadoc_pass(ur_lico['diadoc_pass'])
        headers = {"Authorization": f"DiadocAuth ddauth_api_client_id={ur_lico['diadoc_key']}"}
        response = requests.post(f"{self.url}/V3/Authenticate?type=password", headers=headers, data=login_password.SerializeToString())
        if response.status_code != 200:
            return None
        api_key = response.text
        db = FreshDBSync(crm_write)
        db.save(
            table='ur_lico', update=1, where=f"id={ur_lico['id']}",
            data={
                'diadoc_api_key': api_key,
                'diadoc_api_key_expiration': datetime.now() + timedelta(hours=23, minutes=59),
            },
        )
        return {"Authorization": f"DiadocAuth ddauth_api_client_id={ur_lico['diadoc_key']},ddauth_token={api_key}"}

    def _get_headers(self, ur_lico):
        if ur_lico['diadoc_api_key'] and ur_lico['diadoc_api_key_expiration'] > datetime.now():
            return {"Authorization": f"DiadocAuth ddauth_api_client_id={ur_lico['diadoc_key']},ddauth_token={ur_lico['diadoc_api_key']}"}
        return self._get_api_key(ur_lico)

    @staticmethod
    def _get_signed_content(name_on_shelf):
        signed_content = diadoc_pb2.SignedContent()
        signed_content.NameOnShelf = name_on_shelf
        return signed_content

    @staticmethod
    def counteragent_statuses(status):
        mapping = {
            0: 'Неизвестный статус (Статус в Диадок)',
            1: 'Отношение партнерства установлено и действует',
            2: 'Контрагент прислал запрос на установление отношения партнерства',
            3: 'В адрес контрагента был отправлен запрос на установление отношения партнерства',
            5: 'Контрагент разорвал отношение партнерства или отклонил запрос на установление отношения партнерства',
            6: 'Текущая организация разорвала отношение партнерства или отклонила запрос на установление отношения партнерства',
            7: 'Организации нет в списке контрагентов',
        }
        return mapping.get(status, 'Неизвестный статус')

    @staticmethod
    def doc_titles(doc_type):
        doc_titles = {
            "dogovor": "Договор",
            "bill": "Счет",
            "act": "Акт",
            "dogovor_app": 'Приложение'
        }
        return doc_titles[doc_type]

    def get_organization(self, inn, kpp):
        """получает 1 организацю по инн/кпп"""
        response = requests.get(f"{self.url}/GetOrganization?inn={inn}&kpp={kpp}", headers=self.cliend_id_headers)
        if response.status_code != 200:
            return False, f'get_organization Diadoc вернул {response.status_code}'

        organization_info = diadoc_pb2.Organization()
        organization_info.ParseFromString(response.content)
        return True, organization_info

    def get_organizations_info_id_by_inn_kpp(self, inn, kpp):
        """получает информацию по инн/кпп и возвращает список организаций"""
        response = requests.get(f"{self.url}/GetOrganizationsByInnKpp?inn={inn}", headers=self.cliend_id_headers)
        if response.status_code != 200:
            return False, f'get_organizations_info_id_by_inn_kpp Diadoc вернул {response.status_code}'
        organizations = diadoc_pb2.OrganizationList()
        organizations.ParseFromString(response.content)
        return True, json.loads(MessageToJson(organizations))

    def upload_to_shelf(self, file_path, file_extension):
        """возвращает имя файла, загруженного на полку"""
        with open(file_path, 'rb') as f:
            file_data = f.read()
        params = {"fileExtension": file_extension}
        upload_response = requests.post(f"{self.url}/V2/ShelfUpload", headers=self.full_headers, params=params, data=file_data)

        if upload_response.status_code != 200:
            return False, f'upload_to_shelf Diadoc вернул {upload_response.status_code}'
        return True, upload_response.text

    def get_document_attachments(self, name_on_shelf, doc_type, info_for_meta):
        attachment = diadoc_pb2.DocumentAttachment()
        attachment.SignedContent.CopyFrom(self._get_signed_content(name_on_shelf))
        attachment.NeedRecipientSignature = True
        attachment.NeedReceipt = True

        metadata = {"FileName": f"{info_for_meta['filename']}.pdf", "DocumentDate": info_for_meta['doc_date'], "DocumentNumber": info_for_meta['doc_num']}
        type_named_id = 'Nonformalized'
        if doc_type == 'contract':
            type_named_id = 'Contract'
        elif doc_type == 'bill':
            type_named_id = 'ProformaInvoice'
            metadata |= {"TotalSum": info_for_meta['total_sum']}
        elif doc_type == 'act':
            type_named_id = 'AcceptanceCertificate'
            metadata |= {"TotalSum": info_for_meta['total_sum']}
        elif doc_type == 'adag':
            type_named_id = 'SupplementaryAgreement'
            metadata |= {
                "ContractDocumentNumber": info_for_meta['contract_doc_num'],
                "ContractDocumentDate": info_for_meta['contract_doc_date']
            }

        attachment.TypeNamedId = type_named_id
        for key, value in metadata.items():
            metadata_item = diadoc_pb2.MetadataItem()
            metadata_item.Key = key
            metadata_item.Value = str(value)
            attachment.Metadata.append(metadata_item)

        return attachment

    def post_message(self, user, name_on_shelf, doc_type, info_for_meta):
        message_to_post = diadoc_pb2.MessageToPost()
        message_to_post.FromBoxId = self.ur_lico['diadoc_box_id']
        message_to_post.ToBoxId = user['diadoc_box_id']
        message_to_post.IsDraft = False  # черновик

        message_to_post.DocumentAttachments.extend([self.get_document_attachments(name_on_shelf, doc_type, info_for_meta)])

        response = requests.post(f"{self.url}/V3/PostMessage", headers=self.full_headers, data=message_to_post.SerializeToString())
        if response.status_code != 200:
            return False, f'post_message Diadoc вернул {response.status_code}'
        message = diadoc_pb2.Message()
        message.ParseFromString(response.content)
        return True, message

    def get_counteragent(self, user, box_id):
        counteragent_box_id = user['diadoc_box_id'].split('@')[0] if user else box_id.split('@')[0]
        response = requests.get(
            url=f"{self.url}/V3/GetCounteragent?myBoxId={self.box_id.split('@')[0]}&counteragentBoxId={counteragent_box_id}",
            headers=self.full_headers
        )
        return response.status_code, response.content

    def get_current_counteragent_status(self, user=None, box_id=''):
        status_code, content = self.get_counteragent(user, box_id)
        if status_code == 404:
            return False
        counteragent = diadoc_pb2.Counteragent()
        counteragent.ParseFromString(content)
        return counteragent.CurrentStatus

    def invite_counteragent(self, user):
        dep_qp = f"&myDepartmentId={self.ur_lico['diadoc_dep']}" if self.ur_lico['diadoc_dep'] else ''

        invitation = diadoc_pb2.AcquireCounteragentRequest()
        invitation.OrgId = user['diadoc_org_id']
        invitation.Inn = user['inn']
        invitation.BoxId = user['diadoc_box_id'].split('@')[0]
        response = requests.post(
            url=f"{self.url}/V3/AcquireCounteragent?myBoxId={self.box_id.split('@')[0]}{dep_qp}",
            headers=self.full_headers, data=invitation.SerializeToString()
        )
        if response.status_code != 200:
            return False, f'invite_counteragent Diadoc вернул {response.status_code}'
        async_result = diadoc_pb2.AsyncMethodResult()
        async_result.ParseFromString(response.content)
        return True, async_result.TaskId

    def get_invitation_counteragent_status(self, diadoc_stat_obj):
        task_id = json.loads(diadoc_stat_obj['meta_data'])['task_id']
        response = requests.get(url=f"{self.url}/V2/AcquireCounteragentResult?taskId={task_id}", headers=self.full_headers)
        if response.status_code != 200:
            return response.status_code, response.text
        res = diadoc_pb2.AcquireCounteragentResultV2()
        res.ParseFromString(response.content)
        return response.status_code, res

    def move_documents(self, diadoc_stat_obj):
        document_id = diadoc_pb2.DocumentId()
        document_id.MessageId = diadoc_stat_obj['message_id']
        document_id.EntityId = diadoc_stat_obj['entity_id']

        move_operation = diadoc_pb2.DocumentsMoveOperation()
        move_operation.BoxId = self.box_id
        if self.ur_lico['diadoc_dep']:
            move_operation.ToDepartmentId = self.ur_lico['diadoc_dep']
        move_operation.DocumentIds.extend([document_id])
        r = requests.post(url='https://diadoc-api.kontur.ru/MoveDocuments', headers=self.full_headers, data=move_operation.SerializeToString())

    @staticmethod
    def _is_signed(document, doc_type):
        if document.IsDeleted:
            return DiadocEdoStatStatus.DELETED.value
        severity = document.DocflowStatus.PrimaryStatus.Severity
        status_text = document.DocflowStatus.PrimaryStatus.StatusText

        if doc_type == 'bill' and status_text == 'Документооборот завершен':
            return DiadocEdoStatStatus.SUCCEED.value
        if severity == 'Error':
            return DiadocEdoStatStatus.ERROR.value
        if severity == 'Success':
            return DiadocEdoStatStatus.SUCCEED.value
        if severity == 'Info' and status_text == 'Документооборот завершен':
            return DiadocEdoStatStatus.SUCCEED.value
        if severity == 'Warning' and status_text == 'Ожидается подпись контрагента':
            return DiadocEdoStatStatus.IN_PROCESS.value
        if severity == 'Warning' and status_text == 'Требуется аннулирование':
            return DiadocEdoStatStatus.ERROR.value
        if severity == 'Warning' and status_text == 'Требуется подписать и отправить':
            return DiadocEdoStatStatus.REQUIRED_TO_SIGN.value
        return None

    def check_sign_status(self, diadoc_stat_obj):
        response = requests.get(
            url=f"https://diadoc-api.kontur.ru/V3/GetDocument?boxId={self.box_id}&MessageId={diadoc_stat_obj['message_id']}&entityId={diadoc_stat_obj['entity_id']}",
            headers=self.full_headers,
        )
        if response.status_code != 200:
            return False, f'GetDocument Diadoc вернул {response.status_code}'

        document = diadoc_pb2.Document()
        document.ParseFromString(response.content)
        return True, self._is_signed(document, diadoc_stat_obj['doc_type'])

    def get_document_signed_print_form(self, diadoc_stat_obj):
        response = requests.get(
            url=f"{self.url}/GeneratePrintForm?boxId={self.box_id}&MessageId={diadoc_stat_obj['message_id']}&documentId={diadoc_stat_obj['entity_id']}",
            headers=self.full_headers
        )
        if response.status_code != 200:
            return False, f'set_document_signed вернул {response.status_code}'
        return True, response
