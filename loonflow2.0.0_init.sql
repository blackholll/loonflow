# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.17)
# Database: loonflownew1
# Generation Time: 2020-11-26 23:29:46 +0000
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
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creator` varchar(50) NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `app_name` varchar(50) NOT NULL,
  `token` varchar(50) NOT NULL,
  `ticket_sn_prefix` varchar(20) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `account_apptoken` WRITE;
/*!40000 ALTER TABLE `account_apptoken` DISABLE KEYS */;

INSERT INTO `account_apptoken` (`id`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `app_name`, `token`, `ticket_sn_prefix`)
VALUES
	(1,'admin','2020-07-15 22:48:55.134791','2020-07-15 22:49:17.189447',0,'ops','4e57d414-c6aa-11ea-9ed0-784f437daad6','aaaa'),
	(2,'admin','2020-10-07 22:18:52.426149','2020-10-07 22:18:52.426313',0,'test','069b4418-08a8-11eb-902e-acde48001122','sds'),
	(3,'admin','2020-10-07 22:21:19.313968','2020-10-07 22:21:19.314140',0,'test','5e36d26e-08a8-11eb-8370-acde48001122','sdfsf'),
	(4,'admin','2020-10-07 22:23:07.424740','2020-10-07 22:23:07.425044',0,'eeee','9ea72dc6-08a8-11eb-99fb-acde48001122','dfds'),
	(5,'admin','2020-10-07 22:23:17.620953','2020-10-07 22:41:33.710316',1,'fef','a4bb2d3e-08a8-11eb-8a91-acde48001122','fdef');

/*!40000 ALTER TABLE `account_apptoken` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table account_loondept
# ------------------------------------------------------------

DROP TABLE IF EXISTS `account_loondept`;

CREATE TABLE `account_loondept` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `parent_dept_id` int(11) NOT NULL,
  `leader` varchar(50) NOT NULL,
  `approver` varchar(100) NOT NULL,
  `label` varchar(50) NOT NULL,
  `creator` varchar(50) NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `account_loondept` WRITE;
/*!40000 ALTER TABLE `account_loondept` DISABLE KEYS */;

INSERT INTO `account_loondept` (`id`, `name`, `parent_dept_id`, `leader`, `approver`, `label`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`)
VALUES
	(1,'技术部',0,'aaaa','admin','','','2020-07-13 00:00:00.000000','2020-07-13 00:00:00.000000',1),
	(2,'财务部',0,'','','','','2020-07-13 00:00:00.000000','2020-07-13 00:00:00.000000',0),
	(3,'行政部111',2,'dfsf@163.com','admin,sss','s\'s\'s','admin','2020-10-07 10:17:11.265290','2020-10-07 10:17:11.265389',0),
	(4,'IT',1,'dfsf@163.com','aaaa,3333','sdfs','admin','2020-10-07 10:18:39.932490','2020-10-07 10:18:39.932591',1);

/*!40000 ALTER TABLE `account_loondept` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table account_loonrole
# ------------------------------------------------------------

DROP TABLE IF EXISTS `account_loonrole`;

CREATE TABLE `account_loonrole` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(50) NOT NULL,
  `label` varchar(50) NOT NULL,
  `creator` varchar(50) NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `account_loonrole` WRITE;
/*!40000 ALTER TABLE `account_loonrole` DISABLE KEYS */;

