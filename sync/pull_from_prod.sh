#!/bin/bash
# Pull недостающих таблиц с прода в локальную БД (dev).
#   project_hosting         -> svcms   (карточка хостинга: born_date/hosting_paid_to/crm_id)
#   user/manager/internet_project -> strateg (внешняя CRM: данные ОП)
# Прод read-only: только mysqldump. Локальная БД strateg должна существовать,
# svcms@localhost -- иметь на неё права (см. plan/README).
set -euo pipefail

REMOTE="ssh -o BatchMode=yes -p7725 naumov@178.57.220.192"
DUMP="mysqldump --no-tablespaces --single-transaction --skip-triggers --default-character-set=utf8mb4 -usvcms -h127.0.0.1"

# Карта хостинга (svcms)
$REMOTE "$DUMP svcms project_hosting" | mysql -u svcms svcms

# Данные ОП (внешняя CRM)
$REMOTE "$DUMP strateg user manager internet_project" | mysql -u svcms strateg
