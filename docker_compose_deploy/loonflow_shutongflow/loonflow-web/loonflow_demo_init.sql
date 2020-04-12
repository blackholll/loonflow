# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.17)
# Database: loonflow1111
# Generation Time: 2020-04-12 09:05:16 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table account_apptoken
# ------------------------------------------------------------

DROP TABLE IF EXISTS `account_apptoken`;

CREATE TABLE `account_apptoken` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `app_name` varchar(50) NOT NULL DEFAULT '' COMMENT '调用源应用名',
  `token` varchar(50) NOT NULL DEFAULT '' COMMENT '调用令牌',
  `creator` varchar(50) NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已删除',
  `workflow_ids` varchar(2000) NOT NULL DEFAULT '' COMMENT '有权限的工作流',
  `ticket_sn_prefix` varchar(20) NOT NULL DEFAULT '' COMMENT '生成工单前缀',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `account_apptoken` WRITE;
/*!40000 ALTER TABLE `account_apptoken` DISABLE KEYS */;

INSERT INTO `account_apptoken` (`id`, `app_name`, `token`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `workflow_ids`, `ticket_sn_prefix`)
VALUES
	(1,'ops','8cd585da-3cc6-11e8-9946-784f437daad6','admin','2020-04-12 16:55:46','2020-04-12 16:56:00',0,'1,2','ops');

/*!40000 ALTER TABLE `account_apptoken` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table account_loondept
# ------------------------------------------------------------

DROP TABLE IF EXISTS `account_loondept`;

CREATE TABLE `account_loondept` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `name` varchar(50) NOT NULL DEFAULT '' COMMENT '部门名称',
  `parent_dept_id` int(11) NOT NULL DEFAULT '0' COMMENT '上级部门id',
  `leader` varchar(50) NOT NULL DEFAULT '' COMMENT '部门leader',
  `approver` varchar(100) NOT NULL DEFAULT '0' COMMENT '部门审批人，逗号隔开的username',
  `label` varchar(50) NOT NULL DEFAULT '' COMMENT '标签',
  `creator` varchar(50) NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `account_loondept` WRITE;
/*!40000 ALTER TABLE `account_loondept` DISABLE KEYS */;

INSERT INTO `account_loondept` (`id`, `name`, `parent_dept_id`, `leader`, `approver`, `label`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`)
VALUES
	(1,'loonflow',0,'admin','admin','','admin','2020-04-12 11:24:29','2020-04-12 16:20:24',0),
	(2,'人事部',1,'hr','hr','','admin','2020-04-12 16:20:47','2020-04-12 16:29:05',0),
	(3,'行政部',1,'admin','admin','','admin','2020-04-12 16:21:41','2020-04-12 16:29:19',0),
	(4,'技术部',1,'lilian','lilian','','admin','2020-04-12 16:21:56','2020-04-12 16:29:41',0),
	(5,'交易部',4,'david','david','','admin','2020-04-12 16:23:02','2020-04-12 16:31:04',0),
	(6,'商品部',4,'goods_1','goods_1,goods_2','','admin','2020-04-12 16:23:22','2020-04-12 16:31:17',0),
	(7,'运维部',4,'ops','ops','','admin','2020-04-12 16:23:45','2020-04-12 16:31:30',0);

/*!40000 ALTER TABLE `account_loondept` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table account_loonrole
# ------------------------------------------------------------

DROP TABLE IF EXISTS `account_loonrole`;

CREATE TABLE `account_loonrole` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `name` varchar(50) NOT NULL DEFAULT '' COMMENT '角色名称',
  `description` varchar(50) NOT NULL DEFAULT '' COMMENT '角色描述',
  `label` varchar(50) NOT NULL DEFAULT '' COMMENT '标签',
  `creator` varchar(50) NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `account_loonrole` WRITE;
/*!40000 ALTER TABLE `account_loonrole` DISABLE KEYS */;

INSERT INTO `account_loonrole` (`id`, `name`, `description`, `label`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`)
VALUES
	(1,'运维人员','','','admin','2020-04-12 16:31:59','2020-04-12 16:31:59',0);

/*!40000 ALTER TABLE `account_loonrole` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table account_loonuser
# ------------------------------------------------------------

DROP TABLE IF EXISTS `account_loonuser`;

CREATE TABLE `account_loonuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `password` varchar(128) NOT NULL DEFAULT '' COMMENT '密码',
  `last_login` datetime DEFAULT '0001-01-01 00:00:00' COMMENT '最后登录时间',
  `username` varchar(50) NOT NULL DEFAULT '' COMMENT '用户名',
  `alias` varchar(50) NOT NULL DEFAULT '' COMMENT '中文(昵称)',
  `email` varchar(255) NOT NULL DEFAULT '' COMMENT '邮箱',
  `phone` varchar(13) NOT NULL DEFAULT '' COMMENT '手机号',
  `dept_id` int(11) NOT NULL DEFAULT '0' COMMENT '所属部门id',
  `is_active` tinyint(1) NOT NULL DEFAULT '0' COMMENT '在职',
  `is_admin` tinyint(1) NOT NULL DEFAULT '0' COMMENT '超级管理员',
  `creator` varchar(50) NOT NULL DEFAULT '' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已删除',
  `is_workflow_admin` tinyint(1) NOT NULL DEFAULT '0' COMMENT '工作流管理员',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `account_loonuser` WRITE;
/*!40000 ALTER TABLE `account_loonuser` DISABLE KEYS */;

