# Восстановление потерянных связей «рубрика → параметры» (ds_params_catalog)
# по фактам заполнения значений у товаров (ds_params_good).
#
#   export config=config_svcms_manager
#   .venv/bin/python -m db.restore_ds_params_catalog 5841 --dry-run
#   .venv/bin/python -m db.restore_ds_params_catalog 5841
#
# Идемпотентна: существующие пары (catalog_id, param_id) проекта не трогает,
# новые получают sort = текущий максимум по рубрике + порядок param_id.
# Нужна, когда у товаров есть значения характеристик, а рубрика их «Параметры
# рубрик» не настроена: сайт такие характеристики не показывает
# (sites/lib/dsengine/params.py::good_params берёт их из цепочки рубрик),
# и в карточке товара они не видны.

import asyncio
import sys

from db import FreshDB
from config import config


async def main():
  if len(sys.argv) < 2 or not sys.argv[1].isdigit():
    raise SystemExit('укажите project_id: python -m db.restore_ds_params_catalog <project_id> [--dry-run]')
  project_id = int(sys.argv[1])
  dry = '--dry-run' in sys.argv

  db = FreshDB(config['connects']['crm_write'])
  await db.create_pool()

  # Факты: какие параметры реально заполнены у товаров каждой рубрики
  used = await db.query(
    query='SELECT g.rubricator_id catalog_id, pg.param_id '
          'FROM ds_good g JOIN ds_params_good pg ON pg.good_id=g.id '
          'WHERE g.project_id=%s AND g.rubricator_id IS NOT NULL '
          'AND g.rubricator_id>0 '
          'GROUP BY g.rubricator_id, pg.param_id '
          'ORDER BY g.rubricator_id, pg.param_id',
    values=[project_id], errors=[],
  ) or []

  existing = await db.query(
    query='SELECT catalog_id, param_id, sort FROM ds_params_catalog '
          'WHERE project_id=%s',
    values=[project_id], errors=[],
  ) or []
  have = {(int(r['catalog_id']), int(r['param_id'])) for r in existing}
  max_sort = {}
  for r in existing:
    cid = int(r['catalog_id'])
    max_sort[cid] = max(max_sort.get(cid, 0), int(r.get('sort') or 0))

  plan = {}
  for r in used:
    cid, pid = int(r['catalog_id']), int(r['param_id'])
    if (cid, pid) in have:
      continue
    plan.setdefault(cid, [])
    if pid not in plan[cid]:
      plan[cid].append(pid)

  total = sum(len(v) for v in plan.values())
  if not total:
    print(f'restore_ds_params_catalog: проект {project_id} — потерянных связей нет')
  for cid, pids in sorted(plan.items()):
    print(f'  рубрика {cid}: +{len(pids)} параметров {pids}')
    if not dry:
      s = max_sort.get(cid, 0)
      for pid in pids:
        s += 1
        await db.query(
          query='INSERT INTO ds_params_catalog (param_id, catalog_id, sort, '
                'project_id) VALUES (%s,%s,%s,%s)',
          values=[pid, cid, s, project_id], errors=[],
        )

  print(('[dry-run] ' if dry else '') + f'проект {project_id}: '
        f'{"было бы вставлено" if dry else "вставлено"} связей: {total}')

  await db.close_pool()
  if db.error_str:
    raise SystemExit(f'restore_ds_params_catalog: {db.error_str}')


if __name__ == '__main__':
  asyncio.run(main())
