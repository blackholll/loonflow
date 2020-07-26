# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.7.17)
# Database: loonflow_1_0
# Generation Time: 2020-03-15 02:06:25 +0000
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



# Dump of table account_loonuser
# ------------------------------------------------------------

DROP TABLE IF EXISTS `account_loonuser`;

CREATE TABLE `account_loonuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `password` varchar(128) NOT NULL DEFAULT '' COMMENT '密码',
  `last_login` datetime DEFAULT NULL DEFAULT '0001-01-01 00:00:00' COMMENT '最后登录时间',
  `username` varchar(50) NOT NULL DEFAULT '' COMMENT '用户名',
  `alias` varchar(50) NOT NULL DEFAULT '' COMMENT '中文(昵称)',
  `email` varchar(255) NOT NULL DEFAULT '' COMMENT '邮箱',
  `phone` varchar(13) NOT NULL DEFAULT '' COMMENT '手机号',
  `dept_id` int(11) NOT NULL DEFAULT '0' COMMENT '所属部门id',
  `is_active` tinyint(1) NOT NULL  DEFAULT '0' COMMENT '在职',
  `is_admin` tinyint(1) NOT NULL DEFAULT '0' COMMENT '超级管理员',
  `creator` varchar(50) NOT NULL  DEFAULT '' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL  DEFAULT '0' COMMENT '已删除',
  `is_workflow_admin` tinyint(1) NOT NULL DEFAULT '0' COMMENT '工作流管理员',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `account_loonuser` WRITE;
/*!40000 ALTER TABLE `account_loonuser` DISABLE KEYS */;

INSERT INTO `account_loonuser` (`id`, `password`, `last_login`, `username`, `alias`, `email`, `phone`, `dept_id`, `is_active`, `is_admin`, `creator`, `gmt_created`, `gmt_modified`, `is_deleted`, `is_workflow_admin`)
VALUES
	(1,'pbkdf2_sha256$100000$wZONVjuD1eMK$QM6m9gBR44Elj+Qx65kwzPleULawmgzCQm08xMOyZOQ=','2020-03-15 09:57:33.726154','admin','超级管理员','admin@111.com','',0,1,1,'','2020-03-15 09:57:07.090009','2020-03-15 09:57:07.094560',0,0);

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
	('gnq8ua2c47at1m055h67qj6ml0sc8bmy','ZWUzZTM3NGMyMTkwOGU0ZDEzY2U4ZDYxZDFjNTM3Y2Q2YzhiZDZmNTp7Il9hdXRoX3VzZXJfaWQiOiI0OCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYWVhMWFmNDFmNjM4NDcyOWRmMzdjOWFiY2JjOWIzOGI4ZTBhOGMyNyJ9','2020-03-29 09:57:33.734736');

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
  `time_value` time(6) NOT NULL  DEFAULT '00:00:01' COMMENT '时间值',
  `radio_value` varchar(50) NOT NULL DEFAULT '' COMMENT '单选框值',
  `checkbox_value` varchar(50) NOT NULL DEFAULT '' COMMENT '复选框值',
  `select_value` varchar(50) NOT NULL DEFAULT '' COMMENT '单选下拉列表值',
  `multi_select_value` varchar(50) NOT NULL DEFAULT '' COMMENT '多选下拉列表值',
  `text_value` longtext NOT NULL DEFAULT '' COMMENT '文本域值',
  `username_value` varchar(50) NOT NULL DEFAULT '' COMMENT '用户名值',
  `multi_username_value` varchar(1000) NOT NULL DEFAULT '' COMMENT '多选用户名值',
  PRIMARY KEY (`id`),
  KEY `idx_ticket_id_field_key` (`ticket_id`,`field_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



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
  `suggestion` varchar(10000) NOT NULL DEFAULT '0' COMMENT '处理意见',
  `participant_type_id` int(11) NOT NULL DEFAULT '0' COMMENT '参与人类型',
  `participant` varchar(50) NOT NULL DEFAULT '' COMMENT '参与人',
  `state_id` int(11) NOT NULL DEFAULT '0' COMMENT '状态id',
  `intervene_type_id` int(11) NOT NULL  DEFAULT '0' COMMENT '干预类型',
  `ticket_data` varchar(10000) NOT NULL  DEFAULT '' COMMENT '工单数据',
  PRIMARY KEY (`id`),
  KEY `idx_ticket_id` (`ticket_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



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
  `participant` varchar(1000) NOT NULL DEFAULT '' COMMENT '参与人',
  `relation` varchar(1000) NOT NULL DEFAULT '' COMMENT '工单关系人',
  `in_add_node` tinyint(1) NOT NULL  DEFAULT '0' COMMENT '加签中',
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
  `default_value` varchar(100) DEFAULT NULL DEFAULT '' COMMENT '默认值',
  `description` varchar(100) NOT NULL DEFAULT '' COMMENT '描述',
  `field_template` longtext NOT NULL DEFAULT '' COMMENT '字段模板',
  `boolean_field_display` varchar(100) NOT NULL DEFAULT '{}' COMMENT '布尔类型显示',
  `creator` varchar(50) NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已删除',
  `field_choice` varchar(1000) NOT NULL DEFAULT '{}' COMMENT '布尔类型显示',
  `label` varchar(100) NOT NULL DEFAULT '{}' COMMENT '布尔类型显示',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table workflow_customnotice
# ------------------------------------------------------------

DROP TABLE IF EXISTS `workflow_customnotice`;

CREATE TABLE `workflow_customnotice` (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `name` varchar(50) NOT NULL DEFAULT '' COMMENT '名称',
  `description` varchar(100) DEFAULT NULL DEFAULT '' COMMENT '描述',
  `creator` varchar(50) NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT '0' COMMENT '已删除',
  `hook_token` varchar(100) DEFAULT NULL DEFAULT '' COMMENT 'hook令牌',
  `hook_url` varchar(100) DEFAULT NULL DEFAULT '' COMMENT 'hook地址',
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
  `participant` varchar(1000) NOT NULL DEFAULT '' COMMENT '参与人',
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
  `description` varchar(100) DEFAULT NULL DEFAULT '' COMMENT '描述',
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
