# Миграция: иерархия и группы опций конструктора (ds_options).
#
#   export config=config_svcms_manager
#   .venv/bin/python -m db.migrate_ds_options_tree
#
# Идемпотентна (повторный запуск ничего не ломает). Делает:
#
#   1. Добавляет в ds_options колонки parent_id (иерархия) и note (подсказка
#      для интерфейса), если их ещё нет.
#   2. Собирает группу «Товары»: Рубрики товаров, Характеристики, Параметры
#      рубрик, Значения характеристик, Бренды, Корзина и заказы. Родитель
#      выключен -> все его потомки тоже выключены (см. lib/dsengine/options.py).
#   3. Заводит две новые служебные опции: «Сравнение» и «Избранное»
#      (is_menu=0, родитель — «Товары»).
#   4. Перепривязывает блоки корзины/сравнения/избранного и их счётчики в шапке
#      (ds_blocks_options) к новым опциям, с зависимостью от «Товары».
#   5. Раздаёт новые опции всем проектам, у которых включены «Товары» —
#      иначе сравнение и избранное молча отключатся у действующих сайтов.
#
# Данные сайтов (ds_*) не трогает.
import asyncio

from db import FreshDB
from config import config


# name -> (header|None, parent_name|None, note|None, sort|None)
# header/parent/note/sort == None -> не менять.
OPTIONS = {
  'good':            ('Товары', None,
                      'Ядро магазина: каталог, характеристики, бренды, корзина и заказы', None),
  'catalog':         ('Рубрики товаров', 'good',
                      'Рубрики (категории) товаров', None),
  'params':          (None, 'good',
                      'Справочник характеристик товаров', None),
  'params_catalog':  (None, 'params',
                      'Какие характеристики показывать в рубрике', None),
  'params_good':     (None, 'params',
                      'Значения характеристик у товаров (служебная, без меню)', None),
  'brands':          (None, 'good',
                      'Бренды (производители) товаров', None),
  'zakaz':           ('Корзина и заказы', 'good',
                      'Корзина и оформление заказа на сайте + раздел «Заказы»', None),
  # Независимые разделы — только подсказки для интерфейса.
  'news':            (None, None, 'Раздел новостей', None),
  'article':         (None, None, 'Статьи', None),
  'service':         (None, None, 'Услуги', None),
  'slider':          (None, None,
                      'Слайдер (карусель) на главной странице', None),
  'certificates':    (None, None, 'Сертификаты и дипломы', None),
  'employee':        (None, None, 'Команда (сотрудники)', None),
  'galery':          (None, None, 'Фотогалерея', None),
  'video':           (None, None, 'Раздел видео', None),
  'reviews':         (None, None, 'Отзывы клиентов', None),
  'advantages':      (None, None, 'Преимущества компании', None),
  'clients':         (None, None, 'Логотипы клиентов', None),
  'doc':             (None, None, 'Документы для скачивания', None),
  'form_submit':     (None, None, 'Заявки, отправленные через формы сайта', None),
  'text':            (None, None, 'Статичные текстовые страницы', None),
  'top_menu':        (None, None, 'Верхнее меню сайта', None),
  'bottom_menu':     (None, None, 'Нижнее меню сайта', None),
  'forms':           (None, None,
                      'Формы на страницах сайта (поведение, без пункта меню)', None),
  'contacts':        (None, None,
                      'Контакты: данные, филиалы, карта, реквизиты (без пункта меню)', None),
  'ds_filials':      (None, None, 'Филиалы компании', None),
  'faq':             (None, None,
                      'Вопрос-ответ (поведение, без пункта меню)', None),
  'promo':           (None, None,
                      'Промо-блоки: таймер, бегущая строка, параллакс', None),
  'pages':           (None, None,
                      'Служебные страницы: 404, профиль, регистрация, поиск', None),
  'company':         (None, None,
                      'О компании: история, структура, отчёты', None),
  'template_const':  (None, None,
                      'Настройки сайта: константы, логотип, favicon', None),
}

# Новые служебные опции (сравнение/избранное): name -> (header, sort, note)
NEW_OPTIONS = {
  'compare':   ('Сравнение', 201, 'Сравнение товаров на сайте (без пункта меню)'),
  'favorites': ('Избранное', 202, 'Избранное (закладки) на сайте (без пункта меню)'),
}

# Блок -> опции, все из которых должны быть включены (ds_blocks_options).
# 2 = «Товары»; compare/favorites подставляются по name.
BLOCK_LINKS = {
  'page_basket':    [20, 'good'],
  'page_order':     [20, 'good'],
  'basket_info':    [20, 'good'],
  'page_compare':   ['compare', 'good'],
  'compare_info':   ['compare', 'good'],
  'page_favorites': ['favorites', 'good'],
  'favorites_info': ['favorites', 'good'],
}
BLOCK_UNBIND = list(BLOCK_LINKS.keys())


async def _table_exists(db, name):
  row = await db.query(
    query='SELECT COUNT(*) c FROM information_schema.TABLES '
          'WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME=%s',
    values=[name], onerow=1, errors=[])
  return bool(row and row.get('c'))


