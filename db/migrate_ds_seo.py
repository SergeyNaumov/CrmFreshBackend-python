# Миграция: SEO-поля и H1 карточки у конструкторных сущностей (ds_*),
# плюс константы SEO-шаблонов у DS-шаблонов.
#
#   export config=config_svcms_manager
#   .venv/bin/python -m db.migrate_ds_seo
#
# Идемпотентна (ADD COLUMN IF NOT EXISTS + NOT EXISTS для template_const).
#
# 1. Колонки в ds_news, ds_article, ds_good, ds_service и ds_catalog:
#
#   h1                 varchar(255) — заголовок <h1> на странице сущности
#                                     (пусто → берётся header);
#   promo_title        varchar(255) — <title> страницы (без «— orgname»);
#   promo_description  varchar(512) — <meta name="description">;
#   promo_keywords     varchar(512) — <meta name="keywords">.
#
#   Редактируются в карточке сущности («H1», «Title/Description/Keywords
#   (SEO)», конфиги configs/svcmsmanager/ds_*). Читает движок сайта:
#   sites/lib/dsengine/process_page.py::_set_seo.
#
# 2. Строки template_const для констант из configs/svcmsmanager/ds_const
#   (SEO-шаблоны, доставка и т.п.) — чтобы движок сайта видел их в cnst:
#   sites/lib/dsengine/__init__.py::get_const читает const JOIN template_const.
#   Значения этих констант правятся в «Настройки сайта → SEO-шаблоны».

import asyncio

from config import config
from db.freshdb import FreshDB

# В репозитории конфиги лежат в configs/svcmsmanager/, в рантайме на проде —
# в conf/ (config_folder у config.py). Импортируем то, что есть.
try:
    from configs.svcmsmanager.ds_const.events import CONST_FIELDS
except ImportError:  # рантайм-раскладка (conf/)
    from conf.ds_const.events import CONST_FIELDS

TABLES = ('ds_news', 'ds_article', 'ds_good', 'ds_service', 'ds_catalog')

# Колонки карточки: (name, ddl). Порядок важен для новых таблиц (AFTER).
COLUMNS = [
    ('h1', "varchar(255) NOT NULL DEFAULT ''"),
    ('promo_title', "varchar(255) NOT NULL DEFAULT ''"),
    ('promo_description', "varchar(512) NOT NULL DEFAULT ''"),
    ('promo_keywords', "varchar(512) NOT NULL DEFAULT ''"),
]

# Статичные страницы (ds_text): promo-поля без h1 — заголовок H1 там header
# (страница выводит его через page_head_title), мета — promo_*.
TEXT_TABLES = {
    'ds_text': [('promo_title', "varchar(255) NOT NULL DEFAULT ''"),
                ('promo_description', "varchar(512) NOT NULL DEFAULT ''"),
                ('promo_keywords', "varchar(512) NOT NULL DEFAULT ''")],
}


def add_column_sql(table, existing, name, ddl):
    """ALTER для отсутствующей колонки (без IF NOT EXISTS — нет в MySQL)."""
    if name in existing:
        return None
    return "ALTER TABLE `%s` ADD COLUMN `%s` %s" % (table, name, ddl)

# Константы из «Настройки сайта» → template_const (иначе движок их не увидит).
TEMPLATE_CONST_INSERT = (
    "INSERT INTO template_const (template_id, header, sort, type, description) "
    "SELECT %s, %s, %s, %s, %s FROM DUAL WHERE NOT EXISTS ("
    "  SELECT 1 FROM template_const WHERE template_id=%s AND header=%s"
    ")"
)


async def seed_template_const(db):
  templates = await db.query(
    query='SELECT DISTINCT template_id FROM template WHERE type=6',
    values=[], errors=[],
  ) or []
  inserted = 0
  for row in templates:
    tid = row['template_id']
    for index, (_tab, name, desc, ftype) in enumerate(CONST_FIELDS, start=1):
      exists = await db.query(
        query='SELECT id FROM template_const WHERE template_id=%s AND header=%s',
        values=[tid, name], onevalue=1, errors=[],
      )
      if exists:
        continue
      await db.query(
        query=TEMPLATE_CONST_INSERT,
        values=[tid, name, index, ftype, desc, tid, name],
        errors=[],
      )
      inserted += 1
  return inserted


async def main():
  db = FreshDB(config['connects']['crm_write'])
  await db.create_pool()
  # Карточки сущностей (h1 + promo_*).
  plan = [(table, COLUMNS) for table in TABLES]
  # Статичные страницы (только promo_*).
  plan += list(TEXT_TABLES.items())
  for table, columns in plan:
    rows = await db.query(
      query='SELECT column_name AS col FROM information_schema.columns '
            'WHERE table_schema=DATABASE() AND table_name=%s',
      values=[table], errors=[],
    ) or []
    existing = {str(r['col']).lower() for r in rows}
    for name, ddl in columns:
      statement = add_column_sql(table, existing, name, ddl)
      if statement:
        await db.query(query=statement, values=[], errors=[])
  inserted = await seed_template_const(db)
  await db.close_pool()
  if db.error_str:
    raise SystemExit(f'ds_seo: {db.error_str}')
  print('ds_seo: ' + ', '.join(list(TABLES) + list(TEXT_TABLES)) +
        ': ok; template_const: +%s' % inserted)


if __name__ == '__main__':
  asyncio.run(main())