INSERT INTO `account_loonrole` (`id`, `name`, `description`, `label`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`)
VALUES
	(1,'223232','1222333','1333111','admin','2020-07-22 23:49:48.688015','2020-07-22 23:49:48.688619',0),
	(2,'te222','fds','dfs','admin','2020-10-04 17:09:47.462589','2020-10-04 17:09:47.462709',0);

/*!40000 ALTER TABLE `account_loonrole` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table account_loonuser
# ------------------------------------------------------------

DROP TABLE IF EXISTS `account_loonuser`;

CREATE TABLE `account_loonuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `alias` varchar(50) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(13) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `creator` varchar(50) NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `account_loonuser` WRITE;
/*!40000 ALTER TABLE `account_loonuser` DISABLE KEYS */;

INSERT INTO `account_loonuser` (`id`, `password`, `last_login`, `username`, `alias`, `email`, `phone`, `is_active`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `type_id`)
VALUES
	(1,'pbkdf2_sha256$150000$nex53BPJ3f0T$jsJjWHmpVp11aIt7F8eyKVK2l+YjH8k0GP4oOQf8Jw4=','2020-11-24 07:01:02.692140','admin','超级管理员','admin@aa.com','13888888888',1,'admin','2020-07-13 06:55:33.427320','2020-07-13 06:55:33.430436',0,2),
	(2,'pbkdf2_sha256$150000$Fp4gFoZ5LvIQ$Nhr+cxIfX7pendx12iTieYTQbM58dsuwAEh6tFRq+uA=',NULL,'aaaa','fdsfsf','aaa@163.com','',1,'','2020-07-16 07:50:44.761354','2020-07-16 07:50:44.765578',0,0),
	(3,'pbkdf2_sha256$150000$Ey7I685mHKcU$ZR0vtbG1uSYbqw0Zxc+TQcKPOpYAsfLW4LIjHP55Iak=',NULL,'bbb','','bb@163.com','',1,'','2020-07-16 07:55:04.142103','2020-07-16 07:55:04.145527',0,2),
	(4,'pbkdf2_sha256$150000$XF8kVVHNZYiR$9ayYeh83EGGvF5s1qN5VQx/RYW6ujA/2JGtgANvtYrQ=',NULL,'dfsf@163.com','fdsfs','22222@163.com','',1,'admin','2020-07-18 15:45:55.334270','2020-10-01 10:49:53.418763',0,1),
	(6,'pbkdf2_sha256$150000$KoiIowtSM5ZX$Rc8lE79tRlxOKU22v7dha56qtGATjAERevswh5g/+Io=',NULL,'dsfsffsdf','fdsfs','22222@163.com','',1,'admin','2020-07-18 15:46:28.852181','2020-07-18 15:46:28.852531',0,1),
	(7,'pbkdf2_sha256$150000$6IeqMYuSftxG$UKINFNV+Q+rYunH/htTlobQoAxT0fjuOE1Bm11ZLR0o=',NULL,'dsddsdd','sssddd','22222@163.com','',1,'admin','2020-07-18 15:51:53.984928','2020-07-18 15:51:53.985039',1,2),
	(8,'pbkdf2_sha256$150000$tW3g1qJTOwy6$2zlnzA+IdP5Oy+Y6NV5ik3ymXZmjHU2H+1EVssDZiAQ=',NULL,'3333','3334444','sdfsf@11.com','',1,'admin','2020-07-18 15:52:07.648636','2020-07-18 15:52:07.648742',0,0),
	(9,'pbkdf2_sha256$150000$0fYUbCAGHeGB$w2gRFEy711XUlhHGrhQBJpi/6u9qjL7vitSfqPvMNSE=',NULL,'sss','sfdsfs','22222212@163.com','',1,'admin','2020-07-18 16:08:35.407578','2020-07-18 16:08:35.407667',0,0),
	(10,'pbkdf2_sha256$150000$i9YkFw57LRVg$zJiYWU6YU8BzHqTpZa2AZmAGe1ROrz41xnCnUcepnn4=',NULL,'test1111','haha','sss@111.com','',0,'admin','2020-07-21 06:54:03.944318','2020-07-21 06:54:03.944392',0,1),
	(11,'pbkdf2_sha256$150000$IMpPp4THtW7n$QLv4QH89daAWF+D1XUNNJNm9PdyQuRmmBqjtwSJeyXE=',NULL,'fdsfds','fdsfs','fsdfsfsf@13.com','',1,'admin','2020-09-21 07:25:49.543211','2020-09-21 07:25:49.543231',0,0),
	(12,'pbkdf2_sha256$150000$uhhAEFyioVD2$c2WHSiLpGS8HBivopq0zphvgek+Wnuak1dwyi2S+iyM=',NULL,'23424','3242342','dfsdf@121.com','',1,'admin','2020-09-21 07:26:19.688074','2020-09-21 07:26:19.688095',0,0),
	(13,'pbkdf2_sha256$150000$nex53BPJ3f0T$jsJjWHmpVp11aIt7F8eyKVK2l+YjH8k0GP4oOQf8Jw4=',NULL,'zhangsan','zhangsan','zhangsan@121.com','',1,'admin','2020-09-21 07:26:19.688074','2020-09-21 07:26:19.688095',0,0),
	(14,'pbkdf2_sha256$150000$nex53BPJ3f0T$jsJjWHmpVp11aIt7F8eyKVK2l+YjH8k0GP4oOQf8Jw4=',NULL,'lisi','lisi','lisi@121.com','',1,'admin','2020-09-21 07:26:19.688074','2020-09-21 07:26:19.688095',0,0),
	(15,'pbkdf2_sha256$150000$nex53BPJ3f0T$jsJjWHmpVp11aIt7F8eyKVK2l+YjH8k0GP4oOQf8Jw4=',NULL,'wangwu','wangwu','wangwu@121.com','',1,'admin','2020-09-21 07:26:19.688074','2020-09-21 07:26:19.688095',0,0);

/*!40000 ALTER TABLE `account_loonuser` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table account_loonuserdept
# ------------------------------------------------------------

DROP TABLE IF EXISTS `account_loonuserdept`;

CREATE TABLE `account_loonuserdept` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creator` varchar(50) NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `dept_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `account_loonuserdept_dept_id_ad142af8` (`dept_id`),
  KEY `account_loonuserdept_user_id_17ab09cb` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `account_loonuserdept` WRITE;
/*!40000 ALTER TABLE `account_loonuserdept` DISABLE KEYS */;

INSERT INTO `account_loonuserdept` (`id`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `dept_id`, `user_id`)
VALUES
	(1,'admin','2020-07-13 00:00:00.000000','2020-07-13 00:00:00.000000',0,1,1),
	(2,'admin','2020-07-13 00:00:00.000000','2020-07-13 00:00:00.000000',0,2,1),
	(3,'','2020-07-18 15:46:28.862688','2020-07-18 15:46:28.862806',0,1,6),
	(4,'','2020-07-18 15:46:28.863506','2020-07-18 15:46:28.863627',0,2,6),
	(5,'','2020-07-18 15:51:53.991345','2020-07-18 15:51:53.991440',0,1,7),
	(6,'','2020-07-18 15:52:07.653817','2020-07-18 15:52:07.653913',0,2,8),
	(7,'','2020-07-18 16:08:35.413525','2020-07-18 16:08:35.413671',0,1,9),
	(8,'','2020-07-20 07:59:55.939115','2020-07-20 07:59:55.939207',0,1,2),
	(9,'','2020-07-20 07:59:55.939576','2020-07-20 07:59:55.939646',0,2,2),
	(10,'','2020-07-21 06:54:03.951044','2020-07-21 06:54:03.951179',0,2,10),
	(11,'','2020-09-21 07:25:49.546606','2020-09-21 07:25:49.546641',0,2,11),
	(12,'','2020-09-21 07:26:19.691216','2020-09-21 07:26:19.691242',0,2,12),
	(13,'','2020-09-27 07:16:53.959054','2020-09-27 07:16:53.959722',0,1,13),
	(14,'','2020-09-28 07:05:57.689130','2020-09-28 07:05:57.689660',0,1,15),
	(15,'','2020-09-28 07:08:34.896590','2020-09-28 07:08:34.896876',0,2,16),
	(16,'','2020-09-28 07:08:34.898224','2020-09-28 07:08:34.898496',0,1,16),
	(17,'','2020-09-29 07:41:14.260849','2020-09-29 07:41:14.261150',0,1,17);

/*!40000 ALTER TABLE `account_loonuserdept` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table account_loonuserrole
# ------------------------------------------------------------

DROP TABLE IF EXISTS `account_loonuserrole`;

CREATE TABLE `account_loonuserrole` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creator` varchar(50) NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `account_loonuserrole` WRITE;
/*!40000 ALTER TABLE `account_loonuserrole` DISABLE KEYS */;

INSERT INTO `account_loonuserrole` (`id`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `user_id`, `role_id`)
VALUES
	(1,'admin','2020-10-01 16:46:36.870135','2020-10-01 16:46:36.870239',1,1,1),
	(2,'admin','2020-10-04 20:24:47.386282','2020-10-04 20:24:47.386465',1,3,1),
	(3,'admin','2020-10-04 22:02:45.379547','2020-10-04 22:02:45.379837',1,2,1),
	(4,'admin','2020-10-04 22:02:56.438357','2020-10-04 22:02:56.438721',0,8,1),
	(5,'admin','2020-10-04 22:04:06.550125','2020-10-04 22:04:06.550495',1,12,1),
	(6,'admin','2020-10-04 22:04:55.564884','2020-10-04 22:04:55.565217',1,4,1),
	(7,'admin','2020-10-04 22:05:00.620939','2020-10-04 22:05:00.621249',0,9,1);

/*!40000 ALTER TABLE `account_loonuserrole` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table auth_group
# ------------------------------------------------------------

DROP TABLE IF EXISTS `auth_group`;

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
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

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`)
VALUES
	(1,'Can add log entry',1,'add_logentry'),
	(2,'Can change log entry',1,'change_logentry'),
	(3,'Can delete log entry',1,'delete_logentry'),
	(4,'Can add group',2,'add_group'),
	(5,'Can change group',2,'change_group'),
	(6,'Can delete group',2,'delete_group'),
	(7,'Can add permission',3,'add_permission'),
	(8,'Can change permission',3,'change_permission'),
	(9,'Can delete permission',3,'delete_permission'),
	(10,'Can add content type',4,'add_contenttype'),
	(11,'Can change content type',4,'change_contenttype'),
	(12,'Can delete content type',4,'delete_contenttype'),
	(13,'Can add session',5,'add_session'),
	(14,'Can change session',5,'change_session'),
	(15,'Can delete session',5,'delete_session'),
	(16,'Can add 用户角色',6,'add_loonuserrole'),
	(17,'Can change 用户角色',6,'change_loonuserrole'),
	(18,'Can delete 用户角色',6,'delete_loonuserrole'),
	(19,'Can add 角色',7,'add_loonrole'),
	(20,'Can change 角色',7,'change_loonrole'),
	(21,'Can delete 角色',7,'delete_loonrole'),
	(22,'Can add 部门',8,'add_loondept'),
	(23,'Can change 部门',8,'change_loondept'),
	(24,'Can delete 部门',8,'delete_loondept'),
	(25,'Can add 用户',9,'add_loonuser'),
	(26,'Can change 用户',9,'change_loonuser'),
	(27,'Can delete 用户',9,'delete_loonuser'),
	(28,'Can add ticket record',10,'add_ticketrecord'),
	(29,'Can change ticket record',10,'change_ticketrecord'),
	(30,'Can delete ticket record',10,'delete_ticketrecord'),
	(31,'Can add ticket state last man',11,'add_ticketstatelastman'),
	(32,'Can change ticket state last man',11,'change_ticketstatelastman'),
	(33,'Can delete ticket state last man',11,'delete_ticketstatelastman'),
	(34,'Can add ticket custom field',12,'add_ticketcustomfield'),
	(35,'Can change ticket custom field',12,'change_ticketcustomfield'),
	(36,'Can delete ticket custom field',12,'delete_ticketcustomfield'),
	(37,'Can add ticket flow log',13,'add_ticketflowlog'),
	(38,'Can change ticket flow log',13,'change_ticketflowlog'),
	(39,'Can delete ticket flow log',13,'delete_ticketflowlog'),
	(40,'Can add custom notice',14,'add_customnotice'),
	(41,'Can change custom notice',14,'change_customnotice'),
	(42,'Can delete custom notice',14,'delete_customnotice'),
	(43,'Can add workflow script',15,'add_workflowscript'),
	(44,'Can change workflow script',15,'change_workflowscript'),
	(45,'Can delete workflow script',15,'delete_workflowscript'),
	(46,'Can add custom field',16,'add_customfield'),
	(47,'Can change custom field',16,'change_customfield'),
	(48,'Can delete custom field',16,'delete_customfield'),
	(49,'Can add state',17,'add_state'),
	(50,'Can change state',17,'change_state'),
	(51,'Can delete state',17,'delete_state'),
	(52,'Can add workflow',18,'add_workflow'),
	(53,'Can change workflow',18,'change_workflow'),
	(54,'Can delete workflow',18,'delete_workflow'),
	(55,'Can add transition',19,'add_transition'),
	(56,'Can change transition',19,'change_transition'),
	(57,'Can delete transition',19,'delete_transition'),
	(58,'Can add 调用token',20,'add_apptoken'),
	(59,'Can change 调用token',20,'change_apptoken'),
	(60,'Can delete 调用token',20,'delete_apptoken'),
	(61,'Can add ticket user',21,'add_ticketuser'),
	(62,'Can change ticket user',21,'change_ticketuser'),
	(63,'Can delete ticket user',21,'delete_ticketuser'),
	(64,'Can add workflow admin',22,'add_workflowadmin'),
	(65,'Can change workflow admin',22,'change_workflowadmin'),
	(66,'Can delete workflow admin',22,'delete_workflowadmin'),
	(67,'Can view log entry',1,'view_logentry'),
	(68,'Can view permission',3,'view_permission'),
	(69,'Can view group',2,'view_group'),
	(70,'Can view content type',4,'view_contenttype'),
	(71,'Can view session',5,'view_session'),
	(72,'Can view loon user',9,'view_loonuser'),
	(73,'Can view app token',20,'view_apptoken'),
	(74,'Can view loon dept',8,'view_loondept'),
	(75,'Can view loon role',7,'view_loonrole'),
	(76,'Can view loon user role',6,'view_loonuserrole'),
	(77,'Can add loon user dept',23,'add_loonuserdept'),
	(78,'Can change loon user dept',23,'change_loonuserdept'),
	(79,'Can delete loon user dept',23,'delete_loonuserdept'),
	(80,'Can view loon user dept',23,'view_loonuserdept'),
	(81,'Can view 工单自定义字段',12,'view_ticketcustomfield'),
	(82,'Can view 工单流转日志',13,'view_ticketflowlog'),
	(83,'Can view 工单记录',10,'view_ticketrecord'),
	(84,'Can view ticket user',21,'view_ticketuser'),
	(85,'Can view 工作流自定义字段',16,'view_customfield'),
	(86,'Can view custom notice',14,'view_customnotice'),
	(87,'Can view 工作流状态',17,'view_state'),
	(88,'Can view 工作流流转',19,'view_transition'),
	(89,'Can view 工作流',18,'view_workflow'),
	(90,'Can view workflow admin',22,'view_workflowadmin'),
	(91,'Can view 工作流脚本',15,'view_workflowscript'),
	(92,'Can add loon user dept11',24,'add_loonuserdept11'),
	(93,'Can change loon user dept11',24,'change_loonuserdept11'),
	(94,'Can delete loon user dept11',24,'delete_loonuserdept11'),
	(95,'Can view loon user dept11',24,'view_loonuserdept11'),
	(96,'Can add app token workflow',25,'add_apptokenworkflow'),
	(97,'Can change app token workflow',25,'change_apptokenworkflow'),
	(98,'Can delete app token workflow',25,'delete_apptokenworkflow'),
	(99,'Can view app token workflow',25,'view_apptokenworkflow'),
	(100,'Can add workflow user permission',26,'add_workflowuserpermission'),
	(101,'Can change workflow user permission',26,'change_workflowuserpermission'),
	(102,'Can delete workflow user permission',26,'delete_workflowuserpermission'),
	(103,'Can view workflow user permission',26,'view_workflowuserpermission');

/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table django_admin_log
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_admin_log`;

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
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
	(25,'account','apptokenworkflow'),
	(8,'account','loondept'),
	(7,'account','loonrole'),
	(9,'account','loonuser'),
	(23,'account','loonuserdept'),
	(24,'account','loonuserdept11'),
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
	(15,'workflow','workflowscript'),
	(26,'workflow','workflowuserpermission');

/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table django_migrations
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_migrations`;

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`)
VALUES
	(2,'contenttypes','0001_initial','2018-04-10 16:23:41.088822'),
	(5,'contenttypes','0002_remove_content_type_name','2018-04-10 16:23:41.316210'),
	(6,'auth','0001_initial','2018-04-10 16:23:41.492653'),
	(7,'auth','0002_alter_permission_name_max_length','2018-04-10 16:23:41.536426'),
	(8,'auth','0003_alter_user_email_max_length','2018-04-10 16:23:41.555765'),
	(9,'auth','0004_alter_user_username_opts','2018-04-10 16:23:41.579352'),
	(10,'auth','0005_alter_user_last_login_null','2018-04-10 16:23:41.616306'),
	(11,'auth','0006_require_contenttypes_0002','2018-04-10 16:23:41.620447'),
	(12,'auth','0007_alter_validators_add_error_messages','2018-04-10 16:23:41.643171'),
	(13,'auth','0008_alter_user_username_max_length','2018-04-10 16:23:41.663023'),
	(14,'auth','0009_alter_user_last_name_max_length','2018-04-10 16:23:41.679754'),
	(15,'sessions','0001_initial','2018-04-10 16:23:41.711283'),
	(16,'ticket','0001_initial','2018-04-10 16:23:41.848590'),
	(17,'workflow','0001_initial','2018-04-10 16:23:41.994564'),
	(18,'ticket','0002_auto_20180410_1749','2018-04-10 17:49:06.562710'),
	(19,'workflow','0002_auto_20180410_1749','2018-04-10 17:49:06.690036'),
	(21,'ticket','0003_ticketrecord_relation','2018-04-15 17:21:55.494957'),
	(22,'ticket','0004_auto_20180417_2348','2018-04-17 23:48:22.378917'),
	(23,'workflow','0003_auto_20180417_2348','2018-04-17 23:48:22.391679'),
	(24,'ticket','0005_auto_20180418_0001','2018-04-18 00:01:52.296081'),
	(25,'workflow','0004_workflow_view_permission_check','2018-04-22 15:58:37.766199'),
	(26,'workflow','0005_auto_20180423_2114','2018-04-23 21:14:51.345960'),
	(27,'workflow','0006_auto_20180423_2116','2018-04-23 21:17:03.970113'),
	(28,'workflow','0007_auto_20180424_0656','2018-04-24 06:56:48.399867'),
	(29,'workflow','0008_auto_20180424_0708','2018-04-24 07:08:53.913939'),
	(30,'workflow','0009_auto_20180430_2129','2018-04-30 21:29:29.307194'),
	(31,'ticket','0006_auto_20180505_1549','2018-05-05 15:49:16.131657'),
	(32,'workflow','0010_auto_20180505_1549','2018-05-05 15:49:16.168741'),
	(33,'workflow','0011_auto_20180509_0709','2018-05-09 07:09:37.847547'),
	(34,'workflow','0012_auto_20180511_0654','2018-05-11 06:54:50.920765'),
	(35,'ticket','0007_auto_20180516_0741','2018-05-16 07:46:02.412425'),
	(36,'ticket','0008_auto_20180516_0743','2018-05-16 07:46:02.417966'),
	(37,'workflow','0013_auto_20180511_1826','2018-05-16 07:46:02.420751'),
	(38,'workflow','0014_auto_20180516_0741','2018-05-16 07:46:02.423199'),
	(39,'ticket','0009_ticketflowlog_intervene_type_id','2018-05-17 06:36:01.493028'),
	(40,'ticket','0010_ticketcustomfield_multi_username_value','2018-05-22 06:46:49.124237'),
	(41,'workflow','0015_auto_20180522_0646','2018-05-22 06:46:49.132266'),
	(42,'workflow','0016_auto_20180620_1709','2018-07-30 07:21:05.079135'),
	(43,'workflow','0017_auto_20180730_0720','2018-07-30 07:21:05.193141'),
	(44,'ticket','0011_ticketrecord_script_run_last_result','2018-08-09 07:32:10.254032'),
	(45,'workflow','0018_auto_20180809_0732','2018-08-09 07:32:10.374771'),
	(46,'ticket','0012_delete_ticketstatelastman','2018-08-12 16:58:07.510558'),
	(47,'workflow','0019_state_remember_last_man_enable','2018-08-12 16:58:07.598511'),
	(50,'workflow','0020_workflow_limit_expression','2018-08-24 07:39:19.095010'),
	(51,'workflow','0021_customnotice','2018-08-26 10:30:18.818854'),
	(52,'ticket','0013_ticketrecord_is_end','2018-09-26 06:53:40.535144'),
	(53,'workflow','0022_auto_20180926_0653','2018-09-26 06:53:40.625847'),
	(54,'workflow','0023_auto_20181001_1012','2018-10-01 10:12:52.255104'),
	(56,'ticket','0014_auto_20181003_1708','2018-10-03 17:08:44.788212'),
	(57,'workflow','0024_auto_20181003_1708','2018-10-03 17:08:44.885439'),
	(58,'workflow','0025_transition_condition_expression','2018-10-06 17:03:26.434330'),
	(61,'auth','0010_alter_group_name_max_length','2020-05-24 22:37:33.755398'),
	(62,'auth','0011_update_proxy_permissions','2020-05-24 22:37:33.783096'),
	(63,'ticket','0002_auto_20200524_2236','2020-05-24 22:37:33.790575'),
	(65,'ticket','0003_auto_20200709_0721','2020-07-09 07:24:04.657405'),
	(66,'workflow','0002_auto_20200709_0721','2020-07-09 07:24:04.660250'),
	(78,'account','0001_initial','2020-07-13 06:53:51.327909'),
	(79,'account','0002_auto_20200716_0738','2020-07-16 07:38:46.281028'),
	(80,'account','0003_remove_loonuserdept_primary','2020-07-18 15:48:19.038239'),
	(81,'ticket','0004_auto_20200815_1603','2020-08-15 16:03:58.284651'),
	(82,'workflow','0003_auto_20200815_1603','2020-08-15 16:03:58.428618'),
	(83,'workflow','0004_auto_20200824_2346','2020-08-24 23:47:03.053224'),
	(84,'workflow','0005_auto_20200904_0716','2020-09-04 07:17:05.466431'),
	(85,'account','0004_auto_20201011_0953','2020-10-11 09:53:59.483137'),
	(86,'account','0005_delete_apptokenworkflow','2020-10-11 16:45:22.704833'),
	(87,'workflow','0006_workflowuserpermission','2020-10-11 16:45:22.746102');

/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table django_session
# ------------------------------------------------------------

DROP TABLE IF EXISTS `django_session`;

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`)
VALUES
	('1vk7k3b6bshxfh48y65b8bgujhooquwy','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-12-08 07:01:03.970216'),
	('1y65zkmbewrhmg5k9tsd1f7vwcpcp2di','ZWQ0YzhmMWYzOTZlZWViZTI1Y2U3ZWNmZmFjMDM1ODg2NjQ0MmRjMzp7Il9hdXRoX3VzZXJfaGFzaCI6ImJlOTIwNWY0NzE1MzlkMjBiODRjNTUyNGMyNTAxYTkwYWNlMDRmNzMiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2019-05-21 23:23:56.544517'),
	('2ixontmwlf3hm2fx2kj5i0sv4dv5ivn5','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-10-22 22:32:56.563563'),
	('2p4bd3iu2iz6cakbxn9hamdvqp3fvx7y','MWUzZjFjNThjNmM1MmRlMWIzYjY0NDFiODNlODE3MDIzMjQ2NGQwYzp7Il9hdXRoX3VzZXJfaGFzaCI6IjQ2MTUwYzAwNmQyNGM0Y2QyNzQ5Zjc2NGE4N2MzZDNlNjY0ZDA5NzgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2018-05-06 15:24:30.402451'),
	('2z5h72g5xwd90cippnk3i4l2h54j4hi7','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-10-20 10:32:47.096928'),
	('443zt1x4linfe3q3m8le9799cizpxedv','NTU1NDRhMGM1MDIyMDczYmFlY2MzZDdkZTMyYWZlYmYyMGRiMzhiNDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2019-10-04 15:15:48.843348'),
	('48n6uqarrd4r28j7fkamhjj2ouih60ao','MWM5NmI5ZDEzYmY1ZTBkNzg5MTU5NzcxOWRmMWQ1NTE1NDQyNWJjYTp7Il9hdXRoX3VzZXJfaGFzaCI6ImJlOTIwNWY0NzE1MzlkMjBiODRjNTUyNGMyNTAxYTkwYWNlMDRmNzMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2020-01-07 15:28:56.444956'),
	('6v8g5swfqi3730d43lvnc5wcvza9sema','ZDZmODM5ZWE3NjU3ZDNmNDhmYWNmYWIwNmY2YzFhOGZmNzFiNWZjNzp7Il9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9oYXNoIjoiNzViMTVmZDNhZTdjYzAxMGVhNWUwN2U2OGViZDEwOTI1YzcxMTQyNiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2018-11-14 15:51:42.081978'),
	('7ooloj2vtmn9bf9a2kduu6n769hcbtu8','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-11-10 06:55:03.630203'),
	('89n6o9o1ievv8jp7c75ezg59wz6dz26q','M2EwMmViZmQyZDAxZmU2NmE2Njg4OWYxNzk3ZDVkY2E1NmM0NzNiYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2020-01-30 20:06:35.406507'),
	('8dmqa9gzarnvpt98w3xybsawanwt68vc','M2EwMmViZmQyZDAxZmU2NmE2Njg4OWYxNzk3ZDVkY2E1NmM0NzNiYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2019-03-12 07:23:34.068060'),
	('9cr064a9i4i8ocwjen8zu0tgu1jto0m0','ODFmY2RiYTVlMTg0YTU1NzVjYzQwMWJjNGVmNTY4Zjg3MTQyODBjMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4NWMxYWFmMjUwZTIxZTBkOWIwN2Y1YTMzYzY3YTI3YTFiNzRkZGYyIn0=','2020-06-11 07:31:35.429840'),
	('9lfhc7o23502ik23g9j2w29qge2kfypa','NGI1NWJiMTFiODAwZTI1M2RmZWQ5Mzg0OWVmYTIzY2U0ZjUzZWNmYTp7Il9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NWIxNWZkM2FlN2NjMDEwZWE1ZTA3ZTY4ZWJkMTA5MjVjNzExNDI2In0=','2018-11-14 15:48:39.149124'),
	('9ramvh4gbvkqdaika3gnfv2hk6ph0xqh','OWQ5MzU4ODg1Y2I2ZTU3MGIxZmQyZTZkYzIwNDE0YjkxMGU3NGI4Mjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwMTY3OTkzZTg4NzYyZTc3MGYxOWEwYjgyNGRiMGYzNTdkMTBlMDE4In0=','2020-07-27 07:34:06.377455'),
	('9xwrn8z21q7s4tshhu4vhik5n3hawjud','M2EwMmViZmQyZDAxZmU2NmE2Njg4OWYxNzk3ZDVkY2E1NmM0NzNiYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2019-12-19 20:40:37.899320'),
	('aa8lsabc1g5i96vmj2hggsowtkkit4dg','ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=','2020-04-25 18:23:39.580583'),
	('ad0vu3brcz9mhn171f7tjlh4klanzu7m','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-10-20 10:32:44.346912'),
	('bbnyl8qgsl2jyfwhhib5o73wfqx90mvc','NGJhZGE3MjdhM2Q1MjhkMWI4NzdjYmQ1NjJiODYxYzAyM2YwMmRiZDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NWI3NzlmMDhmYjhiMmFhYzk0Y2U5YTA0NzBiZWIzMzg1NzIxOGY3In0=','2020-07-23 07:01:14.115619'),
	('bd4e3qkwf91tusabodfa8tu23175m4qh','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-11-10 06:55:04.048666'),
	('bzg1408jk06vn7gsnavpxpm8tgf2tq2f','MWM5NmI5ZDEzYmY1ZTBkNzg5MTU5NzcxOWRmMWQ1NTE1NDQyNWJjYTp7Il9hdXRoX3VzZXJfaGFzaCI6ImJlOTIwNWY0NzE1MzlkMjBiODRjNTUyNGMyNTAxYTkwYWNlMDRmNzMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2019-03-26 14:22:53.391084'),
	('cc6v8vs443jhidzfv7tefxc9cndds1ww','ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=','2019-02-26 07:20:43.624282'),
	('eyoe9bj29jnk3hrjwjj7el4z7uamuv8j','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-12-08 07:01:03.461217'),
	('fp4zkhd8cgfj6tacff6giqm75wwd4p93','NTU1NDRhMGM1MDIyMDczYmFlY2MzZDdkZTMyYWZlYmYyMGRiMzhiNDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2018-08-20 07:12:12.680740'),
	('fxdc90snam1vje7bpv3wiafwu9pooeyk','M2EwMmViZmQyZDAxZmU2NmE2Njg4OWYxNzk3ZDVkY2E1NmM0NzNiYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2018-07-17 07:04:43.733996'),
	('g2xrvclza9noaxtq1uyr97bt976snvod','ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=','2019-02-10 17:28:03.379373'),
	('gi4p54ka4u6vww4kpqogolmdquj52wup','YTQyMzg3NzMzMzRkZDgxNzU1YWM1OTE3YWExZTFjMDdlMWZmNzM5Zjp7Il9hdXRoX3VzZXJfaGFzaCI6IjQ2MTUwYzAwNmQyNGM0Y2QyNzQ5Zjc2NGE4N2MzZDNlNjY0ZDA5NzgiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2018-04-24 21:38:48.844698'),
	('gpy4b940016fb6suzh7til0j2sgamgwq','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-08-14 20:35:48.629380'),
	('gwwul2nmxqyrdzx1wbej4uj0ahzsdwow','YmI5MjhmNmQ3YzFjMjM3ZjgwYTg4ZmRkMjk1MmU0ZGU5ZjI4Nzg0Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=','2018-10-28 16:07:27.753614'),
	('h7i2xkk181sk6inahviq9uynm675wdny','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-11-03 06:57:03.149193'),
	('hhgqxdf0hdc8ocy6egn2ggzfdic75vee','ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=','2020-04-26 18:46:49.543046'),
	('hlize0igljpdnym3rqudskfxl2dqzb3k','ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=','2020-05-15 07:58:42.170778'),
	('ikpnzy0jsc0jiede5r6cxhoyagq2payb','YTQyMzg3NzMzMzRkZDgxNzU1YWM1OTE3YWExZTFjMDdlMWZmNzM5Zjp7Il9hdXRoX3VzZXJfaGFzaCI6IjQ2MTUwYzAwNmQyNGM0Y2QyNzQ5Zjc2NGE4N2MzZDNlNjY0ZDA5NzgiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2018-04-24 21:36:50.610586'),
	('jnd3hk7qjask3mnk7m96vqtpecw0zbvb','M2EwMmViZmQyZDAxZmU2NmE2Njg4OWYxNzk3ZDVkY2E1NmM0NzNiYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2019-08-23 11:30:02.254886'),
	('jw2psatj7z4zrur42urk3wluopurpqr1','YmI5MjhmNmQ3YzFjMjM3ZjgwYTg4ZmRkMjk1MmU0ZGU5ZjI4Nzg0Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=','2018-10-21 19:52:52.775319'),
	('jxylntmexpile98og8k5lfzfovkybi8u','YmI5MjhmNmQ3YzFjMjM3ZjgwYTg4ZmRkMjk1MmU0ZGU5ZjI4Nzg0Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=','2019-05-02 06:44:06.734299'),
	('kg8r2wz1n498cp6hvo0c0h5z3r9r98q4','ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=','2020-04-20 20:52:09.179185'),
	('kjlggcmh3exerlwysdryf7flevqmy2jq','MWJjYzQ4N2JlMGVmMjkyMjljOTEyZTRjNTg2NzY4YTdhOTFmOTE3Yjp7Il9hdXRoX3VzZXJfaGFzaCI6ImU4ZTc4MmE5YTU2OWU0MjRjZjgwMGM1MTFjMjViY2JiN2FhMjhhZGEiLCJfYXV0aF91c2VyX2lkIjoiOSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2019-11-17 23:25:30.724572'),
	('kkij8defjj21v1tritqk13edxcvrqmvy','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-11-24 06:59:36.803728'),
	('l187tcfmtjwn2yvr407elnm51dqmaa0u','YmI5MjhmNmQ3YzFjMjM3ZjgwYTg4ZmRkMjk1MmU0ZGU5ZjI4Nzg0Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=','2018-08-13 07:21:42.060139'),
	('lk3sd5w2d6w4g6p53ddc5y9946c1a413','ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=','2018-12-11 07:10:11.233169'),
	('lujtvklj4m0y5g8tktlx5r8djkt1c4yb','ZWQ0YzhmMWYzOTZlZWViZTI1Y2U3ZWNmZmFjMDM1ODg2NjQ0MmRjMzp7Il9hdXRoX3VzZXJfaGFzaCI6ImJlOTIwNWY0NzE1MzlkMjBiODRjNTUyNGMyNTAxYTkwYWNlMDRmNzMiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2019-12-01 23:47:26.990998'),
	('m06alvw9jdi5g69rwxhk4b5pw04g4ag7','ODFmY2RiYTVlMTg0YTU1NzVjYzQwMWJjNGVmNTY4Zjg3MTQyODBjMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4NWMxYWFmMjUwZTIxZTBkOWIwN2Y1YTMzYzY3YTI3YTFiNzRkZGYyIn0=','2020-06-27 20:19:06.371907'),
	('n22ajtmchkt90lljw3f1t9iahaqcdrnm','ODFmY2RiYTVlMTg0YTU1NzVjYzQwMWJjNGVmNTY4Zjg3MTQyODBjMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4NWMxYWFmMjUwZTIxZTBkOWIwN2Y1YTMzYzY3YTI3YTFiNzRkZGYyIn0=','2020-06-16 06:45:47.434338'),
	('obsuhola6a6sgdqbdccd8ye1e807e8te','NTU1NDRhMGM1MDIyMDczYmFlY2MzZDdkZTMyYWZlYmYyMGRiMzhiNDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2019-12-08 10:13:39.832179'),
	('oj3syswyxxx7uav23hs911ipc0br1u92','ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=','2020-04-18 18:35:47.306348'),
	('ovxzxgg507qeixgbvqvq79epgiidwqi9','ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=','2019-05-31 15:13:51.502976'),
	('owlrvg9mccecpbhjfbmdijlo6n2peoa2','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-10-22 22:32:56.080055'),
	('owm2fbdfsrumq18zekbp0zampcwotnq9','ZWQ0YzhmMWYzOTZlZWViZTI1Y2U3ZWNmZmFjMDM1ODg2NjQ0MmRjMzp7Il9hdXRoX3VzZXJfaGFzaCI6ImJlOTIwNWY0NzE1MzlkMjBiODRjNTUyNGMyNTAxYTkwYWNlMDRmNzMiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2019-10-07 17:19:59.997301'),
	('phjijmbxop4lp7go5q5hgvuon2xksd6a','ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=','2020-04-25 10:21:25.512714'),
	('qd0dhjm1eqhu6rsy8lm8yspm24bg5fah','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-11-03 06:57:03.317167'),
	('qkjvfwq4i5uz0ctjsacz8r8h5f57mz16','MWM5NmI5ZDEzYmY1ZTBkNzg5MTU5NzcxOWRmMWQ1NTE1NDQyNWJjYTp7Il9hdXRoX3VzZXJfaGFzaCI6ImJlOTIwNWY0NzE1MzlkMjBiODRjNTUyNGMyNTAxYTkwYWNlMDRmNzMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2019-11-23 16:38:31.799104'),
	('qrugroidqpdoepvimz4mtqrsw8elq3px','M2EwMmViZmQyZDAxZmU2NmE2Njg4OWYxNzk3ZDVkY2E1NmM0NzNiYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2018-06-06 09:50:27.154850'),
	('rhy3t0ut1v8ev1bqja8sql9htybr95k7','NTU1NDRhMGM1MDIyMDczYmFlY2MzZDdkZTMyYWZlYmYyMGRiMzhiNDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2018-09-05 07:18:38.000344'),
	('rq6afbvp5ag5ftezg16ba3qb32nhtq5y','YmI5MjhmNmQ3YzFjMjM3ZjgwYTg4ZmRkMjk1MmU0ZGU5ZjI4Nzg0Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=','2019-10-28 15:20:04.381595'),
	('s9elc56k3l0r6m0w0ab5dexnuxylllrc','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-11-03 06:57:03.525007'),
	('sdnytru1oj6p8kpy6y9zchz8vxi30p5p','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-11-24 06:59:36.537690'),
	('svnhzwfovvsn5p4x7o4xmqir13bkj23u','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-12-08 07:01:03.561301'),
	('u6ajtwkt000z632l1cbw1sfycv5ij80j','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-10-04 22:17:49.413496'),
	('uc120vlnss4jhy3i8kxow00uqbozf6m4','ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=','2018-05-23 06:56:36.173728'),
	('uo7kcl3nolb5hi95e32tp7rgg3zt820j','NTU1NDRhMGM1MDIyMDczYmFlY2MzZDdkZTMyYWZlYmYyMGRiMzhiNDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2019-01-27 15:55:29.014400'),
	('uoi4cbhlba7iskcp1yty57rhb7blwav8','NTU1NDRhMGM1MDIyMDczYmFlY2MzZDdkZTMyYWZlYmYyMGRiMzhiNDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2019-06-15 16:16:15.853121'),
	('v5js0l5la617b973ib4gp5qr9i1y3h3m','ZDZmODM5ZWE3NjU3ZDNmNDhmYWNmYWIwNmY2YzFhOGZmNzFiNWZjNzp7Il9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9oYXNoIjoiNzViMTVmZDNhZTdjYzAxMGVhNWUwN2U2OGViZDEwOTI1YzcxMTQyNiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2018-11-14 15:47:30.453740'),
	('v5sw3zyxvlfb38n6kdqgv870ja21c692','ZWQ0YzhmMWYzOTZlZWViZTI1Y2U3ZWNmZmFjMDM1ODg2NjQ0MmRjMzp7Il9hdXRoX3VzZXJfaGFzaCI6ImJlOTIwNWY0NzE1MzlkMjBiODRjNTUyNGMyNTAxYTkwYWNlMDRmNzMiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2019-09-07 10:22:52.001363'),
	('vfet6rpq8v3cf8q2snjqasp56t5mk7bh','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-08-28 09:41:32.755572'),
	('wr3brfyg056entiteumea6sgwvtdiwi0','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-12-08 07:01:03.457139'),
	('wzsw1jekty6312454wpgy50ojwzj8b8w','YmI5MjhmNmQ3YzFjMjM3ZjgwYTg4ZmRkMjk1MmU0ZGU5ZjI4Nzg0Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=','2018-11-28 23:44:17.536284'),
	('x2bb8rj0b7gkdd8zzs2qpmqbp1qskl28','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-11-24 06:59:37.139488'),
	('x3s6nbkrjx7m7kpb8zorzvaqqo19lkqm','ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=','2020-06-07 17:49:02.144519'),
	('xjsbhzbqt0b4e6mee6jt80d3l9k9cy84','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-12-08 07:01:04.519791'),
	('xri4fxmn0mnbiqel4n5xu2agw3rqe9kz','ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=','2019-11-26 17:56:10.530875'),
	('yp4eflhf4z6ryg43yfp103j3e1jlprp5','ZWQ0YzhmMWYzOTZlZWViZTI1Y2U3ZWNmZmFjMDM1ODg2NjQ0MmRjMzp7Il9hdXRoX3VzZXJfaGFzaCI6ImJlOTIwNWY0NzE1MzlkMjBiODRjNTUyNGMyNTAxYTkwYWNlMDRmNzMiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=','2019-06-29 18:15:12.485234'),
	('yqo3dtnk8pasr19u3qwkgz4bvpv0yg08','NTU1NDRhMGM1MDIyMDczYmFlY2MzZDdkZTMyYWZlYmYyMGRiMzhiNDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=','2018-05-28 10:04:09.557125'),
	('zaewvjgfzeo085bk65usxwd70zwch1fs','ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=','2020-11-10 06:55:03.901421');

/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table ticket_ticketcustomfield
# ------------------------------------------------------------

DROP TABLE IF EXISTS `ticket_ticketcustomfield`;

CREATE TABLE `ticket_ticketcustomfield` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `ticket_id` int(11) NOT NULL,
  `field_key` varchar(50) NOT NULL DEFAULT '',
  `field_type_id` int(11) NOT NULL,
  `char_value` varchar(1000) NOT NULL,
  `int_value` int(11) NOT NULL,
  `float_value` double NOT NULL,
  `bool_value` tinyint(1) NOT NULL,
  `date_value` date NOT NULL,
  `datetime_value` datetime(6) NOT NULL,
  `time_value` time(6) NOT NULL,
  `radio_value` varchar(50) NOT NULL,
  `checkbox_value` varchar(50) NOT NULL,
  `select_value` varchar(50) NOT NULL,
  `multi_select_value` varchar(50) NOT NULL,
  `text_value` longtext NOT NULL,
  `username_value` varchar(50) NOT NULL,
  `creator` varchar(50) NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `multi_username_value` varchar(1000) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_ticket_field` (`ticket_id`,`field_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `ticket_ticketcustomfield` WRITE;
/*!40000 ALTER TABLE `ticket_ticketcustomfield` DISABLE KEYS */;

INSERT INTO `ticket_ticketcustomfield` (`id`, `name`, `ticket_id`, `field_key`, `field_type_id`, `char_value`, `int_value`, `float_value`, `bool_value`, `date_value`, `datetime_value`, `time_value`, `radio_value`, `checkbox_value`, `select_value`, `multi_select_value`, `text_value`, `username_value`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `multi_username_value`)
VALUES
	(14,'请假类型',13,'leave_type',40,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','2','','','','','admin','2018-05-13 21:53:15.776693','2018-05-13 21:53:15.776753',0,''),
	(15,'代理人',13,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','zhangsan','admin','2018-05-13 21:53:15.784787','2018-05-13 21:53:15.784839',0,''),
	(16,'请假原因及相关附件',13,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','去喝喜酒','','admin','2018-05-13 21:53:15.792655','2018-05-13 21:53:15.792711',0,''),
	(17,'开始时间',13,'leave_start',30,'',0,0,0,'0001-01-01','2018-04-10 09:00:00.000000','00:00:01.000000','','','','','','','admin','2018-05-13 21:53:15.800632','2018-05-13 21:53:15.800683',0,''),
	(18,'请假天数(0.5的倍数)',13,'leave_days',5,'3',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','admin','2018-05-13 21:53:15.809216','2018-05-13 21:53:15.809266',0,''),
	(19,'结束时间',13,'leave_end',30,'',0,0,0,'0001-01-01','2018-04-12 18:00:00.000000','00:00:01.000000','','','','','','','admin','2018-05-13 21:53:15.817437','2018-05-13 21:53:15.817484',0,''),
	(20,'代理人',14,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','zhangsan1','admin','2018-05-13 22:24:41.969926','2018-05-13 22:24:41.969982',0,''),
	(21,'请假天数(0.5的倍数)',14,'leave_days',5,'3',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','admin','2018-05-13 22:24:41.978508','2018-05-13 22:24:41.978600',0,''),
	(22,'开始时间',14,'leave_start',30,'',0,0,0,'0001-01-01','2018-05-10 09:00:00.000000','00:00:01.000000','','','','','','','admin','2018-05-13 22:24:41.988270','2018-05-13 22:24:41.988346',0,''),
	(23,'请假类型',14,'leave_type',40,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','1','','','','','admin','2018-05-13 22:24:41.997839','2018-05-13 22:24:41.997891',0,''),
	(24,'结束时间',14,'leave_end',30,'',0,0,0,'0001-01-01','2018-05-13 09:00:00.000000','00:00:01.000000','','','','','','','admin','2018-05-13 22:24:42.008241','2018-05-13 22:24:42.008292',0,''),
	(25,'请假原因及相关附件',14,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','喝喜酒','','admin','2018-05-13 22:24:42.016808','2018-05-13 22:24:42.016898',0,''),
	(26,'结束时间',15,'leave_end',30,'',0,0,0,'0001-01-01','2018-05-13 09:00:00.000000','00:00:01.000000','','','','','','','admin','2018-05-13 22:28:21.643297','2018-05-13 22:28:21.643346',0,''),
	(27,'请假原因及相关附件',15,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','喝喜酒','','admin','2018-05-13 22:28:21.650778','2018-05-13 22:28:21.650828',0,''),
	(28,'代理人',15,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','zhangsan1','admin','2018-05-13 22:28:21.659327','2018-05-13 22:28:21.659375',0,''),
	(29,'请假天数(0.5的倍数)',15,'leave_days',5,'3',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','admin','2018-05-13 22:28:21.667908','2018-05-13 22:28:21.667955',0,''),
	(30,'开始时间',15,'leave_start',30,'',0,0,0,'0001-01-01','2018-05-10 09:00:00.000000','00:00:01.000000','','','','','','','admin','2018-05-13 22:28:21.675754','2018-05-13 22:28:21.675803',0,''),
	(31,'请假类型',15,'leave_type',40,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','1','','','','','admin','2018-05-13 22:28:21.683366','2018-05-13 22:28:21.683414',0,''),
	(32,'结束时间',16,'leave_end',30,'',0,0,0,'0001-01-01','2018-04-12 18:00:00.000000','00:00:01.000000','','','','','','','admin','2018-05-13 22:34:12.690959','2018-05-13 22:34:12.691033',0,''),
	(33,'请假原因及相关附件',16,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','去喝喜酒','','admin','2018-05-13 22:34:12.701832','2018-05-13 22:34:12.701889',0,''),
	(34,'代理人',16,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','zhangsan','admin','2018-05-13 22:34:12.711844','2018-05-13 22:34:12.711905',0,''),
	(35,'请假天数(0.5的倍数)',16,'leave_days',5,'3',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','admin','2018-05-13 22:34:12.721909','2018-05-13 22:34:12.721966',0,''),
	(36,'开始时间',16,'leave_start',30,'',0,0,0,'0001-01-01','2018-04-10 09:00:00.000000','00:00:01.000000','','','','','','','admin','2018-05-13 22:34:12.730191','2018-05-13 22:34:12.730245',0,''),
	(37,'请假类型',16,'leave_type',40,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','2','','','','','admin','2018-05-13 22:34:12.741366','2018-05-13 22:34:12.741426',0,''),
	(38,'申请原因',17,'vpn_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','在家办公','','admin','2018-05-15 07:16:38.326174','2018-05-15 07:16:38.326274',0,''),
	(39,'申请原因',18,'vpn_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','在家办公','','admin','2018-05-15 07:37:28.008199','2018-05-15 07:37:28.008245',0,''),
	(40,'请假天数(0.5的倍数)',19,'leave_days',5,'2',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','admin','2018-10-19 00:08:40.397150','2018-10-19 00:08:40.397166',0,''),
	(41,'请假类型',19,'leave_type',35,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','2','','','','','','admin','2018-10-19 00:08:40.402913','2018-10-19 00:08:40.402928',0,''),
	(42,'开始时间',19,'leave_start',30,'',0,0,0,'0001-01-01','2018-10-20 09:00:00.000000','00:00:01.000000','','','','','','','admin','2018-10-19 00:08:40.408762','2018-10-19 00:08:40.408775',0,''),
	(43,'请假原因及相关附件',19,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>teste</p>','','admin','2018-10-19 00:08:40.413509','2018-10-19 00:08:40.413529',0,''),
	(44,'结束时间',19,'leave_end',30,'',0,0,0,'0001-01-01','2018-10-21 18:00:00.000000','00:00:01.000000','','','','','','','admin','2018-10-19 00:08:40.419809','2018-10-19 00:08:40.419833',0,''),
	(45,'代理人',19,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','admin','admin','2018-10-19 00:08:40.425879','2018-10-19 00:08:40.425895',0,''),
	(46,'结束时间',20,'leave_end',30,'',0,0,0,'0001-01-01','2018-10-20 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-10-19 00:38:41.367687','2018-10-19 00:38:41.367703',0,''),
	(47,'开始时间',20,'leave_start',30,'',0,0,0,'0001-01-01','2018-10-19 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-10-19 00:38:41.372330','2018-10-19 00:38:41.372352',0,''),
	(48,'代理人',20,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','admin','admin','2018-10-19 00:38:41.376402','2018-10-19 00:38:41.376417',0,''),
	(49,'请假天数(0.5的倍数)',20,'leave_days',5,'2',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','admin','2018-10-19 00:38:41.379313','2018-10-19 00:38:41.379327',0,''),
	(50,'请假类型',20,'leave_type',35,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','2','','','','','','admin','2018-10-19 00:38:41.383436','2018-10-19 00:38:41.383450',0,''),
	(51,'请假原因及相关附件',20,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>dfsf</p>','','admin','2018-10-19 00:38:41.387250','2018-10-19 00:38:41.387266',0,''),
	(52,'项目标识',21,'project_code',5,'prj001',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','admin','2018-10-21 11:14:37.680365','2018-10-21 11:14:37.680400',0,''),
	(53,'项目开发人员',21,'project_devs',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','admin','admin','2018-10-21 11:14:37.686541','2018-10-21 11:14:37.686575',0,''),
	(54,'项目测试人员',21,'project_qas',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','admin','admin','2018-10-21 11:14:37.692349','2018-10-21 11:14:37.692382',0,''),
	(55,'请假原因及相关附件',22,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>ddd</p>','','admin','2018-10-22 07:12:16.466886','2018-10-22 07:12:16.466914',0,''),
	(56,'请假天数(0.5的倍数)',22,'leave_days',5,'1',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','admin','2018-10-22 07:12:16.472163','2018-10-22 07:12:16.472181',0,''),
	(57,'请假类型',22,'leave_type',35,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','3','','','','','','admin','2018-10-22 07:12:16.477751','2018-10-22 07:12:16.477769',0,''),
	(58,'开始时间',22,'leave_start',30,'',0,0,0,'0001-01-01','2018-10-22 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-10-22 07:12:16.481785','2018-10-22 07:12:16.481810',0,''),
	(59,'代理人',22,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','admin','admin','2018-10-22 07:12:16.485136','2018-10-22 07:12:16.485153',0,''),
	(60,'结束时间',22,'leave_end',30,'',0,0,0,'0001-01-01','2018-10-23 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-10-22 07:12:16.489084','2018-10-22 07:12:16.489109',0,''),
	(61,'请假原因及相关附件',23,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>te</p>','','admin','2018-10-22 08:05:37.200981','2018-10-22 08:05:37.201000',0,''),
	(62,'请假天数(0.5的倍数)',23,'leave_days',5,'2',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','admin','2018-10-22 08:05:37.204565','2018-10-22 08:05:37.204582',0,''),
	(63,'请假类型',23,'leave_type',35,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','3','','','','','','admin','2018-10-22 08:05:37.207974','2018-10-22 08:05:37.207991',0,''),
	(64,'开始时间',23,'leave_start',30,'',0,0,0,'0001-01-01','2018-10-22 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-10-22 08:05:37.212592','2018-10-22 08:05:37.212654',0,''),
	(65,'代理人',23,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','admin','admin','2018-10-22 08:05:37.217232','2018-10-22 08:05:37.217251',0,''),
	(66,'结束时间',23,'leave_end',30,'',0,0,0,'0001-01-01','2018-10-24 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-10-22 08:05:37.221150','2018-10-22 08:05:37.221170',0,''),
	(67,'请假原因及相关附件',24,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>11</p>','','admin','2018-11-27 07:09:06.342895','2018-11-27 07:09:06.342911',0,''),
	(68,'请假天数(0.5的倍数)',24,'leave_days',5,'1',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:09:06.348005','2018-11-27 07:09:06.348020',0,''),
	(69,'请假类型',24,'leave_type',35,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','1','','','','','','admin','2018-11-27 07:09:06.351837','2018-11-27 07:09:06.351853',0,''),
	(70,'代理人',24,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','admin','admin','2018-11-27 07:09:06.355020','2018-11-27 07:09:06.355035',0,''),
	(71,'开始时间',24,'leave_start',30,'',0,0,0,'0001-01-01','2018-11-27 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:09:06.358199','2018-11-27 07:09:06.358214',0,''),
	(72,'结束时间',24,'leave_end',30,'',0,0,0,'0001-01-01','2018-11-28 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:09:06.362700','2018-11-27 07:09:06.362715',0,''),
	(73,'请假原因及相关附件',25,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>111</p>','','admin','2018-11-27 07:12:27.937822','2018-11-27 07:12:27.937842',0,''),
	(74,'请假天数(0.5的倍数)',25,'leave_days',5,'1',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:12:27.943184','2018-11-27 07:12:27.943204',0,''),
	(75,'请假类型',25,'leave_type',35,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','1','','','','','','admin','2018-11-27 07:12:27.947050','2018-11-27 07:12:27.947069',0,''),
	(76,'代理人',25,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','admin','admin','2018-11-27 07:12:27.950977','2018-11-27 07:12:27.951038',0,''),
	(77,'开始时间',25,'leave_start',30,'',0,0,0,'0001-01-01','2018-11-27 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:12:27.954845','2018-11-27 07:12:27.954863',0,''),
	(78,'结束时间',25,'leave_end',30,'',0,0,0,'0001-01-01','2018-11-28 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:12:27.958336','2018-11-27 07:12:27.958353',0,''),
	(79,'开始时间',26,'leave_start',30,'',0,0,0,'0001-01-01','2018-11-27 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:14:06.394830','2018-11-27 07:14:06.394870',0,''),
	(80,'代理人',26,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','admin','admin','2018-11-27 07:14:06.401115','2018-11-27 07:14:06.401155',0,''),
	(81,'请假原因及相关附件',26,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>111</p>','','admin','2018-11-27 07:14:06.408893','2018-11-27 07:14:06.408933',0,''),
	(82,'结束时间',26,'leave_end',30,'',0,0,0,'0001-01-01','2018-11-28 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:14:06.416352','2018-11-27 07:14:06.416392',0,''),
	(83,'请假天数(0.5的倍数)',26,'leave_days',5,'1',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:14:06.423573','2018-11-27 07:14:06.423612',0,''),
	(84,'请假类型',26,'leave_type',35,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','1','','','','','','admin','2018-11-27 07:14:06.430362','2018-11-27 07:14:06.430401',0,''),
	(85,'请假原因及相关附件',27,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>111</p>','','admin','2018-11-27 07:20:16.259524','2018-11-27 07:20:16.259781',0,''),
	(86,'开始时间',27,'leave_start',30,'',0,0,0,'0001-01-01','2018-11-27 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:20:16.291175','2018-11-27 07:20:16.291268',0,''),
	(87,'请假天数(0.5的倍数)',27,'leave_days',5,'1',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:20:16.317001','2018-11-27 07:20:16.317439',0,''),
	(88,'代理人',27,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','admin','admin','2018-11-27 07:20:16.336555','2018-11-27 07:20:16.336888',0,''),
	(89,'结束时间',27,'leave_end',30,'',0,0,0,'0001-01-01','2018-11-28 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:20:16.367837','2018-11-27 07:20:16.368304',0,''),
	(90,'请假类型',27,'leave_type',35,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','1','','','','','','admin','2018-11-27 07:20:16.400435','2018-11-27 07:20:16.400677',0,''),
	(91,'请假原因及相关附件',28,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>1111</p>','','admin','2018-11-27 07:21:00.039873','2018-11-27 07:21:00.039912',0,''),
	(92,'开始时间',28,'leave_start',30,'',0,0,0,'0001-01-01','2018-11-27 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:21:00.047632','2018-11-27 07:21:00.047695',0,''),
	(93,'请假天数(0.5的倍数)',28,'leave_days',5,'1',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:21:00.055101','2018-11-27 07:21:00.055147',0,''),
	(94,'代理人',28,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','admin','admin','2018-11-27 07:21:00.072241','2018-11-27 07:21:00.072379',0,''),
	(95,'结束时间',28,'leave_end',30,'',0,0,0,'0001-01-01','2018-11-28 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:21:00.086745','2018-11-27 07:21:00.086787',0,''),
	(96,'请假类型',28,'leave_type',35,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','1','','','','','','admin','2018-11-27 07:21:00.105107','2018-11-27 07:21:00.105174',0,''),
	(97,'结束时间',29,'leave_end',30,'',0,0,0,'0001-01-01','2018-11-28 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:23:04.049887','2018-11-27 07:23:04.049926',0,''),
	(98,'请假类型',29,'leave_type',35,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','1','','','','','','admin','2018-11-27 07:23:04.057211','2018-11-27 07:23:04.057275',0,''),
	(99,'开始时间',29,'leave_start',30,'',0,0,0,'0001-01-01','2018-11-27 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:23:04.071338','2018-11-27 07:23:04.071400',0,''),
	(100,'请假原因及相关附件',29,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>11</p>','','admin','2018-11-27 07:23:04.092423','2018-11-27 07:23:04.092484',0,''),
	(101,'代理人',29,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','admin','admin','2018-11-27 07:23:04.101704','2018-11-27 07:23:04.101740',0,''),
	(102,'请假天数(0.5的倍数)',29,'leave_days',5,'1',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:23:04.107897','2018-11-27 07:23:04.107944',0,''),
	(103,'开始时间',30,'leave_start',30,'',0,0,0,'0001-01-01','2018-11-27 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:23:47.936083','2018-11-27 07:23:47.936106',0,''),
	(104,'请假类型',30,'leave_type',35,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','1','','','','','','admin','2018-11-27 07:23:47.939649','2018-11-27 07:23:47.939668',0,''),
	(105,'请假天数(0.5的倍数)',30,'leave_days',5,'1',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:23:47.943261','2018-11-27 07:23:47.943279',0,''),
	(106,'请假原因及相关附件',30,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>11</p>','','admin','2018-11-27 07:23:47.947946','2018-11-27 07:23:47.947967',0,''),
	(107,'结束时间',30,'leave_end',30,'',0,0,0,'0001-01-01','2018-11-28 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:23:47.951685','2018-11-27 07:23:47.951702',0,''),
	(108,'代理人',30,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','admin','admin','2018-11-27 07:23:47.955157','2018-11-27 07:23:47.955174',0,''),
	(109,'开始时间',31,'leave_start',30,'',0,0,0,'0001-01-01','2018-11-27 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:24:07.542624','2018-11-27 07:24:07.542643',0,''),
	(110,'请假类型',31,'leave_type',35,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','1','','','','','','admin','2018-11-27 07:24:07.546783','2018-11-27 07:24:07.546807',0,''),
	(111,'请假天数(0.5的倍数)',31,'leave_days',5,'1',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:24:07.550448','2018-11-27 07:24:07.550466',0,''),
	(112,'请假原因及相关附件',31,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>sdf</p>','','admin','2018-11-27 07:24:07.555116','2018-11-27 07:24:07.555134',0,''),
	(113,'结束时间',31,'leave_end',30,'',0,0,0,'0001-01-01','2018-11-28 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:24:07.559471','2018-11-27 07:24:07.559489',0,''),
	(114,'代理人',31,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','admin','admin','2018-11-27 07:24:07.564760','2018-11-27 07:24:07.564778',0,''),
	(115,'开始时间',32,'leave_start',30,'',0,0,0,'0001-01-01','2018-11-27 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:24:31.262779','2018-11-27 07:24:31.262796',0,''),
	(116,'请假类型',32,'leave_type',35,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','1','','','','','','admin','2018-11-27 07:24:31.266424','2018-11-27 07:24:31.266442',0,''),
	(117,'请假天数(0.5的倍数)',32,'leave_days',5,'1',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:24:31.269982','2018-11-27 07:24:31.270000',0,''),
	(118,'请假原因及相关附件',32,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>1111</p>','','admin','2018-11-27 07:24:31.274681','2018-11-27 07:24:31.274703',0,''),
	(119,'结束时间',32,'leave_end',30,'',0,0,0,'0001-01-01','2018-11-28 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:24:31.278645','2018-11-27 07:24:31.278662',0,''),
	(120,'代理人',32,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','admin','admin','2018-11-27 07:24:31.282746','2018-11-27 07:24:31.282764',0,''),
	(121,'开始时间',33,'leave_start',30,'',0,0,0,'0001-01-01','2018-11-27 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:27:39.244015','2018-11-27 07:27:39.244036',0,''),
	(122,'请假类型',33,'leave_type',35,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','1','','','','','','admin','2018-11-27 07:27:39.251612','2018-11-27 07:27:39.251630',0,''),
	(123,'代理人',33,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','admin','admin','2018-11-27 07:27:39.255660','2018-11-27 07:27:39.255678',0,''),
	(124,'请假原因及相关附件',33,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>111</p>','','admin','2018-11-27 07:27:39.259256','2018-11-27 07:27:39.259274',0,''),
	(125,'请假天数(0.5的倍数)',33,'leave_days',5,'1',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:27:39.263655','2018-11-27 07:27:39.263673',0,''),
	(126,'结束时间',33,'leave_end',30,'',0,0,0,'0001-01-01','2018-11-28 12:00:00.000000','00:00:01.000000','','','','','','','admin','2018-11-27 07:27:39.267158','2018-11-27 07:27:39.267176',0,''),
	(127,'请假原因及相关附件',34,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>testest<br/></p>','','','2019-11-24 10:23:07.239887','2019-11-24 10:23:07.239935',0,''),
	(128,'代理人',34,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','admin','','2019-11-24 10:23:07.254463','2019-11-24 10:23:07.254513',0,''),
	(129,'结束时间',34,'leave_end',30,'',0,0,0,'0001-01-01','2019-11-27 00:00:00.000000','00:00:01.000000','','','','','','','','2019-11-24 10:23:07.260910','2019-11-24 10:23:07.260954',0,''),
	(130,'请假类型',34,'leave_type',35,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','1','','','','','','','2019-11-24 10:23:07.269189','2019-11-24 10:23:07.269245',0,''),
	(131,'开始时间',34,'leave_start',30,'',0,0,0,'0001-01-01','2019-11-26 00:00:00.000000','00:00:01.000000','','','','','','','','2019-11-24 10:23:07.275128','2019-11-24 10:23:07.275171',0,''),
	(132,'请假天数(0.5的倍数)',34,'leave_days',5,'1',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','','2019-11-24 10:23:07.283184','2019-11-24 10:23:07.283251',0,''),
	(133,'结束时间',35,'leave_end',30,'',0,0,0,'0001-01-01','2019-11-27 00:00:00.000000','00:00:01.000000','','','','','','','','2019-11-24 10:24:31.601549','2019-11-24 10:24:31.601604',0,''),
	(134,'开始时间',35,'leave_start',30,'',0,0,0,'0001-01-01','2019-11-26 00:00:00.000000','00:00:01.000000','','','','','','','','2019-11-24 10:24:31.612317','2019-11-24 10:24:31.612378',0,''),
	(135,'代理人',35,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','admin','','2019-11-24 10:24:31.620276','2019-11-24 10:24:31.620391',0,''),
	(136,'请假类型',35,'leave_type',35,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','1','','','','','','','2019-11-24 10:24:31.630119','2019-11-24 10:24:31.630172',0,''),
	(137,'请假原因及相关附件',35,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>testest<br/></p>','','','2019-11-24 10:24:31.645703','2019-11-24 10:24:31.645796',0,''),
	(138,'请假天数(0.5的倍数)',35,'leave_days',5,'1',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','','2019-11-24 10:24:31.691046','2019-11-24 10:24:31.691145',0,''),
	(139,'申请原因',36,'vpn_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>sfdsf</p>','','','2020-04-11 10:40:30.931733','2020-04-11 10:40:30.931986',0,''),
	(140,'申请原因',37,'vpn_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>testst</p>','','','2020-05-01 09:19:28.707812','2020-05-01 09:19:28.707852',0,''),
	(141,'申请原因',38,'vpn_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>sssss</p>','','','2020-05-01 09:21:56.857777','2020-05-01 09:21:56.857801',0,''),
	(142,'代理人',39,'leave_proxy',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','lilian','','2020-05-07 22:42:17.268983','2020-05-07 22:42:17.269009',0,''),
	(143,'开始时间',39,'leave_start',30,'',0,0,0,'0001-01-01','2020-05-08 00:00:00.000000','00:00:01.000000','','','','','','','','2020-05-07 22:42:17.272037','2020-05-07 22:42:17.272062',0,''),
	(144,'请假类型',39,'leave_type',35,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','2','','','','','','','2020-05-07 22:42:17.275146','2020-05-07 22:42:17.275176',0,''),
	(145,'请假原因及相关附件',39,'leave_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>testse</p>','','','2020-05-07 22:42:17.278852','2020-05-07 22:42:17.278881',0,''),
	(146,'结束时间',39,'leave_end',30,'',0,0,0,'0001-01-01','2020-05-08 00:00:00.000000','00:00:01.000000','','','','','','','','2020-05-07 22:42:17.281930','2020-05-07 22:42:17.281954',0,''),
	(147,'申请原因',40,'vpn_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>test</p>','','','2020-05-07 22:54:58.877521','2020-05-07 22:54:58.877549',0,''),
	(148,'申请原因',41,'vpn_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>test</p>','','','2020-05-17 17:31:54.248584','2020-05-17 17:31:54.248606',0,''),
	(149,'申请原因',42,'vpn_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>1111<br/></p>','','','2020-05-17 17:44:45.473731','2020-05-17 17:44:45.473777',0,''),
	(150,'申请原因',43,'vpn_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','<p>TEST</p>','','','2020-05-18 23:18:15.558838','2020-05-18 23:18:15.558867',0,''),
	(151,'申请原因',44,'vpn_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','sdfdsfsdfs','','','2020-08-21 10:39:32.866381','2020-08-21 10:39:32.866507',0,''),
	(152,'布尔字段',45,'bool_field',20,'',0,0,1,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','','2020-08-21 18:33:35.051863','2020-08-21 18:33:35.052315',0,''),
	(153,'单选字段',45,'checkbox_field',35,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','1','','','','','','','2020-08-21 18:33:35.103585','2020-08-21 18:33:35.103849',0,''),
	(154,'多选字段',45,'multi_checkbox_field',40,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','2','','','','','','2020-08-21 18:33:35.153087','2020-08-21 18:33:35.153593',0,''),
	(155,'下拉选择字段',45,'select_field',45,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','1','','','','','2020-08-21 18:33:35.233367','2020-08-21 18:33:35.233979',0,''),
	(156,'多选下拉列表',45,'multi_select_field',50,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','1,3','','','','2020-08-21 18:33:35.307356','2020-08-21 18:33:35.307723',0,''),
	(157,'文本字段',45,'text_field',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','fs','','','2020-08-21 18:33:35.356586','2020-08-21 18:33:35.356866',0,''),
	(158,'用户选择字段',45,'user_fleld',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','fdsf','','2020-08-21 18:33:35.400575','2020-08-21 18:33:35.400947',0,''),
	(159,'多选用户字段',45,'multi_user_field',70,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','','2020-08-21 18:33:35.436945','2020-08-21 18:33:35.437200',0,'sdfds'),
	(160,'附件字段',45,'attachment_field',80,'fdsfs',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','','2020-08-21 18:33:35.469506','2020-08-21 18:33:35.470104',0,''),
	(161,'布尔字段',46,'bool_field',20,'',0,0,1,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','','2020-08-21 18:42:06.328201','2020-08-21 18:42:06.328465',0,''),
	(162,'单选字段',46,'checkbox_field',35,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','1','','','','','','','2020-08-21 18:42:06.379073','2020-08-21 18:42:06.379318',0,''),
	(163,'多选字段',46,'multi_checkbox_field',40,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','2,3','','','','','','2020-08-21 18:42:06.422130','2020-08-21 18:42:06.422375',0,''),
	(164,'下拉选择字段',46,'select_field',45,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','1','','','','','2020-08-21 18:42:06.464354','2020-08-21 18:42:06.464590',0,''),
	(165,'多选下拉列表',46,'multi_select_field',50,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','1,2,3','','','','2020-08-21 18:42:06.503037','2020-08-21 18:42:06.503408',0,''),
	(166,'文本字段',46,'text_field',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','dfs','','','2020-08-21 18:42:06.540434','2020-08-21 18:42:06.540785',0,''),
	(167,'用户选择字段',46,'user_fleld',60,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','fdsf','','2020-08-21 18:42:06.579294','2020-08-21 18:42:06.579603',0,''),
	(168,'多选用户字段',46,'multi_user_field',70,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','','2020-08-21 18:42:06.614813','2020-08-21 18:42:06.615049',0,'fdsf'),
	(169,'附件字段',46,'attachment_field',80,'fdsfs',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','','2020-08-21 18:42:06.658653','2020-08-21 18:42:06.658897',0,''),
	(170,'开始时间',46,'leave_start',30,'',0,0,0,'0001-01-01','2020-08-21 00:00:05.000000','00:00:01.000000','','','','','','','','2020-08-21 18:42:06.707711','2020-08-21 18:42:06.708026',0,''),
	(171,'结束时间',46,'leave_end',30,'',0,0,0,'0001-01-01','2020-08-21 18:15:52.000000','00:00:01.000000','','','','','','','','2020-08-21 18:42:06.758803','2020-08-21 18:42:06.759161',0,''),
	(172,'请假类型',46,'leave_type',35,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','1','','','','','','','2020-08-21 18:42:06.803855','2020-08-21 18:42:06.804139',0,''),
	(173,'请假原因及相关附件',46,'leave_reason',10,'',111,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','','','','2020-08-21 18:42:06.856788','2020-08-21 18:42:06.857048',0,''),
	(174,'申请原因',47,'vpn_reason',55,'',0,0,0,'0001-01-01','0001-01-01 00:00:00.000000','00:00:01.000000','','','','','fdsfsfsffhahhah哈哈哈发\nfdsfsfsffhahhah哈哈哈发\nfdsfsfsffhahhah哈哈哈发\nfdsfsfsffhahhah哈哈哈发\nfdsfsfsffhahhah哈哈哈发fdsfsfsffhahhah哈哈哈发\nfdsfsfsffhahhah哈哈哈发','','','2020-08-22 08:46:19.951465','2020-08-22 08:46:19.951703',0,'');

/*!40000 ALTER TABLE `ticket_ticketcustomfield` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table ticket_ticketflowlog
# ------------------------------------------------------------

DROP TABLE IF EXISTS `ticket_ticketflowlog`;

CREATE TABLE `ticket_ticketflowlog` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ticket_id` int(11) NOT NULL,
  `transition_id` int(11) NOT NULL,
  `suggestion` varchar(10000) NOT NULL,
  `participant_type_id` int(11) NOT NULL,
  `participant` varchar(50) NOT NULL,
  `state_id` int(11) NOT NULL,
  `ticket_data` longtext NOT NULL,
  `creator` varchar(50) NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `intervene_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_ticket_id` (`ticket_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `ticket_ticketflowlog` WRITE;
/*!40000 ALTER TABLE `ticket_ticketflowlog` DISABLE KEYS */;

INSERT INTO `ticket_ticketflowlog` (`id`, `ticket_id`, `transition_id`, `suggestion`, `participant_type_id`, `participant`, `state_id`, `ticket_data`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `intervene_type_id`)
VALUES
	(9,13,1,'',1,'lilei',1,'','admin','2018-05-13 21:53:15.820550','2018-05-13 21:53:15.820610',0,0),
	(10,14,2,'',1,'lilei',1,'','admin','2018-05-13 22:24:42.021711','2018-05-13 22:24:42.021792',0,0),
	(11,15,2,'',1,'lilei',1,'','admin','2018-05-13 22:28:21.686709','2018-05-13 22:28:21.686769',0,0),
	(12,16,1,'',1,'lilei',1,'','admin','2018-05-13 22:34:12.744844','2018-05-13 22:34:12.744912',0,0),
	(13,14,14,'保存草稿',1,'lilei',2,'','lilei','2018-05-13 22:59:06.743524','2018-05-13 22:59:06.743634',0,0),
	(14,14,14,'保存草稿',1,'lilei',2,'','lilei','2018-05-13 23:00:44.421329','2018-05-13 23:00:44.421396',0,0),
	(15,14,14,'保存草稿',1,'lilei',2,'','lilei','2018-05-13 23:04:40.758014','2018-05-13 23:04:40.758125',0,0),
	(16,14,14,'保存草稿',1,'lilei',2,'','lilei','2018-05-13 23:07:21.279315','2018-05-13 23:07:21.280068',0,0),
	(17,14,14,'保存草稿',1,'lilei',2,'','lilei','2018-05-13 23:10:19.742789','2018-05-13 23:10:19.742861',0,0),
	(18,14,14,'保存草稿',1,'lilei',2,'','lilei','2018-05-13 23:52:21.760281','2018-05-13 23:52:21.760339',0,0),
	(19,14,14,'保存草稿',1,'lilei',2,'','lilei','2018-05-14 00:01:54.824910','2018-05-14 00:01:54.824974',0,0),
	(20,14,14,'保存草稿',1,'lilei',2,'','lilei','2018-05-14 00:02:45.942264','2018-05-14 00:02:45.942325',0,0),
	(21,14,14,'保存草稿',1,'lilei',2,'','lilei','2018-05-14 00:12:18.293208','2018-05-14 00:12:18.293269',0,0),
	(22,14,14,'保存草稿',1,'lilei',2,'','lilei','2018-05-14 00:15:43.074352','2018-05-14 00:15:43.074635',0,0),
	(23,14,14,'保存草稿',1,'lilei',2,'','lilei','2018-05-14 00:21:56.019252','2018-05-14 00:21:56.019666',0,0),
	(24,14,14,'保存草稿',1,'lilei',2,'','lilei','2018-05-14 00:24:11.381536','2018-05-14 00:24:11.381609',0,0),
	(25,14,14,'保存草稿',1,'lilei',2,'','lilei','2018-05-14 06:55:24.437483','2018-05-14 06:55:24.437546',0,0),
	(26,15,0,'转交工单',1,'lilei',2,'','lilei','2018-05-14 06:56:26.664730','2018-05-14 06:56:26.664802',0,0),
	(27,15,0,'转交工单',1,'zhangsan',2,'','zhangsan','2018-05-14 06:56:52.101637','2018-05-14 06:56:52.101705',0,0),
	(28,15,14,'保存草稿',1,'lilei',2,'','lilei','2018-05-14 06:59:33.505946','2018-05-14 06:59:33.506019',0,0),
	(29,15,13,'保存草稿',1,'lilei',2,'','lilei','2018-05-14 07:00:03.655105','2018-05-14 07:00:03.655196',0,0),
	(30,15,0,'强制修改工单状态',1,'lilei',3,'','admin','2018-05-14 07:07:39.586383','2018-05-14 07:07:39.586456',0,0),
	(31,14,0,'加签工单',1,'lilei',2,'','lilei','2018-05-15 06:46:11.225083','2018-05-15 06:46:11.225146',0,0),
	(32,17,7,'',1,'lilei',6,'','admin','2018-05-15 07:16:38.332521','2018-05-15 07:16:38.332680',0,0),
	(33,17,8,'同意申请',1,'lilei',7,'','lilei','2018-05-15 07:20:40.816765','2018-05-15 07:20:40.816925',0,0),
	(34,18,7,'',1,'lilei',6,'','admin','2018-05-15 07:37:28.012487','2018-05-15 07:37:28.012548',0,0),
	(35,18,8,'同意申请',1,'lilei',7,'','lilei','2018-05-15 07:37:37.111956','2018-05-15 07:37:37.112027',0,0),
	(36,17,0,'接单处理',1,'guiji',8,'','guiji','2018-05-16 06:42:00.998562','2018-05-16 06:42:00.998625',0,0),
	(37,17,9,'同意',1,'guiji',8,'','guiji','2018-05-16 06:49:55.948811','2018-05-16 06:49:55.948905',0,0),
	(38,17,0,'接单处理',1,'guiji',8,'','guiji','2018-05-16 06:57:31.802266','2018-05-16 06:57:31.802360',0,0),
	(39,17,9,'同意',1,'guiji',8,'','guiji','2018-05-16 06:57:36.347563','2018-05-16 06:57:36.347634',0,0),
	(40,17,9,'同意',1,'guiji',8,'','guiji','2018-05-16 06:58:41.660593','2018-05-16 06:58:41.660701',0,0),
	(41,17,9,'同意',1,'guiji',8,'','guiji','2018-05-16 07:01:53.888622','2018-05-16 07:01:53.888689',0,0),
	(42,17,10,'False\n',6,'demo_script.py',9,'','loonrobot','2018-05-16 07:01:54.040851','2018-05-16 07:01:54.041150',0,0),
	(43,17,9,'同意',1,'guiji',8,'','guiji','2018-05-16 07:03:34.673960','2018-05-16 07:03:34.674037',0,0),
	(44,17,10,'False\n',6,'demo_script.py',9,'','loonrobot','2018-05-16 07:03:34.846610','2018-05-16 07:03:34.847216',0,0),
	(45,17,9,'同意',1,'guiji',8,'','guiji','2018-05-16 07:04:45.745455','2018-05-16 07:04:45.745521',0,0),
	(46,17,10,'False\n',6,'demo_script.py',9,'','loonrobot','2018-05-16 07:04:45.955902','2018-05-16 07:04:45.956166',0,0),
	(47,17,9,'同意',1,'guiji',8,'','guiji','2018-05-16 07:31:29.378033','2018-05-16 07:31:29.378090',0,0),
	(48,17,10,'lilei\n',6,'demo_script.py',9,'','loonrobot','2018-05-16 07:31:29.552179','2018-05-16 07:31:29.552446',0,0),
	(49,17,9,'同意',1,'guiji',8,'','guiji','2018-05-16 23:21:00.251306','2018-05-16 23:21:00.251363',0,0),
	(50,17,10,'lilei\n',6,'demo_script.py',9,'','loonrobot','2018-05-16 23:21:00.578354','2018-05-16 23:21:00.578555',0,0),
	(51,17,9,'同意',1,'guiji',8,'','guiji','2018-05-16 23:24:03.606092','2018-05-16 23:24:03.606156',0,0),
	(52,17,10,'lilei\n',6,'demo_script.py',9,'','loonrobot','2018-05-16 23:24:03.779136','2018-05-16 23:24:03.779504',0,0),
	(53,17,9,'同意',1,'guiji',8,'','guiji','2018-05-16 23:24:44.286319','2018-05-16 23:24:44.286429',0,0),
	(54,17,10,'lilei\n',6,'demo_script.py',9,'','loonrobot','2018-05-16 23:24:44.338829','2018-05-16 23:24:44.339101',0,0),
	(55,17,9,'同意',1,'guiji',8,'','guiji','2018-05-16 23:33:26.619543','2018-05-16 23:33:26.619613',0,0),
	(56,17,10,'lilei\n',6,'demo_script.py',9,'','loonrobot','2018-05-16 23:33:26.803850','2018-05-16 23:33:26.804073',0,0),
	(57,17,0,'请处理',1,'lilei',10,'','lilei','2018-05-17 06:45:58.830078','2018-05-17 06:45:58.830167',0,1),
	(58,17,0,'请协助处理',1,'zhangsan',10,'','zhangsan','2018-05-17 06:47:46.380983','2018-05-17 06:47:46.381055',0,2),
	(59,19,1,'',1,'admin',1,'{\"leave_days\": \"2\", \"leave_proxy\": \"admin\", \"title\": \"testt\", \"in_add_node\": false, \"is_deleted\": false, \"gmt_modified\": \"2018-10-19 00:08:40.380672\", \"add_node_man\": \"\", \"sn\": \"loonflow_201810190001\", \"leave_type\": \"2\", \"gmt_created\": \"2018-10-19 00:08:40.371908\", \"parent_ticket_id\": 0, \"leave_reason\": \"<p>teste</p>\", \"leave_start\": \"2018-10-20 09:00:00\", \"participant_type_id\": 1, \"state_id\": 3, \"workflow_id\": 1, \"parent_ticket_state_id\": 0, \"relation\": \"admin\", \"participant\": \"admin\", \"leave_end\": \"2018-10-21 18:00:00\", \"creator\": \"admin\"}','admin','2018-10-19 00:08:40.466104','2018-10-19 00:08:40.466128',0,0),
	(60,20,1,'',1,'admin',1,'{\"leave_reason\": \"<p>dfsf</p>\", \"sn\": \"loonflow_201810190002\", \"add_node_man\": \"\", \"leave_days\": \"2\", \"participant\": \"admin\", \"title\": \"teste\", \"gmt_modified\": \"2018-10-19 00:38:41.359283\", \"workflow_id\": 1, \"creator\": \"admin\", \"leave_start\": \"2018-10-19 12:00:00\", \"is_deleted\": false, \"parent_ticket_id\": 0, \"relation\": \"admin\", \"leave_type\": \"2\", \"leave_end\": \"2018-10-20 12:00:00\", \"state_id\": 3, \"in_add_node\": false, \"leave_proxy\": \"admin\", \"participant_type_id\": 1, \"gmt_created\": \"2018-10-19 00:38:41.354008\", \"parent_ticket_state_id\": 0}','admin','2018-10-19 00:38:41.428448','2018-10-19 00:38:41.428473',0,0),
	(61,20,3,'fdsfsf',1,'admin',3,'{\"leave_reason\": \"<p>dfsf</p>\", \"sn\": \"loonflow_201810190002\", \"add_node_man\": \"\", \"leave_days\": \"2\", \"participant\": \"jack\", \"title\": \"teste\", \"gmt_modified\": \"2018-10-19 00:38:53.872124\", \"workflow_id\": 1, \"creator\": \"admin\", \"leave_start\": \"2018-10-19 12:00:00\", \"is_deleted\": false, \"parent_ticket_id\": 0, \"relation\": \"jack,admin\", \"leave_type\": \"2\", \"leave_end\": \"2018-10-20 12:00:00\", \"state_id\": 4, \"in_add_node\": false, \"leave_proxy\": \"admin\", \"participant_type_id\": 1, \"gmt_created\": \"2018-10-19 00:38:41.354008\", \"parent_ticket_state_id\": 0}','admin','2018-10-19 00:38:53.942394','2018-10-19 00:38:53.942431',0,0),
	(62,21,15,'',1,'admin',13,'{\"gmt_modified\": \"2018-10-21 11:14:37.663604\", \"gmt_created\": \"2018-10-21 11:14:37.656067\", \"creator\": \"admin\", \"parent_ticket_state_id\": 0, \"participant\": \"loonrobot\", \"workflow_id\": 3, \"parent_ticket_id\": 0, \"in_add_node\": false, \"project_qas\": \"admin\", \"participant_type_id\": 1, \"relation\": \"loonrobot,admin\", \"project_devs\": \"admin\", \"state_id\": 14, \"is_deleted\": false, \"sn\": \"loonflow_201810210001\", \"add_node_man\": \"\", \"title\": \"\", \"project_code\": \"prj001\"}','admin','2018-10-21 11:14:37.775029','2018-10-21 11:14:37.775227',0,0),
	(63,19,5,'111',1,'jack',4,'{\"leave_end\": \"2018-10-21 18:00:00\", \"parent_ticket_state_id\": 0, \"participant_type_id\": 0, \"title\": \"testt\", \"sn\": \"loonflow_201810190001\", \"leave_reason\": \"<p>teste</p>\", \"gmt_modified\": \"2018-10-21 20:06:57.527067\", \"participant\": \"\", \"parent_ticket_id\": 0, \"workflow_id\": 1, \"relation\": \"jack,admin\", \"is_deleted\": false, \"creator\": \"admin\", \"leave_type\": \"2\", \"add_node_man\": \"\", \"leave_start\": \"2018-10-20 09:00:00\", \"in_add_node\": false, \"state_id\": 5, \"leave_proxy\": \"admin\", \"leave_days\": \"2\", \"gmt_created\": \"2018-10-19 00:08:40.371908\"}','jack','2018-10-21 20:06:57.579230','2018-10-21 20:06:57.579267',0,0),
	(64,22,1,'',1,'jack',1,'{\"is_deleted\": false, \"parent_ticket_state_id\": 0, \"leave_proxy\": \"admin\", \"leave_end\": \"2018-10-23 12:00:00\", \"leave_start\": \"2018-10-22 12:00:00\", \"creator\": \"jack\", \"participant_type_id\": 1, \"in_add_node\": false, \"parent_ticket_id\": 0, \"relation\": \"jack\", \"title\": \"tttttt\", \"leave_days\": \"1\", \"sn\": \"loonflowhhh_201810220001\", \"participant\": \"jack\", \"leave_type\": \"3\", \"add_node_man\": \"\", \"gmt_modified\": \"2018-10-22 07:12:16.455740\", \"leave_reason\": \"<p>ddd</p>\", \"state_id\": 3, \"workflow_id\": 1, \"gmt_created\": \"2018-10-22 07:12:16.451086\"}','admin','2018-10-22 07:12:16.542137','2018-10-22 07:12:16.542163',0,0),
	(65,23,1,'',1,'jack',1,'{\"is_deleted\": false, \"parent_ticket_state_id\": 0, \"leave_proxy\": \"admin\", \"leave_end\": \"2018-10-24 12:00:00\", \"leave_start\": \"2018-10-22 12:00:00\", \"creator\": \"jack\", \"participant_type_id\": 1, \"in_add_node\": false, \"parent_ticket_id\": 0, \"relation\": \"jack\", \"title\": \"ttttest\", \"leave_days\": \"2\", \"sn\": \"loonflow_201810220002\", \"participant\": \"jack\", \"leave_type\": \"3\", \"add_node_man\": \"\", \"gmt_modified\": \"2018-10-22 08:05:37.192994\", \"leave_reason\": \"<p>te</p>\", \"state_id\": 3, \"workflow_id\": 1, \"gmt_created\": \"2018-10-22 08:05:37.187794\"}','admin','2018-10-22 08:05:37.270333','2018-10-22 08:05:37.270359',0,0),
	(66,24,1,'',1,'admin',1,'{\"relation\": \"admin\", \"leave_reason\": \"<p>11</p>\", \"sn\": \"loonflow_201811270001\", \"parent_ticket_id\": 0, \"participant_type_id\": 1, \"title\": \"tttt\", \"leave_proxy\": \"admin\", \"parent_ticket_state_id\": 0, \"gmt_modified\": \"2018-11-27 07:09:06.326441\", \"add_node_man\": \"\", \"is_deleted\": false, \"creator\": \"admin\", \"state_id\": 3, \"leave_type\": \"1\", \"workflow_id\": 1, \"participant\": \"admin\", \"in_add_node\": false, \"leave_start\": \"2018-11-27 12:00:00\", \"leave_end\": \"2018-11-28 12:00:00\", \"gmt_created\": \"2018-11-27 07:09:06.308678\", \"leave_days\": \"1\"}','admin','2018-11-27 07:09:06.409476','2018-11-27 07:09:06.409515',0,0),
	(67,25,1,'',1,'admin',1,'{\"relation\": \"guiji,admin,lilei,zhangsan\", \"leave_reason\": \"<p>111</p>\", \"sn\": \"loonflow_201811270002\", \"parent_ticket_id\": 0, \"participant_type_id\": 4, \"title\": \"ttt21\", \"leave_proxy\": \"admin\", \"parent_ticket_state_id\": 0, \"gmt_modified\": \"2018-11-27 07:12:27.929123\", \"add_node_man\": \"\", \"is_deleted\": false, \"creator\": \"admin\", \"state_id\": 3, \"leave_type\": \"1\", \"workflow_id\": 1, \"participant\": \"2\", \"in_add_node\": false, \"leave_start\": \"2018-11-27 12:00:00\", \"leave_end\": \"2018-11-28 12:00:00\", \"gmt_created\": \"2018-11-27 07:12:27.917523\", \"leave_days\": \"1\"}','admin','2018-11-27 07:12:28.003629','2018-11-27 07:12:28.003659',0,0),
	(68,26,1,'',1,'admin',1,'{\"leave_start\": \"2018-11-27 12:00:00\", \"leave_reason\": \"<p>111</p>\", \"creator\": \"admin\", \"participant\": \"2\", \"relation\": \"lilei,admin,zhangsan,guiji\", \"leave_days\": \"1\", \"is_deleted\": false, \"parent_ticket_state_id\": 0, \"leave_end\": \"2018-11-28 12:00:00\", \"workflow_id\": 1, \"leave_type\": \"1\", \"in_add_node\": false, \"parent_ticket_id\": 0, \"sn\": \"loonflow_201811270003\", \"leave_proxy\": \"admin\", \"add_node_man\": \"\", \"title\": \"tttt\", \"participant_type_id\": 4, \"gmt_created\": \"2018-11-27 07:14:06.360734\", \"state_id\": 3, \"gmt_modified\": \"2018-11-27 07:14:06.377165\"}','admin','2018-11-27 07:14:06.525209','2018-11-27 07:14:06.525258',0,0),
	(69,27,1,'',1,'admin',1,'{\"parent_ticket_state_id\": 0, \"gmt_modified\": \"2018-11-27 07:20:16.212155\", \"gmt_created\": \"2018-11-27 07:20:16.194872\", \"relation\": \"admin,zhangsan,lilei,guiji\", \"workflow_id\": 1, \"state_id\": 3, \"in_add_node\": false, \"sn\": \"loonflow_201811270004\", \"leave_end\": \"2018-11-28 12:00:00\", \"title\": \"11111\", \"leave_proxy\": \"admin\", \"leave_reason\": \"<p>111</p>\", \"participant\": \"2\", \"creator\": \"admin\", \"leave_days\": \"1\", \"add_node_man\": \"\", \"is_deleted\": false, \"parent_ticket_id\": 0, \"leave_type\": \"1\", \"leave_start\": \"2018-11-27 12:00:00\", \"participant_type_id\": 4}','admin','2018-11-27 07:20:16.498933','2018-11-27 07:20:16.498980',0,0),
	(70,28,1,'',1,'admin',1,'{\"parent_ticket_state_id\": 0, \"gmt_modified\": \"2018-11-27 07:21:00.015804\", \"gmt_created\": \"2018-11-27 07:21:00.015751\", \"relation\": \"admin\", \"workflow_id\": 1, \"state_id\": 3, \"in_add_node\": false, \"sn\": \"loonflow_201811270005\", \"leave_end\": \"2018-11-28 12:00:00\", \"title\": \"tttt\", \"leave_proxy\": \"admin\", \"leave_reason\": \"<p>1111</p>\", \"participant\": \"[\'zhangsan\']\", \"creator\": \"admin\", \"leave_days\": \"1\", \"add_node_man\": \"\", \"is_deleted\": false, \"parent_ticket_id\": 0, \"leave_type\": \"1\", \"leave_start\": \"2018-11-27 12:00:00\", \"participant_type_id\": 1}','admin','2018-11-27 07:21:00.213080','2018-11-27 07:21:00.213125',0,0),
	(71,29,1,'',1,'admin',1,'{\"leave_end\": \"2018-11-28 12:00:00\", \"in_add_node\": false, \"add_node_man\": \"\", \"participant\": \"zhangsan\", \"leave_days\": \"1\", \"leave_start\": \"2018-11-27 12:00:00\", \"state_id\": 3, \"gmt_modified\": \"2018-11-27 07:23:04.031786\", \"title\": \"111122\", \"workflow_id\": 1, \"parent_ticket_id\": 0, \"gmt_created\": \"2018-11-27 07:23:04.023879\", \"relation\": \"admin,zhangsan\", \"leave_type\": \"1\", \"is_deleted\": false, \"parent_ticket_state_id\": 0, \"leave_reason\": \"<p>11</p>\", \"participant_type_id\": 1, \"leave_proxy\": \"admin\", \"creator\": \"admin\", \"sn\": \"loonflow_201811270006\"}','admin','2018-11-27 07:23:04.196933','2018-11-27 07:23:04.196977',0,0),
	(72,30,1,'',1,'admin',1,'{\"parent_ticket_id\": 0, \"leave_reason\": \"<p>11</p>\", \"leave_type\": \"1\", \"leave_proxy\": \"admin\", \"title\": \"111ww\", \"gmt_modified\": \"2018-11-27 07:23:47.926368\", \"leave_days\": \"1\", \"parent_ticket_state_id\": 0, \"workflow_id\": 1, \"participant_type_id\": 1, \"leave_start\": \"2018-11-27 12:00:00\", \"gmt_created\": \"2018-11-27 07:23:47.920099\", \"in_add_node\": false, \"add_node_man\": \"\", \"participant\": \"zhangsan\", \"is_deleted\": false, \"sn\": \"loonflow_201811270007\", \"leave_end\": \"2018-11-28 12:00:00\", \"relation\": \"zhangsan,admin\", \"state_id\": 3, \"creator\": \"admin\"}','admin','2018-11-27 07:23:48.000430','2018-11-27 07:23:48.000457',0,0),
	(73,31,1,'',1,'admin',1,'{\"parent_ticket_id\": 0, \"leave_reason\": \"<p>sdf</p>\", \"leave_type\": \"1\", \"leave_proxy\": \"admin\", \"title\": \"122131\", \"gmt_modified\": \"2018-11-27 07:24:07.533129\", \"leave_days\": \"1\", \"parent_ticket_state_id\": 0, \"workflow_id\": 1, \"participant_type_id\": 1, \"leave_start\": \"2018-11-27 12:00:00\", \"gmt_created\": \"2018-11-27 07:24:07.528102\", \"in_add_node\": false, \"add_node_man\": \"\", \"participant\": \"zhangsan\", \"is_deleted\": false, \"sn\": \"loonflow_201811270008\", \"leave_end\": \"2018-11-28 12:00:00\", \"relation\": \"zhangsan,admin\", \"state_id\": 3, \"creator\": \"admin\"}','admin','2018-11-27 07:24:07.615996','2018-11-27 07:24:07.616022',0,0),
	(74,32,1,'',1,'admin',1,'{\"parent_ticket_id\": 0, \"leave_reason\": \"<p>1111</p>\", \"leave_type\": \"1\", \"leave_proxy\": \"admin\", \"title\": \"fdfsfds\", \"gmt_modified\": \"2018-11-27 07:24:31.254020\", \"leave_days\": \"1\", \"parent_ticket_state_id\": 0, \"workflow_id\": 1, \"participant_type_id\": 1, \"leave_start\": \"2018-11-27 12:00:00\", \"gmt_created\": \"2018-11-27 07:24:31.249309\", \"in_add_node\": false, \"add_node_man\": \"\", \"participant\": \"guiji\", \"is_deleted\": false, \"sn\": \"loonflow_201811270009\", \"leave_end\": \"2018-11-28 12:00:00\", \"relation\": \"admin,guiji\", \"state_id\": 3, \"creator\": \"admin\"}','admin','2018-11-27 07:24:31.325195','2018-11-27 07:24:31.325223',0,0),
	(75,33,1,'',1,'admin',1,'{\"creator\": \"admin\", \"leave_days\": \"1\", \"relation\": \"lilei,admin\", \"parent_ticket_id\": 0, \"add_node_man\": \"\", \"leave_type\": \"1\", \"leave_reason\": \"<p>111</p>\", \"leave_start\": \"2018-11-27 12:00:00\", \"is_deleted\": false, \"state_id\": 3, \"participant\": \"lilei\", \"participant_type_id\": 1, \"leave_proxy\": \"admin\", \"leave_end\": \"2018-11-28 12:00:00\", \"gmt_modified\": \"2018-11-27 07:27:39.233032\", \"parent_ticket_state_id\": 0, \"workflow_id\": 1, \"sn\": \"loonflow_201811270010\", \"gmt_created\": \"2018-11-27 07:27:39.226722\", \"in_add_node\": false, \"title\": \"ttt1\"}','admin','2018-11-27 07:27:39.310221','2018-11-27 07:27:39.310259',0,0),
	(76,34,1,'',1,'admin',1,'{\"is_rejected\": false, \"state_id\": 3, \"sn\": \"ops_201911240001\", \"in_add_node\": false, \"gmt_modified\": \"2019-11-24 10:23:07\", \"participant_type_id\": 6, \"leave_days\": \"1\", \"gmt_created\": \"2019-11-24 10:23:07\", \"is_deleted\": false, \"leave_proxy\": \"admin\", \"leave_end\": \"2019-11-27 00:00:00\", \"title\": \"stestet\", \"leave_start\": \"2019-11-26 00:00:00\", \"creator\": \"admin\", \"parent_ticket_state_id\": 0, \"leave_reason\": \"<p>testest<br/></p>\", \"relation\": \"admin\", \"participant\": \"1\", \"id\": 34, \"script_run_last_result\": true, \"parent_ticket_id\": 0, \"leave_type\": \"1\", \"add_node_man\": \"\", \"multi_all_person\": \"{}\", \"is_end\": false, \"workflow_id\": 1}','admin','2019-11-24 10:23:07.370718','2019-11-24 10:23:07.370766',0,0),
	(77,35,1,'',1,'admin',1,'{\"add_node_man\": \"\", \"multi_all_person\": \"{}\", \"leave_type\": \"1\", \"relation\": \"admin\", \"state_id\": 3, \"leave_end\": \"2019-11-27 00:00:00\", \"leave_days\": \"1\", \"participant_type_id\": 6, \"in_add_node\": false, \"title\": \"stestet\", \"gmt_modified\": \"2019-11-24 10:24:31\", \"id\": 35, \"parent_ticket_state_id\": 0, \"sn\": \"ops_201911240002\", \"is_end\": false, \"is_deleted\": false, \"participant\": \"1\", \"workflow_id\": 1, \"is_rejected\": false, \"leave_start\": \"2019-11-26 00:00:00\", \"leave_proxy\": \"admin\", \"creator\": \"admin\", \"script_run_last_result\": true, \"leave_reason\": \"<p>testest<br/></p>\", \"gmt_created\": \"2019-11-24 10:24:31\", \"parent_ticket_id\": 0}','admin','2019-11-24 10:24:31.830258','2019-11-24 10:24:31.830309',0,0),
	(78,35,3,'Missing parentheses in call to \'print\' (<string>, line 1)',6,'脚本:(id:1, name:创建虚拟机)',3,'','loonrobot','2020-01-16 22:22:40.114676','2020-01-16 22:22:40.114927',0,0),
	(79,35,0,'testt',1,'admin',3,'{\"id\": 35, \"creator\": \"admin\", \"gmt_created\": \"2019-11-24 10:24:31\", \"gmt_modified\": \"2020-03-29 09:47:04\", \"is_deleted\": false, \"title\": \"stestet\", \"workflow_id\": 1, \"sn\": \"ops_201911240002\", \"state_id\": 4, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"jack\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": false, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2019-11-26 00:00:00\", \"leave_end\": \"2019-11-27 00:00:00\", \"leave_days\": \"1\", \"leave_proxy\": \"admin\", \"leave_type\": \"1\", \"leave_reason\": \"<p>testest<br/></p>\"}','admin','2020-03-29 09:47:04.414407','2020-03-29 09:47:04.414431',0,8),
	(80,35,0,'tee',1,'admin',4,'{\"id\": 35, \"creator\": \"admin\", \"gmt_created\": \"2019-11-24 10:24:31\", \"gmt_modified\": \"2020-03-29 09:47:26\", \"is_deleted\": false, \"title\": \"stestet\", \"workflow_id\": 1, \"sn\": \"ops_201911240002\", \"state_id\": 4, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"lilei\", \"relation\": \"admin,lilei\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": false, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2019-11-26 00:00:00\", \"leave_end\": \"2019-11-27 00:00:00\", \"leave_days\": \"1\", \"leave_proxy\": \"admin\", \"leave_type\": \"1\", \"leave_reason\": \"<p>testest<br/></p>\"}','admin','2020-03-29 09:47:26.556723','2020-03-29 09:47:26.556747',0,1),
	(81,35,0,'强制关闭工单:ts',1,'admin',5,'{\"id\": 35, \"creator\": \"admin\", \"gmt_created\": \"2019-11-24 10:24:31\", \"gmt_modified\": \"2020-03-29 09:47:26\", \"is_deleted\": false, \"title\": \"stestet\", \"workflow_id\": 1, \"sn\": \"ops_201911240002\", \"state_id\": 4, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"lilei\", \"relation\": \"admin,lilei\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": false, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2019-11-26 00:00:00\", \"leave_end\": \"2019-11-27 00:00:00\", \"leave_days\": \"1\", \"leave_proxy\": \"admin\", \"leave_type\": \"1\", \"leave_reason\": \"<p>testest<br/></p>\"}','admin','2020-03-29 09:47:33.838219','2020-03-29 09:47:33.838250',0,7),
	(82,36,7,'',1,'admin',6,'{\"id\": 36, \"creator\": \"admin\", \"gmt_created\": \"2020-04-11 10:40:30\", \"gmt_modified\": \"2020-04-11 10:40:30\", \"is_deleted\": false, \"title\": \"fdfdsf\", \"workflow_id\": 2, \"sn\": \"ops1_bd_202004110004\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"admin\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"vpn_reason\": \"<p>sfdsf</p>\"}','admin','2020-04-11 10:40:31.070230','2020-04-11 10:40:31.070508',0,0),
	(83,37,7,'',1,'admin',6,'{\"id\": 37, \"creator\": \"admin\", \"gmt_created\": \"2020-05-01 09:19:28\", \"gmt_modified\": \"2020-05-01 09:19:28\", \"is_deleted\": false, \"title\": \"test\", \"workflow_id\": 2, \"sn\": \"ops122222212_202005010001\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"admin\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"vpn_reason\": \"<p>testst</p>\"}','admin','2020-05-01 09:19:28.723074','2020-05-01 09:19:28.723096',0,0),
	(84,37,0,'强制关闭工单:test',1,'admin',11,'{\"id\": 37, \"creator\": \"admin\", \"gmt_created\": \"2020-05-01 09:19:28\", \"gmt_modified\": \"2020-05-01 09:19:28\", \"is_deleted\": false, \"title\": \"test\", \"workflow_id\": 2, \"sn\": \"ops122222212_202005010001\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"admin\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"vpn_reason\": \"<p>testst</p>\"}','admin','2020-05-01 09:19:48.333223','2020-05-01 09:19:48.333253',0,7),
	(85,38,7,'',1,'admin',6,'{\"id\": 38, \"creator\": \"admin\", \"gmt_created\": \"2020-05-01 09:21:56\", \"gmt_modified\": \"2020-05-01 09:21:56\", \"is_deleted\": false, \"title\": \"ttte\", \"workflow_id\": 2, \"sn\": \"ops122222212_202005010002\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"admin\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"vpn_reason\": \"<p>sssss</p>\"}','admin','2020-05-01 09:21:56.866220','2020-05-01 09:21:56.866256',0,0),
	(86,38,0,'强制关闭工单:sdfsfs',1,'admin',11,'{\"id\": 38, \"creator\": \"admin\", \"gmt_created\": \"2020-05-01 09:21:56\", \"gmt_modified\": \"2020-05-01 09:21:56\", \"is_deleted\": false, \"title\": \"ttte\", \"workflow_id\": 2, \"sn\": \"ops122222212_202005010002\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"admin\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"vpn_reason\": \"<p>sssss</p>\"}','admin','2020-05-01 09:22:31.753568','2020-05-01 09:22:31.753597',0,7),
	(87,39,1,'',1,'admin',1,'{\"id\": 39, \"creator\": \"admin\", \"gmt_created\": \"2020-05-07 22:42:17\", \"gmt_modified\": \"2020-05-07 22:42:17\", \"is_deleted\": false, \"title\": \"testest\", \"workflow_id\": 1, \"sn\": \"ops122222212_202005070001\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"zhangsan,lisi\", \"relation\": \"admin,zhangsan,lisi\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"zhangsan\\\": {}, \\\"lisi\\\": {}}\", \"leave_start\": \"2020-05-08 00:00:00\", \"leave_end\": \"2020-05-08 00:00:00\", \"leave_proxy\": \"lilian\", \"leave_type\": \"2\", \"leave_reason\": \"<p>testse</p>\"}','admin','2020-05-07 22:42:17.314732','2020-05-07 22:42:17.314757',0,0),
	(88,40,7,'',1,'zhangsan',6,'{\"id\": 40, \"creator\": \"zhangsan\", \"gmt_created\": \"2020-05-07 22:54:58\", \"gmt_modified\": \"2020-05-07 22:54:58\", \"is_deleted\": false, \"title\": \"test\", \"workflow_id\": 2, \"sn\": \"ops122222212_202005070002\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"zhangsan,admin\", \"relation\": \"admin,zhangsan\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"zhangsan\\\": {}, \\\"admin\\\": {}}\", \"vpn_reason\": \"<p>test</p>\"}','zhangsan','2020-05-07 22:54:58.888888','2020-05-07 22:54:58.888926',0,0),
	(89,40,8,'同意',1,'zhangsan',7,'\"{\\\"id\\\": 40, \\\"creator\\\": \\\"zhangsan\\\", \\\"gmt_created\\\": \\\"2020-05-07 22:54:58\\\", \\\"gmt_modified\\\": \\\"2020-05-07 22:55:09\\\", \\\"is_deleted\\\": false, \\\"title\\\": \\\"test\\\", \\\"workflow_id\\\": 2, \\\"sn\\\": \\\"ops122222212_202005070002\\\", \\\"state_id\\\": 8, \\\"parent_ticket_id\\\": 0, \\\"parent_ticket_state_id\\\": 0, \\\"participant_type_id\\\": 2, \\\"participant\\\": \\\"admin\\\", \\\"relation\\\": \\\"admin,zhangsan\\\", \\\"in_add_node\\\": false, \\\"add_node_man\\\": \\\"\\\", \\\"script_run_last_result\\\": true, \\\"act_state_id\\\": 1, \\\"multi_all_person\\\": \\\"{\\\\\\\"zhangsan\\\\\\\": {}, \\\\\\\"admin\\\\\\\": {}}\\\", \\\"vpn_reason\\\": \\\"<p>test</p>\\\"}\"','zhangsan','2020-05-07 22:55:09.151811','2020-05-07 22:55:09.151836',0,0),
	(90,41,7,'',1,'admin',6,'{\"id\": 41, \"creator\": \"admin\", \"gmt_created\": \"2020-05-17 17:31:54\", \"gmt_modified\": \"2020-05-17 17:31:54\", \"is_deleted\": false, \"title\": \"test\", \"workflow_id\": 2, \"sn\": \"ops122222212_202005170001\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"zhangsan,admin\", \"relation\": \"zhangsan,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"zhangsan\\\": {}, \\\"admin\\\": {}}\", \"vpn_reason\": \"<p>test</p>\"}','admin','2020-05-17 17:31:54.259314','2020-05-17 17:31:54.259334',0,0),
	(91,41,8,'同意',1,'admin',7,'\"{\\\"id\\\": 41, \\\"creator\\\": \\\"admin\\\", \\\"gmt_created\\\": \\\"2020-05-17 17:31:54\\\", \\\"gmt_modified\\\": \\\"2020-05-17 17:33:49\\\", \\\"is_deleted\\\": false, \\\"title\\\": \\\"test\\\", \\\"workflow_id\\\": 2, \\\"sn\\\": \\\"ops122222212_202005170001\\\", \\\"state_id\\\": 7, \\\"parent_ticket_id\\\": 0, \\\"parent_ticket_state_id\\\": 0, \\\"participant_type_id\\\": 2, \\\"participant\\\": \\\"zhangsan\\\", \\\"relation\\\": \\\"zhangsan,admin\\\", \\\"in_add_node\\\": false, \\\"add_node_man\\\": \\\"\\\", \\\"script_run_last_result\\\": true, \\\"act_state_id\\\": 1, \\\"multi_all_person\\\": \\\"{\\\\\\\"zhangsan\\\\\\\": {}, \\\\\\\"admin\\\\\\\": {}}\\\", \\\"vpn_reason\\\": \\\"<p>test</p>\\\"}\"','admin','2020-05-17 17:33:49.927763','2020-05-17 17:33:49.927798',0,0),
	(92,41,8,'test',1,'zhangsan',7,'\"{\\\"id\\\": 41, \\\"creator\\\": \\\"admin\\\", \\\"gmt_created\\\": \\\"2020-05-17 17:31:54\\\", \\\"gmt_modified\\\": \\\"2020-05-17 17:38:51\\\", \\\"is_deleted\\\": false, \\\"title\\\": \\\"test\\\", \\\"workflow_id\\\": 2, \\\"sn\\\": \\\"ops122222212_202005170001\\\", \\\"state_id\\\": 7, \\\"parent_ticket_id\\\": 0, \\\"parent_ticket_state_id\\\": 0, \\\"participant_type_id\\\": 2, \\\"participant\\\": \\\"admin\\\", \\\"relation\\\": \\\"zhangsan,admin\\\", \\\"in_add_node\\\": false, \\\"add_node_man\\\": \\\"\\\", \\\"script_run_last_result\\\": true, \\\"act_state_id\\\": 1, \\\"multi_all_person\\\": \\\"{\\\\\\\"zhangsan\\\\\\\": {}, \\\\\\\"admin\\\\\\\": {}}\\\", \\\"vpn_reason\\\": \\\"<p>test</p>\\\"}\"','zhangsan','2020-05-17 17:38:51.153578','2020-05-17 17:38:51.153600',0,0),
	(93,42,7,'',1,'zhangsan',6,'{\"id\": 42, \"creator\": \"zhangsan\", \"gmt_created\": \"2020-05-17 17:44:45\", \"gmt_modified\": \"2020-05-17 17:44:45\", \"is_deleted\": false, \"title\": \"test111\", \"workflow_id\": 2, \"sn\": \"ops122222212_202005170002\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"zhangsan,admin\", \"relation\": \"zhangsan,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"zhangsan\\\": {}, \\\"admin\\\": {}}\", \"vpn_reason\": \"<p>1111<br/></p>\"}','zhangsan','2020-05-17 17:44:45.482217','2020-05-17 17:44:45.482238',0,0),
	(94,42,8,'12222',1,'zhangsan',7,'\"{\\\"id\\\": 42, \\\"creator\\\": \\\"zhangsan\\\", \\\"gmt_created\\\": \\\"2020-05-17 17:44:45\\\", \\\"gmt_modified\\\": \\\"2020-05-17 17:44:52\\\", \\\"is_deleted\\\": false, \\\"title\\\": \\\"test111\\\", \\\"workflow_id\\\": 2, \\\"sn\\\": \\\"ops122222212_202005170002\\\", \\\"state_id\\\": 7, \\\"parent_ticket_id\\\": 0, \\\"parent_ticket_state_id\\\": 0, \\\"participant_type_id\\\": 2, \\\"participant\\\": \\\"admin\\\", \\\"relation\\\": \\\"zhangsan,admin\\\", \\\"in_add_node\\\": false, \\\"add_node_man\\\": \\\"\\\", \\\"script_run_last_result\\\": true, \\\"act_state_id\\\": 1, \\\"multi_all_person\\\": \\\"{\\\\\\\"zhangsan\\\\\\\": {\\\\\\\"transition_id\\\\\\\": 8, \\\\\\\"transition_name\\\\\\\": \\\\\\\"\\\\\\\\u540c\\\\\\\\u610f\\\\\\\"}, \\\\\\\"admin\\\\\\\": {}}\\\", \\\"vpn_reason\\\": \\\"<p>1111<br/></p>\\\"}\"','zhangsan','2020-05-17 17:44:52.675300','2020-05-17 17:44:52.675336',0,0),
	(95,42,8,'同意',1,'admin',7,'\"{\\\"id\\\": 42, \\\"creator\\\": \\\"zhangsan\\\", \\\"gmt_created\\\": \\\"2020-05-17 17:44:45\\\", \\\"gmt_modified\\\": \\\"2020-05-17 17:45:34\\\", \\\"is_deleted\\\": false, \\\"title\\\": \\\"test111\\\", \\\"workflow_id\\\": 2, \\\"sn\\\": \\\"ops122222212_202005170002\\\", \\\"state_id\\\": 8, \\\"parent_ticket_id\\\": 0, \\\"parent_ticket_state_id\\\": 0, \\\"participant_type_id\\\": 3, \\\"participant\\\": \\\"3\\\", \\\"relation\\\": \\\"wangwu,zhangsan,guiji,admin\\\", \\\"in_add_node\\\": false, \\\"add_node_man\\\": \\\"\\\", \\\"script_run_last_result\\\": true, \\\"act_state_id\\\": 1, \\\"multi_all_person\\\": \\\"{}\\\", \\\"vpn_reason\\\": \\\"<p>1111<br/></p>\\\"}\"','admin','2020-05-17 17:45:34.529864','2020-05-17 17:45:34.529883',0,0),
	(96,43,7,'',1,'admin',6,'{\"id\": 43, \"creator\": \"admin\", \"gmt_created\": \"2020-05-18 23:18:15\", \"gmt_modified\": \"2020-05-18 23:18:15\", \"is_deleted\": false, \"title\": \"TEST\", \"workflow_id\": 2, \"sn\": \"ops122222212_202005180001\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"zhangsan,admin\", \"relation\": \"admin,zhangsan\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"zhangsan\\\": {}, \\\"admin\\\": {}}\", \"vpn_reason\": \"<p>TEST</p>\"}','admin','2020-05-18 23:18:15.575623','2020-05-18 23:18:15.575649',0,0),
	(97,43,8,'同意',1,'admin',7,'\"{\\\"id\\\": 43, \\\"creator\\\": \\\"admin\\\", \\\"gmt_created\\\": \\\"2020-05-18 23:18:15\\\", \\\"gmt_modified\\\": \\\"2020-05-18 23:18:30\\\", \\\"is_deleted\\\": false, \\\"title\\\": \\\"TEST\\\", \\\"workflow_id\\\": 2, \\\"sn\\\": \\\"ops122222212_202005180001\\\", \\\"state_id\\\": 7, \\\"parent_ticket_id\\\": 0, \\\"parent_ticket_state_id\\\": 0, \\\"participant_type_id\\\": 2, \\\"participant\\\": \\\"zhangsan\\\", \\\"relation\\\": \\\"admin,zhangsan\\\", \\\"in_add_node\\\": false, \\\"add_node_man\\\": \\\"\\\", \\\"script_run_last_result\\\": true, \\\"act_state_id\\\": 1, \\\"multi_all_person\\\": \\\"{\\\\\\\"zhangsan\\\\\\\": {}, \\\\\\\"admin\\\\\\\": {\\\\\\\"transition_id\\\\\\\": 8, \\\\\\\"transition_name\\\\\\\": \\\\\\\"\\\\\\\\u540c\\\\\\\\u610f\\\\\\\"}}\\\", \\\"vpn_reason\\\": \\\"<p>TEST</p>\\\"}\"','admin','2020-05-18 23:18:30.423578','2020-05-18 23:18:30.423601',0,0),
	(98,44,7,'',1,'admin',6,'{\"id\": 44, \"creator\": \"admin\", \"gmt_created\": \"2020-08-21 10:39:32\", \"gmt_modified\": \"2020-08-21 10:39:32\", \"is_deleted\": false, \"title\": \"dfdsf\", \"workflow_id\": 2, \"sn\": \"loonflow_202008210004\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"admin,zhangsan\", \"relation\": \"admin,zhangsan\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"admin\\\": {}, \\\"zhangsan\\\": {}}\", \"vpn_reason\": \"sdfdsfsdfs\"}','admin','2020-08-21 10:39:32.970241','2020-08-21 10:39:32.970403',0,0),
	(99,46,1,'',1,'admin',1,'{\"id\": 46, \"creator\": \"admin\", \"gmt_created\": \"2020-08-21 18:42:06\", \"gmt_modified\": \"2020-08-21 18:42:06\", \"is_deleted\": false, \"title\": \"\", \"workflow_id\": 1, \"sn\": \"loonflow_202008210006\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"lisi,zhangsan\", \"relation\": \"admin,lisi,zhangsan\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"lisi\\\": {}, \\\"zhangsan\\\": {}}\", \"leave_start\": \"2020-08-21 00:00:05\", \"leave_end\": \"2020-08-21 18:15:52\", \"leave_proxy\": \"None\", \"leave_type\": \"1\", \"leave_reason\": 111, \"bool_field\": true, \"date_filed\": \"None\", \"datetime_field\": \"None\", \"checkbox_field\": \"1\", \"multi_checkbox_field\": \"2,3\", \"select_field\": \"1\", \"multi_select_field\": \"1,2,3\", \"text_field\": \"dfs\", \"user_fleld\": \"fdsf\", \"multi_user_field\": \"fdsf\", \"attachment_field\": \"fdsfs\"}','admin','2020-08-21 18:42:08.466941','2020-08-21 18:42:08.467161',0,0),
	(100,47,7,'',1,'admin',6,'{\"id\": 47, \"creator\": \"admin\", \"gmt_created\": \"2020-08-22 08:46:19\", \"gmt_modified\": \"2020-08-22 08:46:19\", \"is_deleted\": false, \"title\": \"fdfafa \", \"workflow_id\": 2, \"sn\": \"loonflow_202008220001\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"admin,zhangsan\", \"relation\": \"admin,zhangsan\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"admin\\\": {}, \\\"zhangsan\\\": {}}\", \"vpn_reason\": \"fdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1\\nfdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1\\nfdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1\\nfdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1\\nfdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1fdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1\\nfdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1\"}','admin','2020-08-22 08:46:20.051663','2020-08-22 08:46:20.051898',0,0);

/*!40000 ALTER TABLE `ticket_ticketflowlog` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table ticket_ticketrecord
# ------------------------------------------------------------

DROP TABLE IF EXISTS `ticket_ticketrecord`;

CREATE TABLE `ticket_ticketrecord` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) NOT NULL,
  `workflow_id` int(11) NOT NULL,
  `sn` varchar(25) NOT NULL,
  `state_id` int(11) NOT NULL,
  `parent_ticket_id` int(11) NOT NULL,
  `parent_ticket_state_id` int(11) NOT NULL,
  `participant_type_id` int(11) NOT NULL,
  `participant` varchar(1000) NOT NULL,
  `creator` varchar(50) NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `relation` varchar(1000) NOT NULL,
  `add_node_man` varchar(50) NOT NULL,
  `in_add_node` tinyint(1) NOT NULL,
  `script_run_last_result` tinyint(1) NOT NULL,
  `act_state_id` int(11) NOT NULL DEFAULT '0' COMMENT '进行状态',
  `multi_all_person` varchar(1000) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_creator` (`creator`),
  KEY `idx_created` (`gmt_created`),
  KEY `idx_act_state` (`act_state_id`),
  KEY `idx_workflow` (`workflow_id`),
  KEY `idx_sn` (`sn`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `ticket_ticketrecord` WRITE;
/*!40000 ALTER TABLE `ticket_ticketrecord` DISABLE KEYS */;

INSERT INTO `ticket_ticketrecord` (`id`, `title`, `workflow_id`, `sn`, `state_id`, `parent_ticket_id`, `parent_ticket_state_id`, `participant_type_id`, `participant`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `relation`, `add_node_man`, `in_add_node`, `script_run_last_result`, `act_state_id`, `multi_all_person`)
VALUES
	(14,'12',1,'loonflow_201805130012',2,0,0,1,'zhangsan','lilei','2018-05-13 22:24:41.952132','2018-08-09 07:33:44.762337',0,'lileilileilileilileilileilileilileilileilileilileilileilileilileilileilileilileilileililei','lilei',1,1,1,'{}'),
	(15,'请假哈哈22哈',1,'loonflow_201805130013',2,0,0,5,'creator','lilei','2018-05-13 22:28:21.623510','2018-05-14 07:07:39.579607',0,'lileilileililei','',0,1,1,'{}'),
	(16,'请假申请3',1,'loonflow_201805130014',3,0,0,1,'lilei','lilei','2018-05-13 22:34:12.668018','2018-05-13 22:34:12.668141',0,'lilei','',0,1,1,'{}'),
	(17,'vpn申请2',2,'loonflow_201805150001',10,0,0,3,'1','lilei','2018-05-15 07:16:38.281209','2018-05-22 07:26:54.685116',0,'guiji,wangwu,lilei','zhangsan',1,1,1,'{}'),
	(18,'vpn申请11',2,'loonflow_201805150002',8,0,0,2,'guiji,wangwu','lilei','2018-05-15 07:37:27.984815','2018-05-21 19:27:37.550734',0,'lilei,guiji,wangwu','',0,1,1,'{}'),
	(19,'testt',1,'loonflow_201810190001',5,0,0,0,'','admin','2018-10-19 00:08:40.371908','2018-10-21 20:06:57.527067',0,'jack,admin','',0,1,4,'{}'),
	(20,'teste',1,'loonflow_201810190002',4,0,0,1,'jack','admin','2018-10-19 00:38:41.354008','2018-10-19 00:38:53.872124',0,'jack,admin','',0,1,1,'{}'),
	(22,'tttttt',1,'loonflowhhh_201810220001',3,0,0,1,'jack','jack','2018-10-22 07:12:16.451086','2018-10-22 07:12:16.455740',0,'jack','',0,1,1,'{\'jack\': \'jack\'}'),
	(23,'ttttest',1,'loonflow_201810220002',3,0,0,1,'jack','jack','2018-10-22 08:05:37.187794','2018-10-22 08:05:37.192994',0,'jack','',0,1,1,'{\'jack\': \'jack\'}'),
	(24,'tttt',1,'loonflow_201811270001',3,0,0,1,'admin','admin','2018-11-27 07:09:06.308678','2018-11-27 07:09:06.326441',0,'admin','',0,1,1,'{}'),
	(25,'ttt21',1,'loonflow_201811270002',3,0,0,4,'2','admin','2018-11-27 07:12:27.917523','2018-11-27 07:12:27.929123',0,'guiji,admin,lilei,zhangsan','',0,1,1,'{}'),
	(26,'tttt',1,'loonflow_201811270003',3,0,0,4,'2','admin','2018-11-27 07:14:06.360734','2018-11-27 07:14:06.377165',0,'lilei,admin,zhangsan,guiji','',0,1,1,'{}'),
	(27,'11111',1,'loonflow_201811270004',3,0,0,4,'2','admin','2018-11-27 07:20:16.194872','2018-11-27 07:20:16.212155',0,'admin,zhangsan,lilei,guiji','',0,1,1,'{}'),
	(28,'tttt',1,'loonflow_201811270005',3,0,0,1,'zhangsan','admin','2018-11-27 07:21:00.015751','2018-11-27 07:21:00.015804',0,'admin','',0,1,1,'{}'),
	(29,'111122',1,'loonflow_201811270006',3,0,0,1,'zhangsan','admin','2018-11-27 07:23:04.023879','2018-11-27 07:23:04.031786',0,'admin,zhangsan','',0,1,1,'{}'),
	(30,'111ww',1,'loonflow_201811270007',3,0,0,1,'zhangsan','admin','2018-11-27 07:23:47.920099','2018-11-27 07:23:47.926368',0,'zhangsan,admin','',0,1,1,'{}'),
	(31,'122131',1,'loonflow_201811270008',3,0,0,1,'zhangsan','admin','2018-11-27 07:24:07.528102','2018-11-27 07:24:07.533129',0,'zhangsan,admin','',0,1,1,'{}'),
	(32,'fdfsfds',1,'loonflow_201811270009',3,0,0,1,'guiji','admin','2018-11-27 07:24:31.249309','2018-11-27 07:24:31.254020',0,'admin,guiji','',0,1,1,'{}'),
	(33,'ttt1',1,'loonflow_201811270010',3,0,0,1,'lilei','admin','2018-11-27 07:27:39.226722','2018-11-27 07:27:39.233032',0,'lilei,admin','',0,1,1,'{}'),
	(34,'stestet',1,'ops_201911240001',3,0,0,6,'1','admin','2019-11-24 10:23:07.212945','2019-11-24 10:23:07.212995',0,'admin','',0,1,1,'{}'),
	(35,'stestet',1,'ops_201911240002',5,0,0,0,'','admin','2019-11-24 10:24:31.578220','2020-03-29 09:47:33.834505',0,'admin,lilei','',0,0,1,'{}'),
	(36,'fdfdsf',2,'ops1_bd_202004110004',7,0,0,1,'admin','admin','2020-04-11 10:40:30.714885','2020-04-11 10:40:30.754360',0,'admin','',0,1,1,'{}'),
	(37,'test',2,'ops122222212_202005010001',11,0,0,0,'','admin','2020-05-01 09:19:28.683766','2020-05-01 09:19:48.328193',0,'admin','',0,1,5,'{}'),
	(38,'ttte',2,'ops122222212_202005010002',11,0,0,0,'','admin','2020-05-01 09:21:56.833968','2020-05-01 09:22:31.749793',0,'admin','',0,1,5,'{}'),
	(39,'testest',1,'ops122222212_202005070001',3,0,0,2,'zhangsan,lisi','admin','2020-05-07 22:42:17.242943','2020-05-07 22:42:17.250021',0,'admin,zhangsan,lisi','',0,1,1,'{\"zhangsan\": {}, \"lisi\": {}}'),
	(40,'test',2,'ops122222212_202005070002',8,0,0,2,'admin','zhangsan','2020-05-07 22:54:58.856151','2020-05-07 22:55:09.134082',0,'admin,zhangsan','',0,1,1,'{\"zhangsan\": {}, \"admin\": {}}'),
	(41,'test',2,'ops122222212_202005170001',7,0,0,2,'admin','admin','2020-05-17 17:31:54.224652','2020-05-17 17:38:51.127539',0,'zhangsan,admin','',0,1,1,'{\"zhangsan\": {}, \"admin\": {}}'),
	(42,'test111',2,'ops122222212_202005170002',8,0,0,3,'3','zhangsan','2020-05-17 17:44:45.452600','2020-05-17 17:45:34.510684',0,'wangwu,zhangsan,guiji,admin','',0,1,1,'{}'),
	(43,'TEST',2,'ops122222212_202005180001',7,0,0,2,'zhangsan','admin','2020-05-18 23:18:15.526179','2020-05-18 23:18:30.394674',0,'admin,zhangsan','',0,1,1,'{\"zhangsan\": {}, \"admin\": {\"transition_id\": 8, \"transition_name\": \"\\u540c\\u610f\"}}'),
	(44,'dfdsf',2,'loonflow_202008210004',7,0,0,2,'admin,zhangsan','admin','2020-08-21 10:39:32.645810','2020-08-21 10:39:32.669576',0,'admin,zhangsan','',0,1,1,'{\"admin\": {}, \"zhangsan\": {}}'),
	(45,'',1,'loonflow_202008210005',3,0,0,2,'lisi,zhangsan','admin','2020-08-21 18:33:34.805366','2020-08-21 18:33:34.868157',0,'admin,lisi,zhangsan','',0,1,1,'{\"lisi\": {}, \"zhangsan\": {}}'),
	(46,'',1,'loonflow_202008210006',3,0,0,2,'lisi,zhangsan','admin','2020-08-21 18:42:06.090420','2020-08-21 18:42:06.131744',0,'admin,lisi,zhangsan','',0,1,1,'{\"lisi\": {}, \"zhangsan\": {}}'),
	(47,'fdfafa ',2,'loonflow_202008220001',7,0,0,2,'admin,zhangsan','admin','2020-08-22 08:46:19.801342','2020-08-22 08:46:19.829325',0,'admin,zhangsan','',0,1,1,'{\"admin\": {}, \"zhangsan\": {}}');

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
	(1,'admin','2018-05-13 22:24:42','2018-05-13 22:24:42',0,'lileilileilileilileilileilileilileilileilileilileilileilileilileilileilileilileilileililei',0,0,14),
	(2,'admin','2018-05-13 22:28:22','2018-05-13 22:28:22',0,'lileilileililei',0,0,15),
	(3,'admin','2018-05-13 22:34:13','2020-03-29 09:38:20',0,'lilei',1,0,16),
	(4,'admin','2018-05-15 07:16:38','2020-03-29 09:41:07',0,'guiji',0,1,17),
	(5,'admin','2018-05-15 07:16:38','2018-05-15 07:16:38',0,'wangwu',0,0,17),
	(6,'admin','2018-05-15 07:16:38','2018-05-15 07:16:38',0,'lilei',0,0,17),
	(7,'admin','2018-05-15 07:37:28','2018-05-15 07:37:28',0,'lilei',0,0,18),
	(8,'admin','2018-05-15 07:37:28','2020-03-29 09:38:20',0,'guiji',1,0,18),
	(9,'admin','2018-05-15 07:37:28','2020-03-29 09:38:20',0,'wangwu',1,0,18),
	(10,'admin','2018-10-19 00:08:40','2020-03-29 09:41:07',0,'jack',0,1,19),
	(11,'admin','2018-10-19 00:08:40','2018-10-19 00:08:40',0,'admin',0,0,19),
	(12,'admin','2018-10-19 00:38:41','2020-03-29 09:38:20',0,'jack',1,0,20),
	(13,'admin','2018-10-19 00:38:41','2018-10-19 00:38:41',0,'admin',0,0,20),
	(14,'admin','2018-10-22 07:12:16','2020-03-29 09:38:20',0,'jack',1,0,22),
	(15,'admin','2018-10-22 08:05:37','2020-03-29 09:38:20',0,'jack',1,0,23),
	(16,'admin','2018-11-27 07:09:06','2020-03-29 09:38:20',0,'admin',1,0,24),
	(17,'admin','2018-11-27 07:12:28','2018-11-27 07:12:28',0,'guiji',0,0,25),
	(18,'admin','2018-11-27 07:12:28','2018-11-27 07:12:28',0,'admin',0,0,25),
	(19,'admin','2018-11-27 07:12:28','2018-11-27 07:12:28',0,'lilei',0,0,25),
	(20,'admin','2018-11-27 07:12:28','2018-11-27 07:12:28',0,'zhangsan',0,0,25),
	(21,'admin','2018-11-27 07:14:06','2018-11-27 07:14:06',0,'lilei',0,0,26),
	(22,'admin','2018-11-27 07:14:06','2018-11-27 07:14:06',0,'admin',0,0,26),
	(23,'admin','2018-11-27 07:14:06','2018-11-27 07:14:06',0,'zhangsan',0,0,26),
	(24,'admin','2018-11-27 07:14:06','2018-11-27 07:14:06',0,'guiji',0,0,26),
	(25,'admin','2018-11-27 07:20:16','2018-11-27 07:20:16',0,'admin',0,0,27),
	(26,'admin','2018-11-27 07:20:16','2018-11-27 07:20:16',0,'zhangsan',0,0,27),
	(27,'admin','2018-11-27 07:20:16','2018-11-27 07:20:16',0,'lilei',0,0,27),
	(28,'admin','2018-11-27 07:20:16','2018-11-27 07:20:16',0,'guiji',0,0,27),
	(29,'admin','2018-11-27 07:21:00','2018-11-27 07:21:00',0,'admin',0,0,28),
	(30,'admin','2018-11-27 07:23:04','2018-11-27 07:23:04',0,'admin',0,0,29),
	(31,'admin','2018-11-27 07:23:04','2020-03-29 09:39:34',0,'zhangsan',1,0,29),
	(32,'admin','2018-11-27 07:23:48','2020-03-29 09:39:34',0,'zhangsan',1,0,30),
	(33,'admin','2018-11-27 07:23:48','2018-11-27 07:23:48',0,'admin',0,0,30),
	(34,'admin','2018-11-27 07:24:08','2020-03-29 09:39:34',0,'zhangsan',1,0,31),
	(35,'admin','2018-11-27 07:24:08','2018-11-27 07:24:08',0,'admin',0,0,31),
	(36,'admin','2018-11-27 07:24:31','2018-11-27 07:24:31',0,'admin',0,0,32),
	(37,'admin','2018-11-27 07:24:31','2020-03-29 09:39:34',0,'guiji',1,0,32),
	(38,'admin','2018-11-27 07:27:39','2020-03-29 09:39:34',0,'lilei',1,0,33),
	(39,'admin','2018-11-27 07:27:39','2018-11-27 07:27:39',0,'admin',0,0,33),
	(40,'admin','2019-11-24 10:23:07','2019-11-24 10:23:07',0,'admin',0,0,34),
	(41,'','2020-03-29 09:47:27','2020-03-29 09:47:27',0,'lilei',1,0,35),
	(42,'','2020-04-11 10:40:31','2020-04-11 10:40:30',0,'admin',1,0,36),
	(43,'','2020-05-01 09:19:29','2020-05-01 09:19:48',0,'admin',0,0,37),
	(44,'','2020-05-01 09:21:57','2020-05-01 09:22:31',0,'admin',0,0,38),
	(45,'','2020-05-07 22:42:17','2020-05-07 22:42:17',0,'admin',0,0,39),
	(46,'','2020-05-07 22:42:17','2020-05-07 22:42:17',0,'zhangsan',1,0,39),
	(47,'','2020-05-07 22:42:17','2020-05-07 22:42:17',0,'lisi',1,0,39),
	(48,'','2020-05-07 22:54:59','2020-05-07 22:55:09',0,'zhangsan',0,1,40),
	(49,'','2020-05-07 22:54:59','2020-05-07 22:54:59',0,'admin',1,0,40),
	(50,'','2020-05-17 17:31:54','2020-05-17 17:38:51',0,'admin',1,1,41),
	(51,'','2020-05-17 17:31:54','2020-05-17 17:38:51',0,'zhangsan',0,1,41),
	(52,'','2020-05-17 17:44:45','2020-05-17 17:44:52',0,'zhangsan',0,1,42),
	(53,'','2020-05-17 17:44:45','2020-05-17 17:45:34',0,'admin',0,1,42),
	(54,'','2020-05-17 17:45:35','2020-05-17 17:45:35',0,'guiji',1,0,42),
	(55,'','2020-05-17 17:45:35','2020-05-17 17:45:35',0,'wangwu',1,0,42),
	(56,'','2020-05-18 23:18:16','2020-05-18 23:18:30',0,'admin',0,1,43),
	(57,'','2020-05-18 23:18:16','2020-05-18 23:18:16',0,'zhangsan',1,0,43),
	(58,'','2020-08-21 10:39:33','2020-08-21 10:39:32',0,'admin',1,0,44),
	(59,'','2020-08-21 10:39:33','2020-08-21 10:39:33',0,'zhangsan',1,0,44),
	(60,'','2020-08-21 18:33:35','2020-08-21 18:33:35',0,'admin',0,0,45),
	(61,'','2020-08-21 18:33:35','2020-08-21 18:33:35',0,'lisi',1,0,45),
	(62,'','2020-08-21 18:33:35','2020-08-21 18:33:35',0,'zhangsan',1,0,45),
	(63,'','2020-08-21 18:42:06','2020-08-21 18:42:06',0,'admin',0,0,46),
	(64,'','2020-08-21 18:42:06','2020-08-21 18:42:06',0,'lisi',1,0,46),
	(65,'','2020-08-21 18:42:06','2020-08-21 18:42:06',0,'zhangsan',1,0,46),
	(66,'','2020-08-22 08:46:20','2020-08-22 08:46:19',0,'admin',1,0,47),
	(67,'','2020-08-22 08:46:20','2020-08-22 08:46:20',0,'zhangsan',1,0,47);

/*!40000 ALTER TABLE `ticket_ticketuser` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table workflow_customfield
# ------------------------------------------------------------

DROP TABLE IF EXISTS `workflow_customfield`;

CREATE TABLE `workflow_customfield` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `workflow_id` int(11) NOT NULL,
  `field_type_id` int(11) NOT NULL,
  `field_key` varchar(50) NOT NULL,
  `field_name` varchar(50) NOT NULL,
  `order_id` int(11) NOT NULL,
  `default_value` varchar(100) DEFAULT NULL,
  `description` varchar(100) NOT NULL,
  `field_template` longtext NOT NULL,
  `boolean_field_display` varchar(100) NOT NULL,
  `creator` varchar(50) NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `field_choice` varchar(1000) NOT NULL,
  `label` varchar(100) NOT NULL,
  `placeholder` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `workflow_customfield` WRITE;
/*!40000 ALTER TABLE `workflow_customfield` DISABLE KEYS */;

INSERT INTO `workflow_customfield` (`id`, `workflow_id`, `field_type_id`, `field_key`, `field_name`, `order_id`, `default_value`, `description`, `field_template`, `boolean_field_display`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `field_choice`, `label`, `placeholder`)
VALUES
	(1,1,30,'leave_start','开始时间',20,'','','','{}','admin','2018-04-23 20:56:25.940486','2018-05-11 07:31:11.133782',0,'{}','{}',''),
	(2,1,30,'leave_end','结束时间',25,NULL,'','','{}','admin','2018-05-10 07:41:03.717540','2018-05-11 07:31:19.923554',0,'{}','{}',''),
	(4,1,60,'leave_proxy','代理人',35,NULL,'请假期间的代理人','','{}','admin','2018-05-11 07:31:01.068850','2018-05-11 07:31:35.323117',0,'{}','',''),
	(5,1,35,'leave_type','请假类型',40,NULL,'','','{}','admin','2018-05-11 07:34:29.608579','2018-05-23 22:38:57.324916',0,'{\"1\": \"年假\", \"2\": \"调休\", \"3\": \"病假\", \"4\": \"婚假\"}','{}',''),
	(6,1,10,'leave_reason','请假原因及相关附件',45,'','','病假请提供证明拍照附件， 婚假请提供结婚证拍照附件','{}','admin','2018-05-11 07:36:41.882377','2018-05-11 07:36:41.882413',0,'{}','{}',''),
	(7,2,55,'vpn_reason','申请原因',110,'请填写申请vpn的理由','','','{}','admin','2018-05-12 10:02:31.501142','2018-05-12 10:02:31.501189',0,'{}','{}',''),
	(8,1,20,'bool_field','布尔字段',0,'','','','{\"1\":\"正确\", \"2\":\"错误\"}','admin','2020-08-15 15:50:14.707215','2020-08-15 15:50:14.707247',0,'{}','{}',''),
	(9,1,25,'date_filed','日期字段',0,'','','','{}','admin','2020-08-15 15:54:19.619379','2020-08-15 15:54:19.619409',0,'{}','{}',''),
	(10,1,30,'datetime_field','日期时间字段',0,'','','','{}','admin','2020-08-15 15:54:33.396096','2020-08-15 15:54:33.396127',0,'{}','{}',''),
	(11,1,35,'checkbox_field','单选字段',0,'','','','{}','admin','2020-08-15 15:55:43.617371','2020-08-15 15:55:43.617394',0,'{\"1\":\"中国\",\"2\":\"美国\",\"3\":\"英国\"}','{}',''),
	(12,1,40,'multi_checkbox_field','多选字段',0,'','','','{}','admin','2020-08-15 15:56:33.283712','2020-08-15 15:56:33.283801',0,'{\"1\":\"中国\", \"2\":\"美国\", \"3\":\"英国\"}','{}',''),
	(13,1,45,'select_field','下拉选择字段',0,'','','','{}','admin','2020-08-15 15:57:04.427730','2020-08-15 15:57:04.427762',0,'{\"1\":\"中国\", \"2\":\"美国\", \"3\":\"英国\"}','{}',''),
	(14,1,50,'multi_select_field','多选下拉列表',0,'','','','{}','admin','2020-08-15 15:57:25.586297','2020-08-15 15:57:25.586346',0,'{\"1\":\"中国\",\"2\":\"美国\",\"3\":\"英国\"}','{}',''),
	(15,1,55,'text_field','文本字段',0,'','','','{}','admin','2020-08-15 15:57:56.756983','2020-08-15 15:57:56.757009',0,'{}','{}',''),
	(16,1,60,'user_fleld','用户选择字段',0,'','','','{}','admin','2020-08-15 15:58:30.818408','2020-08-15 15:58:30.818457',0,'{}','{}',''),
	(17,1,70,'multi_user_field','多选用户字段',0,'','','','{}','admin','2020-08-15 15:58:52.338369','2020-08-15 15:58:52.338431',0,'{}','{}',''),
	(18,1,80,'attachment_field','附件字段',0,'','','','{}','admin','2020-08-15 15:59:31.269502','2020-08-15 15:59:31.269533',0,'{}','{}',''),
	(19,1,35,'fw','fds',23,'sd','dsfs','fee','{}','admin','2020-10-27 06:59:50.901725','2020-10-27 06:59:50.901821',1,'{}','{}',''),
	(20,1,35,'2r','dfsf',2,'','','','{}','admin','2020-10-28 07:39:50.412037','2020-10-28 07:39:50.412132',1,'{}','{}','');

/*!40000 ALTER TABLE `workflow_customfield` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table workflow_customnotice
# ------------------------------------------------------------

DROP TABLE IF EXISTS `workflow_customnotice`;

CREATE TABLE `workflow_customnotice` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `creator` varchar(50) NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `hook_url` varchar(100) NOT NULL DEFAULT '' COMMENT 'hook_url',
  `hook_token` varchar(100) NOT NULL DEFAULT '' COMMENT 'hook_token',
  `appkey` varchar(100) DEFAULT NULL,
  `appsecret` varchar(100) DEFAULT NULL,
  `corpid` varchar(100) DEFAULT NULL,
  `corpsecret` varchar(100) DEFAULT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `workflow_customnotice` WRITE;
/*!40000 ALTER TABLE `workflow_customnotice` DISABLE KEYS */;

INSERT INTO `workflow_customnotice` (`id`, `name`, `description`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `hook_url`, `hook_token`, `appkey`, `appsecret`, `corpid`, `corpsecret`, `type_id`)
VALUES
	(1,'通知1','fdsf','admin','2019-02-12 22:45:20.765495','2019-02-12 22:45:20.765587',0,'222','222','','','','',1),
	(2,'fdsfs','fsdfsd','admin','2020-09-05 22:16:43.661081','2020-09-05 22:16:43.661305',0,'dsfsdf','sdfdsfs','','','','',1),
	(3,'23','333','admin','2020-09-07 23:41:33.792284','2020-09-07 23:41:33.792526',0,'','','','','fds','332323',2),
	(4,'test','222','admin','2020-09-08 06:35:20.027469','2020-09-08 06:35:20.027744',0,'','','fdsf','fdsfs','','',3),
	(5,'2323','dfsf','admin','2020-09-08 06:38:05.143667','2020-09-08 06:38:05.143866',1,'','','fdsfs','dfsf','','',3),
	(6,'2233342','','admin','2020-09-08 06:38:33.228658','2020-09-08 06:38:33.228952',1,'','','','','dfs','fdsf',2);

/*!40000 ALTER TABLE `workflow_customnotice` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table workflow_state
# ------------------------------------------------------------

DROP TABLE IF EXISTS `workflow_state`;

CREATE TABLE `workflow_state` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `workflow_id` int(11) NOT NULL,
  `is_hidden` tinyint(1) NOT NULL,
  `order_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  `participant_type_id` int(11) NOT NULL,
  `participant` varchar(1000) NOT NULL,
  `distribute_type_id` int(11) NOT NULL,
  `state_field_str` longtext NOT NULL,
  `label` varchar(1000) NOT NULL,
  `creator` varchar(50) NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `remember_last_man_enable` tinyint(1) NOT NULL,
  `enable_retreat` tinyint(1) unsigned NOT NULL DEFAULT '0' COMMENT '允许撤回',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `workflow_state` WRITE;
/*!40000 ALTER TABLE `workflow_state` DISABLE KEYS */;

INSERT INTO `workflow_state` (`id`, `name`, `workflow_id`, `is_hidden`, `order_id`, `type_id`, `participant_type_id`, `participant`, `distribute_type_id`, `state_field_str`, `label`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `remember_last_man_enable`, `enable_retreat`)
VALUES
	(1,'新建中',1,0,0,1,0,'',1,'{\"attachment_field\":2,\"multi_user_field\":2,\"user_fleld\":2,\"text_field\":2,\"multi_select_field\":2,\"select_field\":2, \"title\":1,\"leave_start\":2,\"leave_end\":2,\"leave_proxy\":3,\"leave_type\":2,\"leave_reason\":2,\"bool_field\":2,\"checkbox_field\":2,\"multi_checkbox_field\":2}','{}','admin','2018-04-23 20:53:33.052134','2018-05-13 11:42:11.273695',0,0,0),
	(2,'发起人-编辑中',1,1,2,0,5,'creator',1,'{\"leave_end\":2,\"leave_days\":2,\"sn\":1,\"state.state_name\":1,\"leave_proxy\":2,\"title\":2,\"gmt_created\":1,\"creator\":1,\"leave_start\":2,\"leave_reason\":2,\"leave_type\":2}','{}','admin','2018-04-30 15:45:48.976712','2018-05-14 06:44:10.661777',1,0,0),
	(3,'TL审批中',1,0,3,0,2,'zhangsan,lisi',4,'{\"leave_reason\":1,\"leave_start\":1,\"leave_type\":1,\"creator\":1,\"gmt_created\":1,\"title\":1,\"leave_proxy\":1,\"sn\":1,\"leave_end\":1}','{}','admin','2018-04-30 15:46:42.184252','2018-11-27 07:20:33.209705',0,1,0),
	(4,'人事部门-处理中',1,0,4,0,1,'jack',1,'{\"sn\":1,  \"title\":1, \"leave_start\": 1,  \"leave_end\":1,  \"leave_days\":1,  \"leave_proxy\":1,  \"leave_type\":1, \"creator\":1, \"gmt_created\":1,  \"leave_reason\":1}','{}','admin','2018-04-30 15:47:58.790510','2018-05-13 11:42:59.834440',0,0,0),
	(5,'结束',1,0,6,2,0,'',1,'{}','{}','admin','2018-04-30 15:51:41.260309','2018-05-11 06:52:39.799922',0,0,0),
	(6,'发起人-新建中',2,0,1,1,5,'creator',1,'{\"vpn_reason\":2, \"title\":2}','{}','admin','2018-05-10 07:34:45.302697','2018-05-15 07:13:06.599270',0,0,0),
	(7,'发起人tl-审批中',2,0,2,0,2,'zhangsan,admin',4,'{\"sn\":1,\"title\":1,\"creator\":1,\"gmt_created\":1,\"vpn_reason\":1}','{}','admin','2018-05-11 06:47:36.381658','2018-05-15 07:19:16.038155',0,0,0),
	(8,'运维人员-审批中',2,0,3,0,3,'3',1,'{\"sn\":1,  \"title\":1, \"creator\":1, \"gmt_created\":1,\"vpn_reason\":1,\"participant_info.participant_alias\":1,\"participant_info.participant_name\":1}','{}','admin','2018-05-11 06:48:26.945117','2018-11-05 23:37:58.618022',0,0,0),
	(9,'授权脚本-自动执行中',2,0,4,0,10,'{}',1,'{}','{}','admin','2018-05-11 06:50:09.416344','2018-05-11 07:10:25.197748',0,0,0),
	(10,'发起人-确认中',2,0,6,0,5,'creator',1,'{\"sn\":1,\"participant_info.participant_name\":1,\"state.state_name\":1,\"workflow.workflow_name\":1}','{}','admin','2018-05-11 06:51:02.913212','2018-05-22 22:21:51.867707',0,0,0),
	(11,'结束',2,0,7,2,0,'',1,'{}','{}','admin','2018-05-11 07:11:53.076731','2018-05-11 07:11:53.076766',0,0,0),
	(19,'test',1,0,0,0,1,'',2,'{\"title\":2}','{}','admin','2019-04-07 17:48:09.224566','2019-04-07 17:48:09.224621',1,1,0),
	(20,'testt',1,0,0,0,1,'',2,'{\"title\":2}','{}','admin','2019-04-07 21:24:17.078594','2019-04-07 21:24:17.078638',1,0,0),
	(21,'11111111',1,0,0,0,1,'',2,'{\"title\":2}','{}','admin','2019-04-07 22:10:52.603902','2019-04-07 22:10:52.603963',1,0,0),
	(22,'ttttttttt',1,0,0,0,1,'',2,'{\"title\":2}','{}','admin','2019-06-13 23:01:34.696459','2019-06-13 23:01:34.696492',1,0,0),
	(23,'11111',1,0,0,0,1,'',2,'{\"title\":2}','{}','admin','2019-06-15 21:34:19.035126','2019-06-15 21:34:19.035160',1,0,0),
	(24,'222',1,0,0,0,1,'',2,'{\"title\":2}','{}','admin','2019-06-15 21:46:16.037190','2019-06-15 21:46:16.037219',1,0,0),
	(25,'tttt',1,0,0,0,1,'',2,'{\"title\":2}','{}','admin','2019-09-20 15:21:24.144219','2019-09-20 15:21:24.144252',1,0,0),
	(26,'tttttt',1,0,0,0,1,'',2,'{\"title\":2}','{}','admin','2019-09-20 15:21:31.081869','2019-09-20 15:21:31.081910',1,0,0),
	(27,'fsfsf',1,0,0,0,1,'',2,'{\"title\":2}','{}','admin','2019-09-20 15:21:37.180213','2019-09-20 15:21:37.180244',1,0,0),
	(28,'fdf',1,0,1,0,1,'fa',1,'{\"gmt_created\":1}','{}','admin','2020-11-03 07:40:02.729021','2020-11-03 07:40:02.729875',1,0,0),
	(29,'test',1,0,0,0,2,'test',2,'{}','{}','admin','2020-11-09 07:20:10.977897','2020-11-09 07:20:10.978040',1,0,0);

/*!40000 ALTER TABLE `workflow_state` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table workflow_transition
# ------------------------------------------------------------

DROP TABLE IF EXISTS `workflow_transition`;

CREATE TABLE `workflow_transition` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `workflow_id` int(11) NOT NULL,
  `transition_type_id` int(11) NOT NULL,
  `source_state_id` int(11) NOT NULL,
  `destination_state_id` int(11) NOT NULL,
  `alert_enable` tinyint(1) NOT NULL,
  `alert_text` varchar(100) NOT NULL,
  `creator` varchar(50) NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `field_require_check` tinyint(1) NOT NULL,
  `timer` int(11) NOT NULL,
  `attribute_type_id` int(11) NOT NULL,
  `condition_expression` varchar(1000) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `workflow_transition` WRITE;
/*!40000 ALTER TABLE `workflow_transition` DISABLE KEYS */;

INSERT INTO `workflow_transition` (`id`, `name`, `workflow_id`, `transition_type_id`, `source_state_id`, `destination_state_id`, `alert_enable`, `alert_text`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `field_require_check`, `timer`, `attribute_type_id`, `condition_expression`)
VALUES
	(1,'提交',1,1,1,3,0,'','admin','2018-04-24 07:09:25.922814','2018-04-30 15:48:57.047369',0,1,0,1,'[]'),
	(2,'保存',1,1,1,1,0,'','admin','2018-04-30 15:30:25.650813','2018-04-30 15:48:52.372363',0,1,0,2,'[]'),
	(3,'同意',1,1,3,4,0,'','admin','2018-04-30 15:49:23.451582','2018-04-30 15:49:23.451627',0,1,0,1,'[]'),
	(4,'拒绝',1,1,3,1,0,'fdsfdsfsf','admin','2018-04-30 15:54:32.069649','2018-05-11 07:00:24.370322',0,0,0,1,'[]'),
	(5,'同意',1,1,4,5,0,'','admin','2018-04-30 15:55:00.072437','2018-05-11 07:03:29.349770',0,1,0,1,'[]'),
	(6,'退回',1,1,4,1,0,'','admin','2018-05-11 06:58:43.395655','2018-05-11 07:04:14.896678',0,0,0,1,'[]'),
	(7,'提交',2,1,6,7,0,'','admin','2018-05-11 07:06:22.745312','2018-05-11 07:06:22.745342',0,1,0,1,'[]'),
	(8,'同意',2,1,7,8,0,'','admin','2018-05-11 07:07:33.213731','2018-05-11 07:07:33.213760',0,1,0,1,'[]'),
	(9,'同意',2,1,8,9,0,'','admin','2018-05-11 07:12:53.036037','2018-05-11 07:12:53.036077',0,1,0,1,'[]'),
	(10,'脚本执行完成',2,1,9,10,0,'','admin','2018-05-11 07:13:12.070223','2018-05-11 07:13:12.070254',0,1,0,1,'[]'),
	(11,'确认完成',2,1,10,11,0,'','admin','2018-05-11 07:13:52.427815','2018-05-11 07:13:52.427844',0,1,0,1,'[]'),
	(12,'未生效',2,1,10,8,1,'是否真的退回？  请查看vpn使用文档保证使用姿势正确，再退回','admin','2018-05-11 07:16:26.826525','2018-05-11 07:16:36.072876',0,0,0,1,'[]'),
	(25,'tttt',2,1,28,6,0,'','admin','2019-12-08 16:46:06.801015','2019-12-08 16:46:06.801074',1,0,0,1,'[]'),
	(26,'tet',1,0,1,4,0,'','admin','2020-11-14 15:57:37.758568','2020-11-14 15:57:37.758662',1,1,0,1,'[]');

/*!40000 ALTER TABLE `workflow_transition` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table workflow_workflow
# ------------------------------------------------------------

DROP TABLE IF EXISTS `workflow_workflow`;

CREATE TABLE `workflow_workflow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` varchar(50) NOT NULL,
  `display_form_str` varchar(10000) NOT NULL,
  `creator` varchar(50) NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `view_permission_check` tinyint(1) NOT NULL,
  `limit_expression` varchar(1000) NOT NULL,
  `notices` varchar(50) NOT NULL,
  `title_template` varchar(100) NOT NULL DEFAULT '' COMMENT '标题模板',
  `content_template` varchar(1000) NOT NULL DEFAULT '' COMMENT '内容模板',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `workflow_workflow` WRITE;
/*!40000 ALTER TABLE `workflow_workflow` DISABLE KEYS */;

INSERT INTO `workflow_workflow` (`id`, `name`, `description`, `display_form_str`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `view_permission_check`, `limit_expression`, `notices`, `title_template`, `content_template`)
VALUES
	(1,'请假申请','请假申请','[\"sn\", \"title\", \"leave_start\", \"leave_end\", \"leave_days\", \"leave_proxy\",  \"leave_type\", \"creator\", \"gmt_created\", \"leave_reason\"]','admin','2018-04-23 20:49:32.229386','2018-10-22 08:05:15.574860',0,1,'{}','1,2','你有一个待办工单:{title}','标题:{title}, 创建时间:{gmt_created}'),
	(2,'vpn申请','vpn权限申请','[\"sn\", \"title\", \"model\", \"gmt_created\",\"participant.participant_alias\",\"vpn_reason\"]','admin','2018-05-06 12:32:36.690665','2018-11-05 23:32:57.667206',0,1,'{}','','','');

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

LOCK TABLES `workflow_workflowadmin` WRITE;
/*!40000 ALTER TABLE `workflow_workflowadmin` DISABLE KEYS */;

INSERT INTO `workflow_workflowadmin` (`id`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `username`, `workflow_id`)
VALUES
	(1,'admin','2020-04-10 20:08:17','2020-04-10 20:08:17',0,'admin',30),
	(2,'admin','2020-04-11 09:41:35','2020-04-11 09:41:35',0,'guiji',31),
	(3,'admin','2020-04-11 09:47:13','2020-04-11 09:47:13',0,'guiji',35);

/*!40000 ALTER TABLE `workflow_workflowadmin` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table workflow_workflowscript
# ------------------------------------------------------------

DROP TABLE IF EXISTS `workflow_workflowscript`;

CREATE TABLE `workflow_workflowscript` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `saved_name` varchar(100) NOT NULL,
  `description` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `creator` varchar(50) NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `workflow_workflowscript` WRITE;
/*!40000 ALTER TABLE `workflow_workflowscript` DISABLE KEYS */;

INSERT INTO `workflow_workflowscript` (`id`, `name`, `saved_name`, `description`, `is_active`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`)
VALUES
	(1,'创建虚拟机','workflow_script/create_vm.py','用于创建虚拟机的脚本',1,'admin','2019-03-08 07:05:49.613264','2019-03-08 07:05:49.613315',0),
	(2,'werer','workflow_script/e5939be6-4b64-11e9-a255-784f437daad6.py','erewrewrw2222',1,'admin','2019-03-10 10:06:37.450850','2019-03-10 10:06:37.450991',1),
	(3,'teste2221','workflow_script/83b3a57e-42db-11e9-8e30-784f437daad6.py','estt',1,'admin','2019-03-10 10:23:38.640143','2019-03-10 10:23:38.640325',1),
	(4,'111','workflow_script/7401155a-434c-11e9-8621-784f437daad6.py','222',1,'admin','2019-03-10 23:52:05.449189','2019-03-10 23:52:05.449298',1),
	(5,'1313','workflow_script/d5d39ad4-4386-11e9-ac68-784f437daad6.py','13132',1,'admin','2019-03-11 06:50:29.009754','2019-03-11 06:50:29.009916',1),
	(6,'fsdf1','workflow_script/08bb0dec-4387-11e9-af6c-784f437daad6.py','dfdsf1',1,'admin','2019-03-11 06:51:28.891797','2019-03-11 06:51:28.891862',1),
	(7,'12','workflow_script/bc560c22-438b-11e9-8720-784f437daad6.py','122222',1,'admin','2019-03-11 07:25:14.244269','2019-03-11 07:25:14.244333',1),
	(8,'12','workflow_script/e4bbfec2-438b-11e9-a471-784f437daad6.py','22',0,'admin','2019-03-11 07:26:12.872996','2019-03-11 07:26:12.873112',1),
	(9,'121','workflow_script/6be756dc-438c-11e9-866a-784f437daad6.py','21212',0,'admin','2019-03-11 07:29:59.633154','2019-03-11 07:29:59.633211',1),
	(10,'121','workflow_script/743df598-438c-11e9-875b-784f437daad6.py','21212',0,'admin','2019-03-11 07:30:13.623816','2019-03-11 07:30:13.623875',1),
	(11,'121','workflow_script/aa4f5030-438c-11e9-9ac4-784f437daad6.py','2121',0,'admin','2019-03-11 07:31:44.335415','2019-03-11 07:44:31.483375',1),
	(12,'fefef222','workflow_script/8dae6968-4b64-11e9-9404-784f437daad6.py','1222222222',1,'admin','2019-03-21 07:04:45.767163','2019-03-21 07:04:45.767269',1),
	(13,'ses222211122222','workflow_script/b07acb78-4b64-11e9-9300-784f437daad6.py','1222222222',1,'admin','2019-03-21 07:05:44.117895','2019-03-21 07:05:44.117953',1),
	(14,'werer','workflow_script/e1109ee8-4b64-11e9-bd64-784f437daad6.py','erewrewrw',1,'admin','2019-03-21 07:07:05.629952','2019-03-21 07:07:05.630006',1),
	(15,'wf','workflow_script/12f69d08-4c30-11e9-bfd8-784f437daad6.py','sdfsfs',1,'admin','2019-03-22 07:21:37.181812','2019-03-22 07:21:37.181870',1);

/*!40000 ALTER TABLE `workflow_workflowscript` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table workflow_workflowuserpermission
# ------------------------------------------------------------

DROP TABLE IF EXISTS `workflow_workflowuserpermission`;

CREATE TABLE `workflow_workflowuserpermission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creator` varchar(50) NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `permission` varchar(100) DEFAULT NULL,
  `user_type` varchar(100) DEFAULT NULL,
  `user` varchar(100) DEFAULT NULL,
  `workflow_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `workflow_workflowuserpermission_workflow_id_id_0221212d` (`workflow_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
