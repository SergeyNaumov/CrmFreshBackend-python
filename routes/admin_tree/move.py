import re
from lib.core import exists_arg


async def move(form, R):
    """Перенос узла дерева в другую ветку (parent_id + path + пути потомков)."""
    to = str(exists_arg('to', R) or '').strip()
    item_id = form.id

    if not item_id:
        form.errors.append('Параметр id не указан, обратитесь к разработчику')

    elif form.read_only or not form.tree_use:
        form.errors.append('Запрещено перемещать элементы в дереве! операция не выполнена')

    elif to and not to.isnumeric():
        form.errors.append('Параметр to указан неверно, обратитесь к разработчику')

    elif to and str(to) == str(item_id):
        form.errors.append('Нельзя перенести элемент в себя')

    else:
        from_path, to_path = '', ''
        if to:
            to_item = await form.db.query(
                query=f'SELECT * from {form.work_table} WHERE {form.work_table_id}=%s',
                values=[to], onerow=1,
            )
            if to_item:
                to_path = exists_arg('path', to_item) or ''
            else:
                form.errors.append('в базе отсутствует элемент-приёмник. Возможно, состояние базы было изменено')

        from_item = await form.db.query(
            query=f'SELECT * from {form.work_table} WHERE {form.work_table_id}=%s',
            values=[item_id], onerow=1,
        )
        if from_item:
            from_path = exists_arg('path', from_item) or ''
        else:
            form.errors.append('в базе отсутствует элемент-источник. Возможно, состояние базы было изменено')

        # Защита от цикла: нельзя перенести в себя или в собственного потомка
        # (потомки имеют path, начинающийся с path узла + '/').
        if not form.errors and to:
            if to_path == from_path or to_path.startswith(from_path + '/'):
                form.errors.append('Нельзя переместить элемент в собственный потомок')

        if not form.errors:
            new_to_path = (to_path + '/' + str(to)) if to else ''

            await form.db.query(
                query=f'UPDATE {form.work_table} SET parent_id=%s, path=%s WHERE {form.work_table_id}=%s',
                values=[(to if to else None), new_to_path, item_id],
            )

            # Пересчёт путей потомков: старый префикс (path узла + '/' + id) -> новый.
            old_prefix = (from_path + '/' + str(item_id)) if from_path else ('/' + str(item_id))
            new_prefix = (new_to_path + '/' + str(item_id)) if new_to_path else ('/' + str(item_id))

            childs = await form.db.query(
                query=f'SELECT {form.work_table_id} id, path from {form.work_table} WHERE path=%s OR path like %s',
                values=[old_prefix, old_prefix + '/%'],
            )

            for c in childs:
                path = exists_arg('path', c) or ''
                new_path = re.sub('^' + re.escape(old_prefix), lambda m: new_prefix, path)
                await form.db.query(
                    query=f'UPDATE {form.work_table} SET path=%s WHERE {form.work_table_id}=%s',
                    values=[new_path, c['id']],
                )

    return {
        'success': (1, 0)[len(form.errors)],
        'errors': form.errors,
    }
