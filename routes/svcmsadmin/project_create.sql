-- Быстрое создание проекта (svcmsadmin-createproject).
-- Выполнить один раз на БД админки.
--
-- 1) Маркер шаблона-конструктора — template.type=6. Отдельная колонка
--    ds_constructor больше не используется (в коде ссылок нет).
ALTER TABLE `template` DROP COLUMN `ds_constructor`;

-- 2) Включаем пункт меню «Быстрое создание проекта».
UPDATE `admin_menu_new` SET `enabled`=1 WHERE `value`='svcmsadmin-createproject';