INSERT INTO `account_loonuser` (`id`, `password`, `last_login`, `username`, `alias`, `email`, `phone`, `dept_id`, `is_active`, `is_admin`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `is_workflow_admin`)
VALUES
	(1,'pbkdf2_sha256$100000$wZONVjuD1eMK$QM6m9gBR44Elj+Qx65kwzPleULawmgzCQm08xMOyZOQ=','2020-04-12 10:59:13','admin','超级管理员','admin@111.com','',1,1,1,'admin','2020-03-15 09:57:07','2020-04-12 17:05:05',0,0),
	(2,'pbkdf2_sha256$100000$bSjYp1QWJ8Yw$i5uNzFg3h7T+RmC2wsSKTy5/wEZ9WFciSgXXA5C28aM=',NULL,'webb','webb','webb@1111.com','',1,1,0,'admin','2020-04-12 16:19:35','2020-04-12 16:19:35',0,0),
	(3,'pbkdf2_sha256$100000$msze9h7jip0Z$i/WlCAwwfJaYtBhJBGq8aCtMCreedHNaKDRIBmYOkcc=',NULL,'ops','ops','ops@1111.com','',7,1,0,'admin','2020-04-12 16:21:27','2020-04-12 16:27:03',0,0),
	(4,'pbkdf2_sha256$100000$b9gDYKkwgZLa$heji7yQrovqR0BuZlNPYXLtMfv3eu7kmUMkTRALwu0w=',NULL,'hr','hr','hr@1111.com','',2,1,0,'admin','2020-04-12 16:24:24','2020-04-12 16:24:24',0,0),
	(5,'pbkdf2_sha256$100000$GQ6CXyzKcEbp$VOjgkFqwPArvvaemswnxqQ7pytmOh0hKKabGQ9zwJxQ=',NULL,'scm','scm','scm@1111.com','',3,1,0,'admin','2020-04-12 16:24:51','2020-04-12 16:24:51',0,0),
	(6,'pbkdf2_sha256$100000$siusyC0tfp1B$JzNqSZv5+RVhbbfLf30MwRU91ThoX/9x5PPHoDfl6ts=',NULL,'lilian','李亮','lilian@1111.com','',4,1,0,'admin','2020-04-12 16:25:19','2020-04-12 16:25:19',0,0),
	(7,'pbkdf2_sha256$100000$m8tk9prGVn7l$e8Ssz6+lHNoQ5DBnLWe99Rq6jnjGQdnyt/Gk39SQpgw=',NULL,'david','大卫','dawid@1111.com','',5,1,0,'admin','2020-04-12 16:25:44','2020-04-12 16:25:44',0,0),
	(8,'pbkdf2_sha256$100000$nCTCaJylgkol$Gkw2eYi6DOyoKnAlipWKZBApLTJdttIOUU832n77Jy0=',NULL,'goods_1','goods_1','goods_1@1111.com','',6,1,0,'admin','2020-04-12 16:26:24','2020-04-12 16:26:24',0,0),
	(10,'pbkdf2_sha256$100000$fhXc3yEmVRbt$BzniXJXGKZQFI7D7gmqeXQdF5nfm0QrqE9cl6GUPjRM=',NULL,'goods_2','goods_2','goods_2@1111.com','',6,1,0,'admin','2020-04-12 16:26:42','2020-04-12 16:26:42',0,0),
	(11,'pbkdf2_sha256$100000$eQR4TZG5kgoz$h9yowaGVjACfwOoKTWy9zkhE01DubSy7ntNMJZ6/7po=',NULL,'ops2','ops2','ops2@1111.com','',7,1,0,'admin','2020-04-12 16:27:23','2020-04-12 16:27:23',0,0);

/*!40000 ALTER TABLE `account_loonuser` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table account_loonuserrole
# ------------------------------------------------------------

DROP TABLE IF EXISTS `account_loonuserrole`;

CREATE TABLE `account_loonuserrole` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `user_id` int(11) NOT NULL DEFAULT '0' COMMENT '用户id',
  `role_id` int(11) NOT NULL DEFAULT '0' COMMENT '角色id',
  `creator` varchar(50) NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `account_loonuserrole` WRITE;
/*!40000 ALTER TABLE `account_loonuserrole` DISABLE KEYS */;

