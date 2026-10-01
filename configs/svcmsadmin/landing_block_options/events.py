# Опции доступны на редактирование всем администраторам (легаси permissions)
async def permissions_landing_block_options(form):
  form.read_only = 0
  form.make_delete = 1


events = {
  'permissions': [permissions_landing_block_options],
}
