#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tools/syncsvcmsmanager.py — синхронизация кода менеджера (svcms manager) на прод.

Заливает из текущего репозитория в {base} на сервере:
  lib/            -> {base}/lib/
  routes/         -> {base}/routes/
  conf_projects/  -> {base}/conf_projects/   (только с флагом --projects)

Не трогает config.py / config_*.py (их нет внутри lib|routes), conf/ и БД.
Приёмник по умолчанию: /var/www/svcms-async/manager/backend
(тот же каталог, что /var/www/svcms/manager/backend на проде).

Примеры:
  ./tools/syncsvcmsmanager.py --dry-run
  ./tools/syncsvcmsmanager.py                 # заливает lib/ и routes/
  ./tools/syncsvcmsmanager.py --projects      # + conf_projects/
  ./tools/syncsvcmsmanager.py --reload        # + перечитать конфиги (touch routes)

ENV (как в sync/*.sh и /var/www/svcms-async/tools/*.sh):
  SSH_HOST, SSH_PORT, SSH_USER, REMOTE_BASE
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
  repo_root = Path(__file__).resolve().parent.parent

  parser = argparse.ArgumentParser(
    description='Синхронизация кода svcms-manager (lib/routes[/conf_projects]) на прод.',
  )
  parser.add_argument('--host', default=os.environ.get('SSH_HOST', '178.57.220.192'))
  parser.add_argument('--port', default=os.environ.get('SSH_PORT', '7725'))
  parser.add_argument('--user', default=os.environ.get('SSH_USER', 'naumov'))
  parser.add_argument(
    '--base',
    default=os.environ.get('REMOTE_BASE', '/var/www/svcms-async/manager/backend'),
    help='каталог backend менеджера на сервере',
  )
  parser.add_argument('--projects', action='store_true',
                      help='дополнительно синхронизировать conf_projects/')
  parser.add_argument('--dry-run', action='store_true',
                      help='показать, что будет залито (rsync -n), ничего не меняя')
  parser.add_argument('--reload', action='store_true',
                      help='после заливки сделать touch в routes/ (uvicorn --reload перечитает)')
  args = parser.parse_args()

  # --- проверки -------------------------------------------------------------
  if shutil.which('rsync') is None:
    print('❌ не найден rsync', file=sys.stderr)
    return 1

  sources = [('lib', repo_root / 'lib'), ('routes', repo_root / 'routes')]
  if args.projects:
    sources.append(('conf_projects', repo_root / 'conf_projects'))

  for name, path in sources:
    if not path.is_dir():
      print(f'❌ нет локального каталога {name}: {path}', file=sys.stderr)
      return 1

  target = f'{args.user}@{args.host}'
  base = args.base.rstrip('/')

  rsync_opts = [
    '-rltvz', '-O',
    '--no-perms', '--no-owner', '--no-group',
    '--human-readable', '--info=progress2',
    '--exclude=__pycache__/', '--exclude=*.pyc',
    '-e', f'ssh -p {args.port}',
  ]
  if args.dry_run:
    rsync_opts.append('-n')

  print(f'▶ репозиторий : {repo_root}')
  print(f'▶ приёмник    : {target}:{base}')
  print(f'▶ каталоги    : {", ".join(name for name, _ in sources)}'
        + ('  [DRY-RUN]' if args.dry_run else ''))
  print()

  for name, path in sources:
    dst = f'{target}:{base}/{name}/'
    print(f'═══ {name}/  ->  {dst}')
    cmd = ['rsync', *rsync_opts, f'{path}/', dst]
    rc = subprocess.call(cmd)
    if rc != 0:
      print(f'❌ rsync вернул код {rc} на {name}/', file=sys.stderr)
      return rc

  if args.reload and not args.dry_run:
    # systemd смотрит routes/ (см. --reload-dir svcms.manager.service);
    # touch заставляет uvicorn перечитать модули, включая изменённый lib/.
    print('▶ перечитываю конфиги (touch routes/__init__.py на сервере)')
    subprocess.call([
      'ssh', '-p', args.port, target, f"touch '{base}/routes/__init__.py' 2>/dev/null || true",
    ])

  print('\n✅ Готово.' + (' (dry-run: изменения не вносились)' if args.dry_run else ''))
  return 0


if __name__ == '__main__':
  sys.exit(main())
