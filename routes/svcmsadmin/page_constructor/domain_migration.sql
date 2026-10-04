-- Перенос конструктора страниц с template_id на domain_id.
-- Выполнить один раз на БД. Старые таблицы template_page / template_constructor /
-- template_theme_* не удаляются этим скриптом (см. domain_cleanup.sql).

-- ---------- новые таблицы ----------

CREATE TABLE IF NOT EXISTS `domain_page` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `domain_id` int NOT NULL,
  `url` varchar(200) NOT NULL DEFAULT '' COMMENT 'url страницы',
  `header` varchar(255) DEFAULT NULL COMMENT 'название страницы',
  `blocks` mediumtext COMMENT 'json списка блоков (v2)',
  PRIMARY KEY (`id`),
  UNIQUE KEY `domain_id_url` (`domain_id`,`url`),
  CONSTRAINT `fk_dp_domain` FOREIGN KEY (`domain_id`) REFERENCES `domain` (`domain_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Страницы домена (конструктор)';

CREATE TABLE IF NOT EXISTS `domain_constructor` (
  `domain_id` int NOT NULL,
  `color` varchar(100) NOT NULL DEFAULT 'digitalstrateg',
  `style` varchar(100) NOT NULL DEFAULT 'soft',
  `layout` varchar(100) NOT NULL DEFAULT 'standard',
  `font` varchar(100) NOT NULL DEFAULT 'inter',
  `color_css` mediumtext,
  `style_css` mediumtext,
  `layout_css` mediumtext,
  `font_css` mediumtext,
  `header_blocks` mediumtext COMMENT 'шапка (json v2)',
  `footer_blocks` mediumtext COMMENT 'подвал (json v2)',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`domain_id`),
  CONSTRAINT `fk_dc_domain` FOREIGN KEY (`domain_id`) REFERENCES `domain` (`domain_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Тема и структура домена (конструктор)';

CREATE TABLE IF NOT EXISTS `domain_theme_color` (
  `domain_id` int NOT NULL DEFAULT '0' COMMENT '0 — общий пресет, >0 — индивидуальный домена',
  `header` varchar(100) NOT NULL COMMENT 'идентификатор схемы',
  `label` varchar(255) NOT NULL DEFAULT '',
  `short` varchar(500) NOT NULL DEFAULT '',
  `descr` text,
  `css` mediumtext NOT NULL,
  `sort` int NOT NULL DEFAULT '0',
  `is_default` tinyint(1) NOT NULL DEFAULT '0',
  `is_custom` tinyint(1) NOT NULL DEFAULT '0',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`domain_id`,`header`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Схемы цвета темы';

CREATE TABLE IF NOT EXISTS `domain_theme_style` (
  `domain_id` int NOT NULL DEFAULT '0' COMMENT '0 — общий пресет, >0 — индивидуальный домена',
  `header` varchar(100) NOT NULL COMMENT 'идентификатор схемы',
  `label` varchar(255) NOT NULL DEFAULT '',
  `short` varchar(500) NOT NULL DEFAULT '',
  `descr` text,
  `css` mediumtext NOT NULL,
  `sort` int NOT NULL DEFAULT '0',
  `is_default` tinyint(1) NOT NULL DEFAULT '0',
  `is_custom` tinyint(1) NOT NULL DEFAULT '0',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`domain_id`,`header`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Схемы стиля темы';

CREATE TABLE IF NOT EXISTS `domain_theme_layout` (
  `domain_id` int NOT NULL DEFAULT '0' COMMENT '0 — общий пресет, >0 — индивидуальный домена',
  `header` varchar(100) NOT NULL COMMENT 'идентификатор схемы',
  `label` varchar(255) NOT NULL DEFAULT '',
  `short` varchar(500) NOT NULL DEFAULT '',
  `descr` text,
  `css` mediumtext NOT NULL,
  `sort` int NOT NULL DEFAULT '0',
  `is_default` tinyint(1) NOT NULL DEFAULT '0',
  `is_custom` tinyint(1) NOT NULL DEFAULT '0',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`domain_id`,`header`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Схемы компоновки темы';

CREATE TABLE IF NOT EXISTS `domain_theme_font` (
  `domain_id` int NOT NULL DEFAULT '0' COMMENT '0 — общий пресет, >0 — индивидуальный домена',
  `header` varchar(100) NOT NULL COMMENT 'идентификатор схемы',
  `label` varchar(255) NOT NULL DEFAULT '',
  `short` varchar(500) NOT NULL DEFAULT '',
  `descr` text,
  `css` mediumtext NOT NULL,
  `sort` int NOT NULL DEFAULT '0',
  `is_default` tinyint(1) NOT NULL DEFAULT '0',
  `is_custom` tinyint(1) NOT NULL DEFAULT '0',
  `updated` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`domain_id`,`header`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='Схемы шрифта темы';

-- ---------- перенос данных ----------
-- Источник: template_id=2504 (Digitalstrateg Demo1) → домен 9706 (demo1.digitalstrateg.ru).

SET @src_tpl = 2504;
SET @dst_dom = 9706;

-- пресеты (is_custom=0) → общие, domain_id=0
INSERT INTO domain_theme_color  (domain_id,header,label,short,descr,css,sort,is_default,is_custom)
  SELECT 0,name,label,short,descr,css,sort,is_default,is_custom FROM template_theme_color  WHERE is_custom=0;
INSERT INTO domain_theme_style  (domain_id,header,label,short,descr,css,sort,is_default,is_custom)
  SELECT 0,name,label,short,descr,css,sort,is_default,is_custom FROM template_theme_style  WHERE is_custom=0;
INSERT INTO domain_theme_layout (domain_id,header,label,short,descr,css,sort,is_default,is_custom)
  SELECT 0,name,label,short,descr,css,sort,is_default,is_custom FROM template_theme_layout WHERE is_custom=0;
INSERT INTO domain_theme_font   (domain_id,header,label,short,descr,css,sort,is_default,is_custom)
  SELECT 0,name,label,short,descr,css,sort,is_default,is_custom FROM template_theme_font   WHERE is_custom=0;

-- кастомные схемы (is_custom=1) → индивидуальные для целевого домена
INSERT INTO domain_theme_color  (domain_id,header,label,short,descr,css,sort,is_default,is_custom)
  SELECT @dst_dom,name,label,short,descr,css,sort,is_default,is_custom FROM template_theme_color  WHERE is_custom=1;
INSERT INTO domain_theme_style  (domain_id,header,label,short,descr,css,sort,is_default,is_custom)
  SELECT @dst_dom,name,label,short,descr,css,sort,is_default,is_custom FROM template_theme_style  WHERE is_custom=1;
INSERT INTO domain_theme_layout (domain_id,header,label,short,descr,css,sort,is_default,is_custom)
  SELECT @dst_dom,name,label,short,descr,css,sort,is_default,is_custom FROM template_theme_layout WHERE is_custom=1;
INSERT INTO domain_theme_font   (domain_id,header,label,short,descr,css,sort,is_default,is_custom)
  SELECT @dst_dom,name,label,short,descr,css,sort,is_default,is_custom FROM template_theme_font   WHERE is_custom=1;

-- тема шаблона
-- header_blocks/footer_blocks переносятся только если эти колонки уже есть
-- в template_constructor (structure_migration.sql). Иначе шапка/подвал
-- подхватятся из страниц (fallback _structure_from_pages).
SET @has_hf = (
  SELECT COUNT(*) FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA=DATABASE() AND TABLE_NAME='template_constructor' AND COLUMN_NAME='header_blocks'
);

INSERT INTO domain_constructor (domain_id,color,style,layout,font,color_css,style_css,layout_css,font_css)
  SELECT @dst_dom,color,style,layout,font,color_css,style_css,layout_css,font_css
  FROM template_constructor WHERE template_id=@src_tpl;

SET @hf_upd = IF(@has_hf > 0,
  'UPDATE domain_constructor d JOIN template_constructor t ON t.template_id=@src_tpl'
  ' SET d.header_blocks=t.header_blocks, d.footer_blocks=t.footer_blocks WHERE d.domain_id=@dst_dom',
  'DO 0');
PREPARE st_hf FROM @hf_upd;
EXECUTE st_hf;
DEALLOCATE PREPARE st_hf;

-- страницы
INSERT INTO domain_page (domain_id,url,header,blocks)
  SELECT @dst_dom,url,header,blocks FROM template_page WHERE template_id=@src_tpl;

-- ---------- проверка ----------
-- SELECT COUNT(*) FROM domain_page WHERE domain_id=9706;             -- 19
-- SELECT * FROM domain_constructor WHERE domain_id=9706;             -- 1 строка
-- SELECT domain_id,COUNT(*) FROM domain_theme_style GROUP BY domain_id;
