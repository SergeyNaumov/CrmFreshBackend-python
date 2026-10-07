#!/usr/bin/env bash
#
# ./sync/svcmsadmin.sh
# Синхронизация backend-файлов svcms/admin на удалённый сервер через rsync.
#
set -euo pipefail

# ---------- Настройки ----------
REMOTE_USER="naumov"
REMOTE_HOST="178.57.220.192"
REMOTE_PORT="7725"
REMOTE_BASE="/var/www/svcms/admin/backend"

# Корень проекта = папка на уровень выше, чем эта (т.е. родитель ./sync/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

RSYNC_OPTS=(
  -avz
  --delete
  --human-readable
  -e "ssh -p ${REMOTE_PORT}"
)

# ---------- Синхронизация ----------
echo ">> Project root: ${LOCAL_DIR}"

echo ">> Sync: ${LOCAL_DIR}/configs/svcmsadmin/  ->  ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE}/conf/"
rsync "${RSYNC_OPTS[@]}" \
  "${LOCAL_DIR}/configs/svcmsadmin/" \
  "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE}/conf/"

echo ">> Sync: ${LOCAL_DIR}/lib/  ->  ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE}/lib/"
rsync "${RSYNC_OPTS[@]}" \
  "${LOCAL_DIR}/lib/" \
  "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE}/lib/"

echo ">> Sync: ${LOCAL_DIR}/routes/  ->  ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE}/routes/"
rsync "${RSYNC_OPTS[@]}" \
  "${LOCAL_DIR}/routes/" \
  "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE}/routes/"

echo ">> Sync: ${LOCAL_DIR}/db/  ->  ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE}/db/"
rsync "${RSYNC_OPTS[@]}" \
  "${LOCAL_DIR}/db/" \
  "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE}/db/"

# ---------- Файлы проекта (локальный прод -> серверный прод) ----------
# Без --delete: не стираем на приёмнике файлы, которых нет локально.
PROJECT_ID="${PROJECT_ID:-5837}"
LOCAL_FILES="/var/www/svcms-async/sites/files/project_${PROJECT_ID}"
REMOTE_FILES="/var/www/sv-cms/htdocs/files/project_${PROJECT_ID}"

read -r -p "Синхронизировать файлы проекта ${PROJECT_ID}? [y/N] " ans
if [[ "${ans,,}" == "y" ]]; then
  echo ">> Sync: ${LOCAL_FILES}/  ->  ${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_FILES}/"
  rsync -avz --human-readable --exclude '__pycache__' \
    -e "ssh -p ${REMOTE_PORT}" \
    "${LOCAL_FILES}/" \
    "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_FILES}/"
fi

echo ">> Done."