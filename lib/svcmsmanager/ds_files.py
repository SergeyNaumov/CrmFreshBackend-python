# -*- coding: utf-8 -*-
# Совместимость: каскадное удаление переехало в generic-модуль
# lib/CRM/form/cascade_delete.py (механизм тенант-нейтральный).
# Импорты вида `from lib.svcmsmanager import ds_files` продолжают работать.

from lib.CRM.form.cascade_delete import (  # noqa: F401
    cascade_delete,
    children_count,
    descendant_ids,
)
