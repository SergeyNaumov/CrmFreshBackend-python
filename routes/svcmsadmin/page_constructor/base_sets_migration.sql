-- Наборы базовых страниц конструктора.
-- Выполнить один раз на БД.
--
-- 1) Справочник наборов + именованный текущий набор etalon-1 (дефолтный).
-- 2) template_pages_base привязывается к набору (set_id), url уникален внутри набора.
-- 3) domain_constructor помнит набор, применённый к домену.

CREATE TABLE IF NOT EXISTS `base_pages_set` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `sort` int NOT NULL DEFAULT 0,
  `is_default` tinyint(1) NOT NULL DEFAULT 0,
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
  COMMENT='Наборы базовых страниц конструктора';

INSERT INTO `base_pages_set` (`id`,`name`,`sort`,`is_default`) VALUES (1,'etalon-1',1,1)
  ON DUPLICATE KEY UPDATE `name`=VALUES(`name`), `is_default`=VALUES(`is_default`);

ALTER TABLE `template_pages_base`
  DROP INDEX `url`,
  ADD COLUMN `set_id` int unsigned NOT NULL DEFAULT 1,
  ADD UNIQUE KEY `set_id_url` (`set_id`,`url`),
  ADD CONSTRAINT `fk_tpb_set` FOREIGN KEY (`set_id`) REFERENCES `base_pages_set`(`id`) ON DELETE CASCADE;

ALTER TABLE `domain_constructor`
  ADD COLUMN `base_set_id` int unsigned NULL,
  ADD KEY `base_set_id` (`base_set_id`),
  ADD CONSTRAINT `fk_dc_base_set` FOREIGN KEY (`base_set_id`) REFERENCES `base_pages_set`(`id`) ON DELETE SET NULL;
