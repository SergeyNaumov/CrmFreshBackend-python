import re

from lib.core import exists_arg, del_file_and_resizes

# Хелперы удаления сущностей конструктора и их «хвостов» (файлы + ресайзы).
# Используются роутами удаления (delete-element / admin-tree delete_branch):
#   * файлы самой записи и всех её file-полей (кроме виртуальных `expr`);
#   * дочерние записи 1_to_m вместе с их файлами;
#   * потомки дерева (parent_id) — рекурсивно, вместе с файлами.
# Каталоги `files/...` НЕ удаляются — только файлы.


def _plain_table(form):
    """work_table — простое имя таблицы (старый формат — подзапрос — не трогаем)."""
    return bool(re.match(r'^\w+$', str(form.work_table or '')))


async def _delete_record_files(form, record_id):
    """Удаляет файлы (base + все ресайзы) file-полей записи."""
    for f in form.fields:
        if f.get('type') == 'file' and not exists_arg('expr', f):
            value = await form.db.query(
                query=f'SELECT {f["name"]} FROM {form.work_table} '
                      f'WHERE {form.work_table_id}=%s',
                values=[record_id], onevalue=1, errors=[],
            )
            if value:
                del_file_and_resizes(field=f, value=value)


async def descendant_ids(form, record_id):
    """id всех потомков записи в дереве (рекурсивно по parent_id)."""
    if not form.tree_use or not _plain_table(form):
        return []
    result = []
    cur = [record_id]
    while cur:
        ph = ','.join(['%s'] * len(cur))
        rows = await form.db.query(
            query=f'SELECT {form.work_table_id} AS id FROM {form.work_table} '
                  f'WHERE parent_id IN ({ph})',
            values=cur, errors=[],
        ) or []
        nxt = [r['id'] for r in rows if r['id'] not in result]
        result += nxt
        cur = nxt
    return result


async def children_count(form, record_id):
    """Сколько дочерних (1_to_m) и потомков дерева у записи — для попапа."""
    total = 0
    for f in form.fields:
        if f.get('type') == '1_to_m':
            c = await form.db.query(
                query=f'SELECT COUNT(*) FROM {f["table"]} WHERE {f["foreign_key"]}=%s',
                values=[record_id], onevalue=1, errors=[],
            )
            total += int(c or 0)
    total += len(await descendant_ids(form, record_id))
    return total


async def cascade_delete(form, record_id=None):
    """Каскадное удаление записи: файлы + дети 1_to_m + потомки дерева.

    Вызывается роутами ПЕРЕД удалением самой записи (саму строку удаляет роут).
    """
    if record_id is None:
        record_id = form.id
    if not record_id or not _plain_table(form):
        return

    # 1) дети 1_to_m: файлы + строки
    for f in form.fields:
        if f.get('type') != '1_to_m':
            continue
        child_files = [cf for cf in (f.get('fields') or []) if cf.get('type') == 'file'
                       and not exists_arg('expr', cf)]
        if child_files:
            cols = ','.join(cf['name'] for cf in child_files)
            rows = await form.db.query(
                query=f'SELECT {cols} FROM {f["table"]} WHERE {f["foreign_key"]}=%s',
                values=[record_id], errors=[],
            ) or []
            for row in rows:
                for cf in child_files:
                    v = row.get(cf['name'])
                    if v:
                        del_file_and_resizes(field=cf, value=v)
        await form.db.query(
            query=f'DELETE FROM {f["table"]} WHERE {f["foreign_key"]}=%s',
            values=[record_id], errors=[],
        )

    # 2) потомки дерева: файлы + строки
    if form.tree_use:
        ids = await descendant_ids(form, record_id)
        for cid in ids:
            await _delete_record_files(form, cid)
        if ids:
            ph = ','.join(['%s'] * len(ids))
            await form.db.query(
                query=f'DELETE FROM {form.work_table} WHERE {form.work_table_id} IN ({ph})',
                values=ids, errors=[],
            )

    # 3) файлы самой записи
    await _delete_record_files(form, record_id)