async def _column_exists(db, table, column):
  row = await db.query(
    query='SELECT COUNT(*) c FROM information_schema.COLUMNS '
          'WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME=%s AND COLUMN_NAME=%s',
    values=[table, column], onerow=1, errors=[])
  return bool(row and row.get('c'))


async def main():
  db = FreshDB(config['connects']['crm_write'])
  await db.create_pool()
  try:
    if not await _table_exists(db, 'ds_options'):
      raise SystemExit('ds_options: таблица не найдена')

    # 1. Колонки
    if not await _column_exists(db, 'ds_options', 'parent_id'):
      await db.query(
        query="ALTER TABLE `ds_options` "
              "ADD COLUMN `parent_id` int unsigned NULL DEFAULT NULL "
              "COMMENT 'Родительская опция (иерархия/зависимости)'",
        values=[], errors=[])
      await db.query(query='ALTER TABLE `ds_options` ADD KEY `parent_id` (`parent_id`)',
                     values=[], errors=[])
      print('ds_options.parent_id: добавлена')
    if not await _column_exists(db, 'ds_options', 'note'):
      await db.query(
        query="ALTER TABLE `ds_options` "
              "ADD COLUMN `note` varchar(255) NOT NULL DEFAULT '' "
              "COMMENT 'Подсказка для интерфейса'",
        values=[], errors=[])
      print('ds_options.note: добавлена')
    if db.error_str:
      raise SystemExit(f'ALTER ds_options: {db.error_str}')

    # 2-3. Карта name -> id (нужна для parent_id и привязок)
    rows = await db.query(query='SELECT id, name FROM ds_options', values=[], errors=[]) or []
    id_by_name = {str(r['name']): int(r['id']) for r in rows}
    if db.error_str:
      raise SystemExit(f'SELECT ds_options: {db.error_str}')

    # 2. Родители, заголовки, подсказки
    for name, (header, parent, note, sort) in OPTIONS.items():
      oid = id_by_name.get(name)
      if oid is None:
        print(f'  ! опция {name} не найдена — пропуск')
        continue
      sets, values = [], []
      if header is not None:
        sets.append('header=%s'); values.append(header)
      if parent is not None:
        pid = id_by_name.get(parent)
        if pid is None:
          print(f'  ! родитель {parent} для {name} не найден — пропуск parent_id')
        else:
          sets.append('parent_id=%s'); values.append(pid)
      if note is not None:
        sets.append('note=%s'); values.append(note)
      if sort is not None:
        sets.append('sort=%s'); values.append(sort)
      if not sets:
        continue
      values.append(oid)
      await db.query(query='UPDATE ds_options SET ' + ', '.join(sets) + ' WHERE id=%s',
                     values=values, errors=[])

    # 3. Новые опции
    for name, (header, sort, note) in NEW_OPTIONS.items():
      if name in id_by_name:
        continue
      await db.query(
        query='INSERT INTO ds_options(header,name,sort,icon,tool,type,config,is_menu,parent_id,note) '
              'VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',
        values=[header, name, sort, '', '', 'vue', '', 0, id_by_name.get('good'), note],
        errors=[])
    if db.error_str:
      raise SystemExit(f'upsert ds_options: {db.error_str}')

    rows = await db.query(query='SELECT id, name FROM ds_options', values=[], errors=[]) or []
    id_by_name = {str(r['name']): int(r['id']) for r in rows}

    # 4. Перепривязка блоков
    await db.query(
      query='DELETE FROM ds_blocks_options WHERE block_name IN (%s)'
            % ','.join(['%s'] * len(BLOCK_UNBIND)),
      values=BLOCK_UNBIND, errors=[])
    for block, opts in BLOCK_LINKS.items():
      for o in opts:
        oid = o if isinstance(o, int) else id_by_name.get(o)
        if oid is None:
          print(f'  ! опция {o} не найдена — блок {block} без привязки')
          continue
        await db.query(
          query='INSERT IGNORE INTO ds_blocks_options(block_name,option_id) VALUES(%s,%s)',
          values=[block, oid], errors=[])
    if db.error_str:
      raise SystemExit(f'ds_blocks_options: {db.error_str}')

    # 5. Выдача новых опций проектам с включённой опцией «Товары»
    good_id = id_by_name.get('good')
    for name in NEW_OPTIONS:
      oid = id_by_name.get(name)
      if oid is None or good_id is None:
        continue
      await db.query(
        query='INSERT IGNORE INTO ds_options_project(project_id, option_id) '
              'SELECT DISTINCT op.project_id, %s FROM ds_options_project op '
              'WHERE op.option_id=%s AND NOT EXISTS ('
              '  SELECT 1 FROM ds_options_project x '
              '  WHERE x.project_id=op.project_id AND x.option_id=%s)',
        values=[oid, good_id, oid], errors=[])
    if db.error_str:
      raise SystemExit(f'ds_options_project: {db.error_str}')

    print('ds_options: иерархия, новые опции, привязки блоков — ok')
  finally:
    await db.close_pool()


if __name__ == '__main__':
  asyncio.run(main())
