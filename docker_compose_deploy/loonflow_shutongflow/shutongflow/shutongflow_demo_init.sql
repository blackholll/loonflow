-- MySQL dump 10.13  Distrib 5.7.22, for osx10.13 (x86_64)
--
-- Host: localhost    Database: shutong
-- ------------------------------------------------------
-- Server version	5.7.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_shutongdept`
--

DROP TABLE IF EXISTS `account_shutongdept`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_shutongdept` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `name` varchar(100) NOT NULL,
  `parent` int(11) NOT NULL,
  `leader` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_shutongdept`
--

LOCK TABLES `account_shutongdept` WRITE;
/*!40000 ALTER TABLE `account_shutongdept` DISABLE KEYS */;
INSERT INTO `account_shutongdept` VALUES (1,'2018-05-28 17:53:53.131890','2018-05-28 17:53:53.131923',0,'集团总部',0,'admin'),(2,'2018-05-28 17:54:09.064969','2018-05-28 17:54:29.089651',0,'运维',0,'ops'),(3,'2018-05-28 17:54:41.602794','2018-05-28 17:54:41.602823',0,'人事',0,'hr'),(4,'2018-05-28 17:54:51.438660','2018-05-28 17:54:51.438693',0,'配置管理',0,'scm');
/*!40000 ALTER TABLE `account_shutongdept` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_shutonguserrole`
--

