#!/bin/bash
set -euo pipefail

DB="svcms"
# alias stg_w01 не раскрывается в неинтерактивном скрипте -> хост явным ssh
REMOTE="ssh -p7725 naumov@178.57.220.192"

TABLES=(
    admin_menu_new
    ds_advantages
    ds_article
    ds_brands
    ds_catalog
    ds_certificates
    ds_clients
    ds_doc
    ds_employee
    ds_form_submit
    ds_galery
    ds_good
    ds_good_galery
    ds_news
    ds_params
    ds_params_catalog
    ds_params_good
    ds_reviews
    ds_service
    ds_slider
    ds_text
    ds_top_menu
    ds_video
    ds_zakaz
)

# Таблицы конструктора страниц и тем (доменная привязка) — раньше в дампе
# их не было. Родители (base_pages_set) идут первыми, чтобы FK создавались
# по существующим таблицам; mysqldump всё равно отключает FOREIGN_KEY_CHECKS.
CONSTRUCTOR_TABLES=(
    base_pages_set
    template_pages_base
    domain_theme_color
    domain_theme_style
    domain_theme_layout
    domain_theme_font
    domain_page
    domain_constructor
    constructor_options
)

mysqldump -u svcms \
    --no-tablespaces \
    --single-transaction \
    --default-character-set=utf8mb4 \
    "$DB" "${TABLES[@]}" "${CONSTRUCTOR_TABLES[@]}" \
| sed 's/utf8mb4_0900_ai_ci/utf8mb4_unicode_ci/g' \
| $REMOTE 'mysql -usvcms -h127.0.0.1 svcms'

# ---------------------------------------------------------------------------
# Константы проекта 5837 -> серверный прод (upsert, без удаления).
# const общая для всех проектов, поэтому НЕ через общий TABLES: mysqldump
# пересоздаёт таблицу целиком и снёс бы константы остальных проектов.
# Пишем только строки project_id=5837 и без const_id -- конфликт возможен
# лишь по UNIQUE(name, project_id), поэтому чужие проекты не затрагиваются.
PROJECT_CONSTS=5837

(
    echo "START TRANSACTION;"
    mysql -u svcms --default-character-set=utf8mb4 -N -B "$DB" -e "
        SELECT CONCAT(
            'INSERT INTO \`const\` (\`name\`,\`value\`,\`project_id\`,\`read_only\`) VALUES (',
            QUOTE(\`name\`), ',', QUOTE(\`value\`), ',', \`project_id\`, ',', \`read_only\`, ') ',
            'ON DUPLICATE KEY UPDATE \`value\`=VALUES(\`value\`), \`read_only\`=VALUES(\`read_only\`);'
        )
        FROM \`const\` WHERE \`project_id\`=${PROJECT_CONSTS};"
    echo "COMMIT;"
) | $REMOTE 'mysql -usvcms -h127.0.0.1 --default-character-set=utf8mb4 svcms'