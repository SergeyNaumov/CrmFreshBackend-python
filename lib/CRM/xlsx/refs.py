"""Общий резолвер ссылок (рубрики, бренды) для импорта xlsx.

Используется и при проверке файла (routes/parser_excel/refs.py, действие
check_refs), и при самой загрузке (before_loopback конфига парсера), чтобы
правило "id или название" было описано в одном месте.

Дескриптор ссылки (ref) задаётся в конфиге парсера:
  {
    'key':'rubric',                 # ключ ссылки (для create_refs)
    'label':'рубрики',              # как показывать пользователю
    'one':'рубрика',                # ед.ч. для сообщений
    'table':'ds_catalog',
    'id_field':'rubricator_id',     # колонка-источник id
    'name_field':'rubricator_name', # колонка-источник названия (может = id_field)
    'name_col':'header',            # колонка названия в целевой таблице
    'scope':{'project_id':5844},    # принадлежность текущему проекту
    'allow_zero':0,                 # 0 -- допустимое значение (бренд "без бренда")
    'create':{'path':'','anons':'',...},  # значения для INSERT при создании
    'chpu':{'in_url':'/catalog/<%id%>','prefix':'/catalog/'},  # опционально
  }
"""


def clean(v):
  if v is None:
    return ''
  return str(v).replace('\xa0', ' ').strip()


def norm_int(v):
  # "1 200", "1200.0", "1200,50" -> int; мусор -> None
  s = clean(v).replace(' ', '')
  if s == '':
    return None
  s = s.replace(',', '.')
  try:
    return int(float(s))
  except (TypeError, ValueError):
    return None


class RefResolver:
  """Резолвит значение ссылки к id в рамках проекта, с кэшем на запрос."""

  def __init__(self, db, ref, errors=None):
    self.db = db
    self.ref = ref
    self.errors = errors if errors is not None else []
    self.table = ref['table']
    self.scope = ref.get('scope') or {}
    self.name_col = ref.get('name_col', 'name')
    self.id_field = ref.get('id_field')
    self.name_field = ref.get('name_field') or self.id_field
    self.allow_zero = ref.get('allow_zero', 0)
    self.one = ref.get('one') or ref.get('label') or 'запись'
    self._by_id = {}
    self._by_name = {}

  def _scope_where(self):
    parts = []
    values = []
    for col, val in self.scope.items():
      parts.append('`' + col + '`=%s')
      values.append(val)
    return ' AND '.join(parts), values

  async def _id_in_scope(self, rid):
    if rid in self._by_id:
      return self._by_id[rid]
    where, values = self._scope_where()
    query = f'SELECT id FROM `{self.table}` WHERE {where} AND id=%s LIMIT 1'
    row = await self.db.query(query=query, values=values + [rid], onerow=1, errors=[])
    ok = bool(row)
    self._by_id[rid] = ok
    return ok

  async def _id_exists_anywhere(self, rid):
    row = await self.db.query(
      query=f'SELECT id FROM `{self.table}` WHERE id=%s LIMIT 1',
      values=[rid], onerow=1, errors=[])
    return bool(row)

  async def _name_to_id(self, name):
    if name in self._by_name:
      return self._by_name[name]
    where, values = self._scope_where()
    query = f'SELECT id FROM `{self.table}` WHERE {where} AND `{self.name_col}`=%s LIMIT 1'
    row = await self.db.query(query=query, values=values + [name], onerow=1, errors=[])
    rid = row['id'] if row else None
    self._by_name[name] = rid
    return rid

  async def resolve(self, id_v, name_v):
    """Вернуть {'id':int} при успехе и/или
    {'bad_id':int,'foreign_id':0|1}, {'missing_name':str,'note':str}.

    Правило: сначала валидный id в рамках проекта, иначе -- название.
    Для ссылки с одной колонкой (id_field==name_field) нечисловое значение
    считается названием.
    """
    id_v = clean(id_v)
    name_v = clean(name_v)
    out = {}

    rid = norm_int(id_v) if id_v != '' else None
    if id_v != '' and rid is None:
      # нечисловое значение в id-колонке = название (одноколоночный бренд)
      if not name_v:
        name_v = id_v
      id_v = ''
      rid = None

    if rid is not None:
      if rid == 0 and self.allow_zero:
        return {'id': 0}
      if await self._id_in_scope(rid):
        return {'id': rid}
      foreign = await self._id_exists_anywhere(rid)
      out['bad_id'] = rid
      out['foreign_id'] = 1 if foreign else 0
      out['note'] = f'{self.one} id={rid} — ' + (
        'принадлежит другому проекту' if foreign else 'не существует')

    if name_v:
      nid = await self._name_to_id(name_v)
      if nid:
        out['id'] = nid
        return out
      out['missing_name'] = name_v
      out['note'] = f'{self.one} «{name_v}» — нет в текущем проекте'

    return out

  async def create(self, name):
    """Идемпотентно создать ссылку по названию. Вернуть id или None."""
    name = clean(name)
    if not name:
      return None
    nid = await self._name_to_id(name)
    if nid:
      return nid
    data = dict(self.ref.get('create') or {})
    data[self.name_col] = name
    for col, val in self.scope.items():
      data[col] = val
    rid = await self.db.save(table=self.table, data=data, errors=self.errors)
    if not rid:
      return None
    self._by_name[name] = rid
    self._by_id[rid] = True
    await self._save_chpu(rid, name)
    return rid

  async def _save_chpu(self, rid, name):
    chpu = self.ref.get('chpu')
    if not chpu:
      return
    from types import SimpleNamespace
    from lib.CRM.chpu import generate_ext_url, save_chpu
    in_url = str(chpu.get('in_url') or '').replace('<%id%>', str(rid))
    prefix = chpu.get('prefix') or ''
    project_id = self.scope.get('project_id')
    # хелперы ЧПУ работают только с form.db/form.errors
    form = SimpleNamespace(db=self.db, errors=self.errors)
    ext_url = await generate_ext_url(
      form, name, prefix=prefix, project_id=project_id, exclude_in_url=in_url)
    await save_chpu(form, in_url, ext_url, project_id)