INSERT INTO `account_loonuserrole` (`id`, `user_id`, `role_id`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`)
VALUES
	(1,3,1,'admin','2020-04-12 16:32:08','2020-04-12 16:32:08',0),
	(2,11,1,'admin','2020-04-12 16:32:15','2020-04-12 16:32:15',0);

/*!40000 ALTER TABLE `account_loonuserrole` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table auth_group
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_group`;

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table auth_group_permissions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_group_permissions`;

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table auth_permission
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_permission`;

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table django_admin_log
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_admin_log`;

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_account_loonuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_account_loonuser_id` FOREIGN KEY (`user_id`) REFERENCES `account_loonuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table django_content_type
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_content_type`;

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;

INSERT INTO `django_content_type` (`id`, `app_label`, `model`)
VALUES
	(20,'account','apptoken'),
	(8,'account','loondept'),
	(7,'account','loonrole'),
	(9,'account','loonuser'),
	(6,'account','loonuserrole'),
	(1,'admin','logentry'),
	(2,'auth','group'),
	(3,'auth','permission'),
	(4,'contenttypes','contenttype'),
	(5,'sessions','session'),
	(12,'ticket','ticketcustomfield'),
	(13,'ticket','ticketflowlog'),
	(10,'ticket','ticketrecord'),
	(11,'ticket','ticketstatelastman'),
	(21,'ticket','ticketuser'),
	(16,'workflow','customfield'),
	(14,'workflow','customnotice'),
	(17,'workflow','state'),
	(19,'workflow','transition'),
	(18,'workflow','workflow'),
	(22,'workflow','workflowadmin'),
	(15,'workflow','workflowscript');

/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table django_migrations
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_migrations`;

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table django_session
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_session`;

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`)
VALUES
	('2u4a3uup5v85arx0cgz0440umv3fuxya','ZDI2MDU0YTk2Njc2MDhmZWUxM2NkNDBhNzIwYzg0NjQwYzNhMDQxMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhZWExYWY0MWY2Mzg0NzI5ZGYzN2M5YWJjYmM5YjM4YjhlMGE4YzI3In0=','2020-04-26 10:59:13'),
	('gnq8ua2c47at1m055h67qj6ml0sc8bmy','ZWUzZTM3NGMyMTkwOGU0ZDEzY2U4ZDYxZDFjNTM3Y2Q2YzhiZDZmNTp7Il9hdXRoX3VzZXJfaWQiOiI0OCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYWVhMWFmNDFmNjM4NDcyOWRmMzdjOWFiY2JjOWIzOGI4ZTBhOGMyNyJ9','2020-03-29 09:57:34');

/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table ticket_ticketcustomfield
# ------------------------------------------------------------

DROP TABLE IF EXISTS `ticket_ticketcustomfield`;

CREATE TABLE `ticket_ticketcustomfield` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `creator` varchar(50) NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已删除',
  `name` varchar(50) NOT NULL DEFAULT '' COMMENT '名称',
  `field_key` varchar(50) NOT NULL DEFAULT '' COMMENT '字段标识',
  `ticket_id` int(11) NOT NULL DEFAULT '0' COMMENT '工单id',
  `field_type_id` int(11) NOT NULL DEFAULT '0' COMMENT '字段类型',
  `char_value` varchar(1000) NOT NULL DEFAULT '' COMMENT '字符串值',
  `int_value` int(11) NOT NULL DEFAULT '0' COMMENT '整形值',
  `float_value` double NOT NULL DEFAULT '0' COMMENT '浮点值',
  `bool_value` tinyint(1) NOT NULL DEFAULT '0' COMMENT '布尔值',
  `date_value` date NOT NULL DEFAULT '1000-00-01' COMMENT '日期值',
  `datetime_value` datetime NOT NULL DEFAULT '1000-00-01 00:00:00' COMMENT '日期时间值',
  `time_value` time(6) NOT NULL DEFAULT '00:00:01.000000' COMMENT '时间值',
  `radio_value` varchar(50) NOT NULL DEFAULT '' COMMENT '单选框值',
  `checkbox_value` varchar(50) NOT NULL DEFAULT '' COMMENT '复选框值',
  `select_value` varchar(50) NOT NULL DEFAULT '' COMMENT '单选下拉列表值',
  `multi_select_value` varchar(50) NOT NULL DEFAULT '' COMMENT '多选下拉列表值',
  `text_value` longtext NOT NULL COMMENT '文本域值',
  `username_value` varchar(50) NOT NULL DEFAULT '' COMMENT '用户名值',
  `multi_username_value` varchar(1000) NOT NULL DEFAULT '' COMMENT '多选用户名值',
  PRIMARY KEY (`id`),
  KEY `idx_ticket_id_field_key` (`ticket_id`,`field_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `ticket_ticketcustomfield` WRITE;
/*!40000 ALTER TABLE `ticket_ticketcustomfield` DISABLE KEYS */;

INSERT INTO `ticket_ticketcustomfield` (`id`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `name`, `field_key`, `ticket_id`, `field_type_id`, `char_value`, `int_value`, `float_value`, `bool_value`, `date_value`, `datetime_value`, `time_value`, `radio_value`, `checkbox_value`, `select_value`, `multi_select_value`, `text_value`, `username_value`, `multi_username_value`)
VALUES
	(1,'','2020-04-12 17:00:25','2020-04-12 17:00:25',0,'开始日期','date_start',1,30,'',0,0,0,'0001-01-01','2020-04-13 00:00:00','00:00:01.000000','','','','','','',''),
	(2,'','2020-04-12 17:00:25','2020-04-12 17:00:25',0,'截止时间','date_end',1,30,'',0,0,0,'0001-01-01','2020-04-23 00:00:00','00:00:01.000000','','','','','','',''),
	(3,'','2020-04-12 17:00:25','2020-04-12 17:00:25',0,'请假原因','reason',1,55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00','00:00:01.000000','','','','','<p>世界这么大，出去看看</p>','',''),
	(4,'','2020-04-12 17:02:28','2020-04-12 17:02:28',0,'开始日期','date_start',2,30,'',0,0,0,'0001-01-01','2020-04-13 00:00:00','00:00:01.000000','','','','','','',''),
	(5,'','2020-04-12 17:02:28','2020-04-12 17:02:28',0,'截止时间','date_end',2,30,'',0,0,0,'0001-01-01','2020-04-14 00:00:00','00:00:01.000000','','','','','','',''),
	(6,'','2020-04-12 17:02:28','2020-04-12 17:02:28',0,'请假原因','reason',2,55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00','00:00:01.000000','','','','','<p>找不到老婆，请假去相亲</p>','',''),
	(7,'','2020-04-12 17:03:28','2020-04-12 17:03:28',0,'申请原因','reason',3,55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00','00:00:01.000000','','','','','<p>远程办公</p>','','');

/*!40000 ALTER TABLE `ticket_ticketcustomfield` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table ticket_ticketflowlog
# ------------------------------------------------------------

DROP TABLE IF EXISTS `ticket_ticketflowlog`;

CREATE TABLE `ticket_ticketflowlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `creator` varchar(50) NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已删除',
  `ticket_id` int(11) NOT NULL DEFAULT '0' COMMENT '工单id',
  `transition_id` int(11) NOT NULL DEFAULT '0' COMMENT '流转id',
  `suggestion` varchar(1000) NOT NULL DEFAULT '0' COMMENT '处理意见',
  `participant_type_id` int(11) NOT NULL DEFAULT '0' COMMENT '参与人类型',
  `participant` varchar(50) NOT NULL DEFAULT '' COMMENT '参与人',
  `state_id` int(11) NOT NULL DEFAULT '0' COMMENT '状态id',
  `intervene_type_id` int(11) NOT NULL DEFAULT '0' COMMENT '干预类型',
  `ticket_data` varchar(10000) NOT NULL DEFAULT '' COMMENT '工单数据',
  PRIMARY KEY (`id`),
  KEY `idx_ticket_id` (`ticket_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `ticket_ticketflowlog` WRITE;
/*!40000 ALTER TABLE `ticket_ticketflowlog` DISABLE KEYS */;

INSERT INTO `ticket_ticketflowlog` (`id`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `ticket_id`, `transition_id`, `suggestion`, `participant_type_id`, `participant`, `state_id`, `intervene_type_id`, `ticket_data`)
VALUES
	(1,'admin','2020-04-12 17:00:25','2020-04-12 17:00:25',0,1,1,'',1,'admin',1,0,'{\"id\": 1, \"creator\": \"admin\", \"gmt_created\": \"2020-04-12 17:00:25\", \"gmt_modified\": \"2020-04-12 17:00:25\", \"is_deleted\": false, \"title\": \"\\u4e16\\u754c\\u8fd9\\u4e48\\u5927\\uff0c\\u51fa\\u53bb\\u770b\\u770b\", \"workflow_id\": 1, \"sn\": \"ops_202004120001\", \"state_id\": 2, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 5, \"participant\": \"create_tl\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"date_start\": \"2020-04-13 00:00:00\", \"date_end\": \"2020-04-23 00:00:00\", \"reason\": \"<p>\\u4e16\\u754c\\u8fd9\\u4e48\\u5927\\uff0c\\u51fa\\u53bb\\u770b\\u770b</p>\"}'),
	(2,'admin','2020-04-12 17:02:28','2020-04-12 17:02:28',0,2,1,'',1,'admin',1,0,'{\"id\": 2, \"creator\": \"admin\", \"gmt_created\": \"2020-04-12 17:02:28\", \"gmt_modified\": \"2020-04-12 17:02:28\", \"is_deleted\": false, \"title\": \"\\u8bf7\\u5047\\u53bb\\u76f8\\u4eb2\", \"workflow_id\": 1, \"sn\": \"ops_202004120002\", \"state_id\": 2, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"admin\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"date_start\": \"2020-04-13 00:00:00\", \"date_end\": \"2020-04-14 00:00:00\", \"reason\": \"<p>\\u627e\\u4e0d\\u5230\\u8001\\u5a46\\uff0c\\u8bf7\\u5047\\u53bb\\u76f8\\u4eb2</p>\"}'),
	(3,'admin','2020-04-12 17:03:28','2020-04-12 17:03:28',0,3,6,'',1,'admin',5,0,'{\"id\": 3, \"creator\": \"admin\", \"gmt_created\": \"2020-04-12 17:03:28\", \"gmt_modified\": \"2020-04-12 17:03:28\", \"is_deleted\": false, \"title\": \"\\u7533\\u8bf7vpn\\u5728\\u5bb6\\u8fdc\\u7a0b\\u529e\\u516c\", \"workflow_id\": 2, \"sn\": \"ops_202004120003\", \"state_id\": 6, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 4, \"participant\": \"1\", \"relation\": \"ops,ops2,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"reason\": \"<p>\\u8fdc\\u7a0b\\u529e\\u516c</p>\"}');

/*!40000 ALTER TABLE `ticket_ticketflowlog` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table ticket_ticketrecord
# ------------------------------------------------------------

DROP TABLE IF EXISTS `ticket_ticketrecord`;

CREATE TABLE `ticket_ticketrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `creator` varchar(50) NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已删除',
  `title` varchar(500) NOT NULL DEFAULT 'admin' COMMENT '标题',
  `workflow_id` int(11) NOT NULL DEFAULT '0' COMMENT '工作流id',
  `sn` varchar(25) NOT NULL DEFAULT '' COMMENT '工单流水号',
  `state_id` int(11) NOT NULL DEFAULT '0' COMMENT '状态id',
  `parent_ticket_id` int(11) NOT NULL DEFAULT '0' COMMENT '父工单id',
  `parent_ticket_state_id` int(11) NOT NULL DEFAULT '0' COMMENT '对应父工单状态id',
  `participant_type_id` int(11) NOT NULL DEFAULT '0' COMMENT '参与人类型id',
  `participant` varchar(100) NOT NULL DEFAULT '' COMMENT '参与人',
  `relation` varchar(1000) NOT NULL DEFAULT '' COMMENT '工单关系人',
  `in_add_node` tinyint(1) NOT NULL DEFAULT '0' COMMENT '加签中',
  `add_node_man` varchar(50) NOT NULL DEFAULT '' COMMENT '加签对象',
  `script_run_last_result` tinyint(1) NOT NULL DEFAULT '1' COMMENT '脚本/hook执行状态',
  `multi_all_person` varchar(1000) NOT NULL DEFAULT '{}' COMMENT '多人全部处理进展',
  `act_state_id` int(11) NOT NULL DEFAULT '1' COMMENT '进行状态',
  PRIMARY KEY (`id`),
  KEY `idx_act_state_id` (`act_state_id`),
  KEY `idx_sn` (`sn`),
  KEY `idx_workflow_id` (`workflow_id`),
  KEY `idx_creator` (`creator`),
  KEY `idx_gmt_created` (`gmt_created`),
  KEY `idx_parent_ticket_id` (`parent_ticket_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `ticket_ticketrecord` WRITE;
/*!40000 ALTER TABLE `ticket_ticketrecord` DISABLE KEYS */;

INSERT INTO `ticket_ticketrecord` (`id`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `title`, `workflow_id`, `sn`, `state_id`, `parent_ticket_id`, `parent_ticket_state_id`, `participant_type_id`, `participant`, `relation`, `in_add_node`, `add_node_man`, `script_run_last_result`, `multi_all_person`, `act_state_id`)
VALUES
	(1,'admin','2020-04-12 17:00:25','2020-04-12 17:02:43',0,'世界这么大，出去看看',1,'ops_202004120001',2,0,0,1,'admin','admin',0,'',1,'{}',1),
	(2,'admin','2020-04-12 17:02:28','2020-04-12 17:02:28',0,'请假去相亲',1,'ops_202004120002',2,0,0,1,'admin','admin',0,'',1,'{}',1),
	(3,'admin','2020-04-12 17:03:28','2020-04-12 17:03:28',0,'申请vpn在家远程办公',2,'ops_202004120003',6,0,0,4,'1','ops,ops2,admin',0,'',1,'{}',1);

/*!40000 ALTER TABLE `ticket_ticketrecord` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table ticket_ticketuser
# ------------------------------------------------------------

DROP TABLE IF EXISTS `ticket_ticketuser`;

CREATE TABLE `ticket_ticketuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `creator` varchar(50) NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已删除',
  `username` varchar(100) NOT NULL DEFAULT '' COMMENT '用户名',
  `in_process` tinyint(1) NOT NULL DEFAULT '0' COMMENT '处理中',
  `worked` tinyint(1) NOT NULL DEFAULT '0' COMMENT '处理过的',
  `ticket_id` int(11) NOT NULL DEFAULT '0' COMMENT '工单id',
  PRIMARY KEY (`id`),
  KEY `idx_ticket_id` (`ticket_id`),
  KEY `idx_username_in_process` (`username`,`in_process`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `ticket_ticketuser` WRITE;
/*!40000 ALTER TABLE `ticket_ticketuser` DISABLE KEYS */;

INSERT INTO `ticket_ticketuser` (`id`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `username`, `in_process`, `worked`, `ticket_id`)
VALUES
	(1,'','2020-04-12 17:00:25','2020-04-12 17:00:25',0,'admin',0,0,1),
	(2,'','2020-04-12 17:00:25','2020-04-12 17:00:25',0,'',1,0,1),
	(3,'','2020-04-12 17:02:28','2020-04-12 17:02:27',0,'admin',1,0,2),
	(4,'','2020-04-12 17:03:28','2020-04-12 17:03:28',0,'admin',0,0,3),
	(5,'','2020-04-12 17:03:28','2020-04-12 17:03:28',0,'ops',1,0,3),
	(6,'','2020-04-12 17:03:28','2020-04-12 17:03:28',0,'ops2',1,0,3);

/*!40000 ALTER TABLE `ticket_ticketuser` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table workflow_customfield
# ------------------------------------------------------------

DROP TABLE IF EXISTS `workflow_customfield`;

CREATE TABLE `workflow_customfield` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `workflow_id` int(11) NOT NULL DEFAULT '0' COMMENT '工作流id',
  `field_type_id` int(11) NOT NULL DEFAULT '0' COMMENT '字段类型id',
  `field_key` varchar(50) NOT NULL DEFAULT '' COMMENT '字段标识',
  `field_name` varchar(50) NOT NULL DEFAULT '' COMMENT '字段名称',
  `order_id` int(11) NOT NULL DEFAULT '0' COMMENT '顺序id',
  `default_value` varchar(100) DEFAULT '' COMMENT '默认值',
  `description` varchar(100) NOT NULL DEFAULT '' COMMENT '描述',
  `field_template` longtext NOT NULL COMMENT '字段模板',
  `boolean_field_display` varchar(100) NOT NULL DEFAULT '{}' COMMENT '布尔类型显示',
  `creator` varchar(50) NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已删除',
  `field_choice` varchar(1000) NOT NULL DEFAULT '{}' COMMENT '布尔类型显示',
  `label` varchar(100) NOT NULL DEFAULT '{}' COMMENT '布尔类型显示',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `workflow_customfield` WRITE;
/*!40000 ALTER TABLE `workflow_customfield` DISABLE KEYS */;

INSERT INTO `workflow_customfield` (`id`, `workflow_id`, `field_type_id`, `field_key`, `field_name`, `order_id`, `default_value`, `description`, `field_template`, `boolean_field_display`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `field_choice`, `label`)
VALUES
	(1,1,30,'date_start','开始日期',30,'','请选择请假开始日期','','{}','admin','2020-04-12 16:37:44','2020-04-12 16:39:08',0,'{}','{}'),
	(2,1,30,'date_end','截止时间',31,'','请假截止时间','','{}','admin','2020-04-12 16:38:04','2020-04-12 16:39:14',0,'{}','{}'),
	(3,1,55,'reason','请假原因',200,'','请填写请假原因','','{}','admin','2020-04-12 16:38:48','2020-04-12 16:39:24',0,'{}','{}'),
	(4,2,55,'reason','申请原因',200,'','','','{}','admin','2020-04-12 16:46:02','2020-04-12 16:46:02',0,'{}','{}');

/*!40000 ALTER TABLE `workflow_customfield` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table workflow_customnotice
# ------------------------------------------------------------

DROP TABLE IF EXISTS `workflow_customnotice`;

CREATE TABLE `workflow_customnotice` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `name` varchar(50) NOT NULL DEFAULT '' COMMENT '名称',
  `description` varchar(100) DEFAULT '' COMMENT '描述',
  `creator` varchar(50) NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已删除',
  `hook_token` varchar(100) DEFAULT '' COMMENT 'hook令牌',
  `hook_url` varchar(100) DEFAULT '' COMMENT 'hook地址',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table workflow_state
# ------------------------------------------------------------

DROP TABLE IF EXISTS `workflow_state`;

CREATE TABLE `workflow_state` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `name` varchar(50) NOT NULL DEFAULT '' COMMENT '状态名称',
  `workflow_id` int(11) NOT NULL DEFAULT '0' COMMENT '工作id',
  `is_hidden` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否隐藏',
  `order_id` int(11) NOT NULL DEFAULT '0' COMMENT '顺序id',
  `type_id` int(11) NOT NULL DEFAULT '0' COMMENT '类型id',
  `participant_type_id` int(11) NOT NULL DEFAULT '0' COMMENT '参与人类型id',
  `participant` varchar(100) NOT NULL DEFAULT '' COMMENT '参与人',
  `distribute_type_id` int(11) NOT NULL DEFAULT '0' COMMENT '分配类型id',
  `state_field_str` varchar(1000) NOT NULL DEFAULT '{}' COMMENT '状态表单字段',
  `label` varchar(1000) NOT NULL DEFAULT '{}' COMMENT '状态表单字段',
  `creator` varchar(50) NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已删除',
  `remember_last_man_enable` tinyint(1) NOT NULL DEFAULT '0' COMMENT '记忆最后处理人',
  `enable_retreat` tinyint(1) NOT NULL DEFAULT '0' COMMENT '允许发起人撤回',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `workflow_state` WRITE;
/*!40000 ALTER TABLE `workflow_state` DISABLE KEYS */;

INSERT INTO `workflow_state` (`id`, `name`, `workflow_id`, `is_hidden`, `order_id`, `type_id`, `participant_type_id`, `participant`, `distribute_type_id`, `state_field_str`, `label`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `remember_last_man_enable`, `enable_retreat`)
VALUES
	(1,'发起人-编辑中',1,0,0,1,0,'',2,'{\"title\":2,\"reason\":2, \"date_start\":2,\"date_end\":2}','{}','admin','2020-04-12 16:40:21','2020-04-12 16:40:21',0,0,0),
	(2,'tl审批中',1,0,1,0,5,'creator_tl',2,'{\"title\":1,\"reason\":1,\"date_start\":1,\"date_end\":1,\"participant_info.participant_name\":1,\"state.state_name\":1,\"workflow.workflow_name\":1}','{}','admin','2020-04-12 16:41:23','2020-04-12 17:01:43',0,0,0),
	(3,'人事审批中',1,0,3,0,3,'2',2,'{\"title\":1,\"reason\":1,\"date_start\":1,\"date_end\":1,\"participant_info.participant_name\":1,\"state.state_name\":1,\"workflow.workflow_name\":1}','{}','admin','2020-04-12 16:41:59','2020-04-12 16:42:28',0,0,0),
	(4,'结束',1,0,4,2,0,'',2,'{\"title\":1,\"reason\":1, \"date_start\":1,\"date_end\":1,\"participant_info.participant_name\":1,\"state.state_name\":1,\"workflow.workflow_name\":1}','{}','admin','2020-04-12 16:42:47','2020-04-12 16:42:47',0,0,0),
	(5,'发起人-新建中',2,0,1,1,0,'',2,'{\"title\":2,\"reason\":2}','{}','admin','2020-04-12 16:46:34','2020-04-12 16:46:34',0,0,0),
	(6,'运维人员-审批中',2,0,2,0,4,'1',2,'{\"title\":1,\"reason\":1,\"participant_info.participant_name\":1,\"state.state_name\":1,\"workflow.workflow_name\":1}','{}','admin','2020-04-12 16:47:25','2020-04-12 16:47:25',0,0,0),
	(7,'vpn授权中',2,0,3,0,10,'{\"hook_url\":\"http://www.baidu.com\", \"hook_token\":\"xxxx\", \"wait\":false, \"extra_info\":\"xxxx\"}',2,'{\"title\":1,\"reason\":1,\"participant_info.participant_name\":1,\"state.state_name\":1,\"workflow.workflow_name\":1}','{}','admin','2020-04-12 16:48:27','2020-04-12 16:48:42',0,0,0),
	(8,'发起人-确认中',2,0,4,0,5,'creator',2,'{\"title\":1,\"reason\":1,\"participant_info.participant_name\":1,\"state.state_name\":1,\"workflow.workflow_name\":1}','{}','admin','2020-04-12 16:49:10','2020-04-12 16:49:10',0,0,0),
	(9,'结束',2,0,5,2,0,'',2,'{\"title\":1,\"reason\":1,\"participant_info.participant_name\":1,\"state.state_name\":1,\"workflow.workflow_name\":1}','{}','admin','2020-04-12 16:49:24','2020-04-12 16:49:24',0,0,0);

/*!40000 ALTER TABLE `workflow_state` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table workflow_transition
# ------------------------------------------------------------

DROP TABLE IF EXISTS `workflow_transition`;

CREATE TABLE `workflow_transition` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `name` varchar(50) NOT NULL DEFAULT '' COMMENT '流转名称',
  `workflow_id` int(11) NOT NULL DEFAULT '0' COMMENT '工作流id',
  `transition_type_id` int(11) NOT NULL DEFAULT '0' COMMENT '流转类型id',
  `source_state_id` int(11) NOT NULL DEFAULT '0' COMMENT '源状态id',
  `destination_state_id` int(11) NOT NULL DEFAULT '0' COMMENT '目标状态id',
  `alert_enable` tinyint(1) NOT NULL DEFAULT '0' COMMENT '点击弹窗提示',
  `alert_text` varchar(100) NOT NULL DEFAULT '' COMMENT '点击弹窗提示的内容',
  `creator` varchar(50) NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已删除',
  `field_require_check` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否校验必填项',
  `timer` int(11) NOT NULL DEFAULT '0' COMMENT '定时器时长(单位:秒)',
  `attribute_type_id` int(11) NOT NULL DEFAULT '0' COMMENT '属性类型id',
  `condition_expression` varchar(1000) NOT NULL DEFAULT '[]' COMMENT '条件表达式',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `workflow_transition` WRITE;
/*!40000 ALTER TABLE `workflow_transition` DISABLE KEYS */;

INSERT INTO `workflow_transition` (`id`, `name`, `workflow_id`, `transition_type_id`, `source_state_id`, `destination_state_id`, `alert_enable`, `alert_text`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `field_require_check`, `timer`, `attribute_type_id`, `condition_expression`)
VALUES
	(1,'提交',1,1,1,2,0,'','admin','2020-04-12 16:42:58','2020-04-12 16:42:58',0,0,0,1,'[]'),
	(2,'同意',1,1,2,3,0,'','admin','2020-04-12 16:43:21','2020-04-12 16:43:21',0,0,0,1,'[]'),
	(3,'拒绝',1,1,2,1,0,'','admin','2020-04-12 16:43:34','2020-04-12 16:44:57',0,0,0,2,'[]'),
	(4,'同意',1,1,3,4,0,'','admin','2020-04-12 16:44:18','2020-04-12 16:44:18',0,0,0,1,'[]'),
	(5,'拒绝',1,1,3,1,0,'','admin','2020-04-12 16:44:32','2020-04-12 16:45:13',0,0,0,2,'[]'),
	(6,'提交',2,1,5,6,0,'','admin','2020-04-12 16:50:42','2020-04-12 16:50:42',0,0,0,1,'[]'),
	(7,'拒绝',2,1,6,5,0,'','admin','2020-04-12 16:51:06','2020-04-12 16:51:06',0,0,0,2,'[]'),
	(8,'同意',2,1,6,7,0,'','admin','2020-04-12 16:51:29','2020-04-12 16:51:29',0,0,0,1,'[]'),
	(9,'完成',2,1,7,8,0,'','admin','2020-04-12 16:51:54','2020-04-12 16:51:54',0,0,0,1,'[]'),
	(10,'确认完成',2,1,8,9,0,'','admin','2020-04-12 16:52:13','2020-04-12 16:52:13',0,0,0,1,'[]'),
	(11,'权限未成功开通',2,1,8,6,0,'','admin','2020-04-12 16:52:55','2020-04-12 16:52:55',0,0,0,2,'[]');

/*!40000 ALTER TABLE `workflow_transition` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table workflow_workflow
# ------------------------------------------------------------

DROP TABLE IF EXISTS `workflow_workflow`;

CREATE TABLE `workflow_workflow` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `name` varchar(50) NOT NULL DEFAULT '' COMMENT '名称',
  `description` varchar(50) NOT NULL DEFAULT '' COMMENT '描述',
  `display_form_str` varchar(10000) NOT NULL DEFAULT '[]' COMMENT '展现表单字段',
  `creator` varchar(50) NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已删除',
  `view_permission_check` tinyint(1) NOT NULL DEFAULT '0' COMMENT '查看权限校验',
  `limit_expression` varchar(1000) NOT NULL DEFAULT '{}' COMMENT '限制表达式',
  `notices` varchar(50) NOT NULL DEFAULT '' COMMENT '通知',
  `content_template` varchar(1000) DEFAULT '' COMMENT '内容模板',
  `title_template` varchar(50) DEFAULT '' COMMENT '标题模板',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `workflow_workflow` WRITE;
/*!40000 ALTER TABLE `workflow_workflow` DISABLE KEYS */;

INSERT INTO `workflow_workflow` (`id`, `name`, `description`, `display_form_str`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `view_permission_check`, `limit_expression`, `notices`, `content_template`, `title_template`)
VALUES
	(1,'请假流程','','[\"title\",\"sn\",\"gmt_created\", \"state.state_name\", \"participant_info.participant_name\",\"workflow.workflow_name\"]','admin','2020-04-12 16:34:25','2020-04-12 16:34:25',0,0,'{}','','标题:{title}, 创建时间:{gmt_created}','你有一个待办工单:{title}'),
	(2,'vpn申请','','[\"title\",\"sn\",\"gmt_created\", \"state.state_name\", \"participant_info.participant_name\",\"workflow.workflow_name\"]','admin','2020-04-12 16:36:10','2020-04-12 16:36:21',0,0,'{}','','标题:{title}, 创建时间:{gmt_created}','你有一个待办工单:{title}');

/*!40000 ALTER TABLE `workflow_workflow` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table workflow_workflowadmin
# ------------------------------------------------------------

DROP TABLE IF EXISTS `workflow_workflowadmin`;

CREATE TABLE `workflow_workflowadmin` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `creator` varchar(50) NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已删除',
  `username` varchar(100) NOT NULL DEFAULT '' COMMENT '用户名',
  `workflow_id` int(11) NOT NULL DEFAULT '0' COMMENT '工作流id',
  PRIMARY KEY (`id`),
  KEY `idx_workflow_id` (`workflow_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table workflow_workflowscript
# ------------------------------------------------------------

DROP TABLE IF EXISTS `workflow_workflowscript`;

CREATE TABLE `workflow_workflowscript` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `name` varchar(50) NOT NULL DEFAULT '' COMMENT '名称',
  `saved_name` varchar(100) NOT NULL DEFAULT '' COMMENT '保存的文件名',
  `description` varchar(100) DEFAULT '' COMMENT '描述',
  `is_active` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否可用',
  `creator` varchar(50) NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已删除',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
