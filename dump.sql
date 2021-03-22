CREATE TABLE `manager` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `login` varchar(50) NOT NULL DEFAULT '',
  `password` varchar(100) NOT NULL DEFAULT '',
  `name` varchar(100) NOT NULL DEFAULT '',
  `email` varchar(100) NOT NULL DEFAULT '',
  `group_id` int(10) unsigned DEFAULT NULL,
  `login_tel` varchar(50) NOT NULL DEFAULT '',
  `re_id` int(10) unsigned NOT NULL DEFAULT '0',
  `gone` tinyint(1) NOT NULL DEFAULT '0',
  `gone_date` date NOT NULL DEFAULT '0000-00-00',
  `phone` varchar(30) NOT NULL DEFAULT '',
  `current_role` int(10) unsigned NOT NULL DEFAULT '0',
  `enabled` tinyint(1) NOT NULL DEFAULT '1',
  `mobile_phone` varchar(30) NOT NULL DEFAULT '',
  `photo` varchar(20) NOT NULL DEFAULT '',
  `phone_dob` varchar(20) NOT NULL DEFAULT '',
  `born` varchar(7) NOT NULL DEFAULT '',
  `position` varchar(50) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `login` (`login`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
INSERT INTO manager(login,password) values('admin',sha2('123',256));


CREATE TABLE `manager_group` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `parent_id` int(11) DEFAULT NULL,
  `path` varchar(20) NOT NULL DEFAULT '',
  `header` varchar(50) NOT NULL DEFAULT '',
  `owner_id` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


CREATE TABLE `session` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `auth_id` int(10) unsigned NOT NULL,
  `registered` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `session_key` varchar(255) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `auth_id` (`auth_id`),
  CONSTRAINT `session_ibfk_1` FOREIGN KEY (`auth_id`) REFERENCES `manager` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `session_fails` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `login` varchar(20) NOT NULL DEFAULT '',
  `ip` varchar(20) NOT NULL DEFAULT '',
  `registered` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `login` (`login`,`registered`),
  KEY `ip` (`ip`,`registered`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `permissions` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `parent_id` int(10) unsigned DEFAULT NULL,
  `sort` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `header` varchar(100) NOT NULL DEFAULT '',
  `pname` varchar(50) NOT NULL DEFAULT '',
  `path` varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  UNIQUE KEY `pname` (`pname`),
  KEY `parent_id` (`parent_id`),
  CONSTRAINT `permissions_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `permissions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

CREATE TABLE `manager_permissions` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `manager_id` int(10) unsigned NOT NULL,
  `permissions_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `manager_id` (`manager_id`),
  KEY `permissions_id` (`permissions_id`),
  CONSTRAINT `manager_permissions_ibfk_1` FOREIGN KEY (`manager_id`) REFERENCES `manager` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `manager_permissions_ibfk_2` FOREIGN KEY (`permissions_id`) REFERENCES `permissions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7676 DEFAULT CHARSET=utf8;
CREATE TABLE `manager_menu` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `parent_id` int(10) unsigned DEFAULT NULL,
  `sort` tinyint(3) unsigned NOT NULL DEFAULT '0',
  `header` varchar(100) NOT NULL DEFAULT '',
  `permission_id` int(10) unsigned DEFAULT NULL,
  `path` varchar(20) NOT NULL DEFAULT '',
  `url` varchar(200) NOT NULL DEFAULT '',
  `target` varchar(20) DEFAULT NULL,
  `params` varchar(512) NOT NULL DEFAULT '',
  `icon` varchar(50) NOT NULL DEFAULT '',
  `value` varchar(512) NOT NULL DEFAULT '',
  `type` varchar(20) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `parent_id` (`parent_id`),
  CONSTRAINT `manager_menu_ibfk_1` FOREIGN KEY (`parent_id`) REFERENCES `manager_menu` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 ;

 CREATE TABLE `manager_menu_permissions` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `denied` tinyint(1) NOT NULL DEFAULT '0',
  `permission_id` int(10) unsigned DEFAULT NULL,
  `menu_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `menu_id` (`menu_id`),
  KEY `permission_id` (`permission_id`),
  CONSTRAINT `manager_menu_permissions_ibfk_1` FOREIGN KEY (`menu_id`) REFERENCES `manager_menu` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `manager_menu_permissions_ibfk_2` FOREIGN KEY (`permission_id`) REFERENCES `permissions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;



CREATE TABLE `manager_group_permissions` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `group_id` int(10) unsigned NOT NULL,
  `permissions_id` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `group_id` (`group_id`),
  KEY `permissions_id` (`permissions_id`),
  CONSTRAINT `manager_group_permissions_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `manager_group` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `manager_group_permissions_ibfk_2` FOREIGN KEY (`permissions_id`) REFERENCES `permissions` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `manager_role` (
  `manager_id` int(10) unsigned DEFAULT NULL COMMENT 'ID менеджера',
  `role` int(10) unsigned DEFAULT NULL COMMENT 'Доступные роли',
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT COMMENT 'ID записи',
  PRIMARY KEY (`id`),
  UNIQUE KEY `manager_id` (`manager_id`,`role`),
  KEY `role` (`role`),
  CONSTRAINT `manager_role_ibfk_1` FOREIGN KEY (`manager_id`) REFERENCES `manager` (`id`) ON DELETE CASCADE,
  CONSTRAINT `manager_role_ibfk_2` FOREIGN KEY (`role`) REFERENCES `manager` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8 COMMENT='Доступные для менеджеров роли (выбираются в карточке менеджера)';