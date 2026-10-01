-- Шапка/подвал на уровень шаблона для конструктора страниц.
-- Выполнить один раз на БД шаблонов.
ALTER TABLE template_constructor
  ADD COLUMN header_blocks MEDIUMTEXT NULL,
  ADD COLUMN footer_blocks MEDIUMTEXT NULL;