DROP TABLE IF EXISTS `account_shutonguserrole`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `account_shutonguserrole` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `user` int(11) NOT NULL,
  `role` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_shutonguserrole`
--

LOCK TABLES `account_shutonguserrole` WRITE;
/*!40000 ALTER TABLE `account_shutonguserrole` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_shutonguserrole` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add permission',3,'add_permission'),(8,'Can change permission',3,'change_permission'),(9,'Can delete permission',3,'delete_permission'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add shutong user',6,'add_shutonguser'),(17,'Can change shutong user',6,'change_shutonguser'),(18,'Can delete shutong user',6,'delete_shutonguser'),(19,'Can add shutong role',7,'add_shutongrole'),(20,'Can change shutong role',7,'change_shutongrole'),(21,'Can delete shutong role',7,'delete_shutongrole'),(22,'Can add shutong dept',8,'add_shutongdept'),(23,'Can change shutong dept',8,'change_shutongdept'),(24,'Can delete shutong dept',8,'delete_shutongdept'),(25,'Can add shutong user role',9,'add_shutonguserrole'),(26,'Can change shutong user role',9,'change_shutonguserrole'),(27,'Can delete shutong user role',9,'delete_shutonguserrole');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
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
  KEY `django_admin_log_user_id_c564eba6_fk_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2018-05-28 17:50:49.535522','2','ops',1,'[{\"added\": {}}]',6,1),(2,'2018-05-28 17:51:13.318917','3','hr',1,'[{\"added\": {}}]',6,1),(3,'2018-05-28 17:51:32.317495','4','scm',1,'[{\"added\": {}}]',6,1),(4,'2018-05-28 17:52:18.165487','5','wangjun',1,'[{\"added\": {}}]',6,1),(5,'2018-05-28 17:52:49.958805','6','lilian',1,'[{\"added\": {}}]',6,1),(6,'2018-05-28 17:53:22.155813','7','david',1,'[{\"added\": {}}]',6,1),(7,'2018-05-28 17:53:32.787333','5','webb',2,'[{\"changed\": {\"fields\": [\"username\"]}}]',6,1),(8,'2018-05-28 17:53:53.132840','1','集团总部',1,'[{\"added\": {}}]',8,1),(9,'2018-05-28 17:54:09.065962','2','运维',1,'[{\"added\": {}}]',8,1),(10,'2018-05-28 17:54:29.091771','2','运维',2,'[{\"changed\": {\"fields\": [\"leader\"]}}]',8,1),(11,'2018-05-28 17:54:41.603467','3','人事',1,'[{\"added\": {}}]',8,1),(12,'2018-05-28 17:54:51.440344','4','配置管理',1,'[{\"added\": {}}]',8,1),(13,'2018-05-30 21:50:03.279097','1','admin',2,'[{\"changed\": {\"fields\": [\"dept\"]}}]',6,1),(14,'2018-05-30 21:51:29.539414','2','ops',2,'[{\"changed\": {\"fields\": [\"dept\"]}}]',6,1),(15,'2018-05-30 21:51:38.279047','3','hr',2,'[{\"changed\": {\"fields\": [\"dept\"]}}]',6,1),(16,'2018-05-30 21:51:46.775370','4','scm',2,'[{\"changed\": {\"fields\": [\"dept\"]}}]',6,1),(17,'2018-05-30 21:51:58.332230','5','webb',2,'[{\"changed\": {\"fields\": [\"dept\"]}}]',6,1),(18,'2018-05-30 21:52:08.310101','6','lilian',2,'[{\"changed\": {\"fields\": [\"dept\"]}}]',6,1),(19,'2018-05-30 21:52:27.650345','7','david',2,'[{\"changed\": {\"fields\": [\"dept\"]}}]',6,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (8,'account','shutongdept'),(7,'account','shutongrole'),(6,'account','shutonguser'),(9,'account','shutonguserrole'),(1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'contenttypes','contenttype'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2018-05-28 17:28:58.257449'),(2,'contenttypes','0002_remove_content_type_name','2018-05-28 17:28:58.306817'),(3,'auth','0001_initial','2018-05-28 17:28:58.431886'),(4,'auth','0002_alter_permission_name_max_length','2018-05-28 17:28:58.451873'),(5,'auth','0003_alter_user_email_max_length','2018-05-28 17:28:58.461113'),(6,'auth','0004_alter_user_username_opts','2018-05-28 17:28:58.472840'),(7,'auth','0005_alter_user_last_login_null','2018-05-28 17:28:58.483443'),(8,'auth','0006_require_contenttypes_0002','2018-05-28 17:28:58.485580'),(9,'auth','0007_alter_validators_add_error_messages','2018-05-28 17:28:58.496731'),(10,'auth','0008_alter_user_username_max_length','2018-05-28 17:28:58.507006'),(11,'auth','0009_alter_user_last_name_max_length','2018-05-28 17:28:58.517957'),(12,'account','0001_initial','2018-05-28 17:28:58.726428'),(13,'admin','0001_initial','2018-05-28 17:28:58.791593'),(14,'admin','0002_logentry_remove_auto_add','2018-05-28 17:28:58.808985'),(15,'sessions','0001_initial','2018-05-28 17:28:58.846171');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('6chmsusan4a4s75wqv7r1vw0q51njoig','MWY2MDc4MDMxYjA0MjUzOWU3MmFhODYwYjRlZTgwMjg2YjExNWI5OTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiJmNzVkNTIwNjFmNTlmZDczZWM1MTU3ZjYzMDE3NjBmYzI5MWM5NzMyIn0=','2018-06-11 17:48:52.145222'),('t82u5qdtumsbgcyb2682fykshu95ypcl','MWY2MDc4MDMxYjA0MjUzOWU3MmFhODYwYjRlZTgwMjg2YjExNWI5OTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiJmNzVkNTIwNjFmNTlmZDczZWM1MTU3ZjYzMDE3NjBmYzI5MWM5NzMyIn0=','2018-06-13 21:44:45.625058');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `username` varchar(100) NOT NULL,
  `alias` varchar(100) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `phone` int(11) DEFAULT NULL,
  `dept` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'pbkdf2_sha256$100000$CeyRxwfai2ph$+1vDkt2SkvcYkVMIE3QrMjF2xYbRu1jDjy/DymXhcrM=','2018-05-31 23:22:48.774573','','','2018-05-28 17:29:58.000000','admin','超级管理员','admin@youshutong.com',NULL,1,1,1,1,'2018-05-28 17:29:59.008564','2018-05-31 23:22:48.775379',0),(2,'pbkdf2_sha256$100000$ZVNTI0GmVAPy$yc1Enn2FAtJdg5YlYUDVVNxqcj37NrkcPqQQrOU5QEg=','2018-05-31 19:50:22.084915','','','2018-05-28 17:49:05.000000','ops','运维管理','ops@youshutong.com',NULL,2,1,0,0,'2018-05-28 17:50:49.527729','2018-05-31 19:50:22.085366',0),(3,'pbkdf2_sha256$100000$S4VRDuZhNyX3$jPFezoftBvRboitvJGQMxjMbI/nP8GVPEi6MKkpms8Q=','2018-05-31 20:05:32.299378','','','2018-05-28 17:50:55.000000','hr','人事管理','hr@youshutong.com',NULL,3,1,0,0,'2018-05-28 17:51:13.312809','2018-05-31 20:05:32.300067',0),(4,'pbkdf2_sha256$100000$poLwmMEL6uxG$vNc+kvE+nGzsF2LymGU/pagXQGUeQfHVrs4KBS1gw6M=','2018-05-31 21:35:16.656591','','','2018-05-28 17:51:16.000000','scm','配置管理','scm@youshutong.com',NULL,4,1,0,0,'2018-05-28 17:51:32.312111','2018-05-31 21:35:16.657775',0),(5,'pbkdf2_sha256$100000$wDNSxcKnAcKu$TpR2/0MdnhNTan7CSfd5s3mtlrC8jDJw6J0zR8qLy1w=','2018-06-02 11:08:55.275013','','','2018-05-28 17:51:38.000000','webb','王先生','webb@youshutong.com',NULL,4,1,0,0,'2018-05-28 17:52:18.160496','2018-06-02 11:08:55.275542',0),(6,'pbkdf2_sha256$100000$DXWsA4qxxRhO$Op9uCWwCeYgYCR8Rer8ymGEUKrDVmvgvGhqlPOE0UFI=',NULL,'','','2018-05-28 17:52:22.000000','lilian','吴小姐','lilian@youshutong.com',NULL,3,1,0,0,'2018-05-28 17:52:49.951892','2018-05-30 21:52:08.303406',0),(7,'pbkdf2_sha256$100000$0u1qGXGsx0V1$HssOkV3IwQhHt9NchtifUkERntjPV3IamIFQeil5ByE=',NULL,'','','2018-05-28 17:52:53.000000','david','李先生','david@youshutong.com',NULL,2,1,0,0,'2018-05-28 17:53:22.150435','2018-05-30 21:52:27.644113',0);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_groups`
--

DROP TABLE IF EXISTS `user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `shutonguser_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_groups_shutonguser_id_group_id_4d07131e_uniq` (`shutonguser_id`,`group_id`),
  KEY `user_groups_group_id_b76f8aba_fk_auth_group_id` (`group_id`),
  CONSTRAINT `user_groups_group_id_b76f8aba_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_groups_shutonguser_id_5fcf9f19_fk_user_id` FOREIGN KEY (`shutonguser_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_groups`
--

LOCK TABLES `user_groups` WRITE;
/*!40000 ALTER TABLE `user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_user_permissions`
--

DROP TABLE IF EXISTS `user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `shutonguser_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_user_permissions_shutonguser_id_permission_id_c8fa6812_uniq` (`shutonguser_id`,`permission_id`),
  KEY `user_user_permission_permission_id_9deb68a3_fk_auth_perm` (`permission_id`),
  CONSTRAINT `user_user_permission_permission_id_9deb68a3_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_user_permissions_shutonguser_id_260a7f99_fk_user_id` FOREIGN KEY (`shutonguser_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_user_permissions`
--

LOCK TABLES `user_user_permissions` WRITE;
/*!40000 ALTER TABLE `user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-06-03  0:24:01
