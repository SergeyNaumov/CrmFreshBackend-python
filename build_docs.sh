#!/bin/bash
# Сборка HTML-документации: docs-developer/*.md -> docs-html/*.html
# Запуск из корня репозитория: ./build_docs.sh
set -e
cd "$(dirname "$0")"
.venv/bin/mkdocs build
echo "Готово: docs-html/index.html (открыть в браузере или: python -m http.server -d docs-html)"
