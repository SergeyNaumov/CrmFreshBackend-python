from lib.core import exists_arg
from lib.core_crm import get_owner, get_manager_email
from lib.send_mes import send_mes
from .get_bills import get_bills
from lib.diadoc.diadoc_services import get_company_or_detail_info_from_diadoc, check_and_prepare_upload


async def diadoc_get_organization_info(form,field,R):
    user_id = exists_arg('id', R)
    buhgalter_card_requisits_id = exists_arg('buhgalter_card_requisits_id', R)
    if not user_id:
        form.errors.append('отсутствует параметр user_id')
    if not buhgalter_card_requisits_id:
        form.errors.append('отсутствует параметр buhgalter_card_requisits_id')
    if form.success():
        st, res = await get_company_or_detail_info_from_diadoc(form, user_id, buhgalter_card_requisits_id)
        if not st:
            form.errors.append(res)
        else:
            return {'success': form.success(), 'errors': form.errors, 'list': res}

    return {'success': form.success(), 'errors': form.errors, 'list': []}


async def action_upload_to_diadoc(form,field,R):
    doc_number = exists_arg('number', R)
    doc_type = exists_arg('doc_type', R)
    box_id = exists_arg('box_id', R)
    org_id = exists_arg('org_id', R)
    if not doc_type:
        form.errors.append('отсутствует параметр doc_type')
    if not doc_number:
        form.errors.append('отсутствует параметр doc_number')
    if not org_id:
        form.errors.append('отсутствует параметр org_id')
    if not box_id:
        form.errors.append('отсутствует параметр box_id')

    if form.success():
        st, res = await check_and_prepare_upload(form, doc_number, org_id, box_id, doc_type)
        if not st:
            form.errors.append(res)
        else:
            return {'success': form.success(), 'errors': form.errors, 'list': res}
    return {'success': form.success(), 'errors': form.errors, 'list': []}
