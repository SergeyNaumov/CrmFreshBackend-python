CREATE TABLE IF NOT EXISTS `[%table_name%]` (
  `[%table_id%]` int unsigned NOT NULL AUTO_INCREMENT,
  `header` varchar(255) NOT NULL DEFAULT '',
  `anons` text,
  `body` mediumtext,
  `photo` varchar(255) NOT NULL DEFAULT '',
  `sort` int NOT NULL DEFAULT 0,
  `enabled` tinyint(1) NOT NULL DEFAULT 1,
  `project_id` int unsigned NOT NULL DEFAULT 0,
  PRIMARY KEY (`[%table_id%]`),
  KEY project_id (`project_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
