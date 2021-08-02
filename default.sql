/*
 Navicat Premium Data Transfer

 Source Server         : 宝塔Mysql
 Source Server Type    : MySQL
 Source Server Version : 50644
 Source Host           : 127.0.0.1:3306
 Source Schema         : t2

 Target Server Type    : MySQL
 Target Server Version : 50644
 File Encoding         : 65001

 Date: 01/08/2021 22:01:41
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for account_apptoken
-- ----------------------------
DROP TABLE IF EXISTS `account_apptoken`;
CREATE TABLE `account_apptoken`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creator` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `app_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `token` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ticket_sn_prefix` varchar(20) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of account_apptoken
-- ----------------------------
INSERT INTO `account_apptoken` VALUES (1, 'admin', '2020-07-15 22:48:55.134791', '2021-07-31 15:55:26.211248', 1, 'ops', '4e57d414-c6aa-11ea-9ed0-784f437daad6', 'aaaa');
INSERT INTO `account_apptoken` VALUES (2, 'admin', '2020-10-07 22:18:52.426149', '2021-07-31 15:55:16.496517', 1, 'test', '069b4418-08a8-11eb-902e-acde48001122', 'sds');
INSERT INTO `account_apptoken` VALUES (3, 'admin', '2020-10-07 22:21:19.313968', '2021-07-31 15:55:20.556723', 1, 'test', '5e36d26e-08a8-11eb-8370-acde48001122', 'sdfsf');
INSERT INTO `account_apptoken` VALUES (4, 'admin', '2020-10-07 22:23:07.424740', '2021-07-31 15:55:10.249831', 1, 'eeee', '9ea72dc6-08a8-11eb-99fb-acde48001122', 'dfds');
INSERT INTO `account_apptoken` VALUES (5, 'admin', '2020-10-07 22:23:17.620953', '2020-10-07 22:41:33.710316', 1, 'fef', 'a4bb2d3e-08a8-11eb-8a91-acde48001122', 'fdef');
INSERT INTO `account_apptoken` VALUES (6, 'admin', '2021-07-30 18:50:30.182302', '2021-08-01 12:36:28.744045', 0, 'admin', 'f504e46a-f123-11eb-960b-f894c2bd30ac', 'Test');

-- ----------------------------
-- Table structure for account_loondept
-- ----------------------------
DROP TABLE IF EXISTS `account_loondept`;
CREATE TABLE `account_loondept`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `parent_dept_id` int(11) NOT NULL,
  `leader` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `approver` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `label` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `creator` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of account_loondept
-- ----------------------------
INSERT INTO `account_loondept` VALUES (1, '技术部', 0, 'aaaa', 'admin', '', '', '2020-07-13 00:00:00.000000', '2020-07-13 00:00:00.000000', 1);
INSERT INTO `account_loondept` VALUES (2, '教师部', 0, '20', '20', '', '', '2020-07-13 00:00:00.000000', '2020-07-13 00:00:00.000000', 0);
INSERT INTO `account_loondept` VALUES (3, '行政部111', 2, 'dfsf@163.com', 'admin,sss', 's\'s\'s', 'admin', '2020-10-07 10:17:11.265290', '2020-10-07 10:17:11.265389', 1);
INSERT INTO `account_loondept` VALUES (4, 'IT', 1, 'dfsf@163.com', 'aaaa,3333', 'sdfs', 'admin', '2020-10-07 10:18:39.932490', '2020-10-07 10:18:39.932591', 1);

-- ----------------------------
-- Table structure for account_loonrole
-- ----------------------------
DROP TABLE IF EXISTS `account_loonrole`;
CREATE TABLE `account_loonrole`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `description` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `label` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `creator` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of account_loonrole
-- ----------------------------
INSERT INTO `account_loonrole` VALUES (1, '223232', '1222333', '1333111', 'admin', '2020-07-22 23:49:48.688015', '2020-07-22 23:49:48.688619', 1);
INSERT INTO `account_loonrole` VALUES (2, 'te222', 'fds', 'dfs', 'admin', '2020-10-04 17:09:47.462589', '2020-10-04 17:09:47.462709', 1);

-- ----------------------------
-- Table structure for account_loonuser
-- ----------------------------
DROP TABLE IF EXISTS `account_loonuser`;
CREATE TABLE `account_loonuser`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `last_login` datetime(6) NULL DEFAULT NULL,
  `username` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `alias` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `phone` varchar(13) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `creator` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `username`(`username`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 23 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of account_loonuser
-- ----------------------------
INSERT INTO `account_loonuser` VALUES (1, 'pbkdf2_sha256$150000$nex53BPJ3f0T$jsJjWHmpVp11aIt7F8eyKVK2l+YjH8k0GP4oOQf8Jw4=', '2021-08-01 14:03:51.558185', 'admin', '超级管理员', 'admin@aa.com', '13888888888', 1, 'admin', '2020-07-13 06:55:33.427320', '2020-07-13 06:55:33.430436', 0, 2);
INSERT INTO `account_loonuser` VALUES (2, 'pbkdf2_sha256$150000$Fp4gFoZ5LvIQ$Nhr+cxIfX7pendx12iTieYTQbM58dsuwAEh6tFRq+uA=', NULL, 'aaaa', 'fdsfsf', 'aaa@163.com', '', 1, '', '2020-07-16 07:50:44.761354', '2020-07-16 07:50:44.765578', 1, 0);
INSERT INTO `account_loonuser` VALUES (3, 'pbkdf2_sha256$150000$Ey7I685mHKcU$ZR0vtbG1uSYbqw0Zxc+TQcKPOpYAsfLW4LIjHP55Iak=', NULL, 'bbb', '', 'bb@163.com', '', 1, '', '2020-07-16 07:55:04.142103', '2020-07-16 07:55:04.145527', 1, 2);
INSERT INTO `account_loonuser` VALUES (4, 'pbkdf2_sha256$150000$XF8kVVHNZYiR$9ayYeh83EGGvF5s1qN5VQx/RYW6ujA/2JGtgANvtYrQ=', NULL, 'dfsf@163.com', 'fdsfs', '22222@163.com', '', 1, 'admin', '2020-07-18 15:45:55.334270', '2020-10-01 10:49:53.418763', 1, 1);
INSERT INTO `account_loonuser` VALUES (6, 'pbkdf2_sha256$150000$KoiIowtSM5ZX$Rc8lE79tRlxOKU22v7dha56qtGATjAERevswh5g/+Io=', NULL, 'dsfsffsdf', 'fdsfs', '22222@163.com', '', 1, 'admin', '2020-07-18 15:46:28.852181', '2020-07-18 15:46:28.852531', 1, 1);
INSERT INTO `account_loonuser` VALUES (7, 'pbkdf2_sha256$150000$6IeqMYuSftxG$UKINFNV+Q+rYunH/htTlobQoAxT0fjuOE1Bm11ZLR0o=', NULL, 'dsddsdd', 'sssddd', '22222@163.com', '', 1, 'admin', '2020-07-18 15:51:53.984928', '2020-07-18 15:51:53.985039', 1, 2);
INSERT INTO `account_loonuser` VALUES (8, 'pbkdf2_sha256$150000$tW3g1qJTOwy6$2zlnzA+IdP5Oy+Y6NV5ik3ymXZmjHU2H+1EVssDZiAQ=', NULL, '3333', '3334444', 'sdfsf@11.com', '', 1, 'admin', '2020-07-18 15:52:07.648636', '2020-07-18 15:52:07.648742', 1, 0);
INSERT INTO `account_loonuser` VALUES (9, 'pbkdf2_sha256$150000$0fYUbCAGHeGB$w2gRFEy711XUlhHGrhQBJpi/6u9qjL7vitSfqPvMNSE=', NULL, 'sss', 'sfdsfs', '22222212@163.com', '', 1, 'admin', '2020-07-18 16:08:35.407578', '2020-07-18 16:08:35.407667', 1, 0);
INSERT INTO `account_loonuser` VALUES (10, 'pbkdf2_sha256$150000$i9YkFw57LRVg$zJiYWU6YU8BzHqTpZa2AZmAGe1ROrz41xnCnUcepnn4=', NULL, 'test1111', 'haha', 'sss@111.com', '', 0, 'admin', '2020-07-21 06:54:03.944318', '2020-07-21 06:54:03.944392', 1, 1);
INSERT INTO `account_loonuser` VALUES (11, 'pbkdf2_sha256$150000$IMpPp4THtW7n$QLv4QH89daAWF+D1XUNNJNm9PdyQuRmmBqjtwSJeyXE=', NULL, 'fdsfds', 'fdsfs', 'fsdfsfsf@13.com', '', 1, 'admin', '2020-09-21 07:25:49.543211', '2020-09-21 07:25:49.543231', 1, 0);
INSERT INTO `account_loonuser` VALUES (12, 'pbkdf2_sha256$150000$uhhAEFyioVD2$c2WHSiLpGS8HBivopq0zphvgek+Wnuak1dwyi2S+iyM=', NULL, '23424', '3242342', 'dfsdf@121.com', '', 1, 'admin', '2020-09-21 07:26:19.688074', '2020-09-21 07:26:19.688095', 1, 0);
INSERT INTO `account_loonuser` VALUES (13, '!uce2gIID0ESM0uf6MVcdauuhadTH460pWWYHvgpl', NULL, 'c\'x\'z', 'z\'x\'c\'z', 'ssss', 'sdfds', 0, 'admin', '2020-09-27 07:16:53.923734', '2020-09-27 07:16:53.924260', 1, 0);
INSERT INTO `account_loonuser` VALUES (15, '!CbDPN3BTa6NrPHyYaoQoBaB5SGho9sUNFCEdZk3R', NULL, 'd', 'sd', 'sd', 'sd', 0, 'admin', '2020-09-28 07:05:57.676251', '2020-09-28 07:05:57.676582', 1, 1);
INSERT INTO `account_loonuser` VALUES (16, '!YUKXMECfKP2otWhQD3NQpCYD0cCBfAs35stuA1Sh', NULL, 'fewf', 'fwd', 'fewf', 'dwf', 1, 'admin', '2020-09-28 07:08:34.885110', '2020-09-28 07:08:34.885428', 1, 1);
INSERT INTO `account_loonuser` VALUES (17, '!AZoAGIvCwPtUJU1yzXfNDwSCrBjTKbTnZSAF2CMX', NULL, 'fdsfwe', 'fes', 'dfsd', '21222', 1, 'admin', '2020-09-29 07:41:14.245816', '2020-09-29 07:41:14.246100', 1, 1);
INSERT INTO `account_loonuser` VALUES (18, 'pbkdf2_sha256$150000$zsaLy0SF7P1C$+JrbYQEGUYh9nA3P1ONd2M1/8WxJhWsBIdVWQD2OrB4=', '2021-08-01 12:39:42.218759', 'test', '张三同学', '123@qq.com', '', 1, 'admin', '2021-07-30 18:48:44.115806', '2021-07-30 18:48:44.115828', 0, 0);
INSERT INTO `account_loonuser` VALUES (19, 'pbkdf2_sha256$150000$sw27ozRTDD30$GDs61jA4DmRmbMpk6GmFrx7r7d2URK4LNxYM5ACjI4w=', '2021-07-31 18:45:43.758359', 'test2', '李四同学', '456@qq.com', '', 1, 'admin', '2021-07-30 22:09:27.339908', '2021-07-30 22:09:27.339933', 0, 0);
INSERT INTO `account_loonuser` VALUES (20, 'pbkdf2_sha256$150000$MUsUo1JEi29F$mRwo+uQTtpbSH7U6tNX7/v9ubRAxHN3fh2yUl+ep7Ys=', '2021-08-01 12:43:45.826265', 'laoshi', '老师A', '789@qq.com', '', 1, 'admin', '2021-07-31 11:34:03.279062', '2021-07-31 11:34:03.279087', 0, 1);
INSERT INTO `account_loonuser` VALUES (22, 'pbkdf2_sha256$150000$9ksZGOmkeYNz$moAaqZ8KZMdGpISu8oX17Q3X6C/iO5te5J9a2gdQ3fw=', NULL, 'laoshia', '老师A', '789@qq.com', '', 1, 'admin', '2021-07-31 11:34:14.989273', '2021-07-31 11:34:14.989297', 1, 1);

-- ----------------------------
-- Table structure for account_loonuserdept
-- ----------------------------
DROP TABLE IF EXISTS `account_loonuserdept`;
CREATE TABLE `account_loonuserdept`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creator` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `dept_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `account_loonuserdept_dept_id_ad142af8`(`dept_id`) USING BTREE,
  INDEX `account_loonuserdept_user_id_17ab09cb`(`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 22 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of account_loonuserdept
-- ----------------------------
INSERT INTO `account_loonuserdept` VALUES (1, 'admin', '2020-07-13 00:00:00.000000', '2020-07-13 00:00:00.000000', 0, 1, 1);
INSERT INTO `account_loonuserdept` VALUES (2, 'admin', '2020-07-13 00:00:00.000000', '2020-07-13 00:00:00.000000', 0, 2, 1);
INSERT INTO `account_loonuserdept` VALUES (3, '', '2020-07-18 15:46:28.862688', '2020-07-18 15:46:28.862806', 0, 1, 6);
INSERT INTO `account_loonuserdept` VALUES (4, '', '2020-07-18 15:46:28.863506', '2020-07-18 15:46:28.863627', 0, 2, 6);
INSERT INTO `account_loonuserdept` VALUES (5, '', '2020-07-18 15:51:53.991345', '2020-07-18 15:51:53.991440', 0, 1, 7);
INSERT INTO `account_loonuserdept` VALUES (6, '', '2020-07-18 15:52:07.653817', '2020-07-18 15:52:07.653913', 0, 2, 8);
INSERT INTO `account_loonuserdept` VALUES (7, '', '2020-07-18 16:08:35.413525', '2020-07-18 16:08:35.413671', 0, 1, 9);
INSERT INTO `account_loonuserdept` VALUES (8, '', '2020-07-20 07:59:55.939115', '2020-07-20 07:59:55.939207', 0, 1, 2);
INSERT INTO `account_loonuserdept` VALUES (9, '', '2020-07-20 07:59:55.939576', '2020-07-20 07:59:55.939646', 0, 2, 2);
INSERT INTO `account_loonuserdept` VALUES (10, '', '2020-07-21 06:54:03.951044', '2020-07-21 06:54:03.951179', 0, 2, 10);
INSERT INTO `account_loonuserdept` VALUES (11, '', '2020-09-21 07:25:49.546606', '2020-09-21 07:25:49.546641', 0, 2, 11);
INSERT INTO `account_loonuserdept` VALUES (12, '', '2020-09-21 07:26:19.691216', '2020-09-21 07:26:19.691242', 0, 2, 12);
INSERT INTO `account_loonuserdept` VALUES (13, '', '2020-09-27 07:16:53.959054', '2020-09-27 07:16:53.959722', 0, 1, 13);
INSERT INTO `account_loonuserdept` VALUES (14, '', '2020-09-28 07:05:57.689130', '2020-09-28 07:05:57.689660', 0, 1, 15);
INSERT INTO `account_loonuserdept` VALUES (15, '', '2020-09-28 07:08:34.896590', '2020-09-28 07:08:34.896876', 0, 2, 16);
INSERT INTO `account_loonuserdept` VALUES (16, '', '2020-09-28 07:08:34.898224', '2020-09-28 07:08:34.898496', 0, 1, 16);
INSERT INTO `account_loonuserdept` VALUES (17, '', '2020-09-29 07:41:14.260849', '2020-09-29 07:41:14.261150', 0, 1, 17);
INSERT INTO `account_loonuserdept` VALUES (18, '', '2021-07-30 18:48:44.119671', '2021-07-30 18:48:44.119695', 0, 2, 18);
INSERT INTO `account_loonuserdept` VALUES (19, '', '2021-07-30 22:09:27.342814', '2021-07-30 22:09:27.342849', 0, 2, 19);
INSERT INTO `account_loonuserdept` VALUES (20, '', '2021-07-31 11:34:14.992167', '2021-07-31 11:34:14.992193', 0, 2, 22);
INSERT INTO `account_loonuserdept` VALUES (21, '', '2021-07-31 11:38:48.040948', '2021-07-31 11:38:48.040970', 0, 2, 20);

-- ----------------------------
-- Table structure for account_loonuserrole
-- ----------------------------
DROP TABLE IF EXISTS `account_loonuserrole`;
CREATE TABLE `account_loonuserrole`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creator` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `user_id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of account_loonuserrole
-- ----------------------------
INSERT INTO `account_loonuserrole` VALUES (1, 'admin', '2020-10-01 16:46:36.870135', '2020-10-01 16:46:36.870239', 1, 1, 1);
INSERT INTO `account_loonuserrole` VALUES (2, 'admin', '2020-10-04 20:24:47.386282', '2020-10-04 20:24:47.386465', 1, 3, 1);
INSERT INTO `account_loonuserrole` VALUES (3, 'admin', '2020-10-04 22:02:45.379547', '2020-10-04 22:02:45.379837', 1, 2, 1);
INSERT INTO `account_loonuserrole` VALUES (4, 'admin', '2020-10-04 22:02:56.438357', '2020-10-04 22:02:56.438721', 0, 8, 1);
INSERT INTO `account_loonuserrole` VALUES (5, 'admin', '2020-10-04 22:04:06.550125', '2020-10-04 22:04:06.550495', 1, 12, 1);
INSERT INTO `account_loonuserrole` VALUES (6, 'admin', '2020-10-04 22:04:55.564884', '2020-10-04 22:04:55.565217', 1, 4, 1);
INSERT INTO `account_loonuserrole` VALUES (7, 'admin', '2020-10-04 22:05:00.620939', '2020-10-04 22:05:00.621249', 0, 9, 1);

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `name`(`name`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_group_permissions_group_id_permission_id_0cd325b0_uniq`(`group_id`, `permission_id`) USING BTREE,
  INDEX `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm`(`permission_id`) USING BTREE,
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `auth_permission_content_type_id_codename_01ab375a_uniq`(`content_type_id`, `codename`) USING BTREE,
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 104 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES (1, 'Can add log entry', 1, 'add_logentry');
INSERT INTO `auth_permission` VALUES (2, 'Can change log entry', 1, 'change_logentry');
INSERT INTO `auth_permission` VALUES (3, 'Can delete log entry', 1, 'delete_logentry');
INSERT INTO `auth_permission` VALUES (4, 'Can add group', 2, 'add_group');
INSERT INTO `auth_permission` VALUES (5, 'Can change group', 2, 'change_group');
INSERT INTO `auth_permission` VALUES (6, 'Can delete group', 2, 'delete_group');
INSERT INTO `auth_permission` VALUES (7, 'Can add permission', 3, 'add_permission');
INSERT INTO `auth_permission` VALUES (8, 'Can change permission', 3, 'change_permission');
INSERT INTO `auth_permission` VALUES (9, 'Can delete permission', 3, 'delete_permission');
INSERT INTO `auth_permission` VALUES (10, 'Can add content type', 4, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (11, 'Can change content type', 4, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (12, 'Can delete content type', 4, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (13, 'Can add session', 5, 'add_session');
INSERT INTO `auth_permission` VALUES (14, 'Can change session', 5, 'change_session');
INSERT INTO `auth_permission` VALUES (15, 'Can delete session', 5, 'delete_session');
INSERT INTO `auth_permission` VALUES (16, 'Can add 用户角色', 6, 'add_loonuserrole');
INSERT INTO `auth_permission` VALUES (17, 'Can change 用户角色', 6, 'change_loonuserrole');
INSERT INTO `auth_permission` VALUES (18, 'Can delete 用户角色', 6, 'delete_loonuserrole');
INSERT INTO `auth_permission` VALUES (19, 'Can add 角色', 7, 'add_loonrole');
INSERT INTO `auth_permission` VALUES (20, 'Can change 角色', 7, 'change_loonrole');
INSERT INTO `auth_permission` VALUES (21, 'Can delete 角色', 7, 'delete_loonrole');
INSERT INTO `auth_permission` VALUES (22, 'Can add 部门', 8, 'add_loondept');
INSERT INTO `auth_permission` VALUES (23, 'Can change 部门', 8, 'change_loondept');
INSERT INTO `auth_permission` VALUES (24, 'Can delete 部门', 8, 'delete_loondept');
INSERT INTO `auth_permission` VALUES (25, 'Can add 用户', 9, 'add_loonuser');
INSERT INTO `auth_permission` VALUES (26, 'Can change 用户', 9, 'change_loonuser');
INSERT INTO `auth_permission` VALUES (27, 'Can delete 用户', 9, 'delete_loonuser');
INSERT INTO `auth_permission` VALUES (28, 'Can add ticket record', 10, 'add_ticketrecord');
INSERT INTO `auth_permission` VALUES (29, 'Can change ticket record', 10, 'change_ticketrecord');
INSERT INTO `auth_permission` VALUES (30, 'Can delete ticket record', 10, 'delete_ticketrecord');
INSERT INTO `auth_permission` VALUES (31, 'Can add ticket state last man', 11, 'add_ticketstatelastman');
INSERT INTO `auth_permission` VALUES (32, 'Can change ticket state last man', 11, 'change_ticketstatelastman');
INSERT INTO `auth_permission` VALUES (33, 'Can delete ticket state last man', 11, 'delete_ticketstatelastman');
INSERT INTO `auth_permission` VALUES (34, 'Can add ticket custom field', 12, 'add_ticketcustomfield');
INSERT INTO `auth_permission` VALUES (35, 'Can change ticket custom field', 12, 'change_ticketcustomfield');
INSERT INTO `auth_permission` VALUES (36, 'Can delete ticket custom field', 12, 'delete_ticketcustomfield');
INSERT INTO `auth_permission` VALUES (37, 'Can add ticket flow log', 13, 'add_ticketflowlog');
INSERT INTO `auth_permission` VALUES (38, 'Can change ticket flow log', 13, 'change_ticketflowlog');
INSERT INTO `auth_permission` VALUES (39, 'Can delete ticket flow log', 13, 'delete_ticketflowlog');
INSERT INTO `auth_permission` VALUES (40, 'Can add custom notice', 14, 'add_customnotice');
INSERT INTO `auth_permission` VALUES (41, 'Can change custom notice', 14, 'change_customnotice');
INSERT INTO `auth_permission` VALUES (42, 'Can delete custom notice', 14, 'delete_customnotice');
INSERT INTO `auth_permission` VALUES (43, 'Can add workflow script', 15, 'add_workflowscript');
INSERT INTO `auth_permission` VALUES (44, 'Can change workflow script', 15, 'change_workflowscript');
INSERT INTO `auth_permission` VALUES (45, 'Can delete workflow script', 15, 'delete_workflowscript');
INSERT INTO `auth_permission` VALUES (46, 'Can add custom field', 16, 'add_customfield');
INSERT INTO `auth_permission` VALUES (47, 'Can change custom field', 16, 'change_customfield');
INSERT INTO `auth_permission` VALUES (48, 'Can delete custom field', 16, 'delete_customfield');
INSERT INTO `auth_permission` VALUES (49, 'Can add state', 17, 'add_state');
INSERT INTO `auth_permission` VALUES (50, 'Can change state', 17, 'change_state');
INSERT INTO `auth_permission` VALUES (51, 'Can delete state', 17, 'delete_state');
INSERT INTO `auth_permission` VALUES (52, 'Can add workflow', 18, 'add_workflow');
INSERT INTO `auth_permission` VALUES (53, 'Can change workflow', 18, 'change_workflow');
INSERT INTO `auth_permission` VALUES (54, 'Can delete workflow', 18, 'delete_workflow');
INSERT INTO `auth_permission` VALUES (55, 'Can add transition', 19, 'add_transition');
INSERT INTO `auth_permission` VALUES (56, 'Can change transition', 19, 'change_transition');
INSERT INTO `auth_permission` VALUES (57, 'Can delete transition', 19, 'delete_transition');
INSERT INTO `auth_permission` VALUES (58, 'Can add 调用token', 20, 'add_apptoken');
INSERT INTO `auth_permission` VALUES (59, 'Can change 调用token', 20, 'change_apptoken');
INSERT INTO `auth_permission` VALUES (60, 'Can delete 调用token', 20, 'delete_apptoken');
INSERT INTO `auth_permission` VALUES (61, 'Can add ticket user', 21, 'add_ticketuser');
INSERT INTO `auth_permission` VALUES (62, 'Can change ticket user', 21, 'change_ticketuser');
INSERT INTO `auth_permission` VALUES (63, 'Can delete ticket user', 21, 'delete_ticketuser');
INSERT INTO `auth_permission` VALUES (64, 'Can add workflow admin', 22, 'add_workflowadmin');
INSERT INTO `auth_permission` VALUES (65, 'Can change workflow admin', 22, 'change_workflowadmin');
INSERT INTO `auth_permission` VALUES (66, 'Can delete workflow admin', 22, 'delete_workflowadmin');
INSERT INTO `auth_permission` VALUES (67, 'Can view log entry', 1, 'view_logentry');
INSERT INTO `auth_permission` VALUES (68, 'Can view permission', 3, 'view_permission');
INSERT INTO `auth_permission` VALUES (69, 'Can view group', 2, 'view_group');
INSERT INTO `auth_permission` VALUES (70, 'Can view content type', 4, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (71, 'Can view session', 5, 'view_session');
INSERT INTO `auth_permission` VALUES (72, 'Can view loon user', 9, 'view_loonuser');
INSERT INTO `auth_permission` VALUES (73, 'Can view app token', 20, 'view_apptoken');
INSERT INTO `auth_permission` VALUES (74, 'Can view loon dept', 8, 'view_loondept');
INSERT INTO `auth_permission` VALUES (75, 'Can view loon role', 7, 'view_loonrole');
INSERT INTO `auth_permission` VALUES (76, 'Can view loon user role', 6, 'view_loonuserrole');
INSERT INTO `auth_permission` VALUES (77, 'Can add loon user dept', 23, 'add_loonuserdept');
INSERT INTO `auth_permission` VALUES (78, 'Can change loon user dept', 23, 'change_loonuserdept');
INSERT INTO `auth_permission` VALUES (79, 'Can delete loon user dept', 23, 'delete_loonuserdept');
INSERT INTO `auth_permission` VALUES (80, 'Can view loon user dept', 23, 'view_loonuserdept');
INSERT INTO `auth_permission` VALUES (81, 'Can view 工单自定义字段', 12, 'view_ticketcustomfield');
INSERT INTO `auth_permission` VALUES (82, 'Can view 工单流转日志', 13, 'view_ticketflowlog');
INSERT INTO `auth_permission` VALUES (83, 'Can view 工单记录', 10, 'view_ticketrecord');
INSERT INTO `auth_permission` VALUES (84, 'Can view ticket user', 21, 'view_ticketuser');
INSERT INTO `auth_permission` VALUES (85, 'Can view 工作流自定义字段', 16, 'view_customfield');
INSERT INTO `auth_permission` VALUES (86, 'Can view custom notice', 14, 'view_customnotice');
INSERT INTO `auth_permission` VALUES (87, 'Can view 工作流状态', 17, 'view_state');
INSERT INTO `auth_permission` VALUES (88, 'Can view 工作流流转', 19, 'view_transition');
INSERT INTO `auth_permission` VALUES (89, 'Can view 工作流', 18, 'view_workflow');
INSERT INTO `auth_permission` VALUES (90, 'Can view workflow admin', 22, 'view_workflowadmin');
INSERT INTO `auth_permission` VALUES (91, 'Can view 工作流脚本', 15, 'view_workflowscript');
INSERT INTO `auth_permission` VALUES (92, 'Can add loon user dept11', 24, 'add_loonuserdept11');
INSERT INTO `auth_permission` VALUES (93, 'Can change loon user dept11', 24, 'change_loonuserdept11');
INSERT INTO `auth_permission` VALUES (94, 'Can delete loon user dept11', 24, 'delete_loonuserdept11');
INSERT INTO `auth_permission` VALUES (95, 'Can view loon user dept11', 24, 'view_loonuserdept11');
INSERT INTO `auth_permission` VALUES (96, 'Can add app token workflow', 25, 'add_apptokenworkflow');
INSERT INTO `auth_permission` VALUES (97, 'Can change app token workflow', 25, 'change_apptokenworkflow');
INSERT INTO `auth_permission` VALUES (98, 'Can delete app token workflow', 25, 'delete_apptokenworkflow');
INSERT INTO `auth_permission` VALUES (99, 'Can view app token workflow', 25, 'view_apptokenworkflow');
INSERT INTO `auth_permission` VALUES (100, 'Can add workflow user permission', 26, 'add_workflowuserpermission');
INSERT INTO `auth_permission` VALUES (101, 'Can change workflow user permission', 26, 'change_workflowuserpermission');
INSERT INTO `auth_permission` VALUES (102, 'Can delete workflow user permission', 26, 'delete_workflowuserpermission');
INSERT INTO `auth_permission` VALUES (103, 'Can view workflow user permission', 26, 'view_workflowuserpermission');

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NULL,
  `object_repr` varchar(200) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL,
  `change_message` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `content_type_id` int(11) NULL DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `django_admin_log_content_type_id_c4bce8eb_fk_django_co`(`content_type_id`) USING BTREE,
  INDEX `django_admin_log_user_id_c564eba6_fk_account_loonuser_id`(`user_id`) USING BTREE,
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_account_loonuser_id` FOREIGN KEY (`user_id`) REFERENCES `account_loonuser` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `model` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `django_content_type_app_label_model_76bd3d3b_uniq`(`app_label`, `model`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 27 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES (20, 'account', 'apptoken');
INSERT INTO `django_content_type` VALUES (25, 'account', 'apptokenworkflow');
INSERT INTO `django_content_type` VALUES (8, 'account', 'loondept');
INSERT INTO `django_content_type` VALUES (7, 'account', 'loonrole');
INSERT INTO `django_content_type` VALUES (9, 'account', 'loonuser');
INSERT INTO `django_content_type` VALUES (23, 'account', 'loonuserdept');
INSERT INTO `django_content_type` VALUES (24, 'account', 'loonuserdept11');
INSERT INTO `django_content_type` VALUES (6, 'account', 'loonuserrole');
INSERT INTO `django_content_type` VALUES (1, 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES (2, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (3, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (4, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (5, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (12, 'ticket', 'ticketcustomfield');
INSERT INTO `django_content_type` VALUES (13, 'ticket', 'ticketflowlog');
INSERT INTO `django_content_type` VALUES (10, 'ticket', 'ticketrecord');
INSERT INTO `django_content_type` VALUES (11, 'ticket', 'ticketstatelastman');
INSERT INTO `django_content_type` VALUES (21, 'ticket', 'ticketuser');
INSERT INTO `django_content_type` VALUES (16, 'workflow', 'customfield');
INSERT INTO `django_content_type` VALUES (14, 'workflow', 'customnotice');
INSERT INTO `django_content_type` VALUES (17, 'workflow', 'state');
INSERT INTO `django_content_type` VALUES (19, 'workflow', 'transition');
INSERT INTO `django_content_type` VALUES (18, 'workflow', 'workflow');
INSERT INTO `django_content_type` VALUES (22, 'workflow', 'workflowadmin');
INSERT INTO `django_content_type` VALUES (15, 'workflow', 'workflowscript');
INSERT INTO `django_content_type` VALUES (26, 'workflow', 'workflowuserpermission');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 88 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES (2, 'contenttypes', '0001_initial', '2018-04-10 16:23:41.088822');
INSERT INTO `django_migrations` VALUES (5, 'contenttypes', '0002_remove_content_type_name', '2018-04-10 16:23:41.316210');
INSERT INTO `django_migrations` VALUES (6, 'auth', '0001_initial', '2018-04-10 16:23:41.492653');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0002_alter_permission_name_max_length', '2018-04-10 16:23:41.536426');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0003_alter_user_email_max_length', '2018-04-10 16:23:41.555765');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0004_alter_user_username_opts', '2018-04-10 16:23:41.579352');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0005_alter_user_last_login_null', '2018-04-10 16:23:41.616306');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0006_require_contenttypes_0002', '2018-04-10 16:23:41.620447');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0007_alter_validators_add_error_messages', '2018-04-10 16:23:41.643171');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0008_alter_user_username_max_length', '2018-04-10 16:23:41.663023');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0009_alter_user_last_name_max_length', '2018-04-10 16:23:41.679754');
INSERT INTO `django_migrations` VALUES (15, 'sessions', '0001_initial', '2018-04-10 16:23:41.711283');
INSERT INTO `django_migrations` VALUES (16, 'ticket', '0001_initial', '2018-04-10 16:23:41.848590');
INSERT INTO `django_migrations` VALUES (17, 'workflow', '0001_initial', '2018-04-10 16:23:41.994564');
INSERT INTO `django_migrations` VALUES (18, 'ticket', '0002_auto_20180410_1749', '2018-04-10 17:49:06.562710');
INSERT INTO `django_migrations` VALUES (19, 'workflow', '0002_auto_20180410_1749', '2018-04-10 17:49:06.690036');
INSERT INTO `django_migrations` VALUES (21, 'ticket', '0003_ticketrecord_relation', '2018-04-15 17:21:55.494957');
INSERT INTO `django_migrations` VALUES (22, 'ticket', '0004_auto_20180417_2348', '2018-04-17 23:48:22.378917');
INSERT INTO `django_migrations` VALUES (23, 'workflow', '0003_auto_20180417_2348', '2018-04-17 23:48:22.391679');
INSERT INTO `django_migrations` VALUES (24, 'ticket', '0005_auto_20180418_0001', '2018-04-18 00:01:52.296081');
INSERT INTO `django_migrations` VALUES (25, 'workflow', '0004_workflow_view_permission_check', '2018-04-22 15:58:37.766199');
INSERT INTO `django_migrations` VALUES (26, 'workflow', '0005_auto_20180423_2114', '2018-04-23 21:14:51.345960');
INSERT INTO `django_migrations` VALUES (27, 'workflow', '0006_auto_20180423_2116', '2018-04-23 21:17:03.970113');
INSERT INTO `django_migrations` VALUES (28, 'workflow', '0007_auto_20180424_0656', '2018-04-24 06:56:48.399867');
INSERT INTO `django_migrations` VALUES (29, 'workflow', '0008_auto_20180424_0708', '2018-04-24 07:08:53.913939');
INSERT INTO `django_migrations` VALUES (30, 'workflow', '0009_auto_20180430_2129', '2018-04-30 21:29:29.307194');
INSERT INTO `django_migrations` VALUES (31, 'ticket', '0006_auto_20180505_1549', '2018-05-05 15:49:16.131657');
INSERT INTO `django_migrations` VALUES (32, 'workflow', '0010_auto_20180505_1549', '2018-05-05 15:49:16.168741');
INSERT INTO `django_migrations` VALUES (33, 'workflow', '0011_auto_20180509_0709', '2018-05-09 07:09:37.847547');
INSERT INTO `django_migrations` VALUES (34, 'workflow', '0012_auto_20180511_0654', '2018-05-11 06:54:50.920765');
INSERT INTO `django_migrations` VALUES (35, 'ticket', '0007_auto_20180516_0741', '2018-05-16 07:46:02.412425');
INSERT INTO `django_migrations` VALUES (36, 'ticket', '0008_auto_20180516_0743', '2018-05-16 07:46:02.417966');
INSERT INTO `django_migrations` VALUES (37, 'workflow', '0013_auto_20180511_1826', '2018-05-16 07:46:02.420751');
INSERT INTO `django_migrations` VALUES (38, 'workflow', '0014_auto_20180516_0741', '2018-05-16 07:46:02.423199');
INSERT INTO `django_migrations` VALUES (39, 'ticket', '0009_ticketflowlog_intervene_type_id', '2018-05-17 06:36:01.493028');
INSERT INTO `django_migrations` VALUES (40, 'ticket', '0010_ticketcustomfield_multi_username_value', '2018-05-22 06:46:49.124237');
INSERT INTO `django_migrations` VALUES (41, 'workflow', '0015_auto_20180522_0646', '2018-05-22 06:46:49.132266');
INSERT INTO `django_migrations` VALUES (42, 'workflow', '0016_auto_20180620_1709', '2018-07-30 07:21:05.079135');
INSERT INTO `django_migrations` VALUES (43, 'workflow', '0017_auto_20180730_0720', '2018-07-30 07:21:05.193141');
INSERT INTO `django_migrations` VALUES (44, 'ticket', '0011_ticketrecord_script_run_last_result', '2018-08-09 07:32:10.254032');
INSERT INTO `django_migrations` VALUES (45, 'workflow', '0018_auto_20180809_0732', '2018-08-09 07:32:10.374771');
INSERT INTO `django_migrations` VALUES (46, 'ticket', '0012_delete_ticketstatelastman', '2018-08-12 16:58:07.510558');
INSERT INTO `django_migrations` VALUES (47, 'workflow', '0019_state_remember_last_man_enable', '2018-08-12 16:58:07.598511');
INSERT INTO `django_migrations` VALUES (50, 'workflow', '0020_workflow_limit_expression', '2018-08-24 07:39:19.095010');
INSERT INTO `django_migrations` VALUES (51, 'workflow', '0021_customnotice', '2018-08-26 10:30:18.818854');
INSERT INTO `django_migrations` VALUES (52, 'ticket', '0013_ticketrecord_is_end', '2018-09-26 06:53:40.535144');
INSERT INTO `django_migrations` VALUES (53, 'workflow', '0022_auto_20180926_0653', '2018-09-26 06:53:40.625847');
INSERT INTO `django_migrations` VALUES (54, 'workflow', '0023_auto_20181001_1012', '2018-10-01 10:12:52.255104');
INSERT INTO `django_migrations` VALUES (56, 'ticket', '0014_auto_20181003_1708', '2018-10-03 17:08:44.788212');
INSERT INTO `django_migrations` VALUES (57, 'workflow', '0024_auto_20181003_1708', '2018-10-03 17:08:44.885439');
INSERT INTO `django_migrations` VALUES (58, 'workflow', '0025_transition_condition_expression', '2018-10-06 17:03:26.434330');
INSERT INTO `django_migrations` VALUES (61, 'auth', '0010_alter_group_name_max_length', '2020-05-24 22:37:33.755398');
INSERT INTO `django_migrations` VALUES (62, 'auth', '0011_update_proxy_permissions', '2020-05-24 22:37:33.783096');
INSERT INTO `django_migrations` VALUES (63, 'ticket', '0002_auto_20200524_2236', '2020-05-24 22:37:33.790575');
INSERT INTO `django_migrations` VALUES (65, 'ticket', '0003_auto_20200709_0721', '2020-07-09 07:24:04.657405');
INSERT INTO `django_migrations` VALUES (66, 'workflow', '0002_auto_20200709_0721', '2020-07-09 07:24:04.660250');
INSERT INTO `django_migrations` VALUES (78, 'account', '0001_initial', '2020-07-13 06:53:51.327909');
INSERT INTO `django_migrations` VALUES (79, 'account', '0002_auto_20200716_0738', '2020-07-16 07:38:46.281028');
INSERT INTO `django_migrations` VALUES (80, 'account', '0003_remove_loonuserdept_primary', '2020-07-18 15:48:19.038239');
INSERT INTO `django_migrations` VALUES (81, 'ticket', '0004_auto_20200815_1603', '2020-08-15 16:03:58.284651');
INSERT INTO `django_migrations` VALUES (82, 'workflow', '0003_auto_20200815_1603', '2020-08-15 16:03:58.428618');
INSERT INTO `django_migrations` VALUES (83, 'workflow', '0004_auto_20200824_2346', '2020-08-24 23:47:03.053224');
INSERT INTO `django_migrations` VALUES (84, 'workflow', '0005_auto_20200904_0716', '2020-09-04 07:17:05.466431');
INSERT INTO `django_migrations` VALUES (85, 'account', '0004_auto_20201011_0953', '2020-10-11 09:53:59.483137');
INSERT INTO `django_migrations` VALUES (86, 'account', '0005_delete_apptokenworkflow', '2020-10-11 16:45:22.704833');
INSERT INTO `django_migrations` VALUES (87, 'workflow', '0006_workflowuserpermission', '2020-10-11 16:45:22.746102');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session`  (
  `session_key` varchar(40) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `session_data` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`) USING BTREE,
  INDEX `django_session_expire_date_a5c62663`(`expire_date`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of django_session
-- ----------------------------
INSERT INTO `django_session` VALUES ('0tb984v0tgzt96htu2v9l0liwtevzypc', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 12:04:08.848816');
INSERT INTO `django_session` VALUES ('166q1hn5a4phhxmz5v0zxol1ukz1xt90', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 21:16:11.827876');
INSERT INTO `django_session` VALUES ('1ut6zqv587m0o9v92p9uo37j2cwzwnm4', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 12:29:46.306746');
INSERT INTO `django_session` VALUES ('1vk7k3b6bshxfh48y65b8bgujhooquwy', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-12-08 07:01:03.970216');
INSERT INTO `django_session` VALUES ('1y65zkmbewrhmg5k9tsd1f7vwcpcp2di', 'ZWQ0YzhmMWYzOTZlZWViZTI1Y2U3ZWNmZmFjMDM1ODg2NjQ0MmRjMzp7Il9hdXRoX3VzZXJfaGFzaCI6ImJlOTIwNWY0NzE1MzlkMjBiODRjNTUyNGMyNTAxYTkwYWNlMDRmNzMiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-05-21 23:23:56.544517');
INSERT INTO `django_session` VALUES ('2ixontmwlf3hm2fx2kj5i0sv4dv5ivn5', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-10-22 22:32:56.563563');
INSERT INTO `django_session` VALUES ('2p4bd3iu2iz6cakbxn9hamdvqp3fvx7y', 'MWUzZjFjNThjNmM1MmRlMWIzYjY0NDFiODNlODE3MDIzMjQ2NGQwYzp7Il9hdXRoX3VzZXJfaGFzaCI6IjQ2MTUwYzAwNmQyNGM0Y2QyNzQ5Zjc2NGE4N2MzZDNlNjY0ZDA5NzgiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2018-05-06 15:24:30.402451');
INSERT INTO `django_session` VALUES ('2z5h72g5xwd90cippnk3i4l2h54j4hi7', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-10-20 10:32:47.096928');
INSERT INTO `django_session` VALUES ('3obnksz4pvo8qu4dgy8r8ho5rfjyh6p2', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 12:14:15.396388');
INSERT INTO `django_session` VALUES ('3uh7w46snn2gc9xfwxrfxz3vudrfnayq', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 10:31:02.274415');
INSERT INTO `django_session` VALUES ('443zt1x4linfe3q3m8le9799cizpxedv', 'NTU1NDRhMGM1MDIyMDczYmFlY2MzZDdkZTMyYWZlYmYyMGRiMzhiNDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2019-10-04 15:15:48.843348');
INSERT INTO `django_session` VALUES ('48n6uqarrd4r28j7fkamhjj2ouih60ao', 'MWM5NmI5ZDEzYmY1ZTBkNzg5MTU5NzcxOWRmMWQ1NTE1NDQyNWJjYTp7Il9hdXRoX3VzZXJfaGFzaCI6ImJlOTIwNWY0NzE1MzlkMjBiODRjNTUyNGMyNTAxYTkwYWNlMDRmNzMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2020-01-07 15:28:56.444956');
INSERT INTO `django_session` VALUES ('4i8xz7bou6zcdi1iuptcm32yvs4l4ito', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 15:53:26.088744');
INSERT INTO `django_session` VALUES ('5b02s2ugjxrijqyf2zsk34y9gld6hmr0', 'NTkxZTY3NWI3N2IyMjNhYjRhYTk1YzJlZmI1NzUyYWRiYWVlYzVlMDp7Il9hdXRoX3VzZXJfaWQiOiIxOCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZDI1OTYwZjY0MjcwNmVjOTY0MGU5OTExYTRmZTczMDJmNjAwNDhjZiJ9', '2021-08-15 12:27:36.675943');
INSERT INTO `django_session` VALUES ('5dmaj0cvo999lzh9fm8mwxdhtocfh81i', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 11:30:20.304501');
INSERT INTO `django_session` VALUES ('6ripe53gt6cx97zsc98t9six73h3kuvi', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 13:48:32.816065');
INSERT INTO `django_session` VALUES ('6v8g5swfqi3730d43lvnc5wcvza9sema', 'ZDZmODM5ZWE3NjU3ZDNmNDhmYWNmYWIwNmY2YzFhOGZmNzFiNWZjNzp7Il9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9oYXNoIjoiNzViMTVmZDNhZTdjYzAxMGVhNWUwN2U2OGViZDEwOTI1YzcxMTQyNiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2018-11-14 15:51:42.081978');
INSERT INTO `django_session` VALUES ('7ooloj2vtmn9bf9a2kduu6n769hcbtu8', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-11-10 06:55:03.630203');
INSERT INTO `django_session` VALUES ('89kmd057jlu3esdskgxd96sfova1eysn', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 15:47:53.156848');
INSERT INTO `django_session` VALUES ('89n6o9o1ievv8jp7c75ezg59wz6dz26q', 'M2EwMmViZmQyZDAxZmU2NmE2Njg4OWYxNzk3ZDVkY2E1NmM0NzNiYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2020-01-30 20:06:35.406507');
INSERT INTO `django_session` VALUES ('89uapbpezlpv0ew0nprpon5v0udfpl72', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 16:52:53.635015');
INSERT INTO `django_session` VALUES ('8dmqa9gzarnvpt98w3xybsawanwt68vc', 'M2EwMmViZmQyZDAxZmU2NmE2Njg4OWYxNzk3ZDVkY2E1NmM0NzNiYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-03-12 07:23:34.068060');
INSERT INTO `django_session` VALUES ('8rrkvw86grfrvnmzkdl5w6iuvz2l08av', 'YjY0NDc0MzQxZWY3YjhkZTlhYzZjMGRiYTgyZDIyNDJmNTI4MjIyNjp7Il9hdXRoX3VzZXJfaWQiOiIyMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNTkzOTJhZTdhNzJiODY3NDBkODgwYjU4YjFmMDNhYmEzMDhmMTJmYiJ9', '2021-08-14 13:51:04.384678');
INSERT INTO `django_session` VALUES ('9581mn1ohbahki3dw0tmijima73xprsy', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 19:27:48.186010');
INSERT INTO `django_session` VALUES ('95dcf2q1a67ynb3pqfaw0u09bzr7nlyi', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 15:44:18.246589');
INSERT INTO `django_session` VALUES ('9cr064a9i4i8ocwjen8zu0tgu1jto0m0', 'ODFmY2RiYTVlMTg0YTU1NzVjYzQwMWJjNGVmNTY4Zjg3MTQyODBjMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4NWMxYWFmMjUwZTIxZTBkOWIwN2Y1YTMzYzY3YTI3YTFiNzRkZGYyIn0=', '2020-06-11 07:31:35.429840');
INSERT INTO `django_session` VALUES ('9ko305jzr9h33vxuajbuxhqt9minkdfw', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 10:12:42.378263');
INSERT INTO `django_session` VALUES ('9lfhc7o23502ik23g9j2w29qge2kfypa', 'NGI1NWJiMTFiODAwZTI1M2RmZWQ5Mzg0OWVmYTIzY2U0ZjUzZWNmYTp7Il9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NWIxNWZkM2FlN2NjMDEwZWE1ZTA3ZTY4ZWJkMTA5MjVjNzExNDI2In0=', '2018-11-14 15:48:39.149124');
INSERT INTO `django_session` VALUES ('9mbkw2ze1mc9iowqzvdhd5sq9dnnbqzh', 'YjY0NDc0MzQxZWY3YjhkZTlhYzZjMGRiYTgyZDIyNDJmNTI4MjIyNjp7Il9hdXRoX3VzZXJfaWQiOiIyMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNTkzOTJhZTdhNzJiODY3NDBkODgwYjU4YjFmMDNhYmEzMDhmMTJmYiJ9', '2021-08-15 12:43:45.828857');
INSERT INTO `django_session` VALUES ('9ramvh4gbvkqdaika3gnfv2hk6ph0xqh', 'OWQ5MzU4ODg1Y2I2ZTU3MGIxZmQyZTZkYzIwNDE0YjkxMGU3NGI4Mjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwMTY3OTkzZTg4NzYyZTc3MGYxOWEwYjgyNGRiMGYzNTdkMTBlMDE4In0=', '2020-07-27 07:34:06.377455');
INSERT INTO `django_session` VALUES ('9xwrn8z21q7s4tshhu4vhik5n3hawjud', 'M2EwMmViZmQyZDAxZmU2NmE2Njg4OWYxNzk3ZDVkY2E1NmM0NzNiYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-12-19 20:40:37.899320');
INSERT INTO `django_session` VALUES ('a49vbr4suoa0gcpjzxl9qj0hjzgl8ase', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 16:53:01.688370');
INSERT INTO `django_session` VALUES ('aa8lsabc1g5i96vmj2hggsowtkkit4dg', 'ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=', '2020-04-25 18:23:39.580583');
INSERT INTO `django_session` VALUES ('ad0vu3brcz9mhn171f7tjlh4klanzu7m', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-10-20 10:32:44.346912');
INSERT INTO `django_session` VALUES ('at72hz9jaq28uxqvei1u11kj1n9dv430', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 19:50:31.927615');
INSERT INTO `django_session` VALUES ('awas6cfmsg1r42hmdgvgo3tr0uyy1t9q', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 21:58:58.496599');
INSERT INTO `django_session` VALUES ('b8uwt83znx1zsxe915v7mfijkmz6ggm7', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 15:47:36.574031');
INSERT INTO `django_session` VALUES ('bawbzn9jp5kt7h0c4124tmwgrwpbl1e7', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 19:44:05.095742');
INSERT INTO `django_session` VALUES ('bbaubm3jdamoffnrmdx3e9mpqocz2a36', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 16:08:21.455257');
INSERT INTO `django_session` VALUES ('bbnyl8qgsl2jyfwhhib5o73wfqx90mvc', 'NGJhZGE3MjdhM2Q1MjhkMWI4NzdjYmQ1NjJiODYxYzAyM2YwMmRiZDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NWI3NzlmMDhmYjhiMmFhYzk0Y2U5YTA0NzBiZWIzMzg1NzIxOGY3In0=', '2020-07-23 07:01:14.115619');
INSERT INTO `django_session` VALUES ('bd4e3qkwf91tusabodfa8tu23175m4qh', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-11-10 06:55:04.048666');
INSERT INTO `django_session` VALUES ('bno7ij876udj7w54vmd7tvht9ny1hnrq', 'YjMwNjMxNDcwNmIwZjRkYjJkNzM2ZDg3MzVmNzg3NDgzZjQ3ZGYzYzp7Il9hdXRoX3VzZXJfaWQiOiIxOSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMjA0MDI4NWJjNTkzMWQ3MjhjYzZjYTVjN2Q0YmY0ODdkODlkOGY5NSJ9', '2021-08-13 22:09:41.247665');
INSERT INTO `django_session` VALUES ('bty41t7n46im6yjf819w5q9k20ux3win', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 20:07:33.587535');
INSERT INTO `django_session` VALUES ('bzg1408jk06vn7gsnavpxpm8tgf2tq2f', 'MWM5NmI5ZDEzYmY1ZTBkNzg5MTU5NzcxOWRmMWQ1NTE1NDQyNWJjYTp7Il9hdXRoX3VzZXJfaGFzaCI6ImJlOTIwNWY0NzE1MzlkMjBiODRjNTUyNGMyNTAxYTkwYWNlMDRmNzMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2019-03-26 14:22:53.391084');
INSERT INTO `django_session` VALUES ('bzssijhverz5rl2pkrshnx52qp1ecib2', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 18:47:55.312206');
INSERT INTO `django_session` VALUES ('cc6v8vs443jhidzfv7tefxc9cndds1ww', 'ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=', '2019-02-26 07:20:43.624282');
INSERT INTO `django_session` VALUES ('cs39dxyyrbu8af246qllzy63dsu7aez4', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 16:52:43.065634');
INSERT INTO `django_session` VALUES ('cxzrjh2kuwgwlw65sq0hnnrk9csnxkmb', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 10:11:49.929623');
INSERT INTO `django_session` VALUES ('d07zkxf8epcywscjy89fiw59mg8gkn4p', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 13:02:48.541457');
INSERT INTO `django_session` VALUES ('djoz8epllmzhsubw4hu62we8bw4c7jvx', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 21:16:11.914530');
INSERT INTO `django_session` VALUES ('dowrdibpfgi174db4mbb6k73yulsznod', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 18:58:24.856414');
INSERT INTO `django_session` VALUES ('edxm373im5em912x6r1mmk89hvxzonaw', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 19:04:56.479794');
INSERT INTO `django_session` VALUES ('eo6muu7ned7a1paps99j0nng37pbsm4a', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 10:27:44.987161');
INSERT INTO `django_session` VALUES ('eyoe9bj29jnk3hrjwjj7el4z7uamuv8j', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-12-08 07:01:03.461217');
INSERT INTO `django_session` VALUES ('f4hd9p8zexyrmofk24ur6qjep0z37kz9', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-15 14:03:51.560926');
INSERT INTO `django_session` VALUES ('fbn2u5kckn39qgyxh5pwyaqtbf7mh12j', 'NTkxZTY3NWI3N2IyMjNhYjRhYTk1YzJlZmI1NzUyYWRiYWVlYzVlMDp7Il9hdXRoX3VzZXJfaWQiOiIxOCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZDI1OTYwZjY0MjcwNmVjOTY0MGU5OTExYTRmZTczMDJmNjAwNDhjZiJ9', '2021-08-15 12:39:42.221246');
INSERT INTO `django_session` VALUES ('fp4zkhd8cgfj6tacff6giqm75wwd4p93', 'NTU1NDRhMGM1MDIyMDczYmFlY2MzZDdkZTMyYWZlYmYyMGRiMzhiNDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2018-08-20 07:12:12.680740');
INSERT INTO `django_session` VALUES ('fpo7585kck0te2u04ic28y7mx07g84z2', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 21:57:07.192358');
INSERT INTO `django_session` VALUES ('fv5q5bk1frmuabfx2xlppidy87v20v2t', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 15:54:10.890207');
INSERT INTO `django_session` VALUES ('fxdc90snam1vje7bpv3wiafwu9pooeyk', 'M2EwMmViZmQyZDAxZmU2NmE2Njg4OWYxNzk3ZDVkY2E1NmM0NzNiYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2018-07-17 07:04:43.733996');
INSERT INTO `django_session` VALUES ('fyfwfspu9mxy8x8zt0pdq2y1g9onorwn', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 19:18:21.756942');
INSERT INTO `django_session` VALUES ('g2xrvclza9noaxtq1uyr97bt976snvod', 'ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=', '2019-02-10 17:28:03.379373');
INSERT INTO `django_session` VALUES ('gfya6uejeijn56h754e3kdkp431pu0s4', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 11:27:56.600252');
INSERT INTO `django_session` VALUES ('gi4p54ka4u6vww4kpqogolmdquj52wup', 'YTQyMzg3NzMzMzRkZDgxNzU1YWM1OTE3YWExZTFjMDdlMWZmNzM5Zjp7Il9hdXRoX3VzZXJfaGFzaCI6IjQ2MTUwYzAwNmQyNGM0Y2QyNzQ5Zjc2NGE4N2MzZDNlNjY0ZDA5NzgiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2018-04-24 21:38:48.844698');
INSERT INTO `django_session` VALUES ('gpy4b940016fb6suzh7til0j2sgamgwq', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-08-14 20:35:48.629380');
INSERT INTO `django_session` VALUES ('gwwul2nmxqyrdzx1wbej4uj0ahzsdwow', 'YmI5MjhmNmQ3YzFjMjM3ZjgwYTg4ZmRkMjk1MmU0ZGU5ZjI4Nzg0Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=', '2018-10-28 16:07:27.753614');
INSERT INTO `django_session` VALUES ('gzl1ecffierqrmrauvc28ptvgody5wij', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 19:32:06.126399');
INSERT INTO `django_session` VALUES ('h7i2xkk181sk6inahviq9uynm675wdny', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-11-03 06:57:03.149193');
INSERT INTO `django_session` VALUES ('hhgqxdf0hdc8ocy6egn2ggzfdic75vee', 'ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=', '2020-04-26 18:46:49.543046');
INSERT INTO `django_session` VALUES ('hky74jwmjxa283tpu34hmos1oy4a45aw', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 15:00:56.326432');
INSERT INTO `django_session` VALUES ('hlize0igljpdnym3rqudskfxl2dqzb3k', 'ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=', '2020-05-15 07:58:42.170778');
INSERT INTO `django_session` VALUES ('hrlydq4fee0v11nq15ixcf2c2b8cd64h', 'YjY0NDc0MzQxZWY3YjhkZTlhYzZjMGRiYTgyZDIyNDJmNTI4MjIyNjp7Il9hdXRoX3VzZXJfaWQiOiIyMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNTkzOTJhZTdhNzJiODY3NDBkODgwYjU4YjFmMDNhYmEzMDhmMTJmYiJ9', '2021-08-14 11:34:40.140688');
INSERT INTO `django_session` VALUES ('hvb5c793uti85osewkkaxd997rg8l5ax', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 15:52:02.382384');
INSERT INTO `django_session` VALUES ('ikpnzy0jsc0jiede5r6cxhoyagq2payb', 'YTQyMzg3NzMzMzRkZDgxNzU1YWM1OTE3YWExZTFjMDdlMWZmNzM5Zjp7Il9hdXRoX3VzZXJfaGFzaCI6IjQ2MTUwYzAwNmQyNGM0Y2QyNzQ5Zjc2NGE4N2MzZDNlNjY0ZDA5NzgiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2018-04-24 21:36:50.610586');
INSERT INTO `django_session` VALUES ('ilfuodquvht8pnxm0mzmxakbvp7z4wny', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 13:50:22.413580');
INSERT INTO `django_session` VALUES ('j1oted0vp31mgcfqy2g4q08issfnw6gm', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 13:10:15.883494');
INSERT INTO `django_session` VALUES ('jnd3hk7qjask3mnk7m96vqtpecw0zbvb', 'M2EwMmViZmQyZDAxZmU2NmE2Njg4OWYxNzk3ZDVkY2E1NmM0NzNiYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-08-23 11:30:02.254886');
INSERT INTO `django_session` VALUES ('jw2psatj7z4zrur42urk3wluopurpqr1', 'YmI5MjhmNmQ3YzFjMjM3ZjgwYTg4ZmRkMjk1MmU0ZGU5ZjI4Nzg0Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=', '2018-10-21 19:52:52.775319');
INSERT INTO `django_session` VALUES ('jxylntmexpile98og8k5lfzfovkybi8u', 'YmI5MjhmNmQ3YzFjMjM3ZjgwYTg4ZmRkMjk1MmU0ZGU5ZjI4Nzg0Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=', '2019-05-02 06:44:06.734299');
INSERT INTO `django_session` VALUES ('kg8r2wz1n498cp6hvo0c0h5z3r9r98q4', 'ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=', '2020-04-20 20:52:09.179185');
INSERT INTO `django_session` VALUES ('kjlggcmh3exerlwysdryf7flevqmy2jq', 'MWJjYzQ4N2JlMGVmMjkyMjljOTEyZTRjNTg2NzY4YTdhOTFmOTE3Yjp7Il9hdXRoX3VzZXJfaGFzaCI6ImU4ZTc4MmE5YTU2OWU0MjRjZjgwMGM1MTFjMjViY2JiN2FhMjhhZGEiLCJfYXV0aF91c2VyX2lkIjoiOSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-11-17 23:25:30.724572');
INSERT INTO `django_session` VALUES ('kkij8defjj21v1tritqk13edxcvrqmvy', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-11-24 06:59:36.803728');
INSERT INTO `django_session` VALUES ('l187tcfmtjwn2yvr407elnm51dqmaa0u', 'YmI5MjhmNmQ3YzFjMjM3ZjgwYTg4ZmRkMjk1MmU0ZGU5ZjI4Nzg0Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=', '2018-08-13 07:21:42.060139');
INSERT INTO `django_session` VALUES ('lk3sd5w2d6w4g6p53ddc5y9946c1a413', 'ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=', '2018-12-11 07:10:11.233169');
INSERT INTO `django_session` VALUES ('lujtvklj4m0y5g8tktlx5r8djkt1c4yb', 'ZWQ0YzhmMWYzOTZlZWViZTI1Y2U3ZWNmZmFjMDM1ODg2NjQ0MmRjMzp7Il9hdXRoX3VzZXJfaGFzaCI6ImJlOTIwNWY0NzE1MzlkMjBiODRjNTUyNGMyNTAxYTkwYWNlMDRmNzMiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-12-01 23:47:26.990998');
INSERT INTO `django_session` VALUES ('m06alvw9jdi5g69rwxhk4b5pw04g4ag7', 'ODFmY2RiYTVlMTg0YTU1NzVjYzQwMWJjNGVmNTY4Zjg3MTQyODBjMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4NWMxYWFmMjUwZTIxZTBkOWIwN2Y1YTMzYzY3YTI3YTFiNzRkZGYyIn0=', '2020-06-27 20:19:06.371907');
INSERT INTO `django_session` VALUES ('m5ztgt89x6o2fyiyc05h3dejr1yj3jqo', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 10:30:09.714487');
INSERT INTO `django_session` VALUES ('n1qedk10gs28ks03d0ozoxdb60yc894g', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 13:37:48.911494');
INSERT INTO `django_session` VALUES ('n22ajtmchkt90lljw3f1t9iahaqcdrnm', 'ODFmY2RiYTVlMTg0YTU1NzVjYzQwMWJjNGVmNTY4Zjg3MTQyODBjMTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI4NWMxYWFmMjUwZTIxZTBkOWIwN2Y1YTMzYzY3YTI3YTFiNzRkZGYyIn0=', '2020-06-16 06:45:47.434338');
INSERT INTO `django_session` VALUES ('n2hfc5zo3skkvc28jelcfu5x6s573wqa', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 22:05:55.844599');
INSERT INTO `django_session` VALUES ('ndrq0vkh9c7el36372vdnpjrq9gzdmgb', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 22:40:49.671194');
INSERT INTO `django_session` VALUES ('ni55h8okvt9xkki8ga876iyv6ukv3ddo', 'YjY0NDc0MzQxZWY3YjhkZTlhYzZjMGRiYTgyZDIyNDJmNTI4MjIyNjp7Il9hdXRoX3VzZXJfaWQiOiIyMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNTkzOTJhZTdhNzJiODY3NDBkODgwYjU4YjFmMDNhYmEzMDhmMTJmYiJ9', '2021-08-15 12:29:51.117746');
INSERT INTO `django_session` VALUES ('njocgkycetbpxy6uwxevnlnym75fc9ae', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 22:08:47.162499');
INSERT INTO `django_session` VALUES ('nucorj97xbfojfy3j8xrm2cm0a50evtp', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 19:48:04.678661');
INSERT INTO `django_session` VALUES ('obsuhola6a6sgdqbdccd8ye1e807e8te', 'NTU1NDRhMGM1MDIyMDczYmFlY2MzZDdkZTMyYWZlYmYyMGRiMzhiNDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2019-12-08 10:13:39.832179');
INSERT INTO `django_session` VALUES ('oj3syswyxxx7uav23hs911ipc0br1u92', 'ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=', '2020-04-18 18:35:47.306348');
INSERT INTO `django_session` VALUES ('ouhbjbt6mtbmv10jv2feogteuc5rgemg', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 11:33:40.255230');
INSERT INTO `django_session` VALUES ('ovxzxgg507qeixgbvqvq79epgiidwqi9', 'ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=', '2019-05-31 15:13:51.502976');
INSERT INTO `django_session` VALUES ('owlrvg9mccecpbhjfbmdijlo6n2peoa2', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-10-22 22:32:56.080055');
INSERT INTO `django_session` VALUES ('owm2fbdfsrumq18zekbp0zampcwotnq9', 'ZWQ0YzhmMWYzOTZlZWViZTI1Y2U3ZWNmZmFjMDM1ODg2NjQ0MmRjMzp7Il9hdXRoX3VzZXJfaGFzaCI6ImJlOTIwNWY0NzE1MzlkMjBiODRjNTUyNGMyNTAxYTkwYWNlMDRmNzMiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-10-07 17:19:59.997301');
INSERT INTO `django_session` VALUES ('pat2k571ihnse2hvlm6u4mqrp8v6e4wh', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 15:41:46.815174');
INSERT INTO `django_session` VALUES ('phjijmbxop4lp7go5q5hgvuon2xksd6a', 'ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=', '2020-04-25 10:21:25.512714');
INSERT INTO `django_session` VALUES ('plmt7utkqsu7qx2wttrt9dvuvmrytwdl', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 19:43:28.437137');
INSERT INTO `django_session` VALUES ('pmqevxllprbv7q78r0qbfjp2h6iqnjgd', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 17:00:45.782207');
INSERT INTO `django_session` VALUES ('pntloe7q7yzqfkcm0kqzcr3g3jvj20ph', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 19:14:20.769003');
INSERT INTO `django_session` VALUES ('qd0dhjm1eqhu6rsy8lm8yspm24bg5fah', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-11-03 06:57:03.317167');
INSERT INTO `django_session` VALUES ('qkjvfwq4i5uz0ctjsacz8r8h5f57mz16', 'MWM5NmI5ZDEzYmY1ZTBkNzg5MTU5NzcxOWRmMWQ1NTE1NDQyNWJjYTp7Il9hdXRoX3VzZXJfaGFzaCI6ImJlOTIwNWY0NzE1MzlkMjBiODRjNTUyNGMyNTAxYTkwYWNlMDRmNzMiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2019-11-23 16:38:31.799104');
INSERT INTO `django_session` VALUES ('qrugroidqpdoepvimz4mtqrsw8elq3px', 'M2EwMmViZmQyZDAxZmU2NmE2Njg4OWYxNzk3ZDVkY2E1NmM0NzNiYjp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2018-06-06 09:50:27.154850');
INSERT INTO `django_session` VALUES ('qxk62g7rwusghocw9u4ngw19k8ytcaky', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 20:32:41.279979');
INSERT INTO `django_session` VALUES ('qxmqja4mrajv6hmcgxy0mbfrf0lhk8ap', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 20:27:42.861099');
INSERT INTO `django_session` VALUES ('rhy3t0ut1v8ev1bqja8sql9htybr95k7', 'NTU1NDRhMGM1MDIyMDczYmFlY2MzZDdkZTMyYWZlYmYyMGRiMzhiNDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2018-09-05 07:18:38.000344');
INSERT INTO `django_session` VALUES ('rq6afbvp5ag5ftezg16ba3qb32nhtq5y', 'YmI5MjhmNmQ3YzFjMjM3ZjgwYTg4ZmRkMjk1MmU0ZGU5ZjI4Nzg0Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=', '2019-10-28 15:20:04.381595');
INSERT INTO `django_session` VALUES ('s9elc56k3l0r6m0w0ab5dexnuxylllrc', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-11-03 06:57:03.525007');
INSERT INTO `django_session` VALUES ('sauc3urt72eb1osf801xff1dbc88q44i', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 20:53:33.674842');
INSERT INTO `django_session` VALUES ('sdnytru1oj6p8kpy6y9zchz8vxi30p5p', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-11-24 06:59:36.537690');
INSERT INTO `django_session` VALUES ('se5gk1o2ciox9vhqi7mb76d6237blgwt', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 19:41:16.339816');
INSERT INTO `django_session` VALUES ('smsfh5eygpb822yn3s1c0g47fveq6jv1', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 16:48:36.417684');
INSERT INTO `django_session` VALUES ('ssy34uijm6rw6augk2nx4vlzlo8iu8py', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 19:39:42.719235');
INSERT INTO `django_session` VALUES ('svnhzwfovvsn5p4x7o4xmqir13bkj23u', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-12-08 07:01:03.561301');
INSERT INTO `django_session` VALUES ('syj6nzjnhnfyt216xx3h12vz48fp6ysy', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 17:02:36.113165');
INSERT INTO `django_session` VALUES ('t529jbyo4qvfk5qryov2jrvmqx1sm95y', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 15:26:44.173349');
INSERT INTO `django_session` VALUES ('tjknon6ymtu49mn6mijhgd4rdq1brbs1', 'NTkxZTY3NWI3N2IyMjNhYjRhYTk1YzJlZmI1NzUyYWRiYWVlYzVlMDp7Il9hdXRoX3VzZXJfaWQiOiIxOCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiZDI1OTYwZjY0MjcwNmVjOTY0MGU5OTExYTRmZTczMDJmNjAwNDhjZiJ9', '2021-08-13 22:02:18.231749');
INSERT INTO `django_session` VALUES ('toag0i2r7g5hpbzkvpuimu3kpfrskk1e', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 09:44:30.888875');
INSERT INTO `django_session` VALUES ('twba284uxsu2ijb95ws4wp259vj0mi9g', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 21:16:11.867715');
INSERT INTO `django_session` VALUES ('typtdmajweiszjxl0qfi005gew30om3x', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 22:04:51.393772');
INSERT INTO `django_session` VALUES ('u1hmwiwj7izvwnrhllkk7iju6xstgiak', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 20:43:46.209288');
INSERT INTO `django_session` VALUES ('u3ccxsvpklu3umsaa8f0sy1bagh3813m', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 09:57:26.822615');
INSERT INTO `django_session` VALUES ('u6ajtwkt000z632l1cbw1sfycv5ij80j', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-10-04 22:17:49.413496');
INSERT INTO `django_session` VALUES ('u8cwzypgqxxefgsnaqwfezxyx3wof9pj', 'YjY0NDc0MzQxZWY3YjhkZTlhYzZjMGRiYTgyZDIyNDJmNTI4MjIyNjp7Il9hdXRoX3VzZXJfaWQiOiIyMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiNTkzOTJhZTdhNzJiODY3NDBkODgwYjU4YjFmMDNhYmEzMDhmMTJmYiJ9', '2021-08-14 15:02:03.345964');
INSERT INTO `django_session` VALUES ('uc120vlnss4jhy3i8kxow00uqbozf6m4', 'ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=', '2018-05-23 06:56:36.173728');
INSERT INTO `django_session` VALUES ('uo7kcl3nolb5hi95e32tp7rgg3zt820j', 'NTU1NDRhMGM1MDIyMDczYmFlY2MzZDdkZTMyYWZlYmYyMGRiMzhiNDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2019-01-27 15:55:29.014400');
INSERT INTO `django_session` VALUES ('uoi4cbhlba7iskcp1yty57rhb7blwav8', 'NTU1NDRhMGM1MDIyMDczYmFlY2MzZDdkZTMyYWZlYmYyMGRiMzhiNDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2019-06-15 16:16:15.853121');
INSERT INTO `django_session` VALUES ('v5js0l5la617b973ib4gp5qr9i1y3h3m', 'ZDZmODM5ZWE3NjU3ZDNmNDhmYWNmYWIwNmY2YzFhOGZmNzFiNWZjNzp7Il9hdXRoX3VzZXJfaWQiOiI4IiwiX2F1dGhfdXNlcl9oYXNoIjoiNzViMTVmZDNhZTdjYzAxMGVhNWUwN2U2OGViZDEwOTI1YzcxMTQyNiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2018-11-14 15:47:30.453740');
INSERT INTO `django_session` VALUES ('v5sw3zyxvlfb38n6kdqgv870ja21c692', 'ZWQ0YzhmMWYzOTZlZWViZTI1Y2U3ZWNmZmFjMDM1ODg2NjQ0MmRjMzp7Il9hdXRoX3VzZXJfaGFzaCI6ImJlOTIwNWY0NzE1MzlkMjBiODRjNTUyNGMyNTAxYTkwYWNlMDRmNzMiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-09-07 10:22:52.001363');
INSERT INTO `django_session` VALUES ('vbilufkem68jwqfki1n2czznznjrm0xd', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 12:19:08.230461');
INSERT INTO `django_session` VALUES ('vfet6rpq8v3cf8q2snjqasp56t5mk7bh', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-08-28 09:41:32.755572');
INSERT INTO `django_session` VALUES ('wr3brfyg056entiteumea6sgwvtdiwi0', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-12-08 07:01:03.457139');
INSERT INTO `django_session` VALUES ('wzsw1jekty6312454wpgy50ojwzj8b8w', 'YmI5MjhmNmQ3YzFjMjM3ZjgwYTg4ZmRkMjk1MmU0ZGU5ZjI4Nzg0Mjp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=', '2018-11-28 23:44:17.536284');
INSERT INTO `django_session` VALUES ('x2bb8rj0b7gkdd8zzs2qpmqbp1qskl28', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-11-24 06:59:37.139488');
INSERT INTO `django_session` VALUES ('x3s6nbkrjx7m7kpb8zorzvaqqo19lkqm', 'ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=', '2020-06-07 17:49:02.144519');
INSERT INTO `django_session` VALUES ('xfumcxgwujjg5pczqltbzbwu42bwo8c4', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-13 18:53:57.997540');
INSERT INTO `django_session` VALUES ('xjsbhzbqt0b4e6mee6jt80d3l9k9cy84', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-12-08 07:01:04.519791');
INSERT INTO `django_session` VALUES ('xri4fxmn0mnbiqel4n5xu2agw3rqe9kz', 'ZGM2OGMzMDU3NDBkMTFhY2ViMjNlZjRhNWQyNDRhOTUxNGExNjQ4Mzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJiZTkyMDVmNDcxNTM5ZDIwYjg0YzU1MjRjMjUwMWE5MGFjZTA0ZjczIn0=', '2019-11-26 17:56:10.530875');
INSERT INTO `django_session` VALUES ('yp4eflhf4z6ryg43yfp103j3e1jlprp5', 'ZWQ0YzhmMWYzOTZlZWViZTI1Y2U3ZWNmZmFjMDM1ODg2NjQ0MmRjMzp7Il9hdXRoX3VzZXJfaGFzaCI6ImJlOTIwNWY0NzE1MzlkMjBiODRjNTUyNGMyNTAxYTkwYWNlMDRmNzMiLCJfYXV0aF91c2VyX2lkIjoiMSIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIn0=', '2019-06-29 18:15:12.485234');
INSERT INTO `django_session` VALUES ('yqo3dtnk8pasr19u3qwkgz4bvpv0yg08', 'NTU1NDRhMGM1MDIyMDczYmFlY2MzZDdkZTMyYWZlYmYyMGRiMzhiNDp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmU5MjA1ZjQ3MTUzOWQyMGI4NGM1NTI0YzI1MDFhOTBhY2UwNGY3MyIsIl9hdXRoX3VzZXJfaWQiOiIxIn0=', '2018-05-28 10:04:09.557125');
INSERT INTO `django_session` VALUES ('zaewvjgfzeo085bk65usxwd70zwch1fs', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2020-11-10 06:55:03.901421');
INSERT INTO `django_session` VALUES ('ze2ea0rbv1ghf4whr71uhtpua67jcwva', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 13:11:20.237898');
INSERT INTO `django_session` VALUES ('zgon0ur5zun4hbumqlp9v9in0yqay2or', 'ZTk1ZTgyYjRiNjNlZGQ2ODExY2M1OTg5NzYzMzExOGI1N2MyYjcxNzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MjQ1ZmIxZTE4MGU1ZWVjYjAxNTFiZTM2MTE5ZmI0NjFiZWRmMzUxIn0=', '2021-08-14 10:32:00.164829');

-- ----------------------------
-- Table structure for ticket_ticketcustomfield
-- ----------------------------
DROP TABLE IF EXISTS `ticket_ticketcustomfield`;
CREATE TABLE `ticket_ticketcustomfield`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `ticket_id` int(11) NOT NULL,
  `field_key` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `field_type_id` int(11) NOT NULL,
  `char_value` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `int_value` int(11) NOT NULL,
  `float_value` double NOT NULL,
  `bool_value` tinyint(1) NOT NULL,
  `date_value` date NOT NULL,
  `datetime_value` datetime(6) NOT NULL,
  `time_value` time(6) NOT NULL,
  `radio_value` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `checkbox_value` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `select_value` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `multi_select_value` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `text_value` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `username_value` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `creator` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `multi_username_value` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_ticket_field`(`ticket_id`, `field_key`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 669 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of ticket_ticketcustomfield
-- ----------------------------
INSERT INTO `ticket_ticketcustomfield` VALUES (14, '请假类型', 13, 'leave_type', 40, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '2', '', '', '', '', 'admin', '2018-05-13 21:53:15.776693', '2018-05-13 21:53:15.776753', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (15, '代理人', 13, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'zhangsan', 'admin', '2018-05-13 21:53:15.784787', '2018-05-13 21:53:15.784839', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (16, '请假原因及相关附件', 13, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '去喝喜酒', '', 'admin', '2018-05-13 21:53:15.792655', '2018-05-13 21:53:15.792711', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (17, '开始时间', 13, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-04-10 09:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-05-13 21:53:15.800632', '2018-05-13 21:53:15.800683', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (18, '请假天数(0.5的倍数)', 13, 'leave_days', 5, '3', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-05-13 21:53:15.809216', '2018-05-13 21:53:15.809266', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (19, '结束时间', 13, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-04-12 18:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-05-13 21:53:15.817437', '2018-05-13 21:53:15.817484', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (20, '代理人', 14, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'zhangsan1', 'admin', '2018-05-13 22:24:41.969926', '2018-05-13 22:24:41.969982', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (21, '请假天数(0.5的倍数)', 14, 'leave_days', 5, '3', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-05-13 22:24:41.978508', '2018-05-13 22:24:41.978600', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (22, '开始时间', 14, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-05-10 09:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-05-13 22:24:41.988270', '2018-05-13 22:24:41.988346', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (23, '请假类型', 14, 'leave_type', 40, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '1', '', '', '', '', 'admin', '2018-05-13 22:24:41.997839', '2018-05-13 22:24:41.997891', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (24, '结束时间', 14, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-05-13 09:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-05-13 22:24:42.008241', '2018-05-13 22:24:42.008292', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (25, '请假原因及相关附件', 14, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '喝喜酒', '', 'admin', '2018-05-13 22:24:42.016808', '2018-05-13 22:24:42.016898', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (26, '结束时间', 15, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-05-13 09:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-05-13 22:28:21.643297', '2018-05-13 22:28:21.643346', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (27, '请假原因及相关附件', 15, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '喝喜酒', '', 'admin', '2018-05-13 22:28:21.650778', '2018-05-13 22:28:21.650828', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (28, '代理人', 15, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'zhangsan1', 'admin', '2018-05-13 22:28:21.659327', '2018-05-13 22:28:21.659375', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (29, '请假天数(0.5的倍数)', 15, 'leave_days', 5, '3', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-05-13 22:28:21.667908', '2018-05-13 22:28:21.667955', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (30, '开始时间', 15, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-05-10 09:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-05-13 22:28:21.675754', '2018-05-13 22:28:21.675803', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (31, '请假类型', 15, 'leave_type', 40, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '1', '', '', '', '', 'admin', '2018-05-13 22:28:21.683366', '2018-05-13 22:28:21.683414', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (32, '结束时间', 16, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-04-12 18:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-05-13 22:34:12.690959', '2018-05-13 22:34:12.691033', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (33, '请假原因及相关附件', 16, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '去喝喜酒', '', 'admin', '2018-05-13 22:34:12.701832', '2018-05-13 22:34:12.701889', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (34, '代理人', 16, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'zhangsan', 'admin', '2018-05-13 22:34:12.711844', '2018-05-13 22:34:12.711905', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (35, '请假天数(0.5的倍数)', 16, 'leave_days', 5, '3', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-05-13 22:34:12.721909', '2018-05-13 22:34:12.721966', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (36, '开始时间', 16, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-04-10 09:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-05-13 22:34:12.730191', '2018-05-13 22:34:12.730245', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (37, '请假类型', 16, 'leave_type', 40, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '2', '', '', '', '', 'admin', '2018-05-13 22:34:12.741366', '2018-05-13 22:34:12.741426', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (38, '申请原因', 17, 'vpn_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '在家办公', '', 'admin', '2018-05-15 07:16:38.326174', '2018-05-15 07:16:38.326274', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (39, '申请原因', 18, 'vpn_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '在家办公', '', 'admin', '2018-05-15 07:37:28.008199', '2018-05-15 07:37:28.008245', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (40, '请假天数(0.5的倍数)', 19, 'leave_days', 5, '2', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-10-19 00:08:40.397150', '2018-10-19 00:08:40.397166', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (41, '请假类型', 19, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '2', '', '', '', '', '', 'admin', '2018-10-19 00:08:40.402913', '2018-10-19 00:08:40.402928', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (42, '开始时间', 19, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-10-20 09:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-10-19 00:08:40.408762', '2018-10-19 00:08:40.408775', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (43, '请假原因及相关附件', 19, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>teste</p>', '', 'admin', '2018-10-19 00:08:40.413509', '2018-10-19 00:08:40.413529', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (44, '结束时间', 19, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-10-21 18:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-10-19 00:08:40.419809', '2018-10-19 00:08:40.419833', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (45, '代理人', 19, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'admin', 'admin', '2018-10-19 00:08:40.425879', '2018-10-19 00:08:40.425895', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (46, '结束时间', 20, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-10-20 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-10-19 00:38:41.367687', '2018-10-19 00:38:41.367703', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (47, '开始时间', 20, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-10-19 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-10-19 00:38:41.372330', '2018-10-19 00:38:41.372352', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (48, '代理人', 20, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'admin', 'admin', '2018-10-19 00:38:41.376402', '2018-10-19 00:38:41.376417', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (49, '请假天数(0.5的倍数)', 20, 'leave_days', 5, '2', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-10-19 00:38:41.379313', '2018-10-19 00:38:41.379327', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (50, '请假类型', 20, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '2', '', '', '', '', '', 'admin', '2018-10-19 00:38:41.383436', '2018-10-19 00:38:41.383450', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (51, '请假原因及相关附件', 20, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>dfsf</p>', '', 'admin', '2018-10-19 00:38:41.387250', '2018-10-19 00:38:41.387266', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (52, '项目标识', 21, 'project_code', 5, 'prj001', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-10-21 11:14:37.680365', '2018-10-21 11:14:37.680400', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (53, '项目开发人员', 21, 'project_devs', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'admin', 'admin', '2018-10-21 11:14:37.686541', '2018-10-21 11:14:37.686575', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (54, '项目测试人员', 21, 'project_qas', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'admin', 'admin', '2018-10-21 11:14:37.692349', '2018-10-21 11:14:37.692382', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (55, '请假原因及相关附件', 22, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>ddd</p>', '', 'admin', '2018-10-22 07:12:16.466886', '2018-10-22 07:12:16.466914', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (56, '请假天数(0.5的倍数)', 22, 'leave_days', 5, '1', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-10-22 07:12:16.472163', '2018-10-22 07:12:16.472181', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (57, '请假类型', 22, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '3', '', '', '', '', '', 'admin', '2018-10-22 07:12:16.477751', '2018-10-22 07:12:16.477769', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (58, '开始时间', 22, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-10-22 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-10-22 07:12:16.481785', '2018-10-22 07:12:16.481810', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (59, '代理人', 22, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'admin', 'admin', '2018-10-22 07:12:16.485136', '2018-10-22 07:12:16.485153', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (60, '结束时间', 22, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-10-23 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-10-22 07:12:16.489084', '2018-10-22 07:12:16.489109', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (61, '请假原因及相关附件', 23, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>te</p>', '', 'admin', '2018-10-22 08:05:37.200981', '2018-10-22 08:05:37.201000', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (62, '请假天数(0.5的倍数)', 23, 'leave_days', 5, '2', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-10-22 08:05:37.204565', '2018-10-22 08:05:37.204582', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (63, '请假类型', 23, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '3', '', '', '', '', '', 'admin', '2018-10-22 08:05:37.207974', '2018-10-22 08:05:37.207991', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (64, '开始时间', 23, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-10-22 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-10-22 08:05:37.212592', '2018-10-22 08:05:37.212654', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (65, '代理人', 23, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'admin', 'admin', '2018-10-22 08:05:37.217232', '2018-10-22 08:05:37.217251', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (66, '结束时间', 23, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-10-24 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-10-22 08:05:37.221150', '2018-10-22 08:05:37.221170', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (67, '请假原因及相关附件', 24, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>11</p>', '', 'admin', '2018-11-27 07:09:06.342895', '2018-11-27 07:09:06.342911', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (68, '请假天数(0.5的倍数)', 24, 'leave_days', 5, '1', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:09:06.348005', '2018-11-27 07:09:06.348020', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (69, '请假类型', 24, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', 'admin', '2018-11-27 07:09:06.351837', '2018-11-27 07:09:06.351853', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (70, '代理人', 24, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'admin', 'admin', '2018-11-27 07:09:06.355020', '2018-11-27 07:09:06.355035', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (71, '开始时间', 24, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-11-27 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:09:06.358199', '2018-11-27 07:09:06.358214', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (72, '结束时间', 24, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-11-28 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:09:06.362700', '2018-11-27 07:09:06.362715', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (73, '请假原因及相关附件', 25, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>111</p>', '', 'admin', '2018-11-27 07:12:27.937822', '2018-11-27 07:12:27.937842', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (74, '请假天数(0.5的倍数)', 25, 'leave_days', 5, '1', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:12:27.943184', '2018-11-27 07:12:27.943204', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (75, '请假类型', 25, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', 'admin', '2018-11-27 07:12:27.947050', '2018-11-27 07:12:27.947069', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (76, '代理人', 25, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'admin', 'admin', '2018-11-27 07:12:27.950977', '2018-11-27 07:12:27.951038', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (77, '开始时间', 25, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-11-27 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:12:27.954845', '2018-11-27 07:12:27.954863', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (78, '结束时间', 25, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-11-28 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:12:27.958336', '2018-11-27 07:12:27.958353', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (79, '开始时间', 26, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-11-27 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:14:06.394830', '2018-11-27 07:14:06.394870', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (80, '代理人', 26, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'admin', 'admin', '2018-11-27 07:14:06.401115', '2018-11-27 07:14:06.401155', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (81, '请假原因及相关附件', 26, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>111</p>', '', 'admin', '2018-11-27 07:14:06.408893', '2018-11-27 07:14:06.408933', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (82, '结束时间', 26, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-11-28 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:14:06.416352', '2018-11-27 07:14:06.416392', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (83, '请假天数(0.5的倍数)', 26, 'leave_days', 5, '1', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:14:06.423573', '2018-11-27 07:14:06.423612', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (84, '请假类型', 26, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', 'admin', '2018-11-27 07:14:06.430362', '2018-11-27 07:14:06.430401', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (85, '请假原因及相关附件', 27, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>111</p>', '', 'admin', '2018-11-27 07:20:16.259524', '2018-11-27 07:20:16.259781', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (86, '开始时间', 27, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-11-27 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:20:16.291175', '2018-11-27 07:20:16.291268', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (87, '请假天数(0.5的倍数)', 27, 'leave_days', 5, '1', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:20:16.317001', '2018-11-27 07:20:16.317439', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (88, '代理人', 27, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'admin', 'admin', '2018-11-27 07:20:16.336555', '2018-11-27 07:20:16.336888', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (89, '结束时间', 27, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-11-28 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:20:16.367837', '2018-11-27 07:20:16.368304', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (90, '请假类型', 27, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', 'admin', '2018-11-27 07:20:16.400435', '2018-11-27 07:20:16.400677', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (91, '请假原因及相关附件', 28, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>1111</p>', '', 'admin', '2018-11-27 07:21:00.039873', '2018-11-27 07:21:00.039912', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (92, '开始时间', 28, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-11-27 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:21:00.047632', '2018-11-27 07:21:00.047695', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (93, '请假天数(0.5的倍数)', 28, 'leave_days', 5, '1', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:21:00.055101', '2018-11-27 07:21:00.055147', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (94, '代理人', 28, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'admin', 'admin', '2018-11-27 07:21:00.072241', '2018-11-27 07:21:00.072379', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (95, '结束时间', 28, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-11-28 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:21:00.086745', '2018-11-27 07:21:00.086787', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (96, '请假类型', 28, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', 'admin', '2018-11-27 07:21:00.105107', '2018-11-27 07:21:00.105174', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (97, '结束时间', 29, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-11-28 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:23:04.049887', '2018-11-27 07:23:04.049926', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (98, '请假类型', 29, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', 'admin', '2018-11-27 07:23:04.057211', '2018-11-27 07:23:04.057275', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (99, '开始时间', 29, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-11-27 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:23:04.071338', '2018-11-27 07:23:04.071400', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (100, '请假原因及相关附件', 29, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>11</p>', '', 'admin', '2018-11-27 07:23:04.092423', '2018-11-27 07:23:04.092484', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (101, '代理人', 29, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'admin', 'admin', '2018-11-27 07:23:04.101704', '2018-11-27 07:23:04.101740', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (102, '请假天数(0.5的倍数)', 29, 'leave_days', 5, '1', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:23:04.107897', '2018-11-27 07:23:04.107944', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (103, '开始时间', 30, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-11-27 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:23:47.936083', '2018-11-27 07:23:47.936106', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (104, '请假类型', 30, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', 'admin', '2018-11-27 07:23:47.939649', '2018-11-27 07:23:47.939668', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (105, '请假天数(0.5的倍数)', 30, 'leave_days', 5, '1', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:23:47.943261', '2018-11-27 07:23:47.943279', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (106, '请假原因及相关附件', 30, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>11</p>', '', 'admin', '2018-11-27 07:23:47.947946', '2018-11-27 07:23:47.947967', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (107, '结束时间', 30, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-11-28 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:23:47.951685', '2018-11-27 07:23:47.951702', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (108, '代理人', 30, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'admin', 'admin', '2018-11-27 07:23:47.955157', '2018-11-27 07:23:47.955174', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (109, '开始时间', 31, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-11-27 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:24:07.542624', '2018-11-27 07:24:07.542643', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (110, '请假类型', 31, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', 'admin', '2018-11-27 07:24:07.546783', '2018-11-27 07:24:07.546807', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (111, '请假天数(0.5的倍数)', 31, 'leave_days', 5, '1', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:24:07.550448', '2018-11-27 07:24:07.550466', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (112, '请假原因及相关附件', 31, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>sdf</p>', '', 'admin', '2018-11-27 07:24:07.555116', '2018-11-27 07:24:07.555134', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (113, '结束时间', 31, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-11-28 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:24:07.559471', '2018-11-27 07:24:07.559489', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (114, '代理人', 31, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'admin', 'admin', '2018-11-27 07:24:07.564760', '2018-11-27 07:24:07.564778', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (115, '开始时间', 32, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-11-27 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:24:31.262779', '2018-11-27 07:24:31.262796', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (116, '请假类型', 32, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', 'admin', '2018-11-27 07:24:31.266424', '2018-11-27 07:24:31.266442', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (117, '请假天数(0.5的倍数)', 32, 'leave_days', 5, '1', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:24:31.269982', '2018-11-27 07:24:31.270000', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (118, '请假原因及相关附件', 32, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>1111</p>', '', 'admin', '2018-11-27 07:24:31.274681', '2018-11-27 07:24:31.274703', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (119, '结束时间', 32, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-11-28 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:24:31.278645', '2018-11-27 07:24:31.278662', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (120, '代理人', 32, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'admin', 'admin', '2018-11-27 07:24:31.282746', '2018-11-27 07:24:31.282764', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (121, '开始时间', 33, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-11-27 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:27:39.244015', '2018-11-27 07:27:39.244036', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (122, '请假类型', 33, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', 'admin', '2018-11-27 07:27:39.251612', '2018-11-27 07:27:39.251630', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (123, '代理人', 33, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'admin', 'admin', '2018-11-27 07:27:39.255660', '2018-11-27 07:27:39.255678', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (124, '请假原因及相关附件', 33, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>111</p>', '', 'admin', '2018-11-27 07:27:39.259256', '2018-11-27 07:27:39.259274', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (125, '请假天数(0.5的倍数)', 33, 'leave_days', 5, '1', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:27:39.263655', '2018-11-27 07:27:39.263673', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (126, '结束时间', 33, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-11-28 12:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', 'admin', '2018-11-27 07:27:39.267158', '2018-11-27 07:27:39.267176', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (127, '请假原因及相关附件', 34, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>testest<br/></p>', '', '', '2019-11-24 10:23:07.239887', '2019-11-24 10:23:07.239935', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (128, '代理人', 34, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'admin', '', '2019-11-24 10:23:07.254463', '2019-11-24 10:23:07.254513', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (129, '结束时间', 34, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2019-11-27 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2019-11-24 10:23:07.260910', '2019-11-24 10:23:07.260954', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (130, '请假类型', 34, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2019-11-24 10:23:07.269189', '2019-11-24 10:23:07.269245', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (131, '开始时间', 34, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2019-11-26 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2019-11-24 10:23:07.275128', '2019-11-24 10:23:07.275171', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (132, '请假天数(0.5的倍数)', 34, 'leave_days', 5, '1', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2019-11-24 10:23:07.283184', '2019-11-24 10:23:07.283251', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (133, '结束时间', 35, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2019-11-27 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2019-11-24 10:24:31.601549', '2019-11-24 10:24:31.601604', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (134, '开始时间', 35, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2019-11-26 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2019-11-24 10:24:31.612317', '2019-11-24 10:24:31.612378', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (135, '代理人', 35, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'admin', '', '2019-11-24 10:24:31.620276', '2019-11-24 10:24:31.620391', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (136, '请假类型', 35, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2019-11-24 10:24:31.630119', '2019-11-24 10:24:31.630172', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (137, '请假原因及相关附件', 35, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>testest<br/></p>', '', '', '2019-11-24 10:24:31.645703', '2019-11-24 10:24:31.645796', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (138, '请假天数(0.5的倍数)', 35, 'leave_days', 5, '1', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2019-11-24 10:24:31.691046', '2019-11-24 10:24:31.691145', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (139, '申请原因', 36, 'vpn_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>sfdsf</p>', '', '', '2020-04-11 10:40:30.931733', '2020-04-11 10:40:30.931986', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (140, '申请原因', 37, 'vpn_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>testst</p>', '', '', '2020-05-01 09:19:28.707812', '2020-05-01 09:19:28.707852', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (141, '申请原因', 38, 'vpn_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>sssss</p>', '', '', '2020-05-01 09:21:56.857777', '2020-05-01 09:21:56.857801', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (142, '代理人', 39, 'leave_proxy', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'lilian', '', '2020-05-07 22:42:17.268983', '2020-05-07 22:42:17.269009', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (143, '开始时间', 39, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2020-05-08 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2020-05-07 22:42:17.272037', '2020-05-07 22:42:17.272062', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (144, '请假类型', 39, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '2', '', '', '', '', '', '', '2020-05-07 22:42:17.275146', '2020-05-07 22:42:17.275176', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (145, '请假原因及相关附件', 39, 'leave_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>testse</p>', '', '', '2020-05-07 22:42:17.278852', '2020-05-07 22:42:17.278881', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (146, '结束时间', 39, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2020-05-08 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2020-05-07 22:42:17.281930', '2020-05-07 22:42:17.281954', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (147, '申请原因', 40, 'vpn_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>test</p>', '', '', '2020-05-07 22:54:58.877521', '2020-05-07 22:54:58.877549', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (148, '申请原因', 41, 'vpn_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>test</p>', '', '', '2020-05-17 17:31:54.248584', '2020-05-17 17:31:54.248606', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (149, '申请原因', 42, 'vpn_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>1111<br/></p>', '', '', '2020-05-17 17:44:45.473731', '2020-05-17 17:44:45.473777', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (150, '申请原因', 43, 'vpn_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '<p>TEST</p>', '', '', '2020-05-18 23:18:15.558838', '2020-05-18 23:18:15.558867', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (151, '申请原因', 44, 'vpn_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'sdfdsfsdfs', '', '', '2020-08-21 10:39:32.866381', '2020-08-21 10:39:32.866507', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (152, '布尔字段', 45, 'bool_field', 20, '', 0, 0, 1, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2020-08-21 18:33:35.051863', '2020-08-21 18:33:35.052315', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (153, '单选字段', 45, 'checkbox_field', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2020-08-21 18:33:35.103585', '2020-08-21 18:33:35.103849', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (154, '多选字段', 45, 'multi_checkbox_field', 40, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '2', '', '', '', '', '', '2020-08-21 18:33:35.153087', '2020-08-21 18:33:35.153593', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (155, '下拉选择字段', 45, 'select_field', 45, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '1', '', '', '', '', '2020-08-21 18:33:35.233367', '2020-08-21 18:33:35.233979', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (156, '多选下拉列表', 45, 'multi_select_field', 50, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '1,3', '', '', '', '2020-08-21 18:33:35.307356', '2020-08-21 18:33:35.307723', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (157, '文本字段', 45, 'text_field', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'fs', '', '', '2020-08-21 18:33:35.356586', '2020-08-21 18:33:35.356866', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (158, '用户选择字段', 45, 'user_fleld', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'fdsf', '', '2020-08-21 18:33:35.400575', '2020-08-21 18:33:35.400947', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (159, '多选用户字段', 45, 'multi_user_field', 70, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2020-08-21 18:33:35.436945', '2020-08-21 18:33:35.437200', 0, 'sdfds');
INSERT INTO `ticket_ticketcustomfield` VALUES (160, '附件字段', 45, 'attachment_field', 80, 'fdsfs', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2020-08-21 18:33:35.469506', '2020-08-21 18:33:35.470104', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (161, '布尔字段', 46, 'bool_field', 20, '', 0, 0, 1, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2020-08-21 18:42:06.328201', '2020-08-21 18:42:06.328465', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (162, '单选字段', 46, 'checkbox_field', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2020-08-21 18:42:06.379073', '2020-08-21 18:42:06.379318', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (163, '多选字段', 46, 'multi_checkbox_field', 40, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '2,3', '', '', '', '', '', '2020-08-21 18:42:06.422130', '2020-08-21 18:42:06.422375', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (164, '下拉选择字段', 46, 'select_field', 45, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '1', '', '', '', '', '2020-08-21 18:42:06.464354', '2020-08-21 18:42:06.464590', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (165, '多选下拉列表', 46, 'multi_select_field', 50, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '1,2,3', '', '', '', '2020-08-21 18:42:06.503037', '2020-08-21 18:42:06.503408', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (166, '文本字段', 46, 'text_field', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'dfs', '', '', '2020-08-21 18:42:06.540434', '2020-08-21 18:42:06.540785', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (167, '用户选择字段', 46, 'user_fleld', 60, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', 'fdsf', '', '2020-08-21 18:42:06.579294', '2020-08-21 18:42:06.579603', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (168, '多选用户字段', 46, 'multi_user_field', 70, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2020-08-21 18:42:06.614813', '2020-08-21 18:42:06.615049', 0, 'fdsf');
INSERT INTO `ticket_ticketcustomfield` VALUES (169, '附件字段', 46, 'attachment_field', 80, 'fdsfs', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2020-08-21 18:42:06.658653', '2020-08-21 18:42:06.658897', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (170, '开始时间', 46, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2020-08-21 00:00:05.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2020-08-21 18:42:06.707711', '2020-08-21 18:42:06.708026', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (171, '结束时间', 46, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2020-08-21 18:15:52.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2020-08-21 18:42:06.758803', '2020-08-21 18:42:06.759161', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (172, '请假类型', 46, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2020-08-21 18:42:06.803855', '2020-08-21 18:42:06.804139', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (173, '请假原因及相关附件', 46, 'leave_reason', 10, '', 111, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2020-08-21 18:42:06.856788', '2020-08-21 18:42:06.857048', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (174, '申请原因', 47, 'vpn_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'fdsfsfsffhahhah哈哈哈发\nfdsfsfsffhahhah哈哈哈发\nfdsfsfsffhahhah哈哈哈发\nfdsfsfsffhahhah哈哈哈发\nfdsfsfsffhahhah哈哈哈发fdsfsfsffhahhah哈哈哈发\nfdsfsfsffhahhah哈哈哈发', '', '', '2020-08-22 08:46:19.951465', '2020-08-22 08:46:19.951703', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (175, '标题', 48, 'title', 5, '1', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 19:34:44.076031', '2021-07-30 19:34:44.076072', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (176, '标题', 49, 'title', 5, '请假申请', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 19:40:51.889449', '2021-07-30 19:40:51.889473', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (177, '请假天数', 50, 'days', 10, '', 5, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 19:48:51.753861', '2021-07-30 19:48:51.753905', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (178, '标题', 50, 'title', 5, '请假', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 19:48:51.758526', '2021-07-30 19:48:51.758548', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (179, '请假类型', 50, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 19:48:51.763462', '2021-07-30 19:48:51.763525', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (180, '标题', 51, 'text_field', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1', '', '', '2021-07-30 19:58:56.322600', '2021-07-30 19:58:56.322628', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (181, '请假天数', 51, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 19:58:56.327156', '2021-07-30 19:58:56.327182', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (182, '请假理由', 51, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '2', '', '', '2021-07-30 19:58:56.331986', '2021-07-30 19:58:56.332054', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (183, '开始时间', 51, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:03.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 19:58:56.337442', '2021-07-30 19:58:56.337469', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (184, '结束时间', 51, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:03.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 19:58:56.341761', '2021-07-30 19:58:56.341789', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (185, '请假类型', 51, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 19:58:56.347179', '2021-07-30 19:58:56.347215', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (186, '请假天数', 52, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 20:09:49.508985', '2021-07-30 20:09:49.509025', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (187, '请假理由', 52, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'wwwwwwww', '', '', '2021-07-30 20:09:49.514000', '2021-07-30 20:09:49.514036', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (188, '开始时间', 52, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 20:09:49.519210', '2021-07-30 20:09:49.519250', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (189, '结束时间', 52, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:04.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 20:09:49.524128', '2021-07-30 20:09:49.524170', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (190, '请假类型', 52, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 20:09:49.529415', '2021-07-30 20:09:49.529444', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (191, '请假天数', 53, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 20:44:09.962891', '2021-07-30 20:44:09.962953', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (192, '请假理由', 53, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1', '', '', '2021-07-30 20:44:09.967148', '2021-07-30 20:44:09.967172', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (193, '开始时间', 53, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 02:00:05.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 20:44:09.971469', '2021-07-30 20:44:09.971495', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (194, '结束时间', 53, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:04.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 20:44:09.975158', '2021-07-30 20:44:09.975181', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (195, '请假天数', 54, 'days', 10, '', 132131, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 20:47:54.717989', '2021-07-30 20:47:54.718016', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (196, '请假理由', 54, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1', '', '', '2021-07-30 20:47:54.723189', '2021-07-30 20:47:54.723217', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (197, '开始时间', 54, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:02.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 20:47:54.727800', '2021-07-30 20:47:54.727838', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (198, '结束时间', 54, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:03:04.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 20:47:54.732502', '2021-07-30 20:47:54.732529', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (199, '请假类型', 54, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 20:47:54.737313', '2021-07-30 20:47:54.737381', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (200, '请假天数', 55, 'days', 10, '', 12313, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 20:48:26.246046', '2021-07-30 20:48:26.246118', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (201, '请假理由', 55, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '12312', '', '', '2021-07-30 20:48:26.251388', '2021-07-30 20:48:26.251452', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (202, '开始时间', 55, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:03.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 20:48:26.257766', '2021-07-30 20:48:26.257795', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (203, '结束时间', 55, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:20.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 20:48:26.263373', '2021-07-30 20:48:26.263411', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (204, '请假类型', 55, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 20:48:26.268963', '2021-07-30 20:48:26.268994', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (205, '申请原因', 56, 'vpn_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '应用', '', '', '2021-07-30 20:59:24.155871', '2021-07-30 20:59:24.155898', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (206, '申请原因', 57, 'vpn_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '申请原因', '', '', '2021-07-30 20:59:53.494150', '2021-07-30 20:59:53.494175', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (207, '申请原因', 58, 'vpn_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '申请原因', '', '', '2021-07-30 21:02:05.627143', '2021-07-30 21:02:05.627168', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (208, '请假天数', 59, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:03:35.912315', '2021-07-30 21:03:35.912344', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (209, '请假理由', 59, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '11', '', '', '2021-07-30 21:03:35.916546', '2021-07-30 21:03:35.916588', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (210, '开始时间', 59, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:07.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:03:35.920347', '2021-07-30 21:03:35.920371', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (211, '结束时间', 59, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:07.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:03:35.924568', '2021-07-30 21:03:35.924595', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (212, '请假类型', 59, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 21:03:35.928170', '2021-07-30 21:03:35.928204', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (213, '请假天数', 60, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:08:42.864024', '2021-07-30 21:08:42.864050', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (214, '结束时间', 60, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:04.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:08:42.867650', '2021-07-30 21:08:42.867675', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (215, '开始时间', 60, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:08:42.871242', '2021-07-30 21:08:42.871266', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (216, '请假类型', 60, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 21:08:42.874586', '2021-07-30 21:08:42.874611', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (217, '请假理由', 60, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'wwwwwwww', '', '', '2021-07-30 21:08:42.879677', '2021-07-30 21:08:42.879701', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (218, '请假天数', 61, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:28:21.578720', '2021-07-30 21:28:21.578767', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (219, '结束时间', 61, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:04.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:28:21.582428', '2021-07-30 21:28:21.582450', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (220, '开始时间', 61, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:28:21.585638', '2021-07-30 21:28:21.585663', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (221, '请假类型', 61, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 21:28:21.589667', '2021-07-30 21:28:21.589690', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (222, '请假理由', 61, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'wwwwwwww', '', '', '2021-07-30 21:28:21.593728', '2021-07-30 21:28:21.593755', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (223, '请假天数', 62, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:28:38.175506', '2021-07-30 21:28:38.175530', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (224, '结束时间', 62, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:04.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:28:38.178395', '2021-07-30 21:28:38.178417', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (225, '开始时间', 62, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:28:38.181654', '2021-07-30 21:28:38.181677', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (226, '请假类型', 62, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 21:28:38.184866', '2021-07-30 21:28:38.184890', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (227, '请假理由', 62, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'wwwwwwww', '', '', '2021-07-30 21:28:38.187695', '2021-07-30 21:28:38.187716', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (228, '请假天数', 63, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:33:27.406675', '2021-07-30 21:33:27.406709', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (229, '结束时间', 63, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:04.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:33:27.411444', '2021-07-30 21:33:27.411477', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (230, '开始时间', 63, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:33:27.415931', '2021-07-30 21:33:27.416062', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (231, '请假类型', 63, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 21:33:27.419963', '2021-07-30 21:33:27.419989', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (232, '请假理由', 63, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'wwwwwwww', '', '', '2021-07-30 21:33:27.424755', '2021-07-30 21:33:27.424784', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (233, '请假天数', 64, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:36:31.730659', '2021-07-30 21:36:31.730683', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (234, '结束时间', 64, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:04.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:36:31.734328', '2021-07-30 21:36:31.734378', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (235, '开始时间', 64, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:36:31.738006', '2021-07-30 21:36:31.738032', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (236, '请假类型', 64, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 21:36:31.741433', '2021-07-30 21:36:31.741456', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (237, '请假理由', 64, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'wwwwwwww', '', '', '2021-07-30 21:36:31.744518', '2021-07-30 21:36:31.744549', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (238, '请假天数', 65, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:36:44.651647', '2021-07-30 21:36:44.651681', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (239, '结束时间', 65, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:04.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:36:44.656544', '2021-07-30 21:36:44.656584', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (240, '开始时间', 65, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:36:44.661166', '2021-07-30 21:36:44.661207', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (241, '请假类型', 65, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 21:36:44.668572', '2021-07-30 21:36:44.668616', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (242, '请假理由', 65, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'wwwwwwww', '', '', '2021-07-30 21:36:44.673037', '2021-07-30 21:36:44.673073', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (243, '请假天数', 66, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:37:43.586607', '2021-07-30 21:37:43.586631', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (244, '结束时间', 66, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:04.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:37:43.590323', '2021-07-30 21:37:43.590348', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (245, '开始时间', 66, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:37:43.593745', '2021-07-30 21:37:43.593769', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (246, '请假类型', 66, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 21:37:43.597286', '2021-07-30 21:37:43.597310', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (247, '请假理由', 66, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'wwwwwwww', '', '', '2021-07-30 21:37:43.600333', '2021-07-30 21:37:43.600354', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (248, '请假天数', 67, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:39:59.966641', '2021-07-30 21:39:59.966665', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (249, '结束时间', 67, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:04.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:39:59.971308', '2021-07-30 21:39:59.971347', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (250, '开始时间', 67, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:39:59.975096', '2021-07-30 21:39:59.975120', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (251, '请假类型', 67, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 21:39:59.979663', '2021-07-30 21:39:59.979686', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (252, '请假理由', 67, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'wwwwwwww', '', '', '2021-07-30 21:39:59.984138', '2021-07-30 21:39:59.984176', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (253, '请假天数', 68, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:40:18.516993', '2021-07-30 21:40:18.517017', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (254, '结束时间', 68, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:04.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:40:18.520015', '2021-07-30 21:40:18.520037', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (255, '开始时间', 68, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:40:18.523052', '2021-07-30 21:40:18.523074', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (256, '请假类型', 68, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 21:40:18.526433', '2021-07-30 21:40:18.526457', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (257, '请假理由', 68, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'wwwwwwww', '', '', '2021-07-30 21:40:18.529808', '2021-07-30 21:40:18.529829', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (258, '请假天数', 69, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:40:20.485079', '2021-07-30 21:40:20.485115', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (259, '结束时间', 69, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:04.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:40:20.489455', '2021-07-30 21:40:20.489484', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (260, '开始时间', 69, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:40:20.493217', '2021-07-30 21:40:20.493240', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (261, '请假类型', 69, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 21:40:20.497888', '2021-07-30 21:40:20.497921', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (262, '请假理由', 69, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'wwwwwwww', '', '', '2021-07-30 21:40:20.501917', '2021-07-30 21:40:20.501939', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (263, '请假天数', 70, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:40:29.998227', '2021-07-30 21:40:29.998253', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (264, '结束时间', 70, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:04.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:40:30.002873', '2021-07-30 21:40:30.002908', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (265, '开始时间', 70, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:40:30.006771', '2021-07-30 21:40:30.006796', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (266, '请假类型', 70, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 21:40:30.011894', '2021-07-30 21:40:30.011947', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (267, '请假理由', 70, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'wwwwwwww', '', '', '2021-07-30 21:40:30.017267', '2021-07-30 21:40:30.017306', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (268, '请假天数', 71, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:40:32.915437', '2021-07-30 21:40:32.915461', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (269, '结束时间', 71, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:04.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:40:32.919374', '2021-07-30 21:40:32.919432', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (270, '开始时间', 71, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:40:32.923251', '2021-07-30 21:40:32.923295', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (271, '请假类型', 71, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 21:40:32.927794', '2021-07-30 21:40:32.927849', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (272, '请假理由', 71, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'wwwwwwww', '', '', '2021-07-30 21:40:32.931444', '2021-07-30 21:40:32.931465', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (273, '请假天数', 72, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:40:54.546226', '2021-07-30 21:40:54.546251', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (274, '结束时间', 72, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:04.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:40:54.550353', '2021-07-30 21:40:54.550404', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (275, '开始时间', 72, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:40:54.554587', '2021-07-30 21:40:54.554612', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (276, '请假类型', 72, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 21:40:54.558813', '2021-07-30 21:40:54.558847', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (277, '请假理由', 72, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'wwwwwwww', '', '', '2021-07-30 21:40:54.562242', '2021-07-30 21:40:54.562265', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (278, '请假天数', 73, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:41:06.620548', '2021-07-30 21:41:06.620581', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (279, '结束时间', 73, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:04.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:41:06.624039', '2021-07-30 21:41:06.624062', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (280, '开始时间', 73, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:41:06.627876', '2021-07-30 21:41:06.627900', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (281, '请假类型', 73, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 21:41:06.631178', '2021-07-30 21:41:06.631203', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (282, '请假理由', 73, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'wwwwwwww', '', '', '2021-07-30 21:41:06.634759', '2021-07-30 21:41:06.634785', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (283, '请假天数', 74, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:43:51.906224', '2021-07-30 21:43:51.906247', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (284, '请假天数', 75, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:45:55.102002', '2021-07-30 21:45:55.102073', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (285, '请假天数', 76, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:46:28.864282', '2021-07-30 21:46:28.864309', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (286, '请假天数', 78, 'days', 10, '', 123123, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:47:22.730974', '2021-07-30 21:47:22.731002', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (287, '结束时间', 78, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 21:47:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:47:22.736555', '2021-07-30 21:47:22.736588', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (288, '开始时间', 78, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 21:47:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 21:47:22.741226', '2021-07-30 21:47:22.741267', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (289, '请假类型', 78, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-07-30 21:47:22.746200', '2021-07-30 21:47:22.746226', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (290, '请假理由', 78, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '123132', '', '', '2021-07-30 21:47:22.751511', '2021-07-30 21:47:22.751549', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (291, '请假类型', 89, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '2', '', '', '', '', '', '', '2021-07-30 22:01:28.881399', '2021-07-30 22:01:28.881426', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (292, '请假天数', 90, 'days', 10, '', 2, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 22:06:36.778419', '2021-07-30 22:06:36.778445', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (293, '结束时间', 90, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 22:06:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 22:06:36.783659', '2021-07-30 22:06:36.783716', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (294, '开始时间', 90, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 22:06:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 22:06:36.789332', '2021-07-30 22:06:36.789359', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (295, '请假类型', 90, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-07-30 22:06:36.794351', '2021-07-30 22:06:36.794387', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (296, '请假理由', 90, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '111', '', '', '2021-07-30 22:06:36.798897', '2021-07-30 22:06:36.798923', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (297, '请假天数', 91, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 22:08:22.267355', '2021-07-30 22:08:22.267387', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (298, '请假理由', 91, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'cs', '', '', '2021-07-30 22:08:22.272974', '2021-07-30 22:08:22.273014', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (299, '开始时间', 91, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:07.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 22:08:22.277913', '2021-07-30 22:08:22.277940', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (300, '结束时间', 91, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:06.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 22:08:22.282395', '2021-07-30 22:08:22.282422', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (301, '请假类型', 91, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-30 22:08:22.287249', '2021-07-30 22:08:22.287376', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (302, '请假天数', 92, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 22:43:46.087068', '2021-07-30 22:43:46.087093', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (303, '结束时间', 92, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-05-13 22:24:41.952132', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 22:43:46.089980', '2021-07-30 22:43:46.089999', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (304, '开始时间', 92, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-05-13 22:24:41.952132', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 22:43:46.092755', '2021-07-30 22:43:46.092777', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (305, '请假类型', 92, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-07-30 22:43:46.095579', '2021-07-30 22:43:46.095599', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (306, '请假理由', 92, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '无', '', '', '2021-07-30 22:43:46.098412', '2021-07-30 22:43:46.098435', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (307, '请假天数', 93, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 22:43:53.678664', '2021-07-30 22:43:53.678690', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (308, '结束时间', 93, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-05-13 22:24:41.952132', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 22:43:53.681935', '2021-07-30 22:43:53.681959', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (309, '开始时间', 93, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-05-13 22:24:41.952132', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 22:43:53.685145', '2021-07-30 22:43:53.685169', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (310, '请假类型', 93, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-07-30 22:43:53.688268', '2021-07-30 22:43:53.688293', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (311, '请假理由', 93, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '无', '', '', '2021-07-30 22:43:53.691485', '2021-07-30 22:43:53.691509', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (312, '请假天数', 94, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 22:44:29.580738', '2021-07-30 22:44:29.580769', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (313, '结束时间', 94, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-05-13 22:24:41.952132', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 22:44:29.584669', '2021-07-30 22:44:29.584702', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (314, '开始时间', 94, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-05-13 22:24:41.952132', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-30 22:44:29.588403', '2021-07-30 22:44:29.588427', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (315, '请假类型', 94, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-07-30 22:44:29.591446', '2021-07-30 22:44:29.591469', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (316, '请假理由', 94, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '无', '', '', '2021-07-30 22:44:29.594465', '2021-07-30 22:44:29.594487', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (317, '请假天数', 95, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:02:44.549925', '2021-07-31 10:02:44.549949', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (318, '结束时间', 95, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 10:02:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:02:44.553920', '2021-07-31 10:02:44.553943', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (319, '开始时间', 95, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 10:02:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:02:44.558151', '2021-07-31 10:02:44.558191', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (320, '请假类型', 95, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-07-31 10:02:44.562918', '2021-07-31 10:02:44.562944', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (321, '请假理由', 95, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1231', '', '', '2021-07-31 10:02:44.567616', '2021-07-31 10:02:44.567641', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (322, '请假天数', 96, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:03:10.971483', '2021-07-31 10:03:10.971506', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (323, '结束时间', 96, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 10:02:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:03:10.975032', '2021-07-31 10:03:10.975054', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (324, '开始时间', 96, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 10:02:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:03:10.978433', '2021-07-31 10:03:10.978455', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (325, '请假类型', 96, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-07-31 10:03:10.981541', '2021-07-31 10:03:10.981563', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (326, '请假理由', 96, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1231', '', '', '2021-07-31 10:03:10.985111', '2021-07-31 10:03:10.985133', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (327, '请假天数', 97, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:03:40.493313', '2021-07-31 10:03:40.493336', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (328, '结束时间', 97, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 10:02:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:03:40.496748', '2021-07-31 10:03:40.496770', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (329, '开始时间', 97, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 10:02:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:03:40.500445', '2021-07-31 10:03:40.500467', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (330, '请假类型', 97, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-07-31 10:03:40.503506', '2021-07-31 10:03:40.503528', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (331, '请假理由', 97, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1231', '', '', '2021-07-31 10:03:40.509026', '2021-07-31 10:03:40.509049', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (332, '请假天数', 98, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:10:30.383026', '2021-07-31 10:10:30.383050', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (333, '请假天数', 99, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:10:39.999833', '2021-07-31 10:10:39.999884', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (334, '结束时间', 99, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 10:10:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:10:40.004066', '2021-07-31 10:10:40.004097', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (335, '开始时间', 99, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 10:10:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:10:40.007400', '2021-07-31 10:10:40.007424', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (336, '请假类型', 99, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-07-31 10:10:40.011598', '2021-07-31 10:10:40.011624', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (337, '请假理由', 99, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1', '', '', '2021-07-31 10:10:40.015060', '2021-07-31 10:10:40.015085', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (338, '请假天数', 100, 'days', 10, '', 111, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:11:38.301578', '2021-07-31 10:11:38.301601', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (339, '结束时间', 100, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 10:11:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:11:38.308060', '2021-07-31 10:11:38.308084', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (340, '开始时间', 100, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 10:11:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:11:38.311323', '2021-07-31 10:11:38.311381', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (341, '请假类型', 100, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-07-31 10:11:38.315364', '2021-07-31 10:11:38.315386', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (342, '请假理由', 100, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '111', '', '', '2021-07-31 10:11:38.319012', '2021-07-31 10:11:38.319073', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (343, '请假天数', 101, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:44:57.169796', '2021-07-31 10:44:57.169960', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (344, '结束时间', 101, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-28 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:44:57.174718', '2021-07-31 10:44:57.174747', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (345, '开始时间', 101, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 10:44:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:44:57.178888', '2021-07-31 10:44:57.178914', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (346, '请假类型', 101, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-07-31 10:44:57.183209', '2021-07-31 10:44:57.183245', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (347, '请假理由', 101, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '11', '', '', '2021-07-31 10:44:57.187477', '2021-07-31 10:44:57.187503', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (348, '请假天数', 102, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:45:19.788810', '2021-07-31 10:45:19.788835', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (349, '结束时间', 102, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-28 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:45:19.792870', '2021-07-31 10:45:19.792898', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (350, '开始时间', 102, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 10:44:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:45:19.796623', '2021-07-31 10:45:19.796647', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (351, '请假类型', 102, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-07-31 10:45:19.801226', '2021-07-31 10:45:19.801256', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (352, '请假理由', 102, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '11', '', '', '2021-07-31 10:45:19.805834', '2021-07-31 10:45:19.805876', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (353, '请假天数', 103, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:45:27.032052', '2021-07-31 10:45:27.032107', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (354, '结束时间', 103, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 10:45:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:45:27.037039', '2021-07-31 10:45:27.037065', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (355, '开始时间', 103, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 10:45:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:45:27.041808', '2021-07-31 10:45:27.041967', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (356, '请假类型', 103, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-07-31 10:45:27.047477', '2021-07-31 10:45:27.047503', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (357, '请假理由', 103, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1', '', '', '2021-07-31 10:45:27.051361', '2021-07-31 10:45:27.051386', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (358, '请假天数', 104, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:47:10.087689', '2021-07-31 10:47:10.087728', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (359, '结束时间', 104, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 10:47:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:47:10.092384', '2021-07-31 10:47:10.092414', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (360, '开始时间', 104, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 10:47:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:47:10.096189', '2021-07-31 10:47:10.096212', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (361, '请假类型', 104, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-07-31 10:47:10.100873', '2021-07-31 10:47:10.100897', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (362, '请假理由', 104, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1', '', '', '2021-07-31 10:47:10.105840', '2021-07-31 10:47:10.105914', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (363, '请假天数', 106, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:48:41.452677', '2021-07-31 10:48:41.452702', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (364, '结束时间', 106, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:48:41.457026', '2021-07-31 10:48:41.457071', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (365, '开始时间', 106, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 10:48:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:48:41.461615', '2021-07-31 10:48:41.461653', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (366, '请假类型', 106, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-31 10:48:41.466100', '2021-07-31 10:48:41.466139', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (367, '请假理由', 106, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1', '', '', '2021-07-31 10:48:41.470540', '2021-07-31 10:48:41.470566', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (368, '请假天数', 107, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:50:42.838220', '2021-07-31 10:50:42.838244', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (369, '结束时间', 107, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 10:50:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:50:42.842086', '2021-07-31 10:50:42.842110', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (370, '开始时间', 107, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 10:50:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:50:42.845675', '2021-07-31 10:50:42.845697', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (371, '请假类型', 107, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-31 10:50:42.850052', '2021-07-31 10:50:42.850094', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (372, '请假理由', 107, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1', '', '', '2021-07-31 10:50:42.854342', '2021-07-31 10:50:42.854364', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (373, '请假天数', 108, 'days', 10, '', 2, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:52:16.285643', '2021-07-31 10:52:16.285666', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (374, '结束时间', 108, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:52:16.290146', '2021-07-31 10:52:16.290190', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (375, '开始时间', 108, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 10:52:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 10:52:16.294038', '2021-07-31 10:52:16.294060', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (376, '请假类型', 108, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-31 10:52:16.298203', '2021-07-31 10:52:16.298227', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (377, '请假理由', 108, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1', '', '', '2021-07-31 10:52:16.302375', '2021-07-31 10:52:16.302402', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (378, '请假天数', 114, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 11:43:56.139549', '2021-07-31 11:43:56.139579', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (379, '结束时间', 114, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 11:43:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 11:43:56.143503', '2021-07-31 11:43:56.143526', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (380, '开始时间', 114, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 11:43:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 11:43:56.147906', '2021-07-31 11:43:56.147931', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (381, '请假类型', 114, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-07-31 11:43:56.151390', '2021-07-31 11:43:56.151430', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (382, '请假理由', 114, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1', '', '', '2021-07-31 11:43:56.155279', '2021-07-31 11:43:56.155303', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (383, '请假天数', 115, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 13:49:10.136730', '2021-07-31 13:49:10.136755', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (384, '结束时间', 115, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 13:49:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 13:49:10.141690', '2021-07-31 13:49:10.141716', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (385, '开始时间', 115, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 13:49:10.146130', '2021-07-31 13:49:10.146153', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (386, '请假类型', 115, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-07-31 13:49:10.150402', '2021-07-31 13:49:10.150427', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (387, '请假理由', 115, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '无无无', '', '', '2021-07-31 13:49:10.153946', '2021-07-31 13:49:10.153968', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (388, '请假天数', 116, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 13:52:11.451129', '2021-07-31 13:52:11.451176', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (389, '结束时间', 116, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 13:52:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 13:52:11.455886', '2021-07-31 13:52:11.455910', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (390, '开始时间', 116, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 13:52:11.460423', '2021-07-31 13:52:11.460447', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (391, '请假类型', 116, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-31 13:52:11.463897', '2021-07-31 13:52:11.463938', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (392, '请假理由', 116, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '文物哇哇哇', '', '', '2021-07-31 13:52:11.467787', '2021-07-31 13:52:11.467813', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (393, '请假天数', 117, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 15:19:42.615681', '2021-07-31 15:19:42.615707', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (394, '结束时间', 117, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 15:19:42.621317', '2021-07-31 15:19:42.621342', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (395, '开始时间', 117, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 15:19:42.624858', '2021-07-31 15:19:42.624881', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (396, '请假类型', 117, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-07-31 15:19:42.628841', '2021-07-31 15:19:42.628864', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (397, '请假理由', 117, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '哇哇哇哇哇哇哇哇哇哇哇哇哇哇哇哇哇哇哇哇哇哇哇哇哇哇哇哇', '', '', '2021-07-31 15:19:42.632941', '2021-07-31 15:19:42.632971', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (398, '请假天数', 118, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 15:31:45.409146', '2021-07-31 15:31:45.409170', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (399, '结束时间', 118, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 15:31:45.413551', '2021-07-31 15:31:45.413576', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (400, '开始时间', 118, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 15:31:45.416786', '2021-07-31 15:31:45.416806', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (401, '请假类型', 118, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-07-31 15:31:45.420625', '2021-07-31 15:31:45.420648', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (402, '请假理由', 118, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '哇哇哇哇哇哇哇哇哇哇哇哇哇', '', '', '2021-07-31 15:31:45.423882', '2021-07-31 15:31:45.423902', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (403, '请假天数', 119, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 15:37:13.279651', '2021-07-31 15:37:13.279673', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (404, '结束时间', 119, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 15:37:13.284303', '2021-07-31 15:37:13.284325', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (405, '开始时间', 119, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 15:37:13.287853', '2021-07-31 15:37:13.287907', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (406, '请假类型', 119, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '事假', '', '', '', '', '', '', '2021-07-31 15:37:13.291878', '2021-07-31 15:37:13.291899', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (407, '请假理由', 119, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '哇哇哇哇哇哇哇哇哇哇哇哇哇', '', '', '2021-07-31 15:37:13.296467', '2021-07-31 15:37:13.296494', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (408, '请假天数', 120, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 15:41:11.418609', '2021-07-31 15:41:11.418632', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (409, '结束时间', 120, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 15:41:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 15:41:11.424458', '2021-07-31 15:41:11.424482', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (410, '开始时间', 120, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 15:41:11.428469', '2021-07-31 15:41:11.428495', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (411, '请假类型', 120, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-31 15:41:11.432491', '2021-07-31 15:41:11.432516', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (412, '请假理由', 120, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1123124125 ', '', '', '2021-07-31 15:41:11.436322', '2021-07-31 15:41:11.436346', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (413, '申请原因', 121, 'vpn_reason', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '去啊啊啊', '', '', '2021-07-31 15:41:43.438513', '2021-07-31 15:41:43.438543', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (414, '请假天数', 157, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 16:25:20.697184', '2021-07-31 16:25:20.697207', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (415, '结束时间', 157, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 16:25:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 16:25:20.702313', '2021-07-31 16:25:20.702337', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (416, '开始时间', 157, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 16:25:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 16:25:20.706239', '2021-07-31 16:25:20.706275', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (417, '请假类型', 157, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-31 16:25:20.710345', '2021-07-31 16:25:20.710367', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (418, '请假理由', 157, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1', '', '', '2021-07-31 16:25:20.714244', '2021-07-31 16:25:20.714270', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (419, '请假天数', 158, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 16:31:50.831806', '2021-07-31 16:31:50.831851', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (420, '结束时间', 158, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-06-08 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 16:31:50.836645', '2021-07-31 16:31:50.836675', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (421, '开始时间', 158, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-07 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 16:31:50.841267', '2021-07-31 16:31:50.841292', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (422, '请假类型', 158, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '2', '', '', '', '', '', '', '2021-07-31 16:31:50.845745', '2021-07-31 16:31:50.845774', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (423, '请假理由', 158, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1', '', '', '2021-07-31 16:31:50.849917', '2021-07-31 16:31:50.849956', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (424, '请假天数', 163, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 17:04:20.953121', '2021-07-31 17:04:20.953172', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (425, '结束时间', 163, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 17:04:20.958804', '2021-07-31 17:04:20.958828', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (426, '开始时间', 163, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 17:04:20.963591', '2021-07-31 17:04:20.963614', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (427, '请假类型', 163, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '事假', '', '', '', '', '', '', '2021-07-31 17:04:20.968131', '2021-07-31 17:04:20.968156', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (428, '请假理由', 163, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '哇哇哇哇哇哇哇哇哇哇哇哇哇', '', '', '2021-07-31 17:04:20.972320', '2021-07-31 17:04:20.972355', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (429, '请假天数', 204, 'days', 10, '', 1231, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 18:22:49.323234', '2021-07-31 18:22:49.323258', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (430, '结束时间', 204, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-08 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 18:22:49.327509', '2021-07-31 18:22:49.327539', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (431, '开始时间', 204, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 18:22:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 18:22:49.331176', '2021-07-31 18:22:49.331199', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (432, '请假类型', 204, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-31 18:22:49.336024', '2021-07-31 18:22:49.336125', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (433, '请假理由', 204, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '231', '', '', '2021-07-31 18:22:49.339968', '2021-07-31 18:22:49.339990', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (434, '请假天数', 205, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 18:48:23.063984', '2021-07-31 18:48:23.064012', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (435, '结束时间', 205, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 18:48:23.068585', '2021-07-31 18:48:23.068608', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (436, '开始时间', 205, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 18:48:23.073437', '2021-07-31 18:48:23.073461', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (437, '请假类型', 205, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '事假', '', '', '', '', '', '', '2021-07-31 18:48:23.077105', '2021-07-31 18:48:23.077127', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (438, '请假理由', 205, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '哇哇哇哇哇哇哇哇哇哇哇哇哇', '', '', '2021-07-31 18:48:23.081604', '2021-07-31 18:48:23.081626', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (439, '请假天数', 207, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 19:22:57.240059', '2021-07-31 19:22:57.240084', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (440, '结束时间', 207, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 19:22:57.244301', '2021-07-31 19:22:57.244335', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (441, '开始时间', 207, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 19:22:57.247620', '2021-07-31 19:22:57.247644', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (442, '请假类型', 207, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '事假', '', '', '', '', '', '', '2021-07-31 19:22:57.251219', '2021-07-31 19:22:57.251252', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (443, '请假理由', 207, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '哇哇哇哇哇哇哇哇哇哇哇哇哇', '', '', '2021-07-31 19:22:57.254715', '2021-07-31 19:22:57.254740', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (444, '请假天数', 198, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 20:54:49.297038', '2021-07-31 20:54:49.297072', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (445, '结束时间', 198, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 20:54:49.301766', '2021-07-31 20:54:49.301792', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (446, '开始时间', 198, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-30 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 20:54:49.305503', '2021-07-31 20:54:49.305528', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (447, '请假类型', 198, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '事假', '', '', '', '', '', '', '2021-07-31 20:54:49.309074', '2021-07-31 20:54:49.309098', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (448, '请假理由', 198, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '哇哇哇哇哇哇哇哇哇哇哇哇哇', '', '', '2021-07-31 20:54:49.313135', '2021-07-31 20:54:49.313160', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (449, '请假天数', 208, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 20:56:43.165508', '2021-07-31 20:56:43.165542', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (450, '结束时间', 208, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-31 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 20:56:43.169562', '2021-07-31 20:56:43.169608', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (451, '开始时间', 208, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-07-24 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-07-31 20:56:43.173578', '2021-07-31 20:56:43.173610', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (452, '请假类型', 208, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-07-31 20:56:43.178287', '2021-07-31 20:56:43.178324', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (453, '请假理由', 208, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '挨打啊啊打啊哇 我啊我', '', '', '2021-07-31 20:56:43.182022', '2021-07-31 20:56:43.182053', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (454, '请假天数', 209, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 12:11:22.383975', '2021-08-01 12:11:22.384016', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (455, '结束时间', 209, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 12:11:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 12:11:22.388116', '2021-08-01 12:11:22.388143', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (456, '开始时间', 209, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 12:11:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 12:11:22.392259', '2021-08-01 12:11:22.392284', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (457, '请假类型', 209, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 12:11:22.395366', '2021-08-01 12:11:22.395390', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (458, '请假理由', 209, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'adad a da da ', '', '', '2021-08-01 12:11:22.399169', '2021-08-01 12:11:22.399196', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (459, '请假天数', 210, 'days', 10, '', 2, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 12:40:41.272659', '2021-08-01 12:40:41.272683', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (460, '结束时间', 210, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-03 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 12:40:41.276702', '2021-08-01 12:40:41.276739', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (461, '开始时间', 210, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 12:40:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 12:40:41.280150', '2021-08-01 12:40:41.280174', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (462, '请假类型', 210, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 12:40:41.284442', '2021-08-01 12:40:41.284469', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (463, '请假理由', 210, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '在这种困难的抉择下，本人思来想去，寝食难安。 带着这些问题，我们来审视一下学生会退会。', '', '', '2021-08-01 12:40:41.287725', '2021-08-01 12:40:41.287748', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (464, '请假天数', 211, 'days', 10, '', 2, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 12:43:30.782696', '2021-08-01 12:43:30.782724', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (465, '结束时间', 211, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-03 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 12:43:30.786767', '2021-08-01 12:43:30.786812', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (466, '开始时间', 211, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 12:43:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 12:43:30.790863', '2021-08-01 12:43:30.790898', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (467, '请假类型', 211, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '2', '', '', '', '', '', '', '2021-08-01 12:43:30.795091', '2021-08-01 12:43:30.795117', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (468, '请假理由', 211, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '哇哇哇哇哇哇哇哇哇哇哇哇', '', '', '2021-08-01 12:43:30.798127', '2021-08-01 12:43:30.798264', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (469, '请假天数', 213, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 12:47:33.583557', '2021-08-01 12:47:33.583591', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (470, '结束时间', 213, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-26 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 12:47:33.588116', '2021-08-01 12:47:33.588153', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (471, '开始时间', 213, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 12:47:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 12:47:33.593143', '2021-08-01 12:47:33.593185', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (472, '请假类型', 213, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 12:47:33.600785', '2021-08-01 12:47:33.600821', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (473, '请假理由', 213, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '嘻嘻嘻嘻哇哇哇哇哇哇哇哇', '', '', '2021-08-01 12:47:33.604520', '2021-08-01 12:47:33.604546', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (474, '请假天数', 214, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 12:55:35.000424', '2021-08-01 12:55:35.000448', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (475, '结束时间', 214, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 12:55:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 12:55:35.004279', '2021-08-01 12:55:35.004304', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (476, '开始时间', 214, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 12:55:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 12:55:35.012666', '2021-08-01 12:55:35.012698', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (477, '请假类型', 214, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 12:55:35.016432', '2021-08-01 12:55:35.016473', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (478, '请假理由', 214, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '哇哇哇哇我我', '', '', '2021-08-01 12:55:35.019887', '2021-08-01 12:55:35.019912', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (479, '请假天数', 215, 'days', 10, '', 1111, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:01:14.896799', '2021-08-01 13:01:14.896843', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (480, '结束时间', 215, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-31 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:01:14.901471', '2021-08-01 13:01:14.901496', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (481, '开始时间', 215, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:01:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:01:14.905705', '2021-08-01 13:01:14.905740', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (482, '请假类型', 215, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 13:01:14.909444', '2021-08-01 13:01:14.909470', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (483, '请假理由', 215, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '121111111111111111', '', '', '2021-08-01 13:01:14.913179', '2021-08-01 13:01:14.913213', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (484, '请假天数', 216, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:05:30.558505', '2021-08-01 13:05:30.558551', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (485, '结束时间', 216, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:05:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:05:30.566208', '2021-08-01 13:05:30.566272', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (486, '开始时间', 216, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:05:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:05:30.601316', '2021-08-01 13:05:30.601343', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (487, '请假类型', 216, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 13:05:30.637754', '2021-08-01 13:05:30.637805', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (488, '请假理由', 216, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '11114124124512', '', '', '2021-08-01 13:05:30.672610', '2021-08-01 13:05:30.672634', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (489, '请假天数', 217, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:07:55.526037', '2021-08-01 13:07:55.526062', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (490, '结束时间', 217, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:07:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:07:55.531100', '2021-08-01 13:07:55.531135', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (491, '开始时间', 217, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:07:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:07:55.535316', '2021-08-01 13:07:55.535347', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (492, '请假类型', 217, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 13:07:55.539748', '2021-08-01 13:07:55.539772', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (493, '请假理由', 217, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '11111', '', '', '2021-08-01 13:07:55.545749', '2021-08-01 13:07:55.545790', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (494, '请假天数', 218, 'days', 10, '', 456, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:17:29.909392', '2021-08-01 13:17:29.909417', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (495, '结束时间', 218, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:17:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:17:29.912552', '2021-08-01 13:17:29.912579', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (496, '开始时间', 218, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:17:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:17:29.916039', '2021-08-01 13:17:29.916064', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (497, '请假类型', 218, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 13:17:29.918970', '2021-08-01 13:17:29.918990', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (498, '请假理由', 218, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'WWWWWW', '', '', '2021-08-01 13:17:29.923088', '2021-08-01 13:17:29.923120', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (499, '请假天数', 219, 'days', 10, '', 1231451, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:22:41.530076', '2021-08-01 13:22:41.530100', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (500, '请假天数', 220, 'days', 10, '', 1231451, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:22:54.978970', '2021-08-01 13:22:54.978999', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (501, '请假天数', 221, 'days', 10, '', 1231451, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:23:08.774277', '2021-08-01 13:23:08.774301', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (502, '结束时间', 221, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:23:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:23:08.777805', '2021-08-01 13:23:08.777828', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (503, '开始时间', 221, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:22:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:23:08.780914', '2021-08-01 13:23:08.780936', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (504, '请假类型', 221, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 13:23:08.784844', '2021-08-01 13:23:08.784868', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (505, '请假理由', 221, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '2141241241', '', '', '2021-08-01 13:23:08.787998', '2021-08-01 13:23:08.788021', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (506, '请假天数', 222, 'days', 10, '', 12, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:26:58.900125', '2021-08-01 13:26:58.900158', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (507, '请假天数', 223, 'days', 10, '', 12, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:33:39.502045', '2021-08-01 13:33:39.502069', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (508, '请假天数', 224, 'days', 10, '', 3123123, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:38:50.673831', '2021-08-01 13:38:50.673863', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (509, '结束时间', 224, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:38:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:38:50.677665', '2021-08-01 13:38:50.677687', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (510, '开始时间', 224, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:38:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:38:50.681020', '2021-08-01 13:38:50.681049', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (511, '请假类型', 224, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 13:38:50.684540', '2021-08-01 13:38:50.684565', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (512, '请假理由', 224, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1313123', '', '', '2021-08-01 13:38:50.688532', '2021-08-01 13:38:50.688558', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (513, '请假天数', 225, 'days', 10, '', 3123123, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:40:21.844043', '2021-08-01 13:40:21.844068', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (514, '结束时间', 225, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:38:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:40:21.847063', '2021-08-01 13:40:21.847086', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (515, '开始时间', 225, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:38:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:40:21.850911', '2021-08-01 13:40:21.850936', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (516, '请假类型', 225, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 13:40:21.854322', '2021-08-01 13:40:21.854351', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (517, '请假理由', 225, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1313123', '', '', '2021-08-01 13:40:21.857922', '2021-08-01 13:40:21.857947', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (518, '请假天数', 226, 'days', 10, '', 123, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:41:05.437167', '2021-08-01 13:41:05.437208', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (519, '结束时间', 226, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-07-10 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:41:05.440534', '2021-08-01 13:41:05.440559', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (520, '开始时间', 226, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:40:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:41:05.444017', '2021-08-01 13:41:05.444050', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (521, '请假类型', 226, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 13:41:05.447533', '2021-08-01 13:41:05.447558', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (522, '请假理由', 226, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1232213123123123123', '', '', '2021-08-01 13:41:05.451212', '2021-08-01 13:41:05.451255', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (523, '请假天数', 227, 'days', 10, '', 1231, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:46:44.613116', '2021-08-01 13:46:44.613146', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (524, '结束时间', 227, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:46:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:46:44.616672', '2021-08-01 13:46:44.616696', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (525, '开始时间', 227, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:46:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:46:44.620854', '2021-08-01 13:46:44.620884', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (526, '请假类型', 227, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 13:46:44.624246', '2021-08-01 13:46:44.624276', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (527, '请假理由', 227, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '2312312312231', '', '', '2021-08-01 13:46:44.628390', '2021-08-01 13:46:44.628416', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (528, '请假天数', 228, 'days', 10, '', 123123, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:48:01.431974', '2021-08-01 13:48:01.432006', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (529, '结束时间', 228, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:47:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:48:01.449886', '2021-08-01 13:48:01.450055', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (530, '开始时间', 228, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:47:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:48:01.461293', '2021-08-01 13:48:01.461334', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (531, '请假类型', 228, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 13:48:01.466660', '2021-08-01 13:48:01.466694', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (532, '请假理由', 228, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1231231', '', '', '2021-08-01 13:48:01.471936', '2021-08-01 13:48:01.471969', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (533, '请假天数', 229, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:48:55.457106', '2021-08-01 13:48:55.457131', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (534, '结束时间', 229, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:48:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:48:55.461339', '2021-08-01 13:48:55.461370', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (535, '开始时间', 229, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:48:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:48:55.464399', '2021-08-01 13:48:55.464422', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (536, '请假类型', 229, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 13:48:55.468183', '2021-08-01 13:48:55.468208', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (537, '请假理由', 229, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '123123', '', '', '2021-08-01 13:48:55.471301', '2021-08-01 13:48:55.471324', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (538, '请假天数', 230, 'days', 10, '', 3, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:50:14.439926', '2021-08-01 13:50:14.439967', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (539, '请假理由', 230, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1w131', '', '', '2021-08-01 13:50:14.444370', '2021-08-01 13:50:14.444394', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (540, '附件', 230, 'filename', 80, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:50:14.448026', '2021-08-01 13:50:14.448052', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (541, '开始时间', 230, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:50:09.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:50:14.451922', '2021-08-01 13:50:14.451947', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (542, '结束时间', 230, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 13:50:08.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 13:50:14.455193', '2021-08-01 13:50:14.455217', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (543, '请假类型', 230, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 13:50:14.458489', '2021-08-01 13:50:14.458512', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (544, '请假天数', 231, 'days', 10, '', 11111, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:02:25.153024', '2021-08-01 14:02:25.153058', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (545, '结束时间', 231, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 14:02:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:02:25.157890', '2021-08-01 14:02:25.157926', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (546, '开始时间', 231, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 14:02:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:02:25.162370', '2021-08-01 14:02:25.162404', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (547, '请假类型', 231, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 14:02:25.166830', '2021-08-01 14:02:25.166865', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (548, '请假理由', 231, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '11', '', '', '2021-08-01 14:02:25.171691', '2021-08-01 14:02:25.171725', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (549, '请假天数', 232, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:06:12.339151', '2021-08-01 14:06:12.339177', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (550, '结束时间', 232, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-05-13 22:24:41.952132', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:06:12.342591', '2021-08-01 14:06:12.342616', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (551, '开始时间', 232, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-05-13 22:24:41.952132', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:06:12.345908', '2021-08-01 14:06:12.345936', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (552, '请假类型', 232, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-08-01 14:06:12.349654', '2021-08-01 14:06:12.349677', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (553, '请假理由', 232, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '无', '', '', '2021-08-01 14:06:12.353169', '2021-08-01 14:06:12.353191', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (554, '附件', 232, 'filename', 80, '123', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:06:12.356727', '2021-08-01 14:06:12.356756', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (555, '请假天数', 233, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:07:59.396948', '2021-08-01 14:07:59.396980', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (556, '结束时间', 233, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-05-13 22:24:41.952132', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:07:59.402517', '2021-08-01 14:07:59.402583', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (557, '开始时间', 233, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-05-13 22:24:41.952132', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:07:59.406544', '2021-08-01 14:07:59.406577', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (558, '请假类型', 233, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-08-01 14:07:59.409975', '2021-08-01 14:07:59.410007', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (559, '请假理由', 233, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '无', '', '', '2021-08-01 14:07:59.413994', '2021-08-01 14:07:59.414044', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (560, '附件', 233, 'filename', 80, 'media/upload/202108/TESTIMG1627796879043.png', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:07:59.417450', '2021-08-01 14:07:59.417476', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (561, '请假天数', 234, 'days', 10, '', 123, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:18:24.233353', '2021-08-01 14:18:24.233382', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (562, '结束时间', 234, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 14:18:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:18:24.236733', '2021-08-01 14:18:24.236757', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (563, '开始时间', 234, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 14:18:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:18:24.240529', '2021-08-01 14:18:24.240595', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (564, '请假类型', 234, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 14:18:24.244145', '2021-08-01 14:18:24.244168', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (565, '请假理由', 234, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'wwwwwwwwwww', '', '', '2021-08-01 14:18:24.248487', '2021-08-01 14:18:24.248532', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (566, '附件', 234, 'filename', 80, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:18:24.252044', '2021-08-01 14:18:24.252068', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (567, '请假天数', 235, 'days', 10, '', 1231231223, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:18:53.674733', '2021-08-01 14:18:53.674771', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (568, '结束时间', 235, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 14:18:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:18:53.700737', '2021-08-01 14:18:53.700771', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (569, '开始时间', 235, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 14:18:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:18:53.728619', '2021-08-01 14:18:53.728652', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (570, '请假类型', 235, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 14:18:53.758312', '2021-08-01 14:18:53.758354', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (571, '请假理由', 235, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '123123213123', '', '', '2021-08-01 14:18:53.790205', '2021-08-01 14:18:53.790236', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (572, '附件', 235, 'filename', 80, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:18:53.816510', '2021-08-01 14:18:53.816538', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (573, '请假天数', 236, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:21:42.478970', '2021-08-01 14:21:42.479003', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (574, '结束时间', 236, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2018-05-13 22:24:41.952132', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:21:42.483371', '2021-08-01 14:21:42.483405', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (575, '开始时间', 236, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2018-05-13 22:24:41.952132', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:21:42.487364', '2021-08-01 14:21:42.487395', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (576, '请假类型', 236, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-08-01 14:21:42.491114', '2021-08-01 14:21:42.491143', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (577, '请假理由', 236, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '无', '', '', '2021-08-01 14:21:42.494601', '2021-08-01 14:21:42.494630', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (578, '附件', 236, 'filename', 80, 'media/upload/202108/TESTIMG21627798723013.png', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:21:42.498379', '2021-08-01 14:21:42.498404', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (579, '请假天数', 237, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:37:14.156998', '2021-08-01 14:37:14.157030', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (580, '结束时间', 237, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-27 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:37:14.160610', '2021-08-01 14:37:14.160635', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (581, '开始时间', 237, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 14:37:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:37:14.164031', '2021-08-01 14:37:14.164057', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (582, '请假类型', 237, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 14:37:14.168336', '2021-08-01 14:37:14.168369', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (583, '请假理由', 237, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', 'WWWWWWWWWW', '', '', '2021-08-01 14:37:14.172569', '2021-08-01 14:37:14.172601', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (584, '附件', 237, 'filename', 80, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:37:14.177054', '2021-08-01 14:37:14.177079', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (585, '请假天数', 238, 'days', 10, '', 12312313, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:39:26.018196', '2021-08-01 14:39:26.018223', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (586, '结束时间', 238, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 14:39:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:39:26.022302', '2021-08-01 14:39:26.022338', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (587, '开始时间', 238, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 14:39:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:39:26.026532', '2021-08-01 14:39:26.026566', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (588, '请假类型', 238, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 14:39:26.031180', '2021-08-01 14:39:26.031214', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (589, '请假理由', 238, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '213123123123', '', '', '2021-08-01 14:39:26.034519', '2021-08-01 14:39:26.034544', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (590, '附件', 238, 'filename', 80, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:39:26.038268', '2021-08-01 14:39:26.038293', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (591, '请假天数', 239, 'days', 10, '', 1231, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:40:44.704236', '2021-08-01 14:40:44.704294', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (592, '结束时间', 239, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 14:40:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:40:44.708048', '2021-08-01 14:40:44.708082', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (593, '开始时间', 239, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 14:40:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:40:44.712062', '2021-08-01 14:40:44.712103', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (594, '请假类型', 239, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 14:40:44.716390', '2021-08-01 14:40:44.716419', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (595, '请假理由', 239, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '322131312', '', '', '2021-08-01 14:40:44.721423', '2021-08-01 14:40:44.721458', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (596, '附件', 239, 'filename', 80, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:40:44.725629', '2021-08-01 14:40:44.725675', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (597, '请假天数', 240, 'days', 10, '', 123131, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:53:01.824663', '2021-08-01 14:53:01.824700', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (598, '结束时间', 240, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 14:52:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:53:01.828490', '2021-08-01 14:53:01.828519', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (599, '开始时间', 240, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 14:52:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:53:01.832378', '2021-08-01 14:53:01.832405', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (600, '请假类型', 240, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 14:53:01.837214', '2021-08-01 14:53:01.837247', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (601, '请假理由', 240, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '3213131231', '', '', '2021-08-01 14:53:01.841520', '2021-08-01 14:53:01.841556', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (602, '附件', 240, 'filename', 80, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:53:01.845225', '2021-08-01 14:53:01.845252', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (603, '请假天数', 241, 'days', 10, '', 123123, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:54:15.795973', '2021-08-01 14:54:15.796000', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (604, '结束时间', 241, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 14:53:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:54:15.800219', '2021-08-01 14:54:15.800247', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (605, '开始时间', 241, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 14:53:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:54:15.803768', '2021-08-01 14:54:15.803798', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (606, '请假类型', 241, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 14:54:15.808312', '2021-08-01 14:54:15.808338', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (607, '请假理由', 241, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '1231231', '', '', '2021-08-01 14:54:15.813030', '2021-08-01 14:54:15.813119', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (608, '附件', 241, 'filename', 80, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:54:15.819547', '2021-08-01 14:54:15.819660', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (609, '请假天数', 242, 'days', 10, '', 213123, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:55:00.135702', '2021-08-01 14:55:00.135740', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (610, '结束时间', 242, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 14:54:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:55:00.139936', '2021-08-01 14:55:00.139972', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (611, '开始时间', 242, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 14:54:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:55:00.144431', '2021-08-01 14:55:00.144465', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (612, '请假类型', 242, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 14:55:00.147977', '2021-08-01 14:55:00.148003', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (613, '请假理由', 242, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '12321313', '', '', '2021-08-01 14:55:00.151791', '2021-08-01 14:55:00.151816', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (614, '附件', 242, 'filename', 80, '/media/upload/202108/21627800887288.png', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 14:55:00.155204', '2021-08-01 14:55:00.155230', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (615, '请假天数', 243, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 15:02:28.936868', '2021-08-01 15:02:28.936913', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (616, '结束时间', 243, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-02 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 15:02:28.940666', '2021-08-01 15:02:28.940698', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (617, '开始时间', 243, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 15:02:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 15:02:28.945016', '2021-08-01 15:02:28.945054', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (618, '请假类型', 243, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 15:02:28.951108', '2021-08-01 15:02:28.951141', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (619, '请假理由', 243, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '哇哇哇哇哇哇哇哇哇哇哇哇哇哇哇哇', '', '', '2021-08-01 15:02:28.954612', '2021-08-01 15:02:28.954639', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (620, '附件', 243, 'filename', 80, '/media/upload/202108/理由1627801346063.docx', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 15:02:28.958639', '2021-08-01 15:02:28.958663', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (621, '请假天数', 244, 'days', 10, '', 2, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 15:08:56.773103', '2021-08-01 15:08:56.773128', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (622, '结束时间', 244, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-03 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 15:08:56.777308', '2021-08-01 15:08:56.777334', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (623, '开始时间', 244, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 15:08:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 15:08:56.780607', '2021-08-01 15:08:56.780629', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (624, '请假类型', 244, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 15:08:56.784338', '2021-08-01 15:08:56.784363', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (625, '请假理由', 244, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '哇哇哇哇哇哇哇', '', '', '2021-08-01 15:08:56.787490', '2021-08-01 15:08:56.787511', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (626, '附件', 244, 'filename', 80, '/media/upload/202108/11627801735068.png', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 15:08:56.791218', '2021-08-01 15:08:56.791242', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (627, '请假天数', 245, 'days', 10, '', 11, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 15:09:22.105026', '2021-08-01 15:09:22.105064', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (628, '结束时间', 245, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-12 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 15:09:22.109876', '2021-08-01 15:09:22.109900', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (629, '开始时间', 245, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 15:09:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 15:09:22.113708', '2021-08-01 15:09:22.113749', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (630, '请假类型', 245, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 15:09:22.117894', '2021-08-01 15:09:22.117918', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (631, '请假理由', 245, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', ' 达瓦达瓦发我f哇哇哒哒哒啊打', '', '', '2021-08-01 15:09:22.122072', '2021-08-01 15:09:22.122099', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (632, '附件', 245, 'filename', 80, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 15:09:22.126065', '2021-08-01 15:09:22.126091', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (633, '请假天数', 246, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:38:55.504261', '2021-08-01 21:38:55.504288', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (634, '结束时间', 246, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-02 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:38:55.511094', '2021-08-01 21:38:55.511125', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (635, '开始时间', 246, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 21:38:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:38:55.515468', '2021-08-01 21:38:55.515527', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (636, '请假类型', 246, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 21:38:55.522301', '2021-08-01 21:38:55.522338', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (637, '请假理由', 246, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '这里是请假原因 这里是请假原因 这里是请假原因', '', '', '2021-08-01 21:38:55.556617', '2021-08-01 21:38:55.556642', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (638, '附件', 246, 'filename', 80, '/media/upload/202108/11627825132912.png', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:38:55.560436', '2021-08-01 21:38:55.560473', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (639, '请假天数', 247, 'days', 10, '', 2, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:39:28.368144', '2021-08-01 21:39:28.368180', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (640, '结束时间', 247, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-03 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:39:28.372291', '2021-08-01 21:39:28.372315', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (641, '开始时间', 247, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 21:39:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:39:28.376593', '2021-08-01 21:39:28.376627', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (642, '请假类型', 247, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 21:39:28.380678', '2021-08-01 21:39:28.380703', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (643, '请假理由', 247, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '这里是请假原因这里是请假原因这里是请假原因这里是请假原因这里是请假原因', '', '', '2021-08-01 21:39:28.384725', '2021-08-01 21:39:28.384750', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (644, '附件', 247, 'filename', 80, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:39:28.391452', '2021-08-01 21:39:28.391476', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (645, '请假天数', 248, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:40:13.998268', '2021-08-01 21:40:13.998301', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (646, '结束时间', 248, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-02 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:40:14.001828', '2021-08-01 21:40:14.001852', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (647, '开始时间', 248, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 21:40:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:40:14.006228', '2021-08-01 21:40:14.006252', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (648, '请假类型', 248, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-08-01 21:40:14.009615', '2021-08-01 21:40:14.009638', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (649, '请假理由', 248, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '这里是请假原因这里是请假原因这里是请假原因这里是请假原因这里是请假原因这里是请假原因', '', '', '2021-08-01 21:40:14.013735', '2021-08-01 21:40:14.013759', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (650, '附件', 248, 'filename', 80, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:40:14.017517', '2021-08-01 21:40:14.017555', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (651, '请假天数', 249, 'days', 10, '', 2, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:40:34.921715', '2021-08-01 21:40:34.921746', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (652, '结束时间', 249, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-03 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:40:34.925522', '2021-08-01 21:40:34.925546', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (653, '开始时间', 249, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 21:40:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:40:34.929822', '2021-08-01 21:40:34.929846', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (654, '请假类型', 249, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '1', '', '', '', '', '', '', '2021-08-01 21:40:34.933125', '2021-08-01 21:40:34.933177', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (655, '请假理由', 249, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '这里是请假原因这里是请假原因这里是请假原因这里是请假原因这里是请假原因这里是请假原因', '', '', '2021-08-01 21:40:34.936901', '2021-08-01 21:40:34.936925', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (656, '附件', 249, 'filename', 80, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:40:34.940496', '2021-08-01 21:40:34.940565', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (657, '请假天数', 250, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:43:22.451574', '2021-08-01 21:43:22.451617', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (658, '结束时间', 250, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-02 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:43:22.455837', '2021-08-01 21:43:22.455863', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (659, '开始时间', 250, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 21:43:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:43:22.460721', '2021-08-01 21:43:22.460766', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (660, '请假类型', 250, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-08-01 21:43:22.464692', '2021-08-01 21:43:22.464717', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (661, '请假理由', 250, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '十四说四十飒飒是', '', '', '2021-08-01 21:43:22.468563', '2021-08-01 21:43:22.468600', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (662, '附件', 250, 'filename', 80, '/media/upload/202108/11627825399282.png', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:43:22.472080', '2021-08-01 21:43:22.472108', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (663, '请假天数', 251, 'days', 10, '', 1, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:53:58.879669', '2021-08-01 21:53:58.879693', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (664, '结束时间', 251, 'leave_end', 30, '', 0, 0, 0, '0001-01-01', '2021-08-02 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:53:58.883520', '2021-08-01 21:53:58.883545', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (665, '开始时间', 251, 'leave_start', 30, '', 0, 0, 0, '0001-01-01', '2021-08-01 21:53:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:53:58.887040', '2021-08-01 21:53:58.887064', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (666, '请假类型', 251, 'leave_type', 35, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '0', '', '', '', '', '', '', '2021-08-01 21:53:58.890933', '2021-08-01 21:53:58.890960', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (667, '请假理由', 251, 'text_desp', 55, '', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '请假原因', '', '', '2021-08-01 21:53:58.895008', '2021-08-01 21:53:58.895054', 0, '');
INSERT INTO `ticket_ticketcustomfield` VALUES (668, '附件', 251, 'filename', 80, '/media/upload/202108/11627826036719.png', 0, 0, 0, '0001-01-01', '0001-01-01 00:00:00.000000', '00:00:01.000000', '', '', '', '', '', '', '', '2021-08-01 21:53:58.898857', '2021-08-01 21:53:58.898881', 0, '');

-- ----------------------------
-- Table structure for ticket_ticketflowlog
-- ----------------------------
DROP TABLE IF EXISTS `ticket_ticketflowlog`;
CREATE TABLE `ticket_ticketflowlog`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `ticket_id` int(11) NOT NULL,
  `transition_id` int(11) NOT NULL,
  `suggestion` varchar(10000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `participant_type_id` int(11) NOT NULL,
  `participant` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `state_id` int(11) NOT NULL,
  `ticket_data` varchar(10000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `creator` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `intervene_type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_ticket_id`(`ticket_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 265 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of ticket_ticketflowlog
-- ----------------------------
INSERT INTO `ticket_ticketflowlog` VALUES (9, 13, 1, '', 1, 'lilei', 1, '', 'admin', '2018-05-13 21:53:15.820550', '2018-05-13 21:53:15.820610', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (10, 14, 2, '', 1, 'lilei', 1, '', 'admin', '2018-05-13 22:24:42.021711', '2018-05-13 22:24:42.021792', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (11, 15, 2, '', 1, 'lilei', 1, '', 'admin', '2018-05-13 22:28:21.686709', '2018-05-13 22:28:21.686769', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (12, 16, 1, '', 1, 'lilei', 1, '', 'admin', '2018-05-13 22:34:12.744844', '2018-05-13 22:34:12.744912', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (13, 14, 14, '保存草稿', 1, 'lilei', 2, '', 'lilei', '2018-05-13 22:59:06.743524', '2018-05-13 22:59:06.743634', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (14, 14, 14, '保存草稿', 1, 'lilei', 2, '', 'lilei', '2018-05-13 23:00:44.421329', '2018-05-13 23:00:44.421396', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (15, 14, 14, '保存草稿', 1, 'lilei', 2, '', 'lilei', '2018-05-13 23:04:40.758014', '2018-05-13 23:04:40.758125', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (16, 14, 14, '保存草稿', 1, 'lilei', 2, '', 'lilei', '2018-05-13 23:07:21.279315', '2018-05-13 23:07:21.280068', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (17, 14, 14, '保存草稿', 1, 'lilei', 2, '', 'lilei', '2018-05-13 23:10:19.742789', '2018-05-13 23:10:19.742861', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (18, 14, 14, '保存草稿', 1, 'lilei', 2, '', 'lilei', '2018-05-13 23:52:21.760281', '2018-05-13 23:52:21.760339', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (19, 14, 14, '保存草稿', 1, 'lilei', 2, '', 'lilei', '2018-05-14 00:01:54.824910', '2018-05-14 00:01:54.824974', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (20, 14, 14, '保存草稿', 1, 'lilei', 2, '', 'lilei', '2018-05-14 00:02:45.942264', '2018-05-14 00:02:45.942325', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (21, 14, 14, '保存草稿', 1, 'lilei', 2, '', 'lilei', '2018-05-14 00:12:18.293208', '2018-05-14 00:12:18.293269', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (22, 14, 14, '保存草稿', 1, 'lilei', 2, '', 'lilei', '2018-05-14 00:15:43.074352', '2018-05-14 00:15:43.074635', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (23, 14, 14, '保存草稿', 1, 'lilei', 2, '', 'lilei', '2018-05-14 00:21:56.019252', '2018-05-14 00:21:56.019666', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (24, 14, 14, '保存草稿', 1, 'lilei', 2, '', 'lilei', '2018-05-14 00:24:11.381536', '2018-05-14 00:24:11.381609', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (25, 14, 14, '保存草稿', 1, 'lilei', 2, '', 'lilei', '2018-05-14 06:55:24.437483', '2018-05-14 06:55:24.437546', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (26, 15, 0, '转交工单', 1, 'lilei', 2, '', 'lilei', '2018-05-14 06:56:26.664730', '2018-05-14 06:56:26.664802', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (27, 15, 0, '转交工单', 1, 'zhangsan', 2, '', 'zhangsan', '2018-05-14 06:56:52.101637', '2018-05-14 06:56:52.101705', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (28, 15, 14, '保存草稿', 1, 'lilei', 2, '', 'lilei', '2018-05-14 06:59:33.505946', '2018-05-14 06:59:33.506019', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (29, 15, 13, '保存草稿', 1, 'lilei', 2, '', 'lilei', '2018-05-14 07:00:03.655105', '2018-05-14 07:00:03.655196', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (30, 15, 0, '强制修改工单状态', 1, 'lilei', 3, '', 'admin', '2018-05-14 07:07:39.586383', '2018-05-14 07:07:39.586456', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (31, 14, 0, '加签工单', 1, 'lilei', 2, '', 'lilei', '2018-05-15 06:46:11.225083', '2018-05-15 06:46:11.225146', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (32, 17, 7, '', 1, 'lilei', 6, '', 'admin', '2018-05-15 07:16:38.332521', '2018-05-15 07:16:38.332680', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (33, 17, 8, '同意申请', 1, 'lilei', 7, '', 'lilei', '2018-05-15 07:20:40.816765', '2018-05-15 07:20:40.816925', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (34, 18, 7, '', 1, 'lilei', 6, '', 'admin', '2018-05-15 07:37:28.012487', '2018-05-15 07:37:28.012548', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (35, 18, 8, '同意申请', 1, 'lilei', 7, '', 'lilei', '2018-05-15 07:37:37.111956', '2018-05-15 07:37:37.112027', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (36, 17, 0, '接单处理', 1, 'guiji', 8, '', 'guiji', '2018-05-16 06:42:00.998562', '2018-05-16 06:42:00.998625', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (37, 17, 9, '同意', 1, 'guiji', 8, '', 'guiji', '2018-05-16 06:49:55.948811', '2018-05-16 06:49:55.948905', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (38, 17, 0, '接单处理', 1, 'guiji', 8, '', 'guiji', '2018-05-16 06:57:31.802266', '2018-05-16 06:57:31.802360', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (39, 17, 9, '同意', 1, 'guiji', 8, '', 'guiji', '2018-05-16 06:57:36.347563', '2018-05-16 06:57:36.347634', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (40, 17, 9, '同意', 1, 'guiji', 8, '', 'guiji', '2018-05-16 06:58:41.660593', '2018-05-16 06:58:41.660701', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (41, 17, 9, '同意', 1, 'guiji', 8, '', 'guiji', '2018-05-16 07:01:53.888622', '2018-05-16 07:01:53.888689', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (42, 17, 10, 'False\n', 6, 'demo_script.py', 9, '', 'loonrobot', '2018-05-16 07:01:54.040851', '2018-05-16 07:01:54.041150', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (43, 17, 9, '同意', 1, 'guiji', 8, '', 'guiji', '2018-05-16 07:03:34.673960', '2018-05-16 07:03:34.674037', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (44, 17, 10, 'False\n', 6, 'demo_script.py', 9, '', 'loonrobot', '2018-05-16 07:03:34.846610', '2018-05-16 07:03:34.847216', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (45, 17, 9, '同意', 1, 'guiji', 8, '', 'guiji', '2018-05-16 07:04:45.745455', '2018-05-16 07:04:45.745521', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (46, 17, 10, 'False\n', 6, 'demo_script.py', 9, '', 'loonrobot', '2018-05-16 07:04:45.955902', '2018-05-16 07:04:45.956166', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (47, 17, 9, '同意', 1, 'guiji', 8, '', 'guiji', '2018-05-16 07:31:29.378033', '2018-05-16 07:31:29.378090', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (48, 17, 10, 'lilei\n', 6, 'demo_script.py', 9, '', 'loonrobot', '2018-05-16 07:31:29.552179', '2018-05-16 07:31:29.552446', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (49, 17, 9, '同意', 1, 'guiji', 8, '', 'guiji', '2018-05-16 23:21:00.251306', '2018-05-16 23:21:00.251363', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (50, 17, 10, 'lilei\n', 6, 'demo_script.py', 9, '', 'loonrobot', '2018-05-16 23:21:00.578354', '2018-05-16 23:21:00.578555', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (51, 17, 9, '同意', 1, 'guiji', 8, '', 'guiji', '2018-05-16 23:24:03.606092', '2018-05-16 23:24:03.606156', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (52, 17, 10, 'lilei\n', 6, 'demo_script.py', 9, '', 'loonrobot', '2018-05-16 23:24:03.779136', '2018-05-16 23:24:03.779504', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (53, 17, 9, '同意', 1, 'guiji', 8, '', 'guiji', '2018-05-16 23:24:44.286319', '2018-05-16 23:24:44.286429', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (54, 17, 10, 'lilei\n', 6, 'demo_script.py', 9, '', 'loonrobot', '2018-05-16 23:24:44.338829', '2018-05-16 23:24:44.339101', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (55, 17, 9, '同意', 1, 'guiji', 8, '', 'guiji', '2018-05-16 23:33:26.619543', '2018-05-16 23:33:26.619613', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (56, 17, 10, 'lilei\n', 6, 'demo_script.py', 9, '', 'loonrobot', '2018-05-16 23:33:26.803850', '2018-05-16 23:33:26.804073', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (57, 17, 0, '请处理', 1, 'lilei', 10, '', 'lilei', '2018-05-17 06:45:58.830078', '2018-05-17 06:45:58.830167', 0, 1);
INSERT INTO `ticket_ticketflowlog` VALUES (58, 17, 0, '请协助处理', 1, 'zhangsan', 10, '', 'zhangsan', '2018-05-17 06:47:46.380983', '2018-05-17 06:47:46.381055', 0, 2);
INSERT INTO `ticket_ticketflowlog` VALUES (59, 19, 1, '', 1, 'admin', 1, '{\"leave_days\": \"2\", \"leave_proxy\": \"admin\", \"title\": \"testt\", \"in_add_node\": false, \"is_deleted\": false, \"gmt_modified\": \"2018-10-19 00:08:40.380672\", \"add_node_man\": \"\", \"sn\": \"loonflow_201810190001\", \"leave_type\": \"2\", \"gmt_created\": \"2018-10-19 00:08:40.371908\", \"parent_ticket_id\": 0, \"leave_reason\": \"<p>teste</p>\", \"leave_start\": \"2018-10-20 09:00:00\", \"participant_type_id\": 1, \"state_id\": 3, \"workflow_id\": 1, \"parent_ticket_state_id\": 0, \"relation\": \"admin\", \"participant\": \"admin\", \"leave_end\": \"2018-10-21 18:00:00\", \"creator\": \"admin\"}', 'admin', '2018-10-19 00:08:40.466104', '2018-10-19 00:08:40.466128', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (60, 20, 1, '', 1, 'admin', 1, '{\"leave_reason\": \"<p>dfsf</p>\", \"sn\": \"loonflow_201810190002\", \"add_node_man\": \"\", \"leave_days\": \"2\", \"participant\": \"admin\", \"title\": \"teste\", \"gmt_modified\": \"2018-10-19 00:38:41.359283\", \"workflow_id\": 1, \"creator\": \"admin\", \"leave_start\": \"2018-10-19 12:00:00\", \"is_deleted\": false, \"parent_ticket_id\": 0, \"relation\": \"admin\", \"leave_type\": \"2\", \"leave_end\": \"2018-10-20 12:00:00\", \"state_id\": 3, \"in_add_node\": false, \"leave_proxy\": \"admin\", \"participant_type_id\": 1, \"gmt_created\": \"2018-10-19 00:38:41.354008\", \"parent_ticket_state_id\": 0}', 'admin', '2018-10-19 00:38:41.428448', '2018-10-19 00:38:41.428473', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (61, 20, 3, 'fdsfsf', 1, 'admin', 3, '{\"leave_reason\": \"<p>dfsf</p>\", \"sn\": \"loonflow_201810190002\", \"add_node_man\": \"\", \"leave_days\": \"2\", \"participant\": \"jack\", \"title\": \"teste\", \"gmt_modified\": \"2018-10-19 00:38:53.872124\", \"workflow_id\": 1, \"creator\": \"admin\", \"leave_start\": \"2018-10-19 12:00:00\", \"is_deleted\": false, \"parent_ticket_id\": 0, \"relation\": \"jack,admin\", \"leave_type\": \"2\", \"leave_end\": \"2018-10-20 12:00:00\", \"state_id\": 4, \"in_add_node\": false, \"leave_proxy\": \"admin\", \"participant_type_id\": 1, \"gmt_created\": \"2018-10-19 00:38:41.354008\", \"parent_ticket_state_id\": 0}', 'admin', '2018-10-19 00:38:53.942394', '2018-10-19 00:38:53.942431', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (62, 21, 15, '', 1, 'admin', 13, '{\"gmt_modified\": \"2018-10-21 11:14:37.663604\", \"gmt_created\": \"2018-10-21 11:14:37.656067\", \"creator\": \"admin\", \"parent_ticket_state_id\": 0, \"participant\": \"loonrobot\", \"workflow_id\": 3, \"parent_ticket_id\": 0, \"in_add_node\": false, \"project_qas\": \"admin\", \"participant_type_id\": 1, \"relation\": \"loonrobot,admin\", \"project_devs\": \"admin\", \"state_id\": 14, \"is_deleted\": false, \"sn\": \"loonflow_201810210001\", \"add_node_man\": \"\", \"title\": \"\", \"project_code\": \"prj001\"}', 'admin', '2018-10-21 11:14:37.775029', '2018-10-21 11:14:37.775227', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (63, 19, 5, '111', 1, 'jack', 4, '{\"leave_end\": \"2018-10-21 18:00:00\", \"parent_ticket_state_id\": 0, \"participant_type_id\": 0, \"title\": \"testt\", \"sn\": \"loonflow_201810190001\", \"leave_reason\": \"<p>teste</p>\", \"gmt_modified\": \"2018-10-21 20:06:57.527067\", \"participant\": \"\", \"parent_ticket_id\": 0, \"workflow_id\": 1, \"relation\": \"jack,admin\", \"is_deleted\": false, \"creator\": \"admin\", \"leave_type\": \"2\", \"add_node_man\": \"\", \"leave_start\": \"2018-10-20 09:00:00\", \"in_add_node\": false, \"state_id\": 5, \"leave_proxy\": \"admin\", \"leave_days\": \"2\", \"gmt_created\": \"2018-10-19 00:08:40.371908\"}', 'jack', '2018-10-21 20:06:57.579230', '2018-10-21 20:06:57.579267', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (64, 22, 1, '', 1, 'jack', 1, '{\"is_deleted\": false, \"parent_ticket_state_id\": 0, \"leave_proxy\": \"admin\", \"leave_end\": \"2018-10-23 12:00:00\", \"leave_start\": \"2018-10-22 12:00:00\", \"creator\": \"jack\", \"participant_type_id\": 1, \"in_add_node\": false, \"parent_ticket_id\": 0, \"relation\": \"jack\", \"title\": \"tttttt\", \"leave_days\": \"1\", \"sn\": \"loonflowhhh_201810220001\", \"participant\": \"jack\", \"leave_type\": \"3\", \"add_node_man\": \"\", \"gmt_modified\": \"2018-10-22 07:12:16.455740\", \"leave_reason\": \"<p>ddd</p>\", \"state_id\": 3, \"workflow_id\": 1, \"gmt_created\": \"2018-10-22 07:12:16.451086\"}', 'admin', '2018-10-22 07:12:16.542137', '2018-10-22 07:12:16.542163', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (65, 23, 1, '', 1, 'jack', 1, '{\"is_deleted\": false, \"parent_ticket_state_id\": 0, \"leave_proxy\": \"admin\", \"leave_end\": \"2018-10-24 12:00:00\", \"leave_start\": \"2018-10-22 12:00:00\", \"creator\": \"jack\", \"participant_type_id\": 1, \"in_add_node\": false, \"parent_ticket_id\": 0, \"relation\": \"jack\", \"title\": \"ttttest\", \"leave_days\": \"2\", \"sn\": \"loonflow_201810220002\", \"participant\": \"jack\", \"leave_type\": \"3\", \"add_node_man\": \"\", \"gmt_modified\": \"2018-10-22 08:05:37.192994\", \"leave_reason\": \"<p>te</p>\", \"state_id\": 3, \"workflow_id\": 1, \"gmt_created\": \"2018-10-22 08:05:37.187794\"}', 'admin', '2018-10-22 08:05:37.270333', '2018-10-22 08:05:37.270359', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (66, 24, 1, '', 1, 'admin', 1, '{\"relation\": \"admin\", \"leave_reason\": \"<p>11</p>\", \"sn\": \"loonflow_201811270001\", \"parent_ticket_id\": 0, \"participant_type_id\": 1, \"title\": \"tttt\", \"leave_proxy\": \"admin\", \"parent_ticket_state_id\": 0, \"gmt_modified\": \"2018-11-27 07:09:06.326441\", \"add_node_man\": \"\", \"is_deleted\": false, \"creator\": \"admin\", \"state_id\": 3, \"leave_type\": \"1\", \"workflow_id\": 1, \"participant\": \"admin\", \"in_add_node\": false, \"leave_start\": \"2018-11-27 12:00:00\", \"leave_end\": \"2018-11-28 12:00:00\", \"gmt_created\": \"2018-11-27 07:09:06.308678\", \"leave_days\": \"1\"}', 'admin', '2018-11-27 07:09:06.409476', '2018-11-27 07:09:06.409515', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (67, 25, 1, '', 1, 'admin', 1, '{\"relation\": \"guiji,admin,lilei,zhangsan\", \"leave_reason\": \"<p>111</p>\", \"sn\": \"loonflow_201811270002\", \"parent_ticket_id\": 0, \"participant_type_id\": 4, \"title\": \"ttt21\", \"leave_proxy\": \"admin\", \"parent_ticket_state_id\": 0, \"gmt_modified\": \"2018-11-27 07:12:27.929123\", \"add_node_man\": \"\", \"is_deleted\": false, \"creator\": \"admin\", \"state_id\": 3, \"leave_type\": \"1\", \"workflow_id\": 1, \"participant\": \"2\", \"in_add_node\": false, \"leave_start\": \"2018-11-27 12:00:00\", \"leave_end\": \"2018-11-28 12:00:00\", \"gmt_created\": \"2018-11-27 07:12:27.917523\", \"leave_days\": \"1\"}', 'admin', '2018-11-27 07:12:28.003629', '2018-11-27 07:12:28.003659', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (68, 26, 1, '', 1, 'admin', 1, '{\"leave_start\": \"2018-11-27 12:00:00\", \"leave_reason\": \"<p>111</p>\", \"creator\": \"admin\", \"participant\": \"2\", \"relation\": \"lilei,admin,zhangsan,guiji\", \"leave_days\": \"1\", \"is_deleted\": false, \"parent_ticket_state_id\": 0, \"leave_end\": \"2018-11-28 12:00:00\", \"workflow_id\": 1, \"leave_type\": \"1\", \"in_add_node\": false, \"parent_ticket_id\": 0, \"sn\": \"loonflow_201811270003\", \"leave_proxy\": \"admin\", \"add_node_man\": \"\", \"title\": \"tttt\", \"participant_type_id\": 4, \"gmt_created\": \"2018-11-27 07:14:06.360734\", \"state_id\": 3, \"gmt_modified\": \"2018-11-27 07:14:06.377165\"}', 'admin', '2018-11-27 07:14:06.525209', '2018-11-27 07:14:06.525258', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (69, 27, 1, '', 1, 'admin', 1, '{\"parent_ticket_state_id\": 0, \"gmt_modified\": \"2018-11-27 07:20:16.212155\", \"gmt_created\": \"2018-11-27 07:20:16.194872\", \"relation\": \"admin,zhangsan,lilei,guiji\", \"workflow_id\": 1, \"state_id\": 3, \"in_add_node\": false, \"sn\": \"loonflow_201811270004\", \"leave_end\": \"2018-11-28 12:00:00\", \"title\": \"11111\", \"leave_proxy\": \"admin\", \"leave_reason\": \"<p>111</p>\", \"participant\": \"2\", \"creator\": \"admin\", \"leave_days\": \"1\", \"add_node_man\": \"\", \"is_deleted\": false, \"parent_ticket_id\": 0, \"leave_type\": \"1\", \"leave_start\": \"2018-11-27 12:00:00\", \"participant_type_id\": 4}', 'admin', '2018-11-27 07:20:16.498933', '2018-11-27 07:20:16.498980', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (70, 28, 1, '', 1, 'admin', 1, '{\"parent_ticket_state_id\": 0, \"gmt_modified\": \"2018-11-27 07:21:00.015804\", \"gmt_created\": \"2018-11-27 07:21:00.015751\", \"relation\": \"admin\", \"workflow_id\": 1, \"state_id\": 3, \"in_add_node\": false, \"sn\": \"loonflow_201811270005\", \"leave_end\": \"2018-11-28 12:00:00\", \"title\": \"tttt\", \"leave_proxy\": \"admin\", \"leave_reason\": \"<p>1111</p>\", \"participant\": \"[\'zhangsan\']\", \"creator\": \"admin\", \"leave_days\": \"1\", \"add_node_man\": \"\", \"is_deleted\": false, \"parent_ticket_id\": 0, \"leave_type\": \"1\", \"leave_start\": \"2018-11-27 12:00:00\", \"participant_type_id\": 1}', 'admin', '2018-11-27 07:21:00.213080', '2018-11-27 07:21:00.213125', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (71, 29, 1, '', 1, 'admin', 1, '{\"leave_end\": \"2018-11-28 12:00:00\", \"in_add_node\": false, \"add_node_man\": \"\", \"participant\": \"zhangsan\", \"leave_days\": \"1\", \"leave_start\": \"2018-11-27 12:00:00\", \"state_id\": 3, \"gmt_modified\": \"2018-11-27 07:23:04.031786\", \"title\": \"111122\", \"workflow_id\": 1, \"parent_ticket_id\": 0, \"gmt_created\": \"2018-11-27 07:23:04.023879\", \"relation\": \"admin,zhangsan\", \"leave_type\": \"1\", \"is_deleted\": false, \"parent_ticket_state_id\": 0, \"leave_reason\": \"<p>11</p>\", \"participant_type_id\": 1, \"leave_proxy\": \"admin\", \"creator\": \"admin\", \"sn\": \"loonflow_201811270006\"}', 'admin', '2018-11-27 07:23:04.196933', '2018-11-27 07:23:04.196977', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (72, 30, 1, '', 1, 'admin', 1, '{\"parent_ticket_id\": 0, \"leave_reason\": \"<p>11</p>\", \"leave_type\": \"1\", \"leave_proxy\": \"admin\", \"title\": \"111ww\", \"gmt_modified\": \"2018-11-27 07:23:47.926368\", \"leave_days\": \"1\", \"parent_ticket_state_id\": 0, \"workflow_id\": 1, \"participant_type_id\": 1, \"leave_start\": \"2018-11-27 12:00:00\", \"gmt_created\": \"2018-11-27 07:23:47.920099\", \"in_add_node\": false, \"add_node_man\": \"\", \"participant\": \"zhangsan\", \"is_deleted\": false, \"sn\": \"loonflow_201811270007\", \"leave_end\": \"2018-11-28 12:00:00\", \"relation\": \"zhangsan,admin\", \"state_id\": 3, \"creator\": \"admin\"}', 'admin', '2018-11-27 07:23:48.000430', '2018-11-27 07:23:48.000457', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (73, 31, 1, '', 1, 'admin', 1, '{\"parent_ticket_id\": 0, \"leave_reason\": \"<p>sdf</p>\", \"leave_type\": \"1\", \"leave_proxy\": \"admin\", \"title\": \"122131\", \"gmt_modified\": \"2018-11-27 07:24:07.533129\", \"leave_days\": \"1\", \"parent_ticket_state_id\": 0, \"workflow_id\": 1, \"participant_type_id\": 1, \"leave_start\": \"2018-11-27 12:00:00\", \"gmt_created\": \"2018-11-27 07:24:07.528102\", \"in_add_node\": false, \"add_node_man\": \"\", \"participant\": \"zhangsan\", \"is_deleted\": false, \"sn\": \"loonflow_201811270008\", \"leave_end\": \"2018-11-28 12:00:00\", \"relation\": \"zhangsan,admin\", \"state_id\": 3, \"creator\": \"admin\"}', 'admin', '2018-11-27 07:24:07.615996', '2018-11-27 07:24:07.616022', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (74, 32, 1, '', 1, 'admin', 1, '{\"parent_ticket_id\": 0, \"leave_reason\": \"<p>1111</p>\", \"leave_type\": \"1\", \"leave_proxy\": \"admin\", \"title\": \"fdfsfds\", \"gmt_modified\": \"2018-11-27 07:24:31.254020\", \"leave_days\": \"1\", \"parent_ticket_state_id\": 0, \"workflow_id\": 1, \"participant_type_id\": 1, \"leave_start\": \"2018-11-27 12:00:00\", \"gmt_created\": \"2018-11-27 07:24:31.249309\", \"in_add_node\": false, \"add_node_man\": \"\", \"participant\": \"guiji\", \"is_deleted\": false, \"sn\": \"loonflow_201811270009\", \"leave_end\": \"2018-11-28 12:00:00\", \"relation\": \"admin,guiji\", \"state_id\": 3, \"creator\": \"admin\"}', 'admin', '2018-11-27 07:24:31.325195', '2018-11-27 07:24:31.325223', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (75, 33, 1, '', 1, 'admin', 1, '{\"creator\": \"admin\", \"leave_days\": \"1\", \"relation\": \"lilei,admin\", \"parent_ticket_id\": 0, \"add_node_man\": \"\", \"leave_type\": \"1\", \"leave_reason\": \"<p>111</p>\", \"leave_start\": \"2018-11-27 12:00:00\", \"is_deleted\": false, \"state_id\": 3, \"participant\": \"lilei\", \"participant_type_id\": 1, \"leave_proxy\": \"admin\", \"leave_end\": \"2018-11-28 12:00:00\", \"gmt_modified\": \"2018-11-27 07:27:39.233032\", \"parent_ticket_state_id\": 0, \"workflow_id\": 1, \"sn\": \"loonflow_201811270010\", \"gmt_created\": \"2018-11-27 07:27:39.226722\", \"in_add_node\": false, \"title\": \"ttt1\"}', 'admin', '2018-11-27 07:27:39.310221', '2018-11-27 07:27:39.310259', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (76, 34, 1, '', 1, 'admin', 1, '{\"is_rejected\": false, \"state_id\": 3, \"sn\": \"ops_201911240001\", \"in_add_node\": false, \"gmt_modified\": \"2019-11-24 10:23:07\", \"participant_type_id\": 6, \"leave_days\": \"1\", \"gmt_created\": \"2019-11-24 10:23:07\", \"is_deleted\": false, \"leave_proxy\": \"admin\", \"leave_end\": \"2019-11-27 00:00:00\", \"title\": \"stestet\", \"leave_start\": \"2019-11-26 00:00:00\", \"creator\": \"admin\", \"parent_ticket_state_id\": 0, \"leave_reason\": \"<p>testest<br/></p>\", \"relation\": \"admin\", \"participant\": \"1\", \"id\": 34, \"script_run_last_result\": true, \"parent_ticket_id\": 0, \"leave_type\": \"1\", \"add_node_man\": \"\", \"multi_all_person\": \"{}\", \"is_end\": false, \"workflow_id\": 1}', 'admin', '2019-11-24 10:23:07.370718', '2019-11-24 10:23:07.370766', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (77, 35, 1, '', 1, 'admin', 1, '{\"add_node_man\": \"\", \"multi_all_person\": \"{}\", \"leave_type\": \"1\", \"relation\": \"admin\", \"state_id\": 3, \"leave_end\": \"2019-11-27 00:00:00\", \"leave_days\": \"1\", \"participant_type_id\": 6, \"in_add_node\": false, \"title\": \"stestet\", \"gmt_modified\": \"2019-11-24 10:24:31\", \"id\": 35, \"parent_ticket_state_id\": 0, \"sn\": \"ops_201911240002\", \"is_end\": false, \"is_deleted\": false, \"participant\": \"1\", \"workflow_id\": 1, \"is_rejected\": false, \"leave_start\": \"2019-11-26 00:00:00\", \"leave_proxy\": \"admin\", \"creator\": \"admin\", \"script_run_last_result\": true, \"leave_reason\": \"<p>testest<br/></p>\", \"gmt_created\": \"2019-11-24 10:24:31\", \"parent_ticket_id\": 0}', 'admin', '2019-11-24 10:24:31.830258', '2019-11-24 10:24:31.830309', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (78, 35, 3, 'Missing parentheses in call to \'print\' (<string>, line 1)', 6, '脚本:(id:1, name:创建虚拟机)', 3, '', 'loonrobot', '2020-01-16 22:22:40.114676', '2020-01-16 22:22:40.114927', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (79, 35, 0, 'testt', 1, 'admin', 3, '{\"id\": 35, \"creator\": \"admin\", \"gmt_created\": \"2019-11-24 10:24:31\", \"gmt_modified\": \"2020-03-29 09:47:04\", \"is_deleted\": false, \"title\": \"stestet\", \"workflow_id\": 1, \"sn\": \"ops_201911240002\", \"state_id\": 4, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"jack\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": false, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2019-11-26 00:00:00\", \"leave_end\": \"2019-11-27 00:00:00\", \"leave_days\": \"1\", \"leave_proxy\": \"admin\", \"leave_type\": \"1\", \"leave_reason\": \"<p>testest<br/></p>\"}', 'admin', '2020-03-29 09:47:04.414407', '2020-03-29 09:47:04.414431', 0, 8);
INSERT INTO `ticket_ticketflowlog` VALUES (80, 35, 0, 'tee', 1, 'admin', 4, '{\"id\": 35, \"creator\": \"admin\", \"gmt_created\": \"2019-11-24 10:24:31\", \"gmt_modified\": \"2020-03-29 09:47:26\", \"is_deleted\": false, \"title\": \"stestet\", \"workflow_id\": 1, \"sn\": \"ops_201911240002\", \"state_id\": 4, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"lilei\", \"relation\": \"admin,lilei\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": false, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2019-11-26 00:00:00\", \"leave_end\": \"2019-11-27 00:00:00\", \"leave_days\": \"1\", \"leave_proxy\": \"admin\", \"leave_type\": \"1\", \"leave_reason\": \"<p>testest<br/></p>\"}', 'admin', '2020-03-29 09:47:26.556723', '2020-03-29 09:47:26.556747', 0, 1);
INSERT INTO `ticket_ticketflowlog` VALUES (81, 35, 0, '强制关闭工单:ts', 1, 'admin', 5, '{\"id\": 35, \"creator\": \"admin\", \"gmt_created\": \"2019-11-24 10:24:31\", \"gmt_modified\": \"2020-03-29 09:47:26\", \"is_deleted\": false, \"title\": \"stestet\", \"workflow_id\": 1, \"sn\": \"ops_201911240002\", \"state_id\": 4, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"lilei\", \"relation\": \"admin,lilei\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": false, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2019-11-26 00:00:00\", \"leave_end\": \"2019-11-27 00:00:00\", \"leave_days\": \"1\", \"leave_proxy\": \"admin\", \"leave_type\": \"1\", \"leave_reason\": \"<p>testest<br/></p>\"}', 'admin', '2020-03-29 09:47:33.838219', '2020-03-29 09:47:33.838250', 0, 7);
INSERT INTO `ticket_ticketflowlog` VALUES (82, 36, 7, '', 1, 'admin', 6, '{\"id\": 36, \"creator\": \"admin\", \"gmt_created\": \"2020-04-11 10:40:30\", \"gmt_modified\": \"2020-04-11 10:40:30\", \"is_deleted\": false, \"title\": \"fdfdsf\", \"workflow_id\": 2, \"sn\": \"ops1_bd_202004110004\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"admin\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"vpn_reason\": \"<p>sfdsf</p>\"}', 'admin', '2020-04-11 10:40:31.070230', '2020-04-11 10:40:31.070508', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (83, 37, 7, '', 1, 'admin', 6, '{\"id\": 37, \"creator\": \"admin\", \"gmt_created\": \"2020-05-01 09:19:28\", \"gmt_modified\": \"2020-05-01 09:19:28\", \"is_deleted\": false, \"title\": \"test\", \"workflow_id\": 2, \"sn\": \"ops122222212_202005010001\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"admin\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"vpn_reason\": \"<p>testst</p>\"}', 'admin', '2020-05-01 09:19:28.723074', '2020-05-01 09:19:28.723096', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (84, 37, 0, '强制关闭工单:test', 1, 'admin', 11, '{\"id\": 37, \"creator\": \"admin\", \"gmt_created\": \"2020-05-01 09:19:28\", \"gmt_modified\": \"2020-05-01 09:19:28\", \"is_deleted\": false, \"title\": \"test\", \"workflow_id\": 2, \"sn\": \"ops122222212_202005010001\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"admin\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"vpn_reason\": \"<p>testst</p>\"}', 'admin', '2020-05-01 09:19:48.333223', '2020-05-01 09:19:48.333253', 0, 7);
INSERT INTO `ticket_ticketflowlog` VALUES (85, 38, 7, '', 1, 'admin', 6, '{\"id\": 38, \"creator\": \"admin\", \"gmt_created\": \"2020-05-01 09:21:56\", \"gmt_modified\": \"2020-05-01 09:21:56\", \"is_deleted\": false, \"title\": \"ttte\", \"workflow_id\": 2, \"sn\": \"ops122222212_202005010002\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"admin\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"vpn_reason\": \"<p>sssss</p>\"}', 'admin', '2020-05-01 09:21:56.866220', '2020-05-01 09:21:56.866256', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (86, 38, 0, '强制关闭工单:sdfsfs', 1, 'admin', 11, '{\"id\": 38, \"creator\": \"admin\", \"gmt_created\": \"2020-05-01 09:21:56\", \"gmt_modified\": \"2020-05-01 09:21:56\", \"is_deleted\": false, \"title\": \"ttte\", \"workflow_id\": 2, \"sn\": \"ops122222212_202005010002\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"admin\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"vpn_reason\": \"<p>sssss</p>\"}', 'admin', '2020-05-01 09:22:31.753568', '2020-05-01 09:22:31.753597', 0, 7);
INSERT INTO `ticket_ticketflowlog` VALUES (87, 39, 1, '', 1, 'admin', 1, '{\"id\": 39, \"creator\": \"admin\", \"gmt_created\": \"2020-05-07 22:42:17\", \"gmt_modified\": \"2020-05-07 22:42:17\", \"is_deleted\": false, \"title\": \"testest\", \"workflow_id\": 1, \"sn\": \"ops122222212_202005070001\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"zhangsan,lisi\", \"relation\": \"admin,zhangsan,lisi\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"zhangsan\\\": {}, \\\"lisi\\\": {}}\", \"leave_start\": \"2020-05-08 00:00:00\", \"leave_end\": \"2020-05-08 00:00:00\", \"leave_proxy\": \"lilian\", \"leave_type\": \"2\", \"leave_reason\": \"<p>testse</p>\"}', 'admin', '2020-05-07 22:42:17.314732', '2020-05-07 22:42:17.314757', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (88, 40, 7, '', 1, 'zhangsan', 6, '{\"id\": 40, \"creator\": \"zhangsan\", \"gmt_created\": \"2020-05-07 22:54:58\", \"gmt_modified\": \"2020-05-07 22:54:58\", \"is_deleted\": false, \"title\": \"test\", \"workflow_id\": 2, \"sn\": \"ops122222212_202005070002\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"zhangsan,admin\", \"relation\": \"admin,zhangsan\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"zhangsan\\\": {}, \\\"admin\\\": {}}\", \"vpn_reason\": \"<p>test</p>\"}', 'zhangsan', '2020-05-07 22:54:58.888888', '2020-05-07 22:54:58.888926', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (89, 40, 8, '同意', 1, 'zhangsan', 7, '\"{\\\"id\\\": 40, \\\"creator\\\": \\\"zhangsan\\\", \\\"gmt_created\\\": \\\"2020-05-07 22:54:58\\\", \\\"gmt_modified\\\": \\\"2020-05-07 22:55:09\\\", \\\"is_deleted\\\": false, \\\"title\\\": \\\"test\\\", \\\"workflow_id\\\": 2, \\\"sn\\\": \\\"ops122222212_202005070002\\\", \\\"state_id\\\": 8, \\\"parent_ticket_id\\\": 0, \\\"parent_ticket_state_id\\\": 0, \\\"participant_type_id\\\": 2, \\\"participant\\\": \\\"admin\\\", \\\"relation\\\": \\\"admin,zhangsan\\\", \\\"in_add_node\\\": false, \\\"add_node_man\\\": \\\"\\\", \\\"script_run_last_result\\\": true, \\\"act_state_id\\\": 1, \\\"multi_all_person\\\": \\\"{\\\\\\\"zhangsan\\\\\\\": {}, \\\\\\\"admin\\\\\\\": {}}\\\", \\\"vpn_reason\\\": \\\"<p>test</p>\\\"}\"', 'zhangsan', '2020-05-07 22:55:09.151811', '2020-05-07 22:55:09.151836', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (90, 41, 7, '', 1, 'admin', 6, '{\"id\": 41, \"creator\": \"admin\", \"gmt_created\": \"2020-05-17 17:31:54\", \"gmt_modified\": \"2020-05-17 17:31:54\", \"is_deleted\": false, \"title\": \"test\", \"workflow_id\": 2, \"sn\": \"ops122222212_202005170001\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"zhangsan,admin\", \"relation\": \"zhangsan,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"zhangsan\\\": {}, \\\"admin\\\": {}}\", \"vpn_reason\": \"<p>test</p>\"}', 'admin', '2020-05-17 17:31:54.259314', '2020-05-17 17:31:54.259334', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (91, 41, 8, '同意', 1, 'admin', 7, '\"{\\\"id\\\": 41, \\\"creator\\\": \\\"admin\\\", \\\"gmt_created\\\": \\\"2020-05-17 17:31:54\\\", \\\"gmt_modified\\\": \\\"2020-05-17 17:33:49\\\", \\\"is_deleted\\\": false, \\\"title\\\": \\\"test\\\", \\\"workflow_id\\\": 2, \\\"sn\\\": \\\"ops122222212_202005170001\\\", \\\"state_id\\\": 7, \\\"parent_ticket_id\\\": 0, \\\"parent_ticket_state_id\\\": 0, \\\"participant_type_id\\\": 2, \\\"participant\\\": \\\"zhangsan\\\", \\\"relation\\\": \\\"zhangsan,admin\\\", \\\"in_add_node\\\": false, \\\"add_node_man\\\": \\\"\\\", \\\"script_run_last_result\\\": true, \\\"act_state_id\\\": 1, \\\"multi_all_person\\\": \\\"{\\\\\\\"zhangsan\\\\\\\": {}, \\\\\\\"admin\\\\\\\": {}}\\\", \\\"vpn_reason\\\": \\\"<p>test</p>\\\"}\"', 'admin', '2020-05-17 17:33:49.927763', '2020-05-17 17:33:49.927798', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (92, 41, 8, 'test', 1, 'zhangsan', 7, '\"{\\\"id\\\": 41, \\\"creator\\\": \\\"admin\\\", \\\"gmt_created\\\": \\\"2020-05-17 17:31:54\\\", \\\"gmt_modified\\\": \\\"2020-05-17 17:38:51\\\", \\\"is_deleted\\\": false, \\\"title\\\": \\\"test\\\", \\\"workflow_id\\\": 2, \\\"sn\\\": \\\"ops122222212_202005170001\\\", \\\"state_id\\\": 7, \\\"parent_ticket_id\\\": 0, \\\"parent_ticket_state_id\\\": 0, \\\"participant_type_id\\\": 2, \\\"participant\\\": \\\"admin\\\", \\\"relation\\\": \\\"zhangsan,admin\\\", \\\"in_add_node\\\": false, \\\"add_node_man\\\": \\\"\\\", \\\"script_run_last_result\\\": true, \\\"act_state_id\\\": 1, \\\"multi_all_person\\\": \\\"{\\\\\\\"zhangsan\\\\\\\": {}, \\\\\\\"admin\\\\\\\": {}}\\\", \\\"vpn_reason\\\": \\\"<p>test</p>\\\"}\"', 'zhangsan', '2020-05-17 17:38:51.153578', '2020-05-17 17:38:51.153600', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (93, 42, 7, '', 1, 'zhangsan', 6, '{\"id\": 42, \"creator\": \"zhangsan\", \"gmt_created\": \"2020-05-17 17:44:45\", \"gmt_modified\": \"2020-05-17 17:44:45\", \"is_deleted\": false, \"title\": \"test111\", \"workflow_id\": 2, \"sn\": \"ops122222212_202005170002\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"zhangsan,admin\", \"relation\": \"zhangsan,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"zhangsan\\\": {}, \\\"admin\\\": {}}\", \"vpn_reason\": \"<p>1111<br/></p>\"}', 'zhangsan', '2020-05-17 17:44:45.482217', '2020-05-17 17:44:45.482238', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (94, 42, 8, '12222', 1, 'zhangsan', 7, '\"{\\\"id\\\": 42, \\\"creator\\\": \\\"zhangsan\\\", \\\"gmt_created\\\": \\\"2020-05-17 17:44:45\\\", \\\"gmt_modified\\\": \\\"2020-05-17 17:44:52\\\", \\\"is_deleted\\\": false, \\\"title\\\": \\\"test111\\\", \\\"workflow_id\\\": 2, \\\"sn\\\": \\\"ops122222212_202005170002\\\", \\\"state_id\\\": 7, \\\"parent_ticket_id\\\": 0, \\\"parent_ticket_state_id\\\": 0, \\\"participant_type_id\\\": 2, \\\"participant\\\": \\\"admin\\\", \\\"relation\\\": \\\"zhangsan,admin\\\", \\\"in_add_node\\\": false, \\\"add_node_man\\\": \\\"\\\", \\\"script_run_last_result\\\": true, \\\"act_state_id\\\": 1, \\\"multi_all_person\\\": \\\"{\\\\\\\"zhangsan\\\\\\\": {\\\\\\\"transition_id\\\\\\\": 8, \\\\\\\"transition_name\\\\\\\": \\\\\\\"\\\\\\\\u540c\\\\\\\\u610f\\\\\\\"}, \\\\\\\"admin\\\\\\\": {}}\\\", \\\"vpn_reason\\\": \\\"<p>1111<br/></p>\\\"}\"', 'zhangsan', '2020-05-17 17:44:52.675300', '2020-05-17 17:44:52.675336', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (95, 42, 8, '同意', 1, 'admin', 7, '\"{\\\"id\\\": 42, \\\"creator\\\": \\\"zhangsan\\\", \\\"gmt_created\\\": \\\"2020-05-17 17:44:45\\\", \\\"gmt_modified\\\": \\\"2020-05-17 17:45:34\\\", \\\"is_deleted\\\": false, \\\"title\\\": \\\"test111\\\", \\\"workflow_id\\\": 2, \\\"sn\\\": \\\"ops122222212_202005170002\\\", \\\"state_id\\\": 8, \\\"parent_ticket_id\\\": 0, \\\"parent_ticket_state_id\\\": 0, \\\"participant_type_id\\\": 3, \\\"participant\\\": \\\"3\\\", \\\"relation\\\": \\\"wangwu,zhangsan,guiji,admin\\\", \\\"in_add_node\\\": false, \\\"add_node_man\\\": \\\"\\\", \\\"script_run_last_result\\\": true, \\\"act_state_id\\\": 1, \\\"multi_all_person\\\": \\\"{}\\\", \\\"vpn_reason\\\": \\\"<p>1111<br/></p>\\\"}\"', 'admin', '2020-05-17 17:45:34.529864', '2020-05-17 17:45:34.529883', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (96, 43, 7, '', 1, 'admin', 6, '{\"id\": 43, \"creator\": \"admin\", \"gmt_created\": \"2020-05-18 23:18:15\", \"gmt_modified\": \"2020-05-18 23:18:15\", \"is_deleted\": false, \"title\": \"TEST\", \"workflow_id\": 2, \"sn\": \"ops122222212_202005180001\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"zhangsan,admin\", \"relation\": \"admin,zhangsan\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"zhangsan\\\": {}, \\\"admin\\\": {}}\", \"vpn_reason\": \"<p>TEST</p>\"}', 'admin', '2020-05-18 23:18:15.575623', '2020-05-18 23:18:15.575649', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (97, 43, 8, '同意', 1, 'admin', 7, '\"{\\\"id\\\": 43, \\\"creator\\\": \\\"admin\\\", \\\"gmt_created\\\": \\\"2020-05-18 23:18:15\\\", \\\"gmt_modified\\\": \\\"2020-05-18 23:18:30\\\", \\\"is_deleted\\\": false, \\\"title\\\": \\\"TEST\\\", \\\"workflow_id\\\": 2, \\\"sn\\\": \\\"ops122222212_202005180001\\\", \\\"state_id\\\": 7, \\\"parent_ticket_id\\\": 0, \\\"parent_ticket_state_id\\\": 0, \\\"participant_type_id\\\": 2, \\\"participant\\\": \\\"zhangsan\\\", \\\"relation\\\": \\\"admin,zhangsan\\\", \\\"in_add_node\\\": false, \\\"add_node_man\\\": \\\"\\\", \\\"script_run_last_result\\\": true, \\\"act_state_id\\\": 1, \\\"multi_all_person\\\": \\\"{\\\\\\\"zhangsan\\\\\\\": {}, \\\\\\\"admin\\\\\\\": {\\\\\\\"transition_id\\\\\\\": 8, \\\\\\\"transition_name\\\\\\\": \\\\\\\"\\\\\\\\u540c\\\\\\\\u610f\\\\\\\"}}\\\", \\\"vpn_reason\\\": \\\"<p>TEST</p>\\\"}\"', 'admin', '2020-05-18 23:18:30.423578', '2020-05-18 23:18:30.423601', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (98, 44, 7, '', 1, 'admin', 6, '{\"id\": 44, \"creator\": \"admin\", \"gmt_created\": \"2020-08-21 10:39:32\", \"gmt_modified\": \"2020-08-21 10:39:32\", \"is_deleted\": false, \"title\": \"dfdsf\", \"workflow_id\": 2, \"sn\": \"loonflow_202008210004\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"admin,zhangsan\", \"relation\": \"admin,zhangsan\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"admin\\\": {}, \\\"zhangsan\\\": {}}\", \"vpn_reason\": \"sdfdsfsdfs\"}', 'admin', '2020-08-21 10:39:32.970241', '2020-08-21 10:39:32.970403', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (99, 46, 1, '', 1, 'admin', 1, '{\"id\": 46, \"creator\": \"admin\", \"gmt_created\": \"2020-08-21 18:42:06\", \"gmt_modified\": \"2020-08-21 18:42:06\", \"is_deleted\": false, \"title\": \"\", \"workflow_id\": 1, \"sn\": \"loonflow_202008210006\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"lisi,zhangsan\", \"relation\": \"admin,lisi,zhangsan\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"lisi\\\": {}, \\\"zhangsan\\\": {}}\", \"leave_start\": \"2020-08-21 00:00:05\", \"leave_end\": \"2020-08-21 18:15:52\", \"leave_proxy\": \"None\", \"leave_type\": \"1\", \"leave_reason\": 111, \"bool_field\": true, \"date_filed\": \"None\", \"datetime_field\": \"None\", \"checkbox_field\": \"1\", \"multi_checkbox_field\": \"2,3\", \"select_field\": \"1\", \"multi_select_field\": \"1,2,3\", \"text_field\": \"dfs\", \"user_fleld\": \"fdsf\", \"multi_user_field\": \"fdsf\", \"attachment_field\": \"fdsfs\"}', 'admin', '2020-08-21 18:42:08.466941', '2020-08-21 18:42:08.467161', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (100, 47, 7, '', 1, 'admin', 6, '{\"id\": 47, \"creator\": \"admin\", \"gmt_created\": \"2020-08-22 08:46:19\", \"gmt_modified\": \"2020-08-22 08:46:19\", \"is_deleted\": false, \"title\": \"fdfafa \", \"workflow_id\": 2, \"sn\": \"loonflow_202008220001\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"admin,zhangsan\", \"relation\": \"admin,zhangsan\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"admin\\\": {}, \\\"zhangsan\\\": {}}\", \"vpn_reason\": \"fdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1\\nfdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1\\nfdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1\\nfdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1\\nfdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1fdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1\\nfdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1\"}', 'admin', '2020-08-22 08:46:20.051663', '2020-08-22 08:46:20.051898', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (101, 47, 0, '', 1, 'admin', 7, '{\"id\": 47, \"creator\": \"admin\", \"gmt_created\": \"2020-08-22 08:46:19\", \"gmt_modified\": \"2020-08-22 08:46:19\", \"is_deleted\": false, \"title\": \"fdfafa \", \"workflow_id\": 2, \"sn\": \"loonflow_202008220001\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"admin,zhangsan\", \"relation\": \"admin,zhangsan\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"admin\\\": {}, \\\"zhangsan\\\": {}}\", \"vpn_reason\": \"fdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1\\nfdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1\\nfdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1\\nfdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1\\nfdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1fdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1\\nfdsfsfsffhahhah\\u54c8\\u54c8\\u54c8\\u53d1\"}', 'admin', '2021-07-30 19:25:50.175237', '2021-07-30 19:25:50.175263', 0, 6);
INSERT INTO `ticket_ticketflowlog` VALUES (102, 46, 0, '', 1, 'admin', 3, '{\"id\": 46, \"creator\": \"admin\", \"gmt_created\": \"2020-08-21 18:42:06\", \"gmt_modified\": \"2020-08-21 18:42:06\", \"is_deleted\": false, \"title\": \"\", \"workflow_id\": 1, \"sn\": \"loonflow_202008210006\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"lisi,zhangsan\", \"relation\": \"admin,lisi,zhangsan\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"lisi\\\": {}, \\\"zhangsan\\\": {}}\", \"leave_start12\": \"None\", \"leave_end\": \"2020-08-21 18:15:52\", \"leave_proxy\": \"None\", \"leave_type\": \"1\", \"leave_reason\": 111, \"date_filed\": \"None\", \"datetime_field\": \"None\", \"text_field\": \"dfs\", \"attachment_field\": \"fdsfs\"}', 'admin', '2021-07-30 19:25:52.457501', '2021-07-30 19:25:52.457539', 0, 6);
INSERT INTO `ticket_ticketflowlog` VALUES (103, 45, 0, '', 1, 'admin', 3, '{\"id\": 45, \"creator\": \"admin\", \"gmt_created\": \"2020-08-21 18:33:34\", \"gmt_modified\": \"2020-08-21 18:33:34\", \"is_deleted\": false, \"title\": \"\", \"workflow_id\": 1, \"sn\": \"loonflow_202008210005\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"lisi,zhangsan\", \"relation\": \"admin,lisi,zhangsan\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"lisi\\\": {}, \\\"zhangsan\\\": {}}\", \"leave_start12\": \"None\", \"leave_end\": \"None\", \"leave_proxy\": \"None\", \"leave_type\": \"None\", \"leave_reason\": \"None\", \"date_filed\": \"None\", \"datetime_field\": \"None\", \"text_field\": \"fs\", \"attachment_field\": \"fdsfs\"}', 'admin', '2021-07-30 19:25:54.598027', '2021-07-30 19:25:54.598053', 0, 6);
INSERT INTO `ticket_ticketflowlog` VALUES (104, 44, 0, '', 1, 'admin', 7, '{\"id\": 44, \"creator\": \"admin\", \"gmt_created\": \"2020-08-21 10:39:32\", \"gmt_modified\": \"2020-08-21 10:39:32\", \"is_deleted\": false, \"title\": \"dfdsf\", \"workflow_id\": 2, \"sn\": \"loonflow_202008210004\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"admin,zhangsan\", \"relation\": \"admin,zhangsan\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"admin\\\": {}, \\\"zhangsan\\\": {}}\", \"vpn_reason\": \"sdfdsfsdfs\"}', 'admin', '2021-07-30 19:25:57.499302', '2021-07-30 19:25:57.499335', 0, 6);
INSERT INTO `ticket_ticketflowlog` VALUES (105, 48, 1, '', 1, 'test', 1, '{\"id\": 48, \"creator\": \"test\", \"gmt_created\": \"2021-07-30 19:34:44\", \"gmt_modified\": \"2021-07-30 19:34:44\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:1\", \"workflow_id\": 1, \"sn\": \"loonflow_202107300001\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"zhangsan,lisi\", \"relation\": \"lisi,zhangsan,test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"None\", \"leave_end\": \"None\", \"leave_proxy\": \"None\", \"leave_type\": \"None\", \"leave_reason\": \"None\", \"datetime_field\": \"None\", \"text_field\": \"None\", \"attachment_field\": \"None\"}', 'test', '2021-07-30 19:34:44.132676', '2021-07-30 19:34:44.132726', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (106, 48, 0, '处理完成', 1, 'admin', 3, '{\"id\": 48, \"creator\": \"test\", \"gmt_created\": \"2021-07-30 19:34:44\", \"gmt_modified\": \"2021-07-30 19:37:20\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:1\", \"workflow_id\": 1, \"sn\": \"loonflow_202107300001\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"test,zhangsan,lisi\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"None\", \"leave_end\": \"None\", \"leave_proxy\": \"None\", \"leave_type\": \"None\", \"leave_reason\": \"None\", \"datetime_field\": \"None\", \"text_field\": \"None\", \"attachment_field\": \"None\"}', 'admin', '2021-07-30 19:37:20.736130', '2021-07-30 19:37:20.736162', 0, 8);
INSERT INTO `ticket_ticketflowlog` VALUES (107, 49, 1, '', 1, 'test', 1, '{\"id\": 49, \"creator\": \"test\", \"gmt_created\": \"2021-07-30 19:40:51\", \"gmt_modified\": \"2021-07-30 19:40:51\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:\\u8bf7\\u5047\\u7533\\u8bf7\", \"workflow_id\": 1, \"sn\": \"loonflow_202107300002\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"zhangsan,lisi\", \"relation\": \"lisi,zhangsan,test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"None\", \"leave_end\": \"None\", \"leave_proxy\": \"None\", \"leave_type\": \"None\", \"leave_reason\": \"None\", \"datetime_field\": \"None\", \"text_field\": \"None\", \"attachment_field\": \"None\"}', 'test', '2021-07-30 19:40:51.933185', '2021-07-30 19:40:51.933227', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (108, 50, 1, '', 1, 'test', 1, '{\"id\": 50, \"creator\": \"test\", \"gmt_created\": \"2021-07-30 19:48:51\", \"gmt_modified\": \"2021-07-30 19:48:51\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:\\u8bf7\\u5047\", \"workflow_id\": 1, \"sn\": \"loonflow_202107300003\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"zhangsan,lisi\", \"relation\": \"lisi,zhangsan,test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"None\", \"leave_end\": \"None\", \"leave_proxy\": \"None\", \"leave_type\": \"1\", \"leave_reason\": \"None\", \"datetime_field\": \"None\", \"text_field\": \"None\", \"attachment_field\": \"None\", \"days\": 5}', 'test', '2021-07-30 19:48:51.836042', '2021-07-30 19:48:51.836081', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (109, 51, 1, '', 1, 'test', 1, '{\"id\": 51, \"creator\": \"test\", \"gmt_created\": \"2021-07-30 19:58:56\", \"gmt_modified\": \"2021-07-30 19:58:56\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:3\", \"workflow_id\": 1, \"sn\": \"loonflow_202107300009\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:03\", \"leave_end\": \"2021-07-30 00:00:03\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"text_field\": \"1\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"2\"}', 'test', '2021-07-30 19:58:56.401376', '2021-07-30 19:58:56.401428', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (110, 52, 1, '', 1, 'test', 1, '{\"id\": 52, \"creator\": \"test\", \"gmt_created\": \"2021-07-30 20:09:49\", \"gmt_modified\": \"2021-07-30 20:09:49\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:\\u8bf7\\u5047\\u7533\\u8bf77-30\", \"workflow_id\": 1, \"sn\": \"loonflow_202107300010\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-30 00:00:04\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"wwwwwwww\"}', 'test', '2021-07-30 20:09:49.567652', '2021-07-30 20:09:49.567677', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (111, 53, 27, '', 1, 'test', 1, '{\"id\": 53, \"creator\": \"test\", \"gmt_created\": \"2021-07-30 20:44:09\", \"gmt_modified\": \"2021-07-30 20:44:09\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:1\", \"workflow_id\": 1, \"sn\": \"loonflow_202107300011\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 4, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 02:00:05\", \"leave_end\": \"2021-07-30 00:00:04\", \"leave_type\": \"None\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1\"}', 'test', '2021-07-30 20:44:10.021128', '2021-07-30 20:44:10.021164', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (112, 54, 27, '', 1, 'test', 1, '{\"id\": 54, \"creator\": \"test\", \"gmt_created\": \"2021-07-30 20:47:54\", \"gmt_modified\": \"2021-07-30 20:47:54\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:2313\", \"workflow_id\": 1, \"sn\": \"loonflow_202107300012\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:02\", \"leave_end\": \"2021-07-30 00:03:04\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 132131, \"text_desp\": \"1\"}', 'test', '2021-07-30 20:47:54.781631', '2021-07-30 20:47:54.781657', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (113, 55, 27, '', 1, 'test', 1, '{\"id\": 55, \"creator\": \"test\", \"gmt_created\": \"2021-07-30 20:48:26\", \"gmt_modified\": \"2021-07-30 20:48:26\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:123123\", \"workflow_id\": 1, \"sn\": \"loonflow_202107300013\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:03\", \"leave_end\": \"2021-07-30 00:00:20\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 12313, \"text_desp\": \"12312\"}', 'test', '2021-07-30 20:48:26.313003', '2021-07-30 20:48:26.313031', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (114, 56, 7, '', 1, 'test', 6, '{\"id\": 56, \"creator\": \"test\", \"gmt_created\": \"2021-07-30 20:59:24\", \"gmt_modified\": \"2021-07-30 20:59:24\", \"is_deleted\": false, \"title\": \"\\u6807\\u9898\", \"workflow_id\": 2, \"sn\": \"loonflow_202107300014\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"admin,zhangsan\", \"relation\": \"admin,zhangsan,test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"a\\\": {}, \\\"d\\\": {}, \\\"m\\\": {}, \\\"i\\\": {}, \\\"n\\\": {}, \\\",\\\": {}, \\\"z\\\": {}, \\\"h\\\": {}, \\\"g\\\": {}, \\\"s\\\": {}}\", \"vpn_reason\": \"\\u5e94\\u7528\"}', 'test', '2021-07-30 20:59:24.168624', '2021-07-30 20:59:24.168656', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (115, 57, 7, '', 1, 'admin', 6, '{\"id\": 57, \"creator\": \"admin\", \"gmt_created\": \"2021-07-30 20:59:53\", \"gmt_modified\": \"2021-07-30 20:59:53\", \"is_deleted\": false, \"title\": \"111\", \"workflow_id\": 2, \"sn\": \"_202107300015\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"admin,zhangsan\", \"relation\": \"admin,zhangsan\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"a\\\": {}, \\\"d\\\": {}, \\\"m\\\": {}, \\\"i\\\": {}, \\\"n\\\": {}, \\\",\\\": {}, \\\"z\\\": {}, \\\"h\\\": {}, \\\"g\\\": {}, \\\"s\\\": {}}\", \"vpn_reason\": \"\\u7533\\u8bf7\\u539f\\u56e0\"}', 'admin', '2021-07-30 20:59:53.525001', '2021-07-30 20:59:53.525031', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (116, 58, 7, '', 1, 'admin', 6, '{\"id\": 58, \"creator\": \"admin\", \"gmt_created\": \"2021-07-30 21:02:05\", \"gmt_modified\": \"2021-07-30 21:02:05\", \"is_deleted\": false, \"title\": \"111\", \"workflow_id\": 2, \"sn\": \"_202107300016\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"admin,zhangsan\", \"relation\": \"admin,zhangsan\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"a\\\": {}, \\\"d\\\": {}, \\\"m\\\": {}, \\\"i\\\": {}, \\\"n\\\": {}, \\\",\\\": {}, \\\"z\\\": {}, \\\"h\\\": {}, \\\"g\\\": {}, \\\"s\\\": {}}\", \"vpn_reason\": \"\\u7533\\u8bf7\\u539f\\u56e0\"}', 'admin', '2021-07-30 21:02:05.639855', '2021-07-30 21:02:05.639880', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (117, 59, 27, '', 1, 'test', 1, '{\"id\": 59, \"creator\": \"test\", \"gmt_created\": \"2021-07-30 21:03:35\", \"gmt_modified\": \"2021-07-30 21:03:35\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:3131\", \"workflow_id\": 1, \"sn\": \"loonflow_202107300017\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:07\", \"leave_end\": \"2021-07-30 00:00:07\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"11\"}', 'test', '2021-07-30 21:03:35.971848', '2021-07-30 21:03:35.971920', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (118, 60, 27, '', 1, 'admin', 1, '{\"id\": 60, \"creator\": \"admin\", \"gmt_created\": \"2021-07-30 21:08:42\", \"gmt_modified\": \"2021-07-30 21:08:42\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:\\u8bf7\\u5047\\u7533\\u8bf77-30\", \"workflow_id\": 1, \"sn\": \"_202107300018\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-30 00:00:04\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"wwwwwwww\"}', 'admin', '2021-07-30 21:08:42.902477', '2021-07-30 21:08:42.902500', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (119, 61, 27, '', 1, 'admin', 1, '{\"id\": 61, \"creator\": \"admin\", \"gmt_created\": \"2021-07-30 21:28:21\", \"gmt_modified\": \"2021-07-30 21:28:21\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:\\u8bf7\\u5047\\u7533\\u8bf77-30\", \"workflow_id\": 1, \"sn\": \"_202107300019\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-30 00:00:04\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"wwwwwwww\"}', 'admin', '2021-07-30 21:28:21.626472', '2021-07-30 21:28:21.626493', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (120, 62, 27, '', 1, 'admin', 1, '{\"id\": 62, \"creator\": \"admin\", \"gmt_created\": \"2021-07-30 21:28:38\", \"gmt_modified\": \"2021-07-30 21:28:38\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:\\u8bf7\\u5047\\u7533\\u8bf77-30\", \"workflow_id\": 1, \"sn\": \"_202107300020\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-30 00:00:04\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"wwwwwwww\"}', 'admin', '2021-07-30 21:28:38.210997', '2021-07-30 21:28:38.211024', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (121, 63, 27, '', 1, 'admin', 1, '{\"id\": 63, \"creator\": \"admin\", \"gmt_created\": \"2021-07-30 21:33:27\", \"gmt_modified\": \"2021-07-30 21:33:27\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:\\u8bf7\\u5047\\u7533\\u8bf77-30\", \"workflow_id\": 1, \"sn\": \"_202107300021\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-30 00:00:04\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"wwwwwwww\"}', 'admin', '2021-07-30 21:33:27.456239', '2021-07-30 21:33:27.456261', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (122, 64, 27, '', 1, 'admin', 1, '{\"id\": 64, \"creator\": \"admin\", \"gmt_created\": \"2021-07-30 21:36:31\", \"gmt_modified\": \"2021-07-30 21:36:31\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:\\u8bf7\\u5047\\u7533\\u8bf77-30\", \"workflow_id\": 1, \"sn\": \"_202107300022\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-30 00:00:04\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"wwwwwwww\"}', 'admin', '2021-07-30 21:36:31.775057', '2021-07-30 21:36:31.775081', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (123, 65, 27, '', 1, 'admin', 1, '{\"id\": 65, \"creator\": \"admin\", \"gmt_created\": \"2021-07-30 21:36:44\", \"gmt_modified\": \"2021-07-30 21:36:44\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:\\u8bf7\\u5047\\u7533\\u8bf77-30\", \"workflow_id\": 1, \"sn\": \"_202107300023\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-30 00:00:04\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"wwwwwwww\"}', 'admin', '2021-07-30 21:36:44.707547', '2021-07-30 21:36:44.707573', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (124, 66, 27, '', 1, 'admin', 1, '{\"id\": 66, \"creator\": \"admin\", \"gmt_created\": \"2021-07-30 21:37:43\", \"gmt_modified\": \"2021-07-30 21:37:43\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:\\u8bf7\\u5047\\u7533\\u8bf77-30\", \"workflow_id\": 1, \"sn\": \"_202107300024\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-30 00:00:04\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"wwwwwwww\"}', 'admin', '2021-07-30 21:37:43.629453', '2021-07-30 21:37:43.629485', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (125, 67, 27, '', 1, 'admin', 1, '{\"id\": 67, \"creator\": \"admin\", \"gmt_created\": \"2021-07-30 21:39:59\", \"gmt_modified\": \"2021-07-30 21:39:59\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:\\u8bf7\\u5047\\u7533\\u8bf77-30\", \"workflow_id\": 1, \"sn\": \"_202107300025\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-30 00:00:04\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"wwwwwwww\"}', 'admin', '2021-07-30 21:40:00.037019', '2021-07-30 21:40:00.037045', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (126, 68, 27, '', 1, 'admin', 1, '{\"id\": 68, \"creator\": \"admin\", \"gmt_created\": \"2021-07-30 21:40:18\", \"gmt_modified\": \"2021-07-30 21:40:18\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:\\u8bf7\\u5047\\u7533\\u8bf77-30\", \"workflow_id\": 1, \"sn\": \"_202107300026\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-30 00:00:04\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"wwwwwwww\"}', 'admin', '2021-07-30 21:40:18.555165', '2021-07-30 21:40:18.555188', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (127, 69, 27, '', 1, 'admin', 1, '{\"id\": 69, \"creator\": \"admin\", \"gmt_created\": \"2021-07-30 21:40:20\", \"gmt_modified\": \"2021-07-30 21:40:20\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:\\u8bf7\\u5047\\u7533\\u8bf77-30\", \"workflow_id\": 1, \"sn\": \"_202107300027\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-30 00:00:04\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"wwwwwwww\"}', 'admin', '2021-07-30 21:40:20.533545', '2021-07-30 21:40:20.533567', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (128, 70, 27, '', 1, 'admin', 1, '{\"id\": 70, \"creator\": \"admin\", \"gmt_created\": \"2021-07-30 21:40:29\", \"gmt_modified\": \"2021-07-30 21:40:29\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:\\u8bf7\\u5047\\u7533\\u8bf77-30\", \"workflow_id\": 1, \"sn\": \"_202107300028\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-30 00:00:04\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"wwwwwwww\"}', 'admin', '2021-07-30 21:40:30.044739', '2021-07-30 21:40:30.044762', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (129, 71, 27, '', 1, 'admin', 1, '{\"id\": 71, \"creator\": \"admin\", \"gmt_created\": \"2021-07-30 21:40:32\", \"gmt_modified\": \"2021-07-30 21:40:32\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:\\u8bf7\\u5047\\u7533\\u8bf77-30\", \"workflow_id\": 1, \"sn\": \"_202107300029\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-30 00:00:04\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"wwwwwwww\"}', 'admin', '2021-07-30 21:40:32.964122', '2021-07-30 21:40:32.964166', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (130, 72, 27, '', 1, 'admin', 1, '{\"id\": 72, \"creator\": \"admin\", \"gmt_created\": \"2021-07-30 21:40:54\", \"gmt_modified\": \"2021-07-30 21:40:54\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:\\u8bf7\\u5047\\u7533\\u8bf77-30\", \"workflow_id\": 1, \"sn\": \"_202107300030\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-30 00:00:04\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"wwwwwwww\"}', 'admin', '2021-07-30 21:40:54.594283', '2021-07-30 21:40:54.594305', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (131, 73, 27, '', 1, 'admin', 1, '{\"id\": 73, \"creator\": \"admin\", \"gmt_created\": \"2021-07-30 21:41:06\", \"gmt_modified\": \"2021-07-30 21:41:06\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:\\u8bf7\\u5047\\u7533\\u8bf77-30\", \"workflow_id\": 1, \"sn\": \"_202107300031\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-30 00:00:04\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"wwwwwwww\"}', 'admin', '2021-07-30 21:41:06.672025', '2021-07-30 21:41:06.672053', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (132, 78, 27, '', 1, 'admin', 1, '{\"id\": 78, \"creator\": \"admin\", \"gmt_created\": \"2021-07-30 21:47:22\", \"gmt_modified\": \"2021-07-30 21:47:22\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:1111\", \"workflow_id\": 1, \"sn\": \"_202107300036\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 21:47:00\", \"leave_end\": \"2021-07-30 21:47:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 123123, \"text_desp\": \"123132\"}', 'admin', '2021-07-30 21:47:22.801550', '2021-07-30 21:47:22.801577', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (133, 89, 27, '', 1, 'admin', 1, '{\"id\": 89, \"creator\": \"admin\", \"gmt_created\": \"2021-07-30 22:01:28\", \"gmt_modified\": \"2021-07-30 22:01:28\", \"is_deleted\": false, \"title\": \"\\u4f60\\u6709\\u4e00\\u4e2a\\u5f85\\u529e\\u5de5\\u5355:1\", \"workflow_id\": 1, \"sn\": \"loonflow_202107300047\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"None\", \"leave_end\": \"None\", \"leave_type\": \"2\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": \"None\", \"text_desp\": \"None\"}', 'admin', '2021-07-30 22:01:28.920060', '2021-07-30 22:01:28.920085', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (134, 90, 27, '', 1, 'admin', 1, '{\"id\": 90, \"creator\": \"admin\", \"gmt_created\": \"2021-07-30 22:06:36\", \"gmt_modified\": \"2021-07-30 22:06:36\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5\", \"workflow_id\": 1, \"sn\": \"\\u8bf7\\u5047_202107300048\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 22:06:00\", \"leave_end\": \"2021-07-30 22:06:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 2, \"text_desp\": \"111\"}', 'admin', '2021-07-30 22:06:36.838236', '2021-07-30 22:06:36.838291', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (135, 91, 27, '', 1, 'test', 1, '{\"id\": 91, \"creator\": \"test\", \"gmt_created\": \"2021-07-30 22:08:22\", \"gmt_modified\": \"2021-07-30 22:08:22\", \"is_deleted\": false, \"title\": \"cs\", \"workflow_id\": 1, \"sn\": \"loonflow_202107300049\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:07\", \"leave_end\": \"2021-07-30 00:00:06\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"cs\"}', 'test', '2021-07-30 22:08:22.326886', '2021-07-30 22:08:22.326911', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (136, 92, 27, '', 1, 'test', 1, '{\"id\": 92, \"creator\": \"test\", \"gmt_created\": \"2021-07-30 22:43:46\", \"gmt_modified\": \"2021-07-30 22:43:46\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5\", \"workflow_id\": 1, \"sn\": \"Test_202107300050\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2018-05-13 22:24:41\", \"leave_end\": \"2018-05-13 22:24:41\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u65e0\"}', 'test', '2021-07-30 22:43:46.129376', '2021-07-30 22:43:46.129399', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (137, 93, 27, '', 1, 'test', 1, '{\"id\": 93, \"creator\": \"test\", \"gmt_created\": \"2021-07-30 22:43:53\", \"gmt_modified\": \"2021-07-30 22:43:53\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5\", \"workflow_id\": 1, \"sn\": \"Test_202107300051\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2018-05-13 22:24:41\", \"leave_end\": \"2018-05-13 22:24:41\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u65e0\"}', 'test', '2021-07-30 22:43:53.718230', '2021-07-30 22:43:53.718254', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (138, 94, 27, '', 1, 'test2', 1, '{\"id\": 94, \"creator\": \"test2\", \"gmt_created\": \"2021-07-30 22:44:29\", \"gmt_modified\": \"2021-07-30 22:44:29\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5\", \"workflow_id\": 1, \"sn\": \"Test_202107300052\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"test2\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2018-05-13 22:24:41\", \"leave_end\": \"2018-05-13 22:24:41\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u65e0\"}', 'test2', '2021-07-30 22:44:29.619398', '2021-07-30 22:44:29.619453', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (139, 95, 27, '', 1, 'admin', 1, '{\"id\": 95, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 10:02:44\", \"gmt_modified\": \"2021-07-31 10:02:44\", \"is_deleted\": false, \"title\": \"cs\", \"workflow_id\": 1, \"sn\": \"Test_202107310001\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 10:02:00\", \"leave_end\": \"2021-07-31 10:02:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1231\"}', 'admin', '2021-07-31 10:02:44.608289', '2021-07-31 10:02:44.608312', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (140, 96, 27, '', 1, 'admin', 1, '{\"id\": 96, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 10:03:10\", \"gmt_modified\": \"2021-07-31 10:03:10\", \"is_deleted\": false, \"title\": \"cs\", \"workflow_id\": 1, \"sn\": \"Test_202107310002\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 10:02:00\", \"leave_end\": \"2021-07-31 10:02:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1231\"}', 'admin', '2021-07-31 10:03:11.011682', '2021-07-31 10:03:11.011703', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (141, 97, 27, '', 1, 'admin', 1, '{\"id\": 97, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 10:03:40\", \"gmt_modified\": \"2021-07-31 10:03:40\", \"is_deleted\": false, \"title\": \"cs\", \"workflow_id\": 1, \"sn\": \"Test_202107310003\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 10:02:00\", \"leave_end\": \"2021-07-31 10:02:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1231\"}', 'admin', '2021-07-31 10:03:40.536219', '2021-07-31 10:03:40.536241', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (142, 99, 27, '', 1, 'admin', 1, '{\"id\": 99, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 10:10:39\", \"gmt_modified\": \"2021-07-31 10:10:39\", \"is_deleted\": false, \"title\": \"1\", \"workflow_id\": 1, \"sn\": \"Test_202107310005\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 10:10:00\", \"leave_end\": \"2021-07-31 10:10:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1\"}', 'admin', '2021-07-31 10:10:40.045093', '2021-07-31 10:10:40.045116', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (143, 100, 27, '', 1, 'test', 1, '{\"id\": 100, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 10:11:38\", \"gmt_modified\": \"2021-07-31 10:11:38\", \"is_deleted\": false, \"title\": \"test\", \"workflow_id\": 1, \"sn\": \"Test_202107310006\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 10:11:00\", \"leave_end\": \"2021-07-31 10:11:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 111, \"text_desp\": \"111\"}', 'test', '2021-07-31 10:11:38.353498', '2021-07-31 10:11:38.353526', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (144, 101, 27, '', 1, 'test', 1, '{\"id\": 101, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 10:44:57\", \"gmt_modified\": \"2021-07-31 10:44:57\", \"is_deleted\": false, \"title\": \"sss\", \"workflow_id\": 1, \"sn\": \"Test_202107310007\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 10:44:00\", \"leave_end\": \"2021-08-28 00:00:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"11\"}', 'test', '2021-07-31 10:44:57.222396', '2021-07-31 10:44:57.222421', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (145, 102, 27, '', 1, 'test', 1, '{\"id\": 102, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 10:45:19\", \"gmt_modified\": \"2021-07-31 10:45:19\", \"is_deleted\": false, \"title\": \"sss\", \"workflow_id\": 1, \"sn\": \"Test_202107310008\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 10:44:00\", \"leave_end\": \"2021-08-28 00:00:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"11\"}', 'test', '2021-07-31 10:45:19.855203', '2021-07-31 10:45:19.855248', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (146, 103, 27, '', 1, 'test', 1, '{\"id\": 103, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 10:45:27\", \"gmt_modified\": \"2021-07-31 10:45:27\", \"is_deleted\": false, \"title\": \"1\", \"workflow_id\": 1, \"sn\": \"Test_202107310009\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 10:45:00\", \"leave_end\": \"2021-07-31 10:45:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1\"}', 'test', '2021-07-31 10:45:27.096376', '2021-07-31 10:45:27.096403', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (147, 104, 27, '', 1, 'test', 1, '{\"id\": 104, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 10:47:10\", \"gmt_modified\": \"2021-07-31 10:47:10\", \"is_deleted\": false, \"title\": \"1\", \"workflow_id\": 1, \"sn\": \"Test_202107310010\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 10:47:00\", \"leave_end\": \"2021-07-31 10:47:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1\"}', 'test', '2021-07-31 10:47:10.142598', '2021-07-31 10:47:10.142620', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (148, 106, 27, '', 1, 'test', 1, '{\"id\": 106, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 10:48:41\", \"gmt_modified\": \"2021-07-31 10:48:41\", \"is_deleted\": false, \"title\": \"1\", \"workflow_id\": 1, \"sn\": \"Test_202107310012\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 10:48:00\", \"leave_end\": \"2021-07-31 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1\"}', 'test', '2021-07-31 10:48:41.504080', '2021-07-31 10:48:41.504126', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (149, 107, 27, '', 1, 'test', 1, '{\"id\": 107, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 10:50:42\", \"gmt_modified\": \"2021-07-31 10:50:42\", \"is_deleted\": false, \"title\": \"1\", \"workflow_id\": 1, \"sn\": \"Test_202107310013\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 10:50:00\", \"leave_end\": \"2021-07-31 10:50:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1\"}', 'test', '2021-07-31 10:50:42.884037', '2021-07-31 10:50:42.884070', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (150, 108, 27, '', 1, 'test', 1, '{\"id\": 108, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 10:52:16\", \"gmt_modified\": \"2021-07-31 10:52:16\", \"is_deleted\": false, \"title\": \"1\", \"workflow_id\": 1, \"sn\": \"Test_202107310014\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 10:52:00\", \"leave_end\": \"2021-07-31 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 2, \"text_desp\": \"1\"}', 'test', '2021-07-31 10:52:16.335272', '2021-07-31 10:52:16.335295', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (151, 100, 0, '', 1, 'admin', 3, '{\"id\": 100, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 10:11:38\", \"gmt_modified\": \"2021-07-31 11:30:49\", \"is_deleted\": false, \"title\": \"test\", \"workflow_id\": 1, \"sn\": \"Test_202107310006\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"admin\", \"relation\": \"test,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 10:11:00\", \"leave_end\": \"2021-07-31 10:11:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 111, \"text_desp\": \"111\"}', 'admin', '2021-07-31 11:30:49.565283', '2021-07-31 11:30:49.565305', 0, 1);
INSERT INTO `ticket_ticketflowlog` VALUES (152, 114, 27, '', 1, 'test', 1, '{\"id\": 114, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 11:43:56\", \"gmt_modified\": \"2021-07-31 11:43:56\", \"is_deleted\": false, \"title\": \"1\", \"workflow_id\": 1, \"sn\": \"Test_202107310020\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"relation\": \"23424,laoshi,fdsfds,admin,test,test2,test1111,laoshia,3333,aaaa,dsfsffsdf,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 11:43:00\", \"leave_end\": \"2021-07-31 11:43:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1\"}', 'test', '2021-07-31 11:43:56.196043', '2021-07-31 11:43:56.196075', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (153, 99, 0, '', 1, 'admin', 3, '{\"id\": 99, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 10:10:39\", \"gmt_modified\": \"2021-07-31 12:04:32\", \"is_deleted\": false, \"title\": \"1\", \"workflow_id\": 1, \"sn\": \"Test_202107310005\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 10:10:00\", \"leave_end\": \"2021-07-31 10:10:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1\"}', 'admin', '2021-07-31 12:04:32.902904', '2021-07-31 12:04:32.902926', 0, 8);
INSERT INTO `ticket_ticketflowlog` VALUES (154, 100, 0, '', 1, 'admin', 3, '{\"id\": 100, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 10:11:38\", \"gmt_modified\": \"2021-07-31 12:29:50\", \"is_deleted\": false, \"title\": \"test\", \"workflow_id\": 1, \"sn\": \"Test_202107310006\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"test,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 10:11:00\", \"leave_end\": \"2021-07-31 10:11:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 111, \"text_desp\": \"111\"}', 'admin', '2021-07-31 12:29:50.235603', '2021-07-31 12:29:50.235644', 0, 8);
INSERT INTO `ticket_ticketflowlog` VALUES (155, 114, 0, '', 1, 'admin', 3, '{\"id\": 114, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 11:43:56\", \"gmt_modified\": \"2021-07-31 13:14:31\", \"is_deleted\": false, \"title\": \"1\", \"workflow_id\": 1, \"sn\": \"Test_202107310020\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 11:43:00\", \"leave_end\": \"2021-07-31 11:43:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1\"}', 'admin', '2021-07-31 13:14:31.843793', '2021-07-31 13:14:31.843814', 0, 8);
INSERT INTO `ticket_ticketflowlog` VALUES (156, 114, 0, '', 1, 'admin', 5, '{\"id\": 114, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 11:43:56\", \"gmt_modified\": \"2021-07-31 13:14:35\", \"is_deleted\": false, \"title\": \"1\", \"workflow_id\": 1, \"sn\": \"Test_202107310020\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"relation\": \"23424,laoshi,fdsfds,admin,test,test2,test1111,laoshia,3333,aaaa,dsfsffsdf,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 11:43:00\", \"leave_end\": \"2021-07-31 11:43:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1\"}', 'admin', '2021-07-31 13:14:35.501682', '2021-07-31 13:14:35.501705', 0, 8);
INSERT INTO `ticket_ticketflowlog` VALUES (157, 115, 27, '', 1, 'admin', 1, '{\"id\": 115, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 13:49:10\", \"gmt_modified\": \"2021-07-31 13:49:10\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd513\\u70b948\\u5206\", \"workflow_id\": 1, \"sn\": \"Test_202107310021\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 13:49:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u65e0\\u65e0\\u65e0\"}', 'admin', '2021-07-31 13:49:10.184524', '2021-07-31 13:49:10.184549', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (158, 116, 27, '', 1, 'test', 1, '{\"id\": 116, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 13:52:11\", \"gmt_modified\": \"2021-07-31 13:52:11\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd513\\u70b952\\u5206\", \"workflow_id\": 1, \"sn\": \"Test_202107310022\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"relation\": \"23424,laoshi,fdsfds,admin,test,test2,test1111,laoshia,3333,aaaa,dsfsffsdf,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 13:52:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u6587\\u7269\\u54c7\\u54c7\\u54c7\"}', 'test', '2021-07-31 13:52:11.510661', '2021-07-31 13:52:11.510698', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (159, 116, 0, '接单处理', 1, 'laoshi', 3, '{\"id\": 116, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 13:52:11\", \"gmt_modified\": \"2021-07-31 15:06:11\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd513\\u70b952\\u5206\", \"workflow_id\": 1, \"sn\": \"Test_202107310022\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"laoshi\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 13:52:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u6587\\u7269\\u54c7\\u54c7\\u54c7\"}', 'laoshi', '2021-07-31 15:06:11.562353', '2021-07-31 15:06:11.562379', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (160, 116, 28, '', 1, 'laoshi', 3, '{\"id\": 116, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 13:52:11\", \"gmt_modified\": \"2021-07-31 15:06:19\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd513\\u70b952\\u5206\", \"workflow_id\": 1, \"sn\": \"Test_202107310022\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 4, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 13:52:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u6587\\u7269\\u54c7\\u54c7\\u54c7\"}', 'laoshi', '2021-07-31 15:06:19.840385', '2021-07-31 15:06:19.840430', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (161, 115, 0, '接单处理', 1, 'laoshi', 3, '{\"id\": 115, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 13:49:10\", \"gmt_modified\": \"2021-07-31 15:07:06\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd513\\u70b948\\u5206\", \"workflow_id\": 1, \"sn\": \"Test_202107310021\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"laoshi\", \"relation\": \"23424,laoshi,fdsfds,admin,test,test2,test1111,laoshia,3333,aaaa,dsfsffsdf,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 13:49:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u65e0\\u65e0\\u65e0\"}', 'laoshi', '2021-07-31 15:07:06.924200', '2021-07-31 15:07:06.924228', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (162, 115, 28, '', 1, 'laoshi', 3, '{\"id\": 115, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 13:49:10\", \"gmt_modified\": \"2021-07-31 15:13:30\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd513\\u70b948\\u5206\", \"workflow_id\": 1, \"sn\": \"Test_202107310021\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"23424,laoshi,fdsfds,admin,test,test2,test1111,laoshia,3333,aaaa,dsfsffsdf,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 4, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 13:49:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u65e0\\u65e0\\u65e0\"}', 'laoshi', '2021-07-31 15:13:30.873434', '2021-07-31 15:13:30.873461', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (163, 114, 0, '接单处理', 1, 'laoshi', 3, '{\"id\": 114, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 11:43:56\", \"gmt_modified\": \"2021-07-31 15:15:19\", \"is_deleted\": false, \"title\": \"1\", \"workflow_id\": 1, \"sn\": \"Test_202107310020\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"laoshi\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 11:43:00\", \"leave_end\": \"2021-07-31 11:43:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1\"}', 'laoshi', '2021-07-31 15:15:19.053368', '2021-07-31 15:15:19.053388', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (164, 114, 28, '', 1, 'laoshi', 3, '{\"id\": 114, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 11:43:56\", \"gmt_modified\": \"2021-07-31 15:15:53\", \"is_deleted\": false, \"title\": \"1\", \"workflow_id\": 1, \"sn\": \"Test_202107310020\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 4, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 11:43:00\", \"leave_end\": \"2021-07-31 11:43:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1\"}', 'laoshi', '2021-07-31 15:15:53.954991', '2021-07-31 15:15:53.955013', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (165, 117, 27, '', 1, 'test', 1, '{\"id\": 117, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 15:19:42\", \"gmt_modified\": \"2021-07-31 15:19:42\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5 \\u6691\\u5047\", \"workflow_id\": 1, \"sn\": \"Test_202107310023\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"relation\": \"23424,laoshi,fdsfds,admin,test,test2,test1111,laoshia,3333,aaaa,dsfsffsdf,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 00:00:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\"}', 'test', '2021-07-31 15:19:42.666519', '2021-07-31 15:19:42.666541', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (166, 117, 0, '接单处理', 1, 'laoshi', 3, '{\"id\": 117, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 15:19:42\", \"gmt_modified\": \"2021-07-31 15:28:48\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5 \\u6691\\u5047\", \"workflow_id\": 1, \"sn\": \"Test_202107310023\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"laoshi\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 00:00:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\"}', 'laoshi', '2021-07-31 15:28:48.606310', '2021-07-31 15:28:48.606332', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (167, 117, 28, '', 1, 'laoshi', 3, '{\"id\": 117, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 15:19:42\", \"gmt_modified\": \"2021-07-31 15:29:41\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5 \\u6691\\u5047\", \"workflow_id\": 1, \"sn\": \"Test_202107310023\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 4, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 00:00:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\"}', 'laoshi', '2021-07-31 15:29:41.729702', '2021-07-31 15:29:41.729740', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (168, 118, 27, '', 1, 'test', 1, '{\"id\": 118, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 15:31:45\", \"gmt_modified\": \"2021-07-31 15:31:45\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5123\", \"workflow_id\": 1, \"sn\": \"Test_202107310024\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"relation\": \"23424,laoshi,fdsfds,admin,test,test2,test1111,laoshia,3333,aaaa,dsfsffsdf,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 00:00:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\"}', 'test', '2021-07-31 15:31:45.455418', '2021-07-31 15:31:45.455440', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (169, 118, 0, '接单处理', 1, 'laoshi', 3, '{\"id\": 118, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 15:31:45\", \"gmt_modified\": \"2021-07-31 15:32:18\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5123\", \"workflow_id\": 1, \"sn\": \"Test_202107310024\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"laoshi\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 00:00:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\"}', 'laoshi', '2021-07-31 15:32:18.788817', '2021-07-31 15:32:18.788838', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (170, 118, 28, '', 1, 'laoshi', 3, '{\"id\": 118, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 15:31:45\", \"gmt_modified\": \"2021-07-31 15:36:31\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5123\", \"workflow_id\": 1, \"sn\": \"Test_202107310024\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 4, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 00:00:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\"}', 'laoshi', '2021-07-31 15:36:31.268772', '2021-07-31 15:36:31.268799', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (171, 119, 27, '', 1, 'test', 1, '{\"id\": 119, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 15:37:13\", \"gmt_modified\": \"2021-07-31 15:37:13\", \"is_deleted\": false, \"title\": \"1\", \"workflow_id\": 1, \"sn\": \"Test_202107310025\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"relation\": \"23424,laoshi,fdsfds,admin,test,test2,test1111,laoshia,3333,aaaa,dsfsffsdf,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 15:37:00\", \"leave_end\": \"2021-07-31 15:37:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"111\"}', 'test', '2021-07-31 15:37:13.331094', '2021-07-31 15:37:13.331116', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (172, 119, 0, '接单处理', 1, 'laoshi', 3, '{\"id\": 119, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 15:37:13\", \"gmt_modified\": \"2021-07-31 15:37:49\", \"is_deleted\": false, \"title\": \"1\", \"workflow_id\": 1, \"sn\": \"Test_202107310025\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"laoshi\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 15:37:00\", \"leave_end\": \"2021-07-31 15:37:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"111\"}', 'laoshi', '2021-07-31 15:37:49.499508', '2021-07-31 15:37:49.499534', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (173, 119, 28, '', 1, 'laoshi', 3, '{\"id\": 119, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 15:37:13\", \"gmt_modified\": \"2021-07-31 15:38:00\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5123\", \"workflow_id\": 1, \"sn\": \"Test_202107310025\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 4, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 00:00:00\", \"leave_type\": \"\\u4e8b\\u5047\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\"}', 'laoshi', '2021-07-31 15:38:00.946343', '2021-07-31 15:38:00.946366', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (174, 120, 27, '', 1, 'test', 1, '{\"id\": 120, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 15:41:11\", \"gmt_modified\": \"2021-07-31 15:41:11\", \"is_deleted\": false, \"title\": \"\\u62d2\\u7edd\", \"workflow_id\": 1, \"sn\": \"Test_202107310026\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"relation\": \"23424,laoshi,fdsfds,admin,test,test2,test1111,laoshia,3333,aaaa,dsfsffsdf,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 00:00:00\", \"leave_end\": \"2021-07-31 15:41:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1123124125 \"}', 'test', '2021-07-31 15:41:11.466329', '2021-07-31 15:41:11.466352', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (175, 120, 0, '接单处理', 1, 'laoshi', 3, '{\"id\": 120, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 15:41:11\", \"gmt_modified\": \"2021-07-31 15:41:25\", \"is_deleted\": false, \"title\": \"\\u62d2\\u7edd\", \"workflow_id\": 1, \"sn\": \"Test_202107310026\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"laoshi\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 00:00:00\", \"leave_end\": \"2021-07-31 15:41:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1123124125 \"}', 'laoshi', '2021-07-31 15:41:25.143626', '2021-07-31 15:41:25.143649', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (176, 121, 7, '', 1, 'laoshi', 6, '{\"id\": 121, \"creator\": \"laoshi\", \"gmt_created\": \"2021-07-31 15:41:43\", \"gmt_modified\": \"2021-07-31 15:41:43\", \"is_deleted\": false, \"title\": \"1\", \"workflow_id\": 2, \"sn\": \"loonflow_202107310027\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"zhangsan,admin\", \"relation\": \"zhangsan,laoshi,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"z\\\": {}, \\\"h\\\": {}, \\\"a\\\": {}, \\\"n\\\": {}, \\\"g\\\": {}, \\\"s\\\": {}, \\\",\\\": {}, \\\"d\\\": {}, \\\"m\\\": {}, \\\"i\\\": {}}\", \"vpn_reason\": \"\\u53bb\\u554a\\u554a\\u554a\"}', 'laoshi', '2021-07-31 15:41:43.446791', '2021-07-31 15:41:43.446820', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (177, 120, 0, '强制关闭工单:意见', 1, 'admin', 5, '{\"id\": 120, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 15:41:11\", \"gmt_modified\": \"2021-07-31 15:41:25\", \"is_deleted\": false, \"title\": \"\\u62d2\\u7edd\", \"workflow_id\": 1, \"sn\": \"Test_202107310026\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"laoshi\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 00:00:00\", \"leave_end\": \"2021-07-31 15:41:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1123124125 \"}', 'admin', '2021-07-31 15:52:46.800963', '2021-07-31 15:52:46.800988', 0, 7);
INSERT INTO `ticket_ticketflowlog` VALUES (178, 121, 0, '强制关闭工单:意见', 1, 'laoshi', 11, '{\"id\": 121, \"creator\": \"laoshi\", \"gmt_created\": \"2021-07-31 15:41:43\", \"gmt_modified\": \"2021-07-31 15:41:43\", \"is_deleted\": false, \"title\": \"1\", \"workflow_id\": 2, \"sn\": \"loonflow_202107310027\", \"state_id\": 7, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"zhangsan,admin\", \"relation\": \"zhangsan,laoshi,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{\\\"z\\\": {}, \\\"h\\\": {}, \\\"a\\\": {}, \\\"n\\\": {}, \\\"g\\\": {}, \\\"s\\\": {}, \\\",\\\": {}, \\\"d\\\": {}, \\\"m\\\": {}, \\\"i\\\": {}}\", \"vpn_reason\": \"\\u53bb\\u554a\\u554a\\u554a\"}', 'laoshi', '2021-07-31 15:53:51.300842', '2021-07-31 15:53:51.300881', 0, 7);
INSERT INTO `ticket_ticketflowlog` VALUES (179, 157, 27, '', 1, 'test', 1, '{\"id\": 157, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 16:25:20\", \"gmt_modified\": \"2021-07-31 16:25:20\", \"is_deleted\": false, \"title\": \"1\", \"workflow_id\": 1, \"sn\": \"Test_202107310063\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"relation\": \"23424,laoshi,fdsfds,admin,test,test2,test1111,laoshia,3333,aaaa,dsfsffsdf,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 16:25:00\", \"leave_end\": \"2021-07-31 16:25:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1\"}', 'test', '2021-07-31 16:25:20.741761', '2021-07-31 16:25:20.741783', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (180, 158, 27, '', 1, 'admin', 1, '{\"id\": 158, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 16:31:50\", \"gmt_modified\": \"2021-07-31 16:31:50\", \"is_deleted\": false, \"title\": \"1\", \"workflow_id\": 1, \"sn\": \"Test_202107310064\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-07 00:00:00\", \"leave_end\": \"2021-06-08 00:00:00\", \"leave_type\": \"2\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"1\"}', 'admin', '2021-07-31 16:31:50.878707', '2021-07-31 16:31:50.878729', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (181, 157, 0, '强制关闭工单:意见', 1, 'admin', 5, '{\"id\": 157, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 16:25:20\", \"gmt_modified\": \"2021-07-31 16:25:20\", \"is_deleted\": false, \"title\": \"1\", \"workflow_id\": 1, \"sn\": \"Test_202107310063\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"relation\": \"23424,laoshi,fdsfds,admin,test,test2,test1111,laoshia,3333,aaaa,dsfsffsdf,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 16:25:00\", \"leave_end\": \"2021-07-31 16:25:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1\"}', 'admin', '2021-07-31 16:50:35.708452', '2021-07-31 16:50:35.708477', 0, 7);
INSERT INTO `ticket_ticketflowlog` VALUES (182, 152, 0, '强制关闭工单:意见', 1, 'admin', 5, '{\"id\": 152, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 16:05:55\", \"gmt_modified\": \"2021-07-31 16:05:55\", \"is_deleted\": false, \"title\": \"\", \"workflow_id\": 1, \"sn\": \"Test_202107310058\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"None\", \"leave_end\": \"None\", \"leave_type\": \"None\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": \"None\", \"text_desp\": \"None\"}', 'admin', '2021-07-31 16:52:34.943031', '2021-07-31 16:52:34.943055', 0, 7);
INSERT INTO `ticket_ticketflowlog` VALUES (183, 182, 0, '强制关闭工单:意见', 1, 'admin', 5, '{\"id\": 182, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 16:39:48\", \"gmt_modified\": \"2021-07-31 16:39:48\", \"is_deleted\": false, \"title\": \"\", \"workflow_id\": 1, \"sn\": \"Test_202107310088\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"None\", \"leave_end\": \"None\", \"leave_type\": \"None\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": \"None\", \"text_desp\": \"None\"}', 'admin', '2021-07-31 16:53:12.190197', '2021-07-31 16:53:12.190220', 0, 7);
INSERT INTO `ticket_ticketflowlog` VALUES (184, 181, 0, '强制关闭工单:意见', 1, 'admin', 5, '{\"id\": 181, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 16:39:48\", \"gmt_modified\": \"2021-07-31 16:39:48\", \"is_deleted\": false, \"title\": \"\", \"workflow_id\": 1, \"sn\": \"Test_202107310087\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"None\", \"leave_end\": \"None\", \"leave_type\": \"None\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": \"None\", \"text_desp\": \"None\"}', 'admin', '2021-07-31 16:54:24.408812', '2021-07-31 16:54:24.408839', 0, 7);
INSERT INTO `ticket_ticketflowlog` VALUES (185, 168, 0, '接单处理', 1, 'admin', 3, '{\"id\": 168, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 16:36:46\", \"gmt_modified\": \"2021-07-31 16:58:53\", \"is_deleted\": false, \"title\": \"\", \"workflow_id\": 1, \"sn\": \"Test_202107310074\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"admin\", \"relation\": \"23424,laoshi,fdsfds,admin,test,test2,test1111,laoshia,3333,aaaa,dsfsffsdf,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"None\", \"leave_end\": \"None\", \"leave_type\": \"None\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": \"None\", \"text_desp\": \"None\"}', 'admin', '2021-07-31 16:58:53.164626', '2021-07-31 16:58:53.164648', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (186, 163, 0, '接单处理', 1, 'admin', 3, '{\"id\": 163, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 16:34:09\", \"gmt_modified\": \"2021-07-31 17:04:18\", \"is_deleted\": false, \"title\": \"\", \"workflow_id\": 1, \"sn\": \"Test_202107310069\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"admin\", \"relation\": \"23424,laoshi,fdsfds,admin,test,test2,test1111,laoshia,3333,aaaa,dsfsffsdf,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"None\", \"leave_end\": \"None\", \"leave_type\": \"None\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": \"None\", \"text_desp\": \"None\"}', 'admin', '2021-07-31 17:04:18.917102', '2021-07-31 17:04:18.917125', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (187, 163, 28, '', 1, 'admin', 3, '{\"id\": 163, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 16:34:09\", \"gmt_modified\": \"2021-07-31 17:04:20\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5123\", \"workflow_id\": 1, \"sn\": \"Test_202107310069\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"23424,laoshi,fdsfds,admin,test,test2,test1111,laoshia,3333,aaaa,dsfsffsdf,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 4, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 00:00:00\", \"leave_type\": \"\\u4e8b\\u5047\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\"}', 'admin', '2021-07-31 17:04:21.006176', '2021-07-31 17:04:21.006217', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (188, 156, 0, '强制关闭工单:意见', 1, 'admin', 5, '{\"id\": 156, \"creator\": \"test\", \"gmt_created\": \"2021-07-31 16:25:10\", \"gmt_modified\": \"2021-07-31 16:25:10\", \"is_deleted\": false, \"title\": \"\", \"workflow_id\": 1, \"sn\": \"Test_202107310062\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"relation\": \"23424,laoshi,fdsfds,admin,test,test2,test1111,laoshia,3333,aaaa,dsfsffsdf,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"None\", \"leave_end\": \"None\", \"leave_type\": \"None\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": \"None\", \"text_desp\": \"None\"}', 'admin', '2021-07-31 17:12:30.317947', '2021-07-31 17:12:30.317983', 0, 7);
INSERT INTO `ticket_ticketflowlog` VALUES (189, 203, 0, '强制关闭工单:意见', 1, 'admin', 5, '{\"id\": 203, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 17:30:43\", \"gmt_modified\": \"2021-07-31 17:30:43\", \"is_deleted\": false, \"title\": \"\", \"workflow_id\": 1, \"sn\": \"Test_202107310109\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"None\", \"leave_end\": \"None\", \"leave_type\": \"None\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": \"None\", \"text_desp\": \"None\"}', 'admin', '2021-07-31 18:18:13.826959', '2021-07-31 18:18:13.826981', 0, 7);
INSERT INTO `ticket_ticketflowlog` VALUES (190, 202, 0, '强制关闭工单:意见', 1, 'admin', 5, '{\"id\": 202, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 17:30:27\", \"gmt_modified\": \"2021-07-31 17:30:27\", \"is_deleted\": false, \"title\": \"\", \"workflow_id\": 1, \"sn\": \"Test_202107310108\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"None\", \"leave_end\": \"None\", \"leave_type\": \"None\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": \"None\", \"text_desp\": \"None\"}', 'admin', '2021-07-31 18:18:54.355541', '2021-07-31 18:18:54.355564', 0, 7);
INSERT INTO `ticket_ticketflowlog` VALUES (191, 201, 0, '强制关闭工单:意见', 1, 'admin', 5, '{\"id\": 201, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 17:30:09\", \"gmt_modified\": \"2021-07-31 17:30:09\", \"is_deleted\": false, \"title\": \"\", \"workflow_id\": 1, \"sn\": \"Test_202107310107\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"None\", \"leave_end\": \"None\", \"leave_type\": \"None\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": \"None\", \"text_desp\": \"None\"}', 'admin', '2021-07-31 18:19:32.721632', '2021-07-31 18:19:32.721657', 0, 7);
INSERT INTO `ticket_ticketflowlog` VALUES (192, 204, 27, '', 1, 'admin', 1, '{\"id\": 204, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 18:22:49\", \"gmt_modified\": \"2021-07-31 18:22:49\", \"is_deleted\": false, \"title\": \"13123\", \"workflow_id\": 1, \"sn\": \"Test_202107310110\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"test1111,fdsfds,aaaa,dsfsffsdf,23424,test2,3333,test,laoshia,admin,laoshi,fewf\", \"relation\": \"test1111,fdsfds,aaaa,dsfsffsdf,23424,test2,3333,test,laoshia,admin,laoshi,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 18:22:00\", \"leave_end\": \"2021-07-08 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1231, \"text_desp\": \"231\"}', 'admin', '2021-07-31 18:22:49.371917', '2021-07-31 18:22:49.371943', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (193, 204, 0, '强制关闭工单:意见', 1, 'admin', 5, '{\"id\": 204, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 18:22:49\", \"gmt_modified\": \"2021-07-31 18:22:49\", \"is_deleted\": false, \"title\": \"13123\", \"workflow_id\": 1, \"sn\": \"Test_202107310110\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"test1111,fdsfds,aaaa,dsfsffsdf,23424,test2,3333,test,laoshia,admin,laoshi,fewf\", \"relation\": \"test1111,fdsfds,aaaa,dsfsffsdf,23424,test2,3333,test,laoshia,admin,laoshi,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-31 18:22:00\", \"leave_end\": \"2021-07-08 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1231, \"text_desp\": \"231\"}', 'admin', '2021-07-31 18:39:41.127565', '2021-07-31 18:39:41.127591', 0, 7);
INSERT INTO `ticket_ticketflowlog` VALUES (194, 94, 0, '强制关闭工单:意见', 1, 'admin', 5, '{\"id\": 94, \"creator\": \"test2\", \"gmt_created\": \"2021-07-30 22:44:29\", \"gmt_modified\": \"2021-07-30 22:44:29\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5\", \"workflow_id\": 1, \"sn\": \"Test_202107300052\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"\", \"relation\": \"test2\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2018-05-13 22:24:41\", \"leave_end\": \"2018-05-13 22:24:41\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u65e0\"}', 'admin', '2021-07-31 18:46:41.800002', '2021-07-31 18:46:41.800032', 0, 7);
INSERT INTO `ticket_ticketflowlog` VALUES (195, 205, 27, '', 1, 'test2', 1, '{\"id\": 205, \"creator\": \"test2\", \"gmt_created\": \"2021-07-31 18:48:23\", \"gmt_modified\": \"2021-07-31 18:48:23\", \"is_deleted\": false, \"title\": \"\\u674e\\u56db\\u8bf7\\u5047 18\\u70b948\\u5206\", \"workflow_id\": 1, \"sn\": \"Test_202107310111\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,fdsfds,test,laoshi,aaaa,test2,laoshia,fewf,dsfsffsdf,3333,admin,test1111\", \"relation\": \"test1111,23424,fdsfds,test,aaaa,test2,laoshia,fewf,dsfsffsdf,3333,admin,laoshi\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\"}', 'test2', '2021-07-31 18:48:23.118208', '2021-07-31 18:48:23.118230', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (196, 205, 0, '接单处理', 1, 'laoshi', 3, '{\"id\": 205, \"creator\": \"test2\", \"gmt_created\": \"2021-07-31 18:48:23\", \"gmt_modified\": \"2021-07-31 18:49:23\", \"is_deleted\": false, \"title\": \"\\u674e\\u56db\\u8bf7\\u5047 18\\u70b948\\u5206\", \"workflow_id\": 1, \"sn\": \"Test_202107310111\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"laoshi\", \"relation\": \"23424,fdsfds,test,laoshi,aaaa,test2,laoshia,fewf,dsfsffsdf,3333,admin,test1111\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\"}', 'laoshi', '2021-07-31 18:49:23.764139', '2021-07-31 18:49:23.764161', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (197, 205, 28, '', 1, 'laoshi', 3, '{\"id\": 205, \"creator\": \"test2\", \"gmt_created\": \"2021-07-31 18:48:23\", \"gmt_modified\": \"2021-07-31 18:49:43\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5123\", \"workflow_id\": 1, \"sn\": \"Test_202107310111\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"23424,fdsfds,test,laoshi,aaaa,test2,laoshia,fewf,dsfsffsdf,3333,admin,test1111\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 4, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 00:00:00\", \"leave_type\": \"\\u4e8b\\u5047\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\"}', 'laoshi', '2021-07-31 18:49:43.587140', '2021-07-31 18:49:43.587164', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (198, 200, 0, '强制关闭工单:意见', 1, 'admin', 5, '{\"id\": 200, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 17:29:43\", \"gmt_modified\": \"2021-07-31 17:29:43\", \"is_deleted\": false, \"title\": \"\", \"workflow_id\": 1, \"sn\": \"Test_202107310106\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"None\", \"leave_end\": \"None\", \"leave_type\": \"None\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": \"None\", \"text_desp\": \"None\"}', 'admin', '2021-07-31 18:54:03.329371', '2021-07-31 18:54:03.329421', 0, 7);
INSERT INTO `ticket_ticketflowlog` VALUES (199, 207, 27, '', 1, 'admin', 1, '{\"id\": 207, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 19:22:57\", \"gmt_modified\": \"2021-07-31 19:22:57\", \"is_deleted\": false, \"title\": \"123\", \"workflow_id\": 1, \"sn\": \"Test_202107310113\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,fdsfds,test,laoshi,aaaa,test2,laoshia,fewf,dsfsffsdf,3333,admin,test1111\", \"relation\": \"test1111,23424,fdsfds,test,aaaa,test2,laoshia,fewf,dsfsffsdf,3333,admin,laoshi\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1123112222222\"}', 'admin', '2021-07-31 19:22:57.285542', '2021-07-31 19:22:57.285575', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (200, 207, 0, '接单处理', 1, 'admin', 3, '{\"id\": 207, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 19:22:57\", \"gmt_modified\": \"2021-07-31 19:23:40\", \"is_deleted\": false, \"title\": \"123\", \"workflow_id\": 1, \"sn\": \"Test_202107310113\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"admin\", \"relation\": \"23424,fdsfds,test,laoshi,aaaa,test2,laoshia,fewf,dsfsffsdf,3333,admin,test1111\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"1123112222222\"}', 'admin', '2021-07-31 19:23:40.044818', '2021-07-31 19:23:40.044851', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (201, 207, 28, '', 1, 'admin', 3, '{\"id\": 207, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 19:22:57\", \"gmt_modified\": \"2021-07-31 19:23:44\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5123\", \"workflow_id\": 1, \"sn\": \"Test_202107310113\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"23424,fdsfds,test,laoshi,aaaa,test2,laoshia,fewf,dsfsffsdf,3333,admin,test1111\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 4, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 00:00:00\", \"leave_type\": \"\\u4e8b\\u5047\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\"}', 'admin', '2021-07-31 19:23:44.413568', '2021-07-31 19:23:44.413599', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (202, 199, 0, '强制关闭工单:意见', 1, 'admin', 5, '{\"id\": 199, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 17:29:13\", \"gmt_modified\": \"2021-07-31 17:29:13\", \"is_deleted\": false, \"title\": \"\", \"workflow_id\": 1, \"sn\": \"Test_202107310105\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"relation\": \"23424,laoshi,fdsfds,test,test2,test1111,laoshia,3333,dsfsffsdf,aaaa,admin,fewf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"None\", \"leave_end\": \"None\", \"leave_type\": \"None\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": \"None\", \"text_desp\": \"None\"}', 'admin', '2021-07-31 19:30:44.865200', '2021-07-31 19:30:44.865226', 0, 7);
INSERT INTO `ticket_ticketflowlog` VALUES (203, 206, 0, '强制关闭工单:', 1, 'admin', 5, '{\"id\": 206, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 18:55:43\", \"gmt_modified\": \"2021-07-31 18:55:43\", \"is_deleted\": false, \"title\": \"\", \"workflow_id\": 1, \"sn\": \"Test_202107310112\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"23424,fdsfds,test,laoshi,aaaa,test2,laoshia,fewf,dsfsffsdf,3333,admin,test1111\", \"relation\": \"test1111,23424,fdsfds,test,aaaa,test2,laoshia,fewf,dsfsffsdf,3333,admin,laoshi\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"None\", \"leave_end\": \"None\", \"leave_type\": \"None\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": \"None\", \"text_desp\": \"None\"}', 'admin', '2021-07-31 20:34:51.584022', '2021-07-31 20:34:51.584091', 0, 7);
INSERT INTO `ticket_ticketflowlog` VALUES (204, 198, 0, '接单处理', 1, 'admin', 3, '{\"id\": 198, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 17:29:04\", \"gmt_modified\": \"2021-07-31 20:40:21\", \"is_deleted\": false, \"title\": \"\", \"workflow_id\": 1, \"sn\": \"Test_202107310104\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"admin\", \"relation\": \"23424,fewf,dsfsffsdf,test1111,laoshi,laoshia,fdsfds,3333,test2,aaaa,test,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"None\", \"leave_end\": \"None\", \"leave_type\": \"None\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": \"None\", \"text_desp\": \"None\"}', 'admin', '2021-07-31 20:40:21.897070', '2021-07-31 20:40:21.897105', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (205, 198, 28, '', 1, 'admin', 3, '{\"id\": 198, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 17:29:04\", \"gmt_modified\": \"2021-07-31 20:54:49\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5123\", \"workflow_id\": 1, \"sn\": \"Test_202107310104\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"23424,fewf,dsfsffsdf,test1111,laoshi,laoshia,fdsfds,3333,test2,aaaa,test,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 4, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-30 00:00:00\", \"leave_end\": \"2021-07-31 00:00:00\", \"leave_type\": \"\\u4e8b\\u5047\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\"}', 'admin', '2021-07-31 20:54:49.351871', '2021-07-31 20:54:49.351897', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (206, 208, 27, '', 1, 'admin', 1, '{\"id\": 208, \"creator\": \"admin\", \"gmt_created\": \"2021-07-31 20:56:43\", \"gmt_modified\": \"2021-07-31 20:56:43\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5\\u662f\", \"workflow_id\": 1, \"sn\": \"Test_202107310114\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"fdsfds,dsfsffsdf,aaaa,laoshia,test2,laoshi,3333,test1111,23424,fewf,admin,test\", \"relation\": \"fdsfds,dsfsffsdf,aaaa,laoshia,test2,laoshi,3333,test1111,23424,fewf,admin,test\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-07-24 00:00:00\", \"leave_end\": \"2021-07-31 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u6328\\u6253\\u554a\\u554a\\u6253\\u554a\\u54c7 \\u6211\\u554a\\u6211\"}', 'admin', '2021-07-31 20:56:43.215536', '2021-07-31 20:56:43.215564', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (207, 209, 27, '', 1, 'admin', 1, '{\"id\": 209, \"creator\": \"admin\", \"gmt_created\": \"2021-08-01 12:11:22\", \"gmt_modified\": \"2021-08-01 12:11:22\", \"is_deleted\": false, \"title\": \"   \", \"workflow_id\": 1, \"sn\": \"Test_202108010001\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"aaaa,dsfsffsdf,test,fewf,test1111,test2,admin,fdsfds,3333,23424,laoshia,laoshi\", \"relation\": \"aaaa,dsfsffsdf,test,fewf,test1111,test2,admin,fdsfds,3333,23424,laoshia,laoshi\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 12:11:00\", \"leave_end\": \"2021-08-01 12:11:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"adad a da da \"}', 'admin', '2021-08-01 12:11:22.433596', '2021-08-01 12:11:22.433628', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (208, 209, 0, '接单处理', 1, 'laoshi', 3, '{\"id\": 209, \"creator\": \"admin\", \"gmt_created\": \"2021-08-01 12:11:22\", \"gmt_modified\": \"2021-08-01 12:12:09\", \"is_deleted\": false, \"title\": \"   \", \"workflow_id\": 1, \"sn\": \"Test_202108010001\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"laoshi\", \"relation\": \"aaaa,dsfsffsdf,test,fewf,test1111,test2,admin,fdsfds,3333,23424,laoshia,laoshi\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 12:11:00\", \"leave_end\": \"2021-08-01 12:11:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"adad a da da \"}', 'laoshi', '2021-08-01 12:12:09.421916', '2021-08-01 12:12:09.421962', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (209, 210, 27, '', 1, 'test', 1, '{\"id\": 210, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 12:40:41\", \"gmt_modified\": \"2021-08-01 12:40:41\", \"is_deleted\": false, \"title\": \"\\u8bf7\\u5047\\u6d4b\\u8bd5\", \"workflow_id\": 1, \"sn\": \"Test_202108010002\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"test,fdsfds,admin,laoshia,23424,3333,laoshi,dsfsffsdf,test2,fewf,test1111,aaaa\", \"relation\": \"test,fdsfds,admin,laoshia,23424,3333,laoshi,dsfsffsdf,test2,fewf,test1111,aaaa\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 12:40:00\", \"leave_end\": \"2021-08-03 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 2, \"text_desp\": \"\\u5728\\u8fd9\\u79cd\\u56f0\\u96be\\u7684\\u6289\\u62e9\\u4e0b\\uff0c\\u672c\\u4eba\\u601d\\u6765\\u60f3\\u53bb\\uff0c\\u5bdd\\u98df\\u96be\\u5b89\\u3002 \\u5e26\\u7740\\u8fd9\\u4e9b\\u95ee\\u9898\\uff0c\\u6211\\u4eec\\u6765\\u5ba1\\u89c6\\u4e00\\u4e0b\\u5b66\\u751f\\u4f1a\\u9000\\u4f1a\\u3002\", \"filename\": \"None\"}', 'test', '2021-08-01 12:40:41.322118', '2021-08-01 12:40:41.322142', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (210, 210, 0, '强制关闭工单:意见', 1, 'admin', 5, '{\"id\": 210, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 12:40:41\", \"gmt_modified\": \"2021-08-01 12:40:41\", \"is_deleted\": false, \"title\": \"\\u8bf7\\u5047\\u6d4b\\u8bd5\", \"workflow_id\": 1, \"sn\": \"Test_202108010002\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"test,fdsfds,admin,laoshia,23424,3333,laoshi,dsfsffsdf,test2,fewf,test1111,aaaa\", \"relation\": \"test,fdsfds,admin,laoshia,23424,3333,laoshi,dsfsffsdf,test2,fewf,test1111,aaaa\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 12:40:00\", \"leave_end\": \"2021-08-03 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 2, \"text_desp\": \"\\u5728\\u8fd9\\u79cd\\u56f0\\u96be\\u7684\\u6289\\u62e9\\u4e0b\\uff0c\\u672c\\u4eba\\u601d\\u6765\\u60f3\\u53bb\\uff0c\\u5bdd\\u98df\\u96be\\u5b89\\u3002 \\u5e26\\u7740\\u8fd9\\u4e9b\\u95ee\\u9898\\uff0c\\u6211\\u4eec\\u6765\\u5ba1\\u89c6\\u4e00\\u4e0b\\u5b66\\u751f\\u4f1a\\u9000\\u4f1a\\u3002\", \"filename\": \"None\"}', 'admin', '2021-08-01 12:41:02.045885', '2021-08-01 12:41:02.045916', 0, 7);
INSERT INTO `ticket_ticketflowlog` VALUES (211, 211, 27, '', 1, 'test', 1, '{\"id\": 211, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 12:43:30\", \"gmt_modified\": \"2021-08-01 12:43:30\", \"is_deleted\": false, \"title\": \"\\u8bf7\\u5047\\u6d4b\\u8bd52\", \"workflow_id\": 1, \"sn\": \"Test_202108010003\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"test,fdsfds,admin,laoshia,23424,3333,laoshi,dsfsffsdf,test2,fewf,test1111,aaaa\", \"relation\": \"test,fdsfds,admin,laoshia,23424,3333,laoshi,dsfsffsdf,test2,fewf,test1111,aaaa\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 12:43:00\", \"leave_end\": \"2021-08-03 00:00:00\", \"leave_type\": \"2\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 2, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\", \"filename\": \"None\"}', 'test', '2021-08-01 12:43:30.835766', '2021-08-01 12:43:30.835806', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (212, 211, 0, '接单处理', 1, 'laoshi', 3, '{\"id\": 211, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 12:43:30\", \"gmt_modified\": \"2021-08-01 12:44:06\", \"is_deleted\": false, \"title\": \"\\u8bf7\\u5047\\u6d4b\\u8bd52\", \"workflow_id\": 1, \"sn\": \"Test_202108010003\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"laoshi\", \"relation\": \"test,fdsfds,admin,laoshia,23424,3333,laoshi,dsfsffsdf,test2,fewf,test1111,aaaa\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 12:43:00\", \"leave_end\": \"2021-08-03 00:00:00\", \"leave_type\": \"2\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 2, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 12:44:06.650406', '2021-08-01 12:44:06.650437', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (213, 211, 28, '', 1, 'laoshi', 3, '{\"id\": 211, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 12:43:30\", \"gmt_modified\": \"2021-08-01 12:44:20\", \"is_deleted\": false, \"title\": \"\\u8bf7\\u5047\\u6d4b\\u8bd52\", \"workflow_id\": 1, \"sn\": \"Test_202108010003\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"test,fdsfds,admin,laoshia,23424,3333,laoshi,dsfsffsdf,test2,fewf,test1111,aaaa\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 4, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 12:43:00\", \"leave_end\": \"2021-08-03 00:00:00\", \"leave_type\": \"2\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 2, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 12:44:20.500805', '2021-08-01 12:44:20.500850', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (214, 213, 27, '', 1, 'test', 1, '{\"id\": 213, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 12:47:33\", \"gmt_modified\": \"2021-08-01 12:47:33\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5\\u8bf7\\u50473\", \"workflow_id\": 1, \"sn\": \"Test_202108010005\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"3333,test,laoshi,laoshia,23424,dsfsffsdf,test1111,test2,fdsfds,fewf,aaaa,admin\", \"relation\": \"3333,test,laoshi,laoshia,23424,dsfsffsdf,test1111,test2,fdsfds,fewf,aaaa,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 12:47:00\", \"leave_end\": \"2021-07-26 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u563b\\u563b\\u563b\\u563b\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\", \"filename\": \"None\"}', 'test', '2021-08-01 12:47:33.645449', '2021-08-01 12:47:33.645473', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (215, 212, 0, '接单处理', 1, 'laoshi', 3, '{\"id\": 212, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 12:47:24\", \"gmt_modified\": \"2021-08-01 12:52:51\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5\\u8bf7\\u50473\", \"workflow_id\": 1, \"sn\": \"Test_202108010004\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"laoshi\", \"relation\": \"3333,test,laoshi,laoshia,23424,dsfsffsdf,test1111,test2,fdsfds,fewf,aaaa,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"None\", \"leave_end\": \"None\", \"leave_type\": \"None\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": \"None\", \"text_desp\": \"None\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 12:52:51.981252', '2021-08-01 12:52:51.981288', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (216, 213, 0, '接单处理', 1, 'laoshi', 3, '{\"id\": 213, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 12:47:33\", \"gmt_modified\": \"2021-08-01 12:53:04\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5\\u8bf7\\u50473\", \"workflow_id\": 1, \"sn\": \"Test_202108010005\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"laoshi\", \"relation\": \"3333,test,laoshi,laoshia,23424,dsfsffsdf,test1111,test2,fdsfds,fewf,aaaa,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 12:47:00\", \"leave_end\": \"2021-07-26 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u563b\\u563b\\u563b\\u563b\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 12:53:04.991421', '2021-08-01 12:53:04.991446', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (217, 214, 27, '', 1, 'test', 1, '{\"id\": 214, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 12:55:34\", \"gmt_modified\": \"2021-08-01 12:55:34\", \"is_deleted\": false, \"title\": \"\\u8bf7\\u5047\\u6d4b\\u8bd5\", \"workflow_id\": 1, \"sn\": \"Test_202108010006\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"3333,test,laoshi,laoshia,23424,dsfsffsdf,test1111,test2,fdsfds,fewf,aaaa,admin\", \"relation\": \"3333,test,laoshi,laoshia,23424,dsfsffsdf,test1111,test2,fdsfds,fewf,aaaa,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 12:55:00\", \"leave_end\": \"2021-08-01 12:55:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u6211\\u6211\", \"filename\": \"None\"}', 'test', '2021-08-01 12:55:35.056383', '2021-08-01 12:55:35.056407', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (218, 214, 0, '接单处理', 1, 'laoshi', 3, '{\"id\": 214, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 12:55:34\", \"gmt_modified\": \"2021-08-01 12:56:03\", \"is_deleted\": false, \"title\": \"\\u8bf7\\u5047\\u6d4b\\u8bd5\", \"workflow_id\": 1, \"sn\": \"Test_202108010006\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"laoshi\", \"relation\": \"3333,test,laoshi,laoshia,23424,dsfsffsdf,test1111,test2,fdsfds,fewf,aaaa,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 12:55:00\", \"leave_end\": \"2021-08-01 12:55:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u6211\\u6211\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 12:56:03.545643', '2021-08-01 12:56:03.545668', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (219, 214, 28, '', 1, 'laoshi', 3, '{\"id\": 214, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 12:55:34\", \"gmt_modified\": \"2021-08-01 12:59:54\", \"is_deleted\": false, \"title\": \"\\u8bf7\\u5047\\u6d4b\\u8bd5\", \"workflow_id\": 1, \"sn\": \"Test_202108010006\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"3333,test,laoshi,laoshia,23424,dsfsffsdf,test1111,test2,fdsfds,fewf,aaaa,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 4, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 12:55:00\", \"leave_end\": \"2021-08-01 12:55:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u6211\\u6211\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 12:59:54.991561', '2021-08-01 12:59:54.991588', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (220, 213, 28, '', 1, 'laoshi', 3, '{\"id\": 213, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 12:47:33\", \"gmt_modified\": \"2021-08-01 13:00:50\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5\\u8bf7\\u50473\", \"workflow_id\": 1, \"sn\": \"Test_202108010005\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"3333,test,laoshi,laoshia,23424,dsfsffsdf,test1111,test2,fdsfds,fewf,aaaa,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 4, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 12:47:00\", \"leave_end\": \"2021-07-26 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u563b\\u563b\\u563b\\u563b\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 13:00:50.815580', '2021-08-01 13:00:50.815608', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (221, 215, 27, '', 1, 'test', 1, '{\"id\": 215, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 13:01:14\", \"gmt_modified\": \"2021-08-01 13:01:14\", \"is_deleted\": false, \"title\": \"\\u8bf7\\u5047\\u6d4b\\u8bd55\", \"workflow_id\": 1, \"sn\": \"Test_202108010007\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"aaaa,test2,laoshia,test1111,fewf,admin,3333,test,laoshi,23424,dsfsffsdf,fdsfds\", \"relation\": \"aaaa,test2,laoshia,test1111,fewf,test,admin,3333,laoshi,23424,dsfsffsdf,fdsfds\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 13:01:00\", \"leave_end\": \"2021-08-31 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1111, \"text_desp\": \"121111111111111111\", \"filename\": \"None\"}', 'test', '2021-08-01 13:01:14.947447', '2021-08-01 13:01:14.947495', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (222, 215, 0, '接单处理', 1, 'laoshi', 3, '{\"id\": 215, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 13:01:14\", \"gmt_modified\": \"2021-08-01 13:01:27\", \"is_deleted\": false, \"title\": \"\\u8bf7\\u5047\\u6d4b\\u8bd55\", \"workflow_id\": 1, \"sn\": \"Test_202108010007\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"laoshi\", \"relation\": \"aaaa,test2,laoshia,test1111,fewf,test,admin,3333,laoshi,23424,dsfsffsdf,fdsfds\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 13:01:00\", \"leave_end\": \"2021-08-31 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1111, \"text_desp\": \"121111111111111111\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 13:01:27.174349', '2021-08-01 13:01:27.174374', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (223, 215, 28, '', 1, 'laoshi', 3, '{\"id\": 215, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 13:01:14\", \"gmt_modified\": \"2021-08-01 13:01:36\", \"is_deleted\": false, \"title\": \"\\u8bf7\\u5047\\u6d4b\\u8bd55\", \"workflow_id\": 1, \"sn\": \"Test_202108010007\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"aaaa,test2,laoshia,test1111,fewf,test,admin,3333,laoshi,23424,dsfsffsdf,fdsfds\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 4, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 13:01:00\", \"leave_end\": \"2021-08-31 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1111, \"text_desp\": \"121111111111111111\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 13:01:37.015868', '2021-08-01 13:01:37.015908', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (224, 216, 27, '', 1, 'test', 1, '{\"id\": 216, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 13:05:30\", \"gmt_modified\": \"2021-08-01 13:05:30\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd51\", \"workflow_id\": 1, \"sn\": \"Test_202108010008\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"test1111,dsfsffsdf,test2,fewf,fdsfds,admin,laoshi,3333,aaaa,laoshia,test,23424\", \"relation\": \"test1111,dsfsffsdf,test2,fewf,fdsfds,admin,3333,aaaa,23424,laoshia,test,laoshi\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 13:05:00\", \"leave_end\": \"2021-08-01 13:05:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"11114124124512\", \"filename\": \"None\"}', 'test', '2021-08-01 13:05:30.736643', '2021-08-01 13:05:30.736667', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (225, 216, 0, '接单处理', 1, 'laoshi', 3, '{\"id\": 216, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 13:05:30\", \"gmt_modified\": \"2021-08-01 13:05:43\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd51\", \"workflow_id\": 1, \"sn\": \"Test_202108010008\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"laoshi\", \"relation\": \"test1111,test2,dsfsffsdf,fewf,fdsfds,admin,laoshi,3333,aaaa,laoshia,test,23424\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 13:05:00\", \"leave_end\": \"2021-08-01 13:05:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"11114124124512\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 13:05:43.110783', '2021-08-01 13:05:43.110824', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (226, 216, 28, '', 1, 'laoshi', 3, '{\"id\": 216, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 13:05:30\", \"gmt_modified\": \"2021-08-01 13:05:43\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd51\", \"workflow_id\": 1, \"sn\": \"Test_202108010008\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"test1111,test2,dsfsffsdf,fewf,fdsfds,admin,laoshi,3333,aaaa,laoshia,test,23424\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 4, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 13:05:00\", \"leave_end\": \"2021-08-01 13:05:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"11114124124512\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 13:05:43.292660', '2021-08-01 13:05:43.292694', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (227, 217, 27, '', 1, 'test', 1, '{\"id\": 217, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 13:07:55\", \"gmt_modified\": \"2021-08-01 13:07:55\", \"is_deleted\": false, \"title\": \"111\", \"workflow_id\": 1, \"sn\": \"Test_202108010009\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"test1111,dsfsffsdf,test2,fewf,fdsfds,admin,laoshi,3333,aaaa,laoshia,test,23424\", \"relation\": \"test1111,dsfsffsdf,test2,fewf,fdsfds,admin,3333,aaaa,23424,laoshia,test,laoshi\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 13:07:00\", \"leave_end\": \"2021-08-01 13:07:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"11111\", \"filename\": \"None\"}', 'test', '2021-08-01 13:07:55.606655', '2021-08-01 13:07:55.606698', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (228, 217, 0, '接单处理', 1, 'laoshi', 3, '{\"id\": 217, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 13:07:55\", \"gmt_modified\": \"2021-08-01 13:08:01\", \"is_deleted\": false, \"title\": \"111\", \"workflow_id\": 1, \"sn\": \"Test_202108010009\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"laoshi\", \"relation\": \"test1111,test2,dsfsffsdf,fewf,fdsfds,admin,laoshi,3333,aaaa,laoshia,test,23424\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 13:07:00\", \"leave_end\": \"2021-08-01 13:07:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"11111\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 13:08:02.008258', '2021-08-01 13:08:02.008292', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (229, 217, 28, '', 1, 'laoshi', 3, '{\"id\": 217, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 13:07:55\", \"gmt_modified\": \"2021-08-01 13:08:02\", \"is_deleted\": false, \"title\": \"111\", \"workflow_id\": 1, \"sn\": \"Test_202108010009\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"test1111,test2,dsfsffsdf,fewf,fdsfds,admin,laoshi,3333,aaaa,laoshia,test,23424\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 4, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 13:07:00\", \"leave_end\": \"2021-08-01 13:07:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"11111\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 13:08:02.110861', '2021-08-01 13:08:02.110899', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (230, 218, 27, '', 1, 'laoshi', 1, '{\"id\": 218, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 13:17:29\", \"gmt_modified\": \"2021-08-01 13:17:29\", \"is_deleted\": false, \"title\": \"123\", \"workflow_id\": 1, \"sn\": \"Test_202108010010\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"fewf,test1111,aaaa,test,laoshia,laoshi,fdsfds,test2,23424,admin,dsfsffsdf,3333\", \"relation\": \"test1111,admin,aaaa,test,laoshia,laoshi,dsfsffsdf,fdsfds,23424,test2,fewf,3333\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 13:17:00\", \"leave_end\": \"2021-08-01 13:17:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 456, \"text_desp\": \"WWWWWW\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 13:17:29.956552', '2021-08-01 13:17:29.956576', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (231, 221, 27, '', 1, 'laoshi', 1, '{\"id\": 221, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 13:23:08\", \"gmt_modified\": \"2021-08-01 13:23:08\", \"is_deleted\": false, \"title\": \"111\", \"workflow_id\": 1, \"sn\": \"Test_202108010013\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"fewf,test1111,aaaa,test,laoshia,laoshi,fdsfds,test2,23424,admin,dsfsffsdf,3333\", \"relation\": \"test1111,admin,aaaa,test,laoshia,laoshi,dsfsffsdf,fdsfds,23424,test2,fewf,3333\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 13:22:00\", \"leave_end\": \"2021-08-01 13:23:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1231451, \"text_desp\": \"2141241241\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 13:23:08.826996', '2021-08-01 13:23:08.827024', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (232, 224, 27, '', 1, 'laoshi', 1, '{\"id\": 224, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 13:38:50\", \"gmt_modified\": \"2021-08-01 13:38:50\", \"is_deleted\": false, \"title\": \"123213123\", \"workflow_id\": 1, \"sn\": \"Test_202108010016\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"dsfsffsdf,3333,laoshi,23424,test,test1111,fewf,aaaa,test2,fdsfds,admin,laoshia\", \"relation\": \"dsfsffsdf,laoshi,3333,23424,test,test1111,fewf,aaaa,test2,fdsfds,admin,laoshia\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 13:38:00\", \"leave_end\": \"2021-08-01 13:38:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 3123123, \"text_desp\": \"1313123\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 13:38:50.718412', '2021-08-01 13:38:50.718442', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (233, 225, 27, '', 1, 'laoshi', 1, '{\"id\": 225, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 13:40:21\", \"gmt_modified\": \"2021-08-01 13:40:21\", \"is_deleted\": false, \"title\": \"123213123\", \"workflow_id\": 1, \"sn\": \"Test_202108010017\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"3333,test2,aaaa,laoshi,23424,fdsfds,fewf,admin,test,laoshia,test1111,dsfsffsdf\", \"relation\": \"3333,test2,aaaa,laoshi,23424,fdsfds,fewf,admin,test,laoshia,test1111,dsfsffsdf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 13:38:00\", \"leave_end\": \"2021-08-01 13:38:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 3123123, \"text_desp\": \"1313123\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 13:40:21.890602', '2021-08-01 13:40:21.890630', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (234, 226, 27, '', 1, 'laoshi', 1, '{\"id\": 226, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 13:41:05\", \"gmt_modified\": \"2021-08-01 13:41:05\", \"is_deleted\": false, \"title\": \"1231\", \"workflow_id\": 1, \"sn\": \"Test_202108010018\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"3333,test2,aaaa,laoshi,23424,fdsfds,fewf,admin,test,laoshia,test1111,dsfsffsdf\", \"relation\": \"3333,test2,aaaa,laoshi,23424,fdsfds,fewf,admin,test,laoshia,test1111,dsfsffsdf\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 13:40:00\", \"leave_end\": \"2021-07-10 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 123, \"text_desp\": \"1232213123123123123\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 13:41:05.483583', '2021-08-01 13:41:05.483610', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (235, 227, 27, '', 1, 'laoshi', 1, '{\"id\": 227, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 13:46:44\", \"gmt_modified\": \"2021-08-01 13:46:44\", \"is_deleted\": false, \"title\": \"1231\", \"workflow_id\": 1, \"sn\": \"Test_202108010019\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"test1111,23424,fdsfds,fewf,laoshia,test,dsfsffsdf,admin,test2,laoshi,3333,aaaa\", \"relation\": \"test1111,23424,fdsfds,fewf,laoshia,3333,dsfsffsdf,admin,test2,laoshi,test,aaaa\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 13:46:00\", \"leave_end\": \"2021-08-01 13:46:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1231, \"text_desp\": \"2312312312231\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 13:46:44.667295', '2021-08-01 13:46:44.667333', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (236, 228, 27, '', 1, 'laoshi', 1, '{\"id\": 228, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 13:48:01\", \"gmt_modified\": \"2021-08-01 13:48:01\", \"is_deleted\": false, \"title\": \"213132\", \"workflow_id\": 1, \"sn\": \"Test_202108010020\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"dsfsffsdf,test,test2,laoshi,laoshia,23424,admin,fewf,aaaa,3333,fdsfds,test1111\", \"relation\": \"test,test2,dsfsffsdf,laoshi,laoshia,admin,fewf,23424,3333,fdsfds,aaaa,test1111\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 13:47:00\", \"leave_end\": \"2021-08-01 13:47:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 123123, \"text_desp\": \"1231231\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 13:48:01.519661', '2021-08-01 13:48:01.519685', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (237, 229, 27, '', 1, 'laoshi', 1, '{\"id\": 229, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 13:48:55\", \"gmt_modified\": \"2021-08-01 13:48:55\", \"is_deleted\": false, \"title\": \"11111111111\", \"workflow_id\": 1, \"sn\": \"Test_202108010021\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"dsfsffsdf,test,test2,laoshi,laoshia,23424,admin,fewf,aaaa,3333,fdsfds,test1111\", \"relation\": \"test,test2,dsfsffsdf,laoshi,laoshia,admin,fewf,23424,3333,fdsfds,aaaa,test1111\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 13:48:00\", \"leave_end\": \"2021-08-01 13:48:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"123123\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 13:48:55.504178', '2021-08-01 13:48:55.504203', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (238, 230, 27, '', 1, 'laoshi', 1, '{\"id\": 230, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 13:50:14\", \"gmt_modified\": \"2021-08-01 13:50:14\", \"is_deleted\": false, \"title\": \"23123123\", \"workflow_id\": 1, \"sn\": \"loonflow_202108010022\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"test,fdsfds,laoshia,dsfsffsdf,3333,23424,fewf,aaaa,admin,test1111,test2,laoshi\", \"relation\": \"test,fdsfds,dsfsffsdf,3333,23424,fewf,aaaa,admin,test1111,laoshia,test2,laoshi\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 13:50:09\", \"leave_end\": \"2021-08-01 13:50:08\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 3, \"text_desp\": \"1w131\", \"filename\": \"\"}', 'laoshi', '2021-08-01 13:50:14.496849', '2021-08-01 13:50:14.496883', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (239, 231, 27, '', 1, 'laoshi', 1, '{\"id\": 231, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 14:02:25\", \"gmt_modified\": \"2021-08-01 14:02:25\", \"is_deleted\": false, \"title\": \"1131\", \"workflow_id\": 1, \"sn\": \"Test_202108010023\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"test,fdsfds,laoshia,dsfsffsdf,3333,23424,fewf,aaaa,admin,test1111,test2,laoshi\", \"relation\": \"test,fdsfds,dsfsffsdf,3333,23424,fewf,aaaa,admin,test1111,laoshia,test2,laoshi\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 14:02:00\", \"leave_end\": \"2021-08-01 14:02:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11111, \"text_desp\": \"11\", \"filename\": \"None\"}', 'laoshi', '2021-08-01 14:02:25.214354', '2021-08-01 14:02:25.214391', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (240, 232, 27, '', 1, 'laoshi', 1, '{\"id\": 232, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 14:06:12\", \"gmt_modified\": \"2021-08-01 14:06:12\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5\", \"workflow_id\": 1, \"sn\": \"Test_202108010024\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"test,fdsfds,laoshia,dsfsffsdf,3333,23424,fewf,aaaa,admin,test1111,test2,laoshi\", \"relation\": \"test,fdsfds,dsfsffsdf,3333,23424,fewf,aaaa,admin,test1111,laoshia,test2,laoshi\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2018-05-13 22:24:41\", \"leave_end\": \"2018-05-13 22:24:41\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u65e0\", \"filename\": \"123\"}', 'laoshi', '2021-08-01 14:06:12.390014', '2021-08-01 14:06:12.390038', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (241, 233, 27, '', 1, 'laoshi', 1, '{\"id\": 233, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 14:07:59\", \"gmt_modified\": \"2021-08-01 14:07:59\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5\", \"workflow_id\": 1, \"sn\": \"Test_202108010025\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"3333,dsfsffsdf,fewf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,admin\", \"relation\": \"3333,dsfsffsdf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,fewf,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2018-05-13 22:24:41\", \"leave_end\": \"2018-05-13 22:24:41\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u65e0\", \"filename\": \"media/upload/202108/TESTIMG1627796879043.png\"}', 'laoshi', '2021-08-01 14:07:59.454486', '2021-08-01 14:07:59.454509', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (242, 234, 27, '', 1, 'laoshi', 1, '{\"id\": 234, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 14:18:24\", \"gmt_modified\": \"2021-08-01 14:18:24\", \"is_deleted\": false, \"title\": \"1231\", \"workflow_id\": 1, \"sn\": \"Test_202108010026\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"3333,dsfsffsdf,fewf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,admin\", \"relation\": \"3333,dsfsffsdf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,fewf,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 14:18:00\", \"leave_end\": \"2021-08-01 14:18:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 123, \"text_desp\": \"wwwwwwwwwww\", \"filename\": \"\"}', 'laoshi', '2021-08-01 14:18:24.289031', '2021-08-01 14:18:24.289061', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (243, 235, 27, '', 1, 'laoshi', 1, '{\"id\": 235, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 14:18:53\", \"gmt_modified\": \"2021-08-01 14:18:53\", \"is_deleted\": false, \"title\": \"2312\", \"workflow_id\": 1, \"sn\": \"Test_202108010027\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"3333,dsfsffsdf,fewf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,admin\", \"relation\": \"3333,dsfsffsdf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,fewf,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 14:18:00\", \"leave_end\": \"2021-08-01 14:18:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1231231223, \"text_desp\": \"123123213123\", \"filename\": \"\"}', 'laoshi', '2021-08-01 14:18:53.886956', '2021-08-01 14:18:53.886979', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (244, 236, 27, '', 1, 'laoshi', 1, '{\"id\": 236, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 14:21:42\", \"gmt_modified\": \"2021-08-01 14:21:42\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5\", \"workflow_id\": 1, \"sn\": \"Test_202108010028\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"3333,dsfsffsdf,fewf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,admin\", \"relation\": \"3333,dsfsffsdf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,fewf,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2018-05-13 22:24:41\", \"leave_end\": \"2018-05-13 22:24:41\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u65e0\", \"filename\": \"media/upload/202108/TESTIMG21627798723013.png\"}', 'laoshi', '2021-08-01 14:21:42.533016', '2021-08-01 14:21:42.533047', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (245, 237, 27, '', 1, 'laoshi', 1, '{\"id\": 237, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 14:37:14\", \"gmt_modified\": \"2021-08-01 14:37:14\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5A\", \"workflow_id\": 1, \"sn\": \"Test_202108010029\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"3333,dsfsffsdf,fewf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,admin\", \"relation\": \"3333,dsfsffsdf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,fewf,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 14:37:00\", \"leave_end\": \"2021-08-27 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"WWWWWWWWWW\", \"filename\": \"\"}', 'laoshi', '2021-08-01 14:37:14.218972', '2021-08-01 14:37:14.218998', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (246, 238, 27, '', 1, 'laoshi', 1, '{\"id\": 238, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 14:39:25\", \"gmt_modified\": \"2021-08-01 14:39:25\", \"is_deleted\": false, \"title\": \"123213\", \"workflow_id\": 1, \"sn\": \"Test_202108010030\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"3333,dsfsffsdf,fewf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,admin\", \"relation\": \"3333,dsfsffsdf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,fewf,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 14:39:00\", \"leave_end\": \"2021-08-01 14:39:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 12312313, \"text_desp\": \"213123123123\", \"filename\": \"\"}', 'laoshi', '2021-08-01 14:39:26.079014', '2021-08-01 14:39:26.079045', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (247, 239, 27, '', 1, 'laoshi', 1, '{\"id\": 239, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 14:40:44\", \"gmt_modified\": \"2021-08-01 14:40:44\", \"is_deleted\": false, \"title\": \"1\", \"workflow_id\": 1, \"sn\": \"Test_202108010031\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"3333,dsfsffsdf,fewf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,admin\", \"relation\": \"3333,dsfsffsdf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,fewf,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 14:40:00\", \"leave_end\": \"2021-08-01 14:40:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1231, \"text_desp\": \"322131312\", \"filename\": \"\"}', 'laoshi', '2021-08-01 14:40:44.775281', '2021-08-01 14:40:44.775318', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (248, 240, 27, '', 1, 'laoshi', 1, '{\"id\": 240, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 14:53:01\", \"gmt_modified\": \"2021-08-01 14:53:01\", \"is_deleted\": false, \"title\": \"1231231\", \"workflow_id\": 1, \"sn\": \"Test_202108010032\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"3333,dsfsffsdf,fewf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,admin\", \"relation\": \"3333,dsfsffsdf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,fewf,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 14:52:00\", \"leave_end\": \"2021-08-01 14:52:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 123131, \"text_desp\": \"3213131231\", \"filename\": \"\"}', 'laoshi', '2021-08-01 14:53:01.896080', '2021-08-01 14:53:01.896113', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (249, 241, 27, '', 1, 'laoshi', 1, '{\"id\": 241, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 14:54:15\", \"gmt_modified\": \"2021-08-01 14:54:15\", \"is_deleted\": false, \"title\": \"12313\", \"workflow_id\": 1, \"sn\": \"Test_202108010033\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"3333,dsfsffsdf,fewf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,admin\", \"relation\": \"3333,dsfsffsdf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,fewf,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 14:53:00\", \"leave_end\": \"2021-08-01 14:53:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 123123, \"text_desp\": \"1231231\", \"filename\": \"\"}', 'laoshi', '2021-08-01 14:54:15.864318', '2021-08-01 14:54:15.864344', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (250, 242, 27, '', 1, 'laoshi', 1, '{\"id\": 242, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 14:55:00\", \"gmt_modified\": \"2021-08-01 14:55:00\", \"is_deleted\": false, \"title\": \"12312313\", \"workflow_id\": 1, \"sn\": \"Test_202108010034\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"3333,dsfsffsdf,fewf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,admin\", \"relation\": \"3333,dsfsffsdf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,fewf,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 14:54:00\", \"leave_end\": \"2021-08-01 14:54:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 213123, \"text_desp\": \"12321313\", \"filename\": \"/media/upload/202108/21627800887288.png\"}', 'laoshi', '2021-08-01 14:55:00.200783', '2021-08-01 14:55:00.200841', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (251, 243, 27, '', 1, 'laoshi', 1, '{\"id\": 243, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 15:02:28\", \"gmt_modified\": \"2021-08-01 15:02:28\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5\\u6d4b\\u8bd5\", \"workflow_id\": 1, \"sn\": \"Test_202108010035\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"3333,dsfsffsdf,fewf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,admin\", \"relation\": \"3333,dsfsffsdf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,fewf,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 15:02:00\", \"leave_end\": \"2021-08-02 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\", \"filename\": \"/media/upload/202108/\\u7406\\u75311627801346063.docx\"}', 'laoshi', '2021-08-01 15:02:28.990151', '2021-08-01 15:02:28.990174', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (252, 243, 0, '接单处理', 1, 'laoshi', 3, '{\"id\": 243, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 15:02:28\", \"gmt_modified\": \"2021-08-01 15:03:25\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5\\u6d4b\\u8bd5\", \"workflow_id\": 1, \"sn\": \"Test_202108010035\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"laoshi\", \"relation\": \"3333,dsfsffsdf,fewf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 15:02:00\", \"leave_end\": \"2021-08-02 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\", \"filename\": \"/media/upload/202108/\\u7406\\u75311627801346063.docx\"}', 'laoshi', '2021-08-01 15:03:25.369092', '2021-08-01 15:03:25.369117', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (253, 243, 28, '', 1, 'laoshi', 3, '{\"id\": 243, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 15:02:28\", \"gmt_modified\": \"2021-08-01 15:03:25\", \"is_deleted\": false, \"title\": \"\\u6d4b\\u8bd5\\u6d4b\\u8bd5\", \"workflow_id\": 1, \"sn\": \"Test_202108010035\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"3333,dsfsffsdf,fewf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 4, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 15:02:00\", \"leave_end\": \"2021-08-02 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\", \"filename\": \"/media/upload/202108/\\u7406\\u75311627801346063.docx\"}', 'laoshi', '2021-08-01 15:03:25.468493', '2021-08-01 15:03:25.468532', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (254, 217, 0, '强制关闭工单:意见', 1, 'admin', 5, '{\"id\": 217, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 13:07:55\", \"gmt_modified\": \"2021-08-01 13:08:02\", \"is_deleted\": false, \"title\": \"111\", \"workflow_id\": 1, \"sn\": \"Test_202108010009\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"test1111,test2,dsfsffsdf,fewf,fdsfds,admin,laoshi,3333,aaaa,laoshia,test,23424\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 4, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 13:07:00\", \"leave_end\": \"2021-08-01 13:07:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \"11111\", \"filename\": \"None\"}', 'admin', '2021-08-01 15:06:54.431651', '2021-08-01 15:06:54.431676', 0, 7);
INSERT INTO `ticket_ticketflowlog` VALUES (255, 244, 27, '', 1, 'test', 1, '{\"id\": 244, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 15:08:56\", \"gmt_modified\": \"2021-08-01 15:08:56\", \"is_deleted\": false, \"title\": \"\\u9644\\u4ef6\", \"workflow_id\": 1, \"sn\": \"Test_202108010036\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"3333,dsfsffsdf,fewf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,admin\", \"relation\": \"3333,dsfsffsdf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,fewf,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 15:08:00\", \"leave_end\": \"2021-08-03 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 2, \"text_desp\": \"\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\\u54c7\", \"filename\": \"/media/upload/202108/11627801735068.png\"}', 'test', '2021-08-01 15:08:56.824696', '2021-08-01 15:08:56.824732', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (256, 245, 27, '', 1, 'test', 1, '{\"id\": 245, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 15:09:22\", \"gmt_modified\": \"2021-08-01 15:09:22\", \"is_deleted\": false, \"title\": \"\\u65e0\\u9644\\u4ef6\", \"workflow_id\": 1, \"sn\": \"Test_202108010037\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"3333,dsfsffsdf,fewf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,admin\", \"relation\": \"3333,dsfsffsdf,fdsfds,aaaa,laoshi,test,laoshia,test1111,test2,23424,fewf,admin\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 15:09:00\", \"leave_end\": \"2021-08-12 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 11, \"text_desp\": \" \\u8fbe\\u74e6\\u8fbe\\u74e6\\u53d1\\u6211f\\u54c7\\u54c7\\u54d2\\u54d2\\u54d2\\u554a\\u6253\", \"filename\": \"\"}', 'test', '2021-08-01 15:09:22.161180', '2021-08-01 15:09:22.161203', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (257, 246, 27, '', 1, 'laoshi', 1, '{\"id\": 246, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 21:38:55\", \"gmt_modified\": \"2021-08-01 21:38:55\", \"is_deleted\": false, \"title\": \"\\u8bf7\\u5047\\u6d4b\\u8bd5\", \"workflow_id\": 1, \"sn\": \"Test_202108010038\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"dsfsffsdf,fdsfds,test2,test1111,23424,aaaa,fewf,admin,test,laoshi,laoshia,3333\", \"relation\": \"dsfsffsdf,fdsfds,test2,test1111,23424,aaaa,fewf,admin,test,laoshi,laoshia,3333\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 21:38:00\", \"leave_end\": \"2021-08-02 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u8fd9\\u91cc\\u662f\\u8bf7\\u5047\\u539f\\u56e0 \\u8fd9\\u91cc\\u662f\\u8bf7\\u5047\\u539f\\u56e0 \\u8fd9\\u91cc\\u662f\\u8bf7\\u5047\\u539f\\u56e0\", \"filename\": \"/media/upload/202108/11627825132912.png\"}', 'laoshi', '2021-08-01 21:38:55.594722', '2021-08-01 21:38:55.594763', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (258, 247, 27, '', 1, 'laoshi', 1, '{\"id\": 247, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 21:39:28\", \"gmt_modified\": \"2021-08-01 21:39:28\", \"is_deleted\": false, \"title\": \"\\u6807\\u9898\", \"workflow_id\": 1, \"sn\": \"Test_202108010039\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"dsfsffsdf,fdsfds,test2,test1111,23424,aaaa,fewf,admin,test,laoshi,laoshia,3333\", \"relation\": \"dsfsffsdf,fdsfds,test2,test1111,23424,aaaa,fewf,admin,test,laoshi,laoshia,3333\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 21:39:00\", \"leave_end\": \"2021-08-03 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 2, \"text_desp\": \"\\u8fd9\\u91cc\\u662f\\u8bf7\\u5047\\u539f\\u56e0\\u8fd9\\u91cc\\u662f\\u8bf7\\u5047\\u539f\\u56e0\\u8fd9\\u91cc\\u662f\\u8bf7\\u5047\\u539f\\u56e0\\u8fd9\\u91cc\\u662f\\u8bf7\\u5047\\u539f\\u56e0\\u8fd9\\u91cc\\u662f\\u8bf7\\u5047\\u539f\\u56e0\", \"filename\": \"\"}', 'laoshi', '2021-08-01 21:39:28.448343', '2021-08-01 21:39:28.448384', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (259, 248, 27, '', 1, 'laoshi', 1, '{\"id\": 248, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 21:40:13\", \"gmt_modified\": \"2021-08-01 21:40:13\", \"is_deleted\": false, \"title\": \"\\u8bf7\\u4e8b\\u5047\", \"workflow_id\": 1, \"sn\": \"Test_202108010040\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"dsfsffsdf,fdsfds,test2,test1111,23424,aaaa,fewf,admin,test,laoshi,laoshia,3333\", \"relation\": \"dsfsffsdf,fdsfds,test2,test1111,23424,aaaa,fewf,admin,test,laoshi,laoshia,3333\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 21:40:00\", \"leave_end\": \"2021-08-02 00:00:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u8fd9\\u91cc\\u662f\\u8bf7\\u5047\\u539f\\u56e0\\u8fd9\\u91cc\\u662f\\u8bf7\\u5047\\u539f\\u56e0\\u8fd9\\u91cc\\u662f\\u8bf7\\u5047\\u539f\\u56e0\\u8fd9\\u91cc\\u662f\\u8bf7\\u5047\\u539f\\u56e0\\u8fd9\\u91cc\\u662f\\u8bf7\\u5047\\u539f\\u56e0\\u8fd9\\u91cc\\u662f\\u8bf7\\u5047\\u539f\\u56e0\", \"filename\": \"\"}', 'laoshi', '2021-08-01 21:40:14.068324', '2021-08-01 21:40:14.068362', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (260, 249, 27, '', 1, 'laoshi', 1, '{\"id\": 249, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 21:40:34\", \"gmt_modified\": \"2021-08-01 21:40:34\", \"is_deleted\": false, \"title\": \"\\u8bf7\\u75c5\\u5047\", \"workflow_id\": 1, \"sn\": \"Test_202108010041\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"dsfsffsdf,fdsfds,test2,test1111,23424,aaaa,fewf,admin,test,laoshi,laoshia,3333\", \"relation\": \"dsfsffsdf,fdsfds,test2,test1111,23424,aaaa,fewf,admin,test,laoshi,laoshia,3333\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 21:40:00\", \"leave_end\": \"2021-08-03 00:00:00\", \"leave_type\": \"1\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 2, \"text_desp\": \"\\u8fd9\\u91cc\\u662f\\u8bf7\\u5047\\u539f\\u56e0\\u8fd9\\u91cc\\u662f\\u8bf7\\u5047\\u539f\\u56e0\\u8fd9\\u91cc\\u662f\\u8bf7\\u5047\\u539f\\u56e0\\u8fd9\\u91cc\\u662f\\u8bf7\\u5047\\u539f\\u56e0\\u8fd9\\u91cc\\u662f\\u8bf7\\u5047\\u539f\\u56e0\\u8fd9\\u91cc\\u662f\\u8bf7\\u5047\\u539f\\u56e0\", \"filename\": \"\"}', 'laoshi', '2021-08-01 21:40:34.982263', '2021-08-01 21:40:34.982371', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (261, 250, 27, '', 1, 'laoshi', 1, '{\"id\": 250, \"creator\": \"laoshi\", \"gmt_created\": \"2021-08-01 21:43:22\", \"gmt_modified\": \"2021-08-01 21:43:22\", \"is_deleted\": false, \"title\": \"\\u6807\\u9898\", \"workflow_id\": 1, \"sn\": \"Test_202108010042\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"dsfsffsdf,fdsfds,test2,test1111,23424,aaaa,fewf,admin,test,laoshi,laoshia,3333\", \"relation\": \"dsfsffsdf,fdsfds,test2,test1111,23424,aaaa,fewf,admin,test,laoshi,laoshia,3333\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 21:43:00\", \"leave_end\": \"2021-08-02 00:00:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u5341\\u56db\\u8bf4\\u56db\\u5341\\u98d2\\u98d2\\u662f\", \"filename\": \"/media/upload/202108/11627825399282.png\"}', 'laoshi', '2021-08-01 21:43:22.508407', '2021-08-01 21:43:22.508431', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (262, 251, 27, '', 1, 'test', 1, '{\"id\": 251, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 21:53:58\", \"gmt_modified\": \"2021-08-01 21:53:58\", \"is_deleted\": false, \"title\": \"\\u8bf7\\u50471\", \"workflow_id\": 1, \"sn\": \"Test_202108010043\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 2, \"participant\": \"dsfsffsdf,fdsfds,test2,test1111,23424,aaaa,fewf,admin,test,laoshi,laoshia,3333\", \"relation\": \"fdsfds,test2,dsfsffsdf,test1111,23424,aaaa,fewf,admin,test,laoshi,laoshia,3333\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 21:53:00\", \"leave_end\": \"2021-08-02 00:00:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u8bf7\\u5047\\u539f\\u56e0\", \"filename\": \"/media/upload/202108/11627826036719.png\"}', 'test', '2021-08-01 21:53:58.938521', '2021-08-01 21:53:58.938551', 0, 0);
INSERT INTO `ticket_ticketflowlog` VALUES (263, 251, 0, '接单处理', 1, 'laoshi', 3, '{\"id\": 251, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 21:53:58\", \"gmt_modified\": \"2021-08-01 21:56:10\", \"is_deleted\": false, \"title\": \"\\u8bf7\\u50471\", \"workflow_id\": 1, \"sn\": \"Test_202108010043\", \"state_id\": 3, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"laoshi\", \"relation\": \"fdsfds,test2,dsfsffsdf,test1111,23424,aaaa,fewf,admin,test,laoshi,laoshia,3333\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 1, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 21:53:00\", \"leave_end\": \"2021-08-02 00:00:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u8bf7\\u5047\\u539f\\u56e0\", \"filename\": \"/media/upload/202108/11627826036719.png\"}', 'laoshi', '2021-08-01 21:56:10.880119', '2021-08-01 21:56:10.880151', 0, 4);
INSERT INTO `ticket_ticketflowlog` VALUES (264, 251, 28, '', 1, 'laoshi', 3, '{\"id\": 251, \"creator\": \"test\", \"gmt_created\": \"2021-08-01 21:53:58\", \"gmt_modified\": \"2021-08-01 21:56:10\", \"is_deleted\": false, \"title\": \"\\u8bf7\\u50471\", \"workflow_id\": 1, \"sn\": \"Test_202108010043\", \"state_id\": 5, \"parent_ticket_id\": 0, \"parent_ticket_state_id\": 0, \"participant_type_id\": 1, \"participant\": \"\", \"relation\": \"fdsfds,test2,dsfsffsdf,test1111,23424,aaaa,fewf,admin,test,laoshi,laoshia,3333\", \"in_add_node\": false, \"add_node_man\": \"\", \"script_run_last_result\": true, \"act_state_id\": 4, \"multi_all_person\": \"{}\", \"leave_start\": \"2021-08-01 21:53:00\", \"leave_end\": \"2021-08-02 00:00:00\", \"leave_type\": \"0\", \"datetime_field\": \"None\", \"attachment_field\": \"None\", \"days\": 1, \"text_desp\": \"\\u8bf7\\u5047\\u539f\\u56e0\", \"filename\": \"/media/upload/202108/11627826036719.png\"}', 'laoshi', '2021-08-01 21:56:10.971799', '2021-08-01 21:56:10.971837', 0, 0);

-- ----------------------------
-- Table structure for ticket_ticketrecord
-- ----------------------------
DROP TABLE IF EXISTS `ticket_ticketrecord`;
CREATE TABLE `ticket_ticketrecord`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `workflow_id` int(11) NOT NULL,
  `sn` varchar(25) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `state_id` int(11) NOT NULL,
  `parent_ticket_id` int(11) NOT NULL,
  `parent_ticket_state_id` int(11) NOT NULL,
  `participant_type_id` int(11) NOT NULL,
  `participant` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `creator` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `relation` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `add_node_man` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `in_add_node` tinyint(1) NOT NULL,
  `script_run_last_result` tinyint(1) NOT NULL,
  `act_state_id` int(11) NOT NULL DEFAULT 0 COMMENT '进行状态',
  `multi_all_person` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_creator`(`creator`) USING BTREE,
  INDEX `idx_created`(`gmt_created`) USING BTREE,
  INDEX `idx_act_state`(`act_state_id`) USING BTREE,
  INDEX `idx_workflow`(`workflow_id`) USING BTREE,
  INDEX `idx_sn`(`sn`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 252 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of ticket_ticketrecord
-- ----------------------------
INSERT INTO `ticket_ticketrecord` VALUES (251, '请假1', 1, 'Test_202108010043', 5, 0, 0, 1, '', 'test', '2021-08-01 21:53:58.858679', '2021-08-01 21:56:10.927270', 0, 'fdsfds,test2,dsfsffsdf,test1111,23424,aaaa,fewf,admin,test,laoshi,laoshia,3333', '', 0, 1, 4, '{}');

-- ----------------------------
-- Table structure for ticket_ticketuser
-- ----------------------------
DROP TABLE IF EXISTS `ticket_ticketuser`;
CREATE TABLE `ticket_ticketuser`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `creator` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '已删除',
  `username` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '用户名',
  `in_process` tinyint(1) NOT NULL DEFAULT 0 COMMENT '处理中',
  `worked` tinyint(1) NOT NULL DEFAULT 0 COMMENT '处理过的',
  `ticket_id` int(11) NOT NULL DEFAULT 0 COMMENT '工单id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_ticket_id`(`ticket_id`) USING BTREE,
  INDEX `idx_username_in_process`(`username`, `in_process`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1854 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of ticket_ticketuser
-- ----------------------------
INSERT INTO `ticket_ticketuser` VALUES (1, 'admin', '2018-05-13 22:24:42', '2018-05-13 22:24:42', 0, 'lileilileilileilileilileilileilileilileilileilileilileilileilileilileilileilileilileililei', 0, 0, 14);
INSERT INTO `ticket_ticketuser` VALUES (2, 'admin', '2018-05-13 22:28:22', '2018-05-13 22:28:22', 0, 'lileilileililei', 0, 0, 15);
INSERT INTO `ticket_ticketuser` VALUES (3, 'admin', '2018-05-13 22:34:13', '2020-03-29 09:38:20', 0, 'lilei', 1, 0, 16);
INSERT INTO `ticket_ticketuser` VALUES (4, 'admin', '2018-05-15 07:16:38', '2020-03-29 09:41:07', 0, 'guiji', 0, 1, 17);
INSERT INTO `ticket_ticketuser` VALUES (5, 'admin', '2018-05-15 07:16:38', '2018-05-15 07:16:38', 0, 'wangwu', 0, 0, 17);
INSERT INTO `ticket_ticketuser` VALUES (6, 'admin', '2018-05-15 07:16:38', '2018-05-15 07:16:38', 0, 'lilei', 0, 0, 17);
INSERT INTO `ticket_ticketuser` VALUES (7, 'admin', '2018-05-15 07:37:28', '2018-05-15 07:37:28', 0, 'lilei', 0, 0, 18);
INSERT INTO `ticket_ticketuser` VALUES (8, 'admin', '2018-05-15 07:37:28', '2020-03-29 09:38:20', 0, 'guiji', 1, 0, 18);
INSERT INTO `ticket_ticketuser` VALUES (9, 'admin', '2018-05-15 07:37:28', '2020-03-29 09:38:20', 0, 'wangwu', 1, 0, 18);
INSERT INTO `ticket_ticketuser` VALUES (10, 'admin', '2018-10-19 00:08:40', '2020-03-29 09:41:07', 0, 'jack', 0, 1, 19);
INSERT INTO `ticket_ticketuser` VALUES (11, 'admin', '2018-10-19 00:08:40', '2018-10-19 00:08:40', 0, 'admin', 0, 0, 19);
INSERT INTO `ticket_ticketuser` VALUES (12, 'admin', '2018-10-19 00:38:41', '2020-03-29 09:38:20', 0, 'jack', 1, 0, 20);
INSERT INTO `ticket_ticketuser` VALUES (13, 'admin', '2018-10-19 00:38:41', '2018-10-19 00:38:41', 0, 'admin', 0, 0, 20);
INSERT INTO `ticket_ticketuser` VALUES (14, 'admin', '2018-10-22 07:12:16', '2020-03-29 09:38:20', 0, 'jack', 1, 0, 22);
INSERT INTO `ticket_ticketuser` VALUES (15, 'admin', '2018-10-22 08:05:37', '2020-03-29 09:38:20', 0, 'jack', 1, 0, 23);
INSERT INTO `ticket_ticketuser` VALUES (16, 'admin', '2018-11-27 07:09:06', '2020-03-29 09:38:20', 0, 'admin', 1, 0, 24);
INSERT INTO `ticket_ticketuser` VALUES (17, 'admin', '2018-11-27 07:12:28', '2018-11-27 07:12:28', 0, 'guiji', 0, 0, 25);
INSERT INTO `ticket_ticketuser` VALUES (18, 'admin', '2018-11-27 07:12:28', '2018-11-27 07:12:28', 0, 'admin', 0, 0, 25);
INSERT INTO `ticket_ticketuser` VALUES (19, 'admin', '2018-11-27 07:12:28', '2018-11-27 07:12:28', 0, 'lilei', 0, 0, 25);
INSERT INTO `ticket_ticketuser` VALUES (20, 'admin', '2018-11-27 07:12:28', '2018-11-27 07:12:28', 0, 'zhangsan', 0, 0, 25);
INSERT INTO `ticket_ticketuser` VALUES (21, 'admin', '2018-11-27 07:14:06', '2018-11-27 07:14:06', 0, 'lilei', 0, 0, 26);
INSERT INTO `ticket_ticketuser` VALUES (22, 'admin', '2018-11-27 07:14:06', '2018-11-27 07:14:06', 0, 'admin', 0, 0, 26);
INSERT INTO `ticket_ticketuser` VALUES (23, 'admin', '2018-11-27 07:14:06', '2018-11-27 07:14:06', 0, 'zhangsan', 0, 0, 26);
INSERT INTO `ticket_ticketuser` VALUES (24, 'admin', '2018-11-27 07:14:06', '2018-11-27 07:14:06', 0, 'guiji', 0, 0, 26);
INSERT INTO `ticket_ticketuser` VALUES (25, 'admin', '2018-11-27 07:20:16', '2018-11-27 07:20:16', 0, 'admin', 0, 0, 27);
INSERT INTO `ticket_ticketuser` VALUES (26, 'admin', '2018-11-27 07:20:16', '2018-11-27 07:20:16', 0, 'zhangsan', 0, 0, 27);
INSERT INTO `ticket_ticketuser` VALUES (27, 'admin', '2018-11-27 07:20:16', '2018-11-27 07:20:16', 0, 'lilei', 0, 0, 27);
INSERT INTO `ticket_ticketuser` VALUES (28, 'admin', '2018-11-27 07:20:16', '2018-11-27 07:20:16', 0, 'guiji', 0, 0, 27);
INSERT INTO `ticket_ticketuser` VALUES (29, 'admin', '2018-11-27 07:21:00', '2018-11-27 07:21:00', 0, 'admin', 0, 0, 28);
INSERT INTO `ticket_ticketuser` VALUES (30, 'admin', '2018-11-27 07:23:04', '2018-11-27 07:23:04', 0, 'admin', 0, 0, 29);
INSERT INTO `ticket_ticketuser` VALUES (31, 'admin', '2018-11-27 07:23:04', '2020-03-29 09:39:34', 0, 'zhangsan', 1, 0, 29);
INSERT INTO `ticket_ticketuser` VALUES (32, 'admin', '2018-11-27 07:23:48', '2020-03-29 09:39:34', 0, 'zhangsan', 1, 0, 30);
INSERT INTO `ticket_ticketuser` VALUES (33, 'admin', '2018-11-27 07:23:48', '2018-11-27 07:23:48', 0, 'admin', 0, 0, 30);
INSERT INTO `ticket_ticketuser` VALUES (34, 'admin', '2018-11-27 07:24:08', '2020-03-29 09:39:34', 0, 'zhangsan', 1, 0, 31);
INSERT INTO `ticket_ticketuser` VALUES (35, 'admin', '2018-11-27 07:24:08', '2018-11-27 07:24:08', 0, 'admin', 0, 0, 31);
INSERT INTO `ticket_ticketuser` VALUES (36, 'admin', '2018-11-27 07:24:31', '2018-11-27 07:24:31', 0, 'admin', 0, 0, 32);
INSERT INTO `ticket_ticketuser` VALUES (37, 'admin', '2018-11-27 07:24:31', '2020-03-29 09:39:34', 0, 'guiji', 1, 0, 32);
INSERT INTO `ticket_ticketuser` VALUES (38, 'admin', '2018-11-27 07:27:39', '2020-03-29 09:39:34', 0, 'lilei', 1, 0, 33);
INSERT INTO `ticket_ticketuser` VALUES (39, 'admin', '2018-11-27 07:27:39', '2018-11-27 07:27:39', 0, 'admin', 0, 0, 33);
INSERT INTO `ticket_ticketuser` VALUES (40, 'admin', '2019-11-24 10:23:07', '2019-11-24 10:23:07', 0, 'admin', 0, 0, 34);
INSERT INTO `ticket_ticketuser` VALUES (41, '', '2020-03-29 09:47:27', '2020-03-29 09:47:27', 0, 'lilei', 1, 0, 35);
INSERT INTO `ticket_ticketuser` VALUES (42, '', '2020-04-11 10:40:31', '2020-04-11 10:40:30', 0, 'admin', 1, 0, 36);
INSERT INTO `ticket_ticketuser` VALUES (43, '', '2020-05-01 09:19:29', '2020-05-01 09:19:48', 0, 'admin', 0, 0, 37);
INSERT INTO `ticket_ticketuser` VALUES (44, '', '2020-05-01 09:21:57', '2020-05-01 09:22:31', 0, 'admin', 0, 0, 38);
INSERT INTO `ticket_ticketuser` VALUES (45, '', '2020-05-07 22:42:17', '2020-05-07 22:42:17', 0, 'admin', 0, 0, 39);
INSERT INTO `ticket_ticketuser` VALUES (46, '', '2020-05-07 22:42:17', '2020-05-07 22:42:17', 0, 'zhangsan', 1, 0, 39);
INSERT INTO `ticket_ticketuser` VALUES (47, '', '2020-05-07 22:42:17', '2020-05-07 22:42:17', 0, 'lisi', 1, 0, 39);
INSERT INTO `ticket_ticketuser` VALUES (48, '', '2020-05-07 22:54:59', '2020-05-07 22:55:09', 0, 'zhangsan', 0, 1, 40);
INSERT INTO `ticket_ticketuser` VALUES (49, '', '2020-05-07 22:54:59', '2020-05-07 22:54:59', 0, 'admin', 1, 0, 40);
INSERT INTO `ticket_ticketuser` VALUES (50, '', '2020-05-17 17:31:54', '2020-05-17 17:38:51', 0, 'admin', 1, 1, 41);
INSERT INTO `ticket_ticketuser` VALUES (51, '', '2020-05-17 17:31:54', '2020-05-17 17:38:51', 0, 'zhangsan', 0, 1, 41);
INSERT INTO `ticket_ticketuser` VALUES (52, '', '2020-05-17 17:44:45', '2020-05-17 17:44:52', 0, 'zhangsan', 0, 1, 42);
INSERT INTO `ticket_ticketuser` VALUES (53, '', '2020-05-17 17:44:45', '2020-05-17 17:45:34', 0, 'admin', 0, 1, 42);
INSERT INTO `ticket_ticketuser` VALUES (54, '', '2020-05-17 17:45:35', '2020-05-17 17:45:35', 0, 'guiji', 1, 0, 42);
INSERT INTO `ticket_ticketuser` VALUES (55, '', '2020-05-17 17:45:35', '2020-05-17 17:45:35', 0, 'wangwu', 1, 0, 42);
INSERT INTO `ticket_ticketuser` VALUES (56, '', '2020-05-18 23:18:16', '2020-05-18 23:18:30', 0, 'admin', 0, 1, 43);
INSERT INTO `ticket_ticketuser` VALUES (57, '', '2020-05-18 23:18:16', '2020-05-18 23:18:16', 0, 'zhangsan', 1, 0, 43);
INSERT INTO `ticket_ticketuser` VALUES (58, '', '2020-08-21 10:39:33', '2020-08-21 10:39:32', 0, 'admin', 1, 0, 44);
INSERT INTO `ticket_ticketuser` VALUES (59, '', '2020-08-21 10:39:33', '2020-08-21 10:39:33', 0, 'zhangsan', 1, 0, 44);
INSERT INTO `ticket_ticketuser` VALUES (60, '', '2020-08-21 18:33:35', '2020-08-21 18:33:35', 0, 'admin', 0, 0, 45);
INSERT INTO `ticket_ticketuser` VALUES (61, '', '2020-08-21 18:33:35', '2020-08-21 18:33:35', 0, 'lisi', 1, 0, 45);
INSERT INTO `ticket_ticketuser` VALUES (62, '', '2020-08-21 18:33:35', '2020-08-21 18:33:35', 0, 'zhangsan', 1, 0, 45);
INSERT INTO `ticket_ticketuser` VALUES (63, '', '2020-08-21 18:42:06', '2020-08-21 18:42:06', 0, 'admin', 0, 0, 46);
INSERT INTO `ticket_ticketuser` VALUES (64, '', '2020-08-21 18:42:06', '2020-08-21 18:42:06', 0, 'lisi', 1, 0, 46);
INSERT INTO `ticket_ticketuser` VALUES (65, '', '2020-08-21 18:42:06', '2020-08-21 18:42:06', 0, 'zhangsan', 1, 0, 46);
INSERT INTO `ticket_ticketuser` VALUES (66, '', '2020-08-22 08:46:20', '2020-08-22 08:46:19', 0, 'admin', 1, 0, 47);
INSERT INTO `ticket_ticketuser` VALUES (67, '', '2020-08-22 08:46:20', '2020-08-22 08:46:20', 0, 'zhangsan', 1, 0, 47);
INSERT INTO `ticket_ticketuser` VALUES (68, '', '2021-07-30 19:34:44', '2021-07-30 19:34:44', 0, 'test', 0, 0, 48);
INSERT INTO `ticket_ticketuser` VALUES (69, '', '2021-07-30 19:34:44', '2021-07-30 19:37:20', 0, 'zhangsan', 0, 0, 48);
INSERT INTO `ticket_ticketuser` VALUES (70, '', '2021-07-30 19:34:44', '2021-07-30 19:37:20', 0, 'lisi', 0, 0, 48);
INSERT INTO `ticket_ticketuser` VALUES (71, '', '2021-07-30 19:37:21', '2021-07-30 19:37:21', 0, '', 1, 0, 48);
INSERT INTO `ticket_ticketuser` VALUES (72, '', '2021-07-30 19:40:52', '2021-07-30 19:40:52', 0, 'test', 0, 0, 49);
INSERT INTO `ticket_ticketuser` VALUES (73, '', '2021-07-30 19:40:52', '2021-07-30 19:40:52', 0, 'zhangsan', 1, 0, 49);
INSERT INTO `ticket_ticketuser` VALUES (74, '', '2021-07-30 19:40:52', '2021-07-30 19:40:52', 0, 'lisi', 1, 0, 49);
INSERT INTO `ticket_ticketuser` VALUES (75, '', '2021-07-30 19:48:52', '2021-07-30 19:48:52', 0, 'test', 0, 0, 50);
INSERT INTO `ticket_ticketuser` VALUES (76, '', '2021-07-30 19:48:52', '2021-07-30 19:48:52', 0, 'zhangsan', 1, 0, 50);
INSERT INTO `ticket_ticketuser` VALUES (77, '', '2021-07-30 19:48:52', '2021-07-30 19:48:52', 0, 'lisi', 1, 0, 50);
INSERT INTO `ticket_ticketuser` VALUES (78, '', '2021-07-30 19:58:56', '2021-07-30 19:58:56', 0, 'test', 0, 0, 51);
INSERT INTO `ticket_ticketuser` VALUES (79, '', '2021-07-30 19:58:56', '2021-07-30 19:58:56', 0, '', 1, 0, 51);
INSERT INTO `ticket_ticketuser` VALUES (80, '', '2021-07-30 20:09:49', '2021-07-30 20:09:49', 0, 'test', 0, 0, 52);
INSERT INTO `ticket_ticketuser` VALUES (81, '', '2021-07-30 20:09:49', '2021-07-30 20:09:49', 0, '', 1, 0, 52);
INSERT INTO `ticket_ticketuser` VALUES (82, '', '2021-07-30 20:44:10', '2021-07-30 20:44:10', 0, 'test', 0, 0, 53);
INSERT INTO `ticket_ticketuser` VALUES (83, '', '2021-07-30 20:44:10', '2021-07-30 20:44:10', 0, '', 1, 0, 53);
INSERT INTO `ticket_ticketuser` VALUES (84, '', '2021-07-30 20:47:55', '2021-07-30 20:47:55', 0, 'test', 0, 0, 54);
INSERT INTO `ticket_ticketuser` VALUES (85, '', '2021-07-30 20:47:55', '2021-07-30 20:47:55', 0, '', 1, 0, 54);
INSERT INTO `ticket_ticketuser` VALUES (86, '', '2021-07-30 20:48:26', '2021-07-30 20:48:26', 0, 'test', 0, 0, 55);
INSERT INTO `ticket_ticketuser` VALUES (87, '', '2021-07-30 20:48:26', '2021-07-30 20:48:26', 0, '', 1, 0, 55);
INSERT INTO `ticket_ticketuser` VALUES (88, '', '2021-07-30 20:59:24', '2021-07-30 20:59:24', 0, 'test', 0, 0, 56);
INSERT INTO `ticket_ticketuser` VALUES (89, '', '2021-07-30 20:59:24', '2021-07-30 20:59:24', 0, 'admin', 1, 0, 56);
INSERT INTO `ticket_ticketuser` VALUES (90, '', '2021-07-30 20:59:24', '2021-07-30 20:59:24', 0, 'zhangsan', 1, 0, 56);
INSERT INTO `ticket_ticketuser` VALUES (91, '', '2021-07-30 20:59:53', '2021-07-30 20:59:53', 0, 'admin', 1, 0, 57);
INSERT INTO `ticket_ticketuser` VALUES (92, '', '2021-07-30 20:59:53', '2021-07-30 20:59:53', 0, 'zhangsan', 1, 0, 57);
INSERT INTO `ticket_ticketuser` VALUES (93, '', '2021-07-30 21:02:06', '2021-07-30 21:02:05', 0, 'admin', 1, 0, 58);
INSERT INTO `ticket_ticketuser` VALUES (94, '', '2021-07-30 21:02:06', '2021-07-30 21:02:06', 0, 'zhangsan', 1, 0, 58);
INSERT INTO `ticket_ticketuser` VALUES (95, '', '2021-07-30 21:03:36', '2021-07-30 21:03:36', 0, 'test', 0, 0, 59);
INSERT INTO `ticket_ticketuser` VALUES (96, '', '2021-07-30 21:03:36', '2021-07-30 21:03:36', 0, '', 1, 0, 59);
INSERT INTO `ticket_ticketuser` VALUES (97, '', '2021-07-30 21:08:43', '2021-07-30 21:08:43', 0, 'admin', 0, 0, 60);
INSERT INTO `ticket_ticketuser` VALUES (98, '', '2021-07-30 21:08:43', '2021-07-30 21:08:43', 0, '', 1, 0, 60);
INSERT INTO `ticket_ticketuser` VALUES (99, '', '2021-07-30 21:28:22', '2021-07-30 21:28:22', 0, 'admin', 0, 0, 61);
INSERT INTO `ticket_ticketuser` VALUES (100, '', '2021-07-30 21:28:22', '2021-07-30 21:28:22', 0, '', 1, 0, 61);
INSERT INTO `ticket_ticketuser` VALUES (101, '', '2021-07-30 21:28:38', '2021-07-30 21:28:38', 0, 'admin', 0, 0, 62);
INSERT INTO `ticket_ticketuser` VALUES (102, '', '2021-07-30 21:28:38', '2021-07-30 21:28:38', 0, '', 1, 0, 62);
INSERT INTO `ticket_ticketuser` VALUES (103, '', '2021-07-30 21:33:27', '2021-07-30 21:33:27', 0, 'admin', 0, 0, 63);
INSERT INTO `ticket_ticketuser` VALUES (104, '', '2021-07-30 21:33:27', '2021-07-30 21:33:27', 0, '', 1, 0, 63);
INSERT INTO `ticket_ticketuser` VALUES (105, '', '2021-07-30 21:36:32', '2021-07-30 21:36:32', 0, 'admin', 0, 0, 64);
INSERT INTO `ticket_ticketuser` VALUES (106, '', '2021-07-30 21:36:32', '2021-07-30 21:36:32', 0, '', 1, 0, 64);
INSERT INTO `ticket_ticketuser` VALUES (107, '', '2021-07-30 21:36:45', '2021-07-30 21:36:45', 0, 'admin', 0, 0, 65);
INSERT INTO `ticket_ticketuser` VALUES (108, '', '2021-07-30 21:36:45', '2021-07-30 21:36:45', 0, '', 1, 0, 65);
INSERT INTO `ticket_ticketuser` VALUES (109, '', '2021-07-30 21:37:44', '2021-07-30 21:37:44', 0, 'admin', 0, 0, 66);
INSERT INTO `ticket_ticketuser` VALUES (110, '', '2021-07-30 21:37:44', '2021-07-30 21:37:44', 0, '', 1, 0, 66);
INSERT INTO `ticket_ticketuser` VALUES (111, '', '2021-07-30 21:40:00', '2021-07-30 21:40:00', 0, 'admin', 0, 0, 67);
INSERT INTO `ticket_ticketuser` VALUES (112, '', '2021-07-30 21:40:00', '2021-07-30 21:40:00', 0, '', 1, 0, 67);
INSERT INTO `ticket_ticketuser` VALUES (113, '', '2021-07-30 21:40:19', '2021-07-30 21:40:19', 0, 'admin', 0, 0, 68);
INSERT INTO `ticket_ticketuser` VALUES (114, '', '2021-07-30 21:40:19', '2021-07-30 21:40:19', 0, '', 1, 0, 68);
INSERT INTO `ticket_ticketuser` VALUES (115, '', '2021-07-30 21:40:20', '2021-07-30 21:40:20', 0, 'admin', 0, 0, 69);
INSERT INTO `ticket_ticketuser` VALUES (116, '', '2021-07-30 21:40:20', '2021-07-30 21:40:20', 0, '', 1, 0, 69);
INSERT INTO `ticket_ticketuser` VALUES (117, '', '2021-07-30 21:40:30', '2021-07-30 21:40:30', 0, 'admin', 0, 0, 70);
INSERT INTO `ticket_ticketuser` VALUES (118, '', '2021-07-30 21:40:30', '2021-07-30 21:40:30', 0, '', 1, 0, 70);
INSERT INTO `ticket_ticketuser` VALUES (119, '', '2021-07-30 21:40:33', '2021-07-30 21:40:33', 0, 'admin', 0, 0, 71);
INSERT INTO `ticket_ticketuser` VALUES (120, '', '2021-07-30 21:40:33', '2021-07-30 21:40:33', 0, '', 1, 0, 71);
INSERT INTO `ticket_ticketuser` VALUES (121, '', '2021-07-30 21:40:55', '2021-07-30 21:40:55', 0, 'admin', 0, 0, 72);
INSERT INTO `ticket_ticketuser` VALUES (122, '', '2021-07-30 21:40:55', '2021-07-30 21:40:55', 0, '', 1, 0, 72);
INSERT INTO `ticket_ticketuser` VALUES (123, '', '2021-07-30 21:41:07', '2021-07-30 21:41:07', 0, 'admin', 0, 0, 73);
INSERT INTO `ticket_ticketuser` VALUES (124, '', '2021-07-30 21:41:07', '2021-07-30 21:41:07', 0, '', 1, 0, 73);
INSERT INTO `ticket_ticketuser` VALUES (125, '', '2021-07-30 21:43:52', '2021-07-30 21:43:52', 0, 'admin', 0, 0, 74);
INSERT INTO `ticket_ticketuser` VALUES (126, '', '2021-07-30 21:43:52', '2021-07-30 21:43:52', 0, '', 1, 0, 74);
INSERT INTO `ticket_ticketuser` VALUES (127, '', '2021-07-30 21:45:55', '2021-07-30 21:45:55', 0, 'admin', 0, 0, 75);
INSERT INTO `ticket_ticketuser` VALUES (128, '', '2021-07-30 21:45:55', '2021-07-30 21:45:55', 0, '', 1, 0, 75);
INSERT INTO `ticket_ticketuser` VALUES (129, '', '2021-07-30 21:46:29', '2021-07-30 21:46:29', 0, 'admin', 0, 0, 76);
INSERT INTO `ticket_ticketuser` VALUES (130, '', '2021-07-30 21:46:29', '2021-07-30 21:46:29', 0, '', 1, 0, 76);
INSERT INTO `ticket_ticketuser` VALUES (131, '', '2021-07-30 21:47:13', '2021-07-30 21:47:13', 0, 'admin', 0, 0, 77);
INSERT INTO `ticket_ticketuser` VALUES (132, '', '2021-07-30 21:47:13', '2021-07-30 21:47:13', 0, '', 1, 0, 77);
INSERT INTO `ticket_ticketuser` VALUES (133, '', '2021-07-30 21:47:23', '2021-07-30 21:47:23', 0, 'admin', 0, 0, 78);
INSERT INTO `ticket_ticketuser` VALUES (134, '', '2021-07-30 21:47:23', '2021-07-30 21:47:23', 0, '', 1, 0, 78);
INSERT INTO `ticket_ticketuser` VALUES (135, '', '2021-07-30 21:49:38', '2021-07-30 21:49:38', 0, 'admin', 0, 0, 79);
INSERT INTO `ticket_ticketuser` VALUES (136, '', '2021-07-30 21:49:38', '2021-07-30 21:49:38', 0, '', 1, 0, 79);
INSERT INTO `ticket_ticketuser` VALUES (137, '', '2021-07-30 21:49:42', '2021-07-30 21:49:42', 0, 'admin', 0, 0, 80);
INSERT INTO `ticket_ticketuser` VALUES (138, '', '2021-07-30 21:49:42', '2021-07-30 21:49:42', 0, '', 1, 0, 80);
INSERT INTO `ticket_ticketuser` VALUES (139, '', '2021-07-30 21:51:07', '2021-07-30 21:51:07', 0, 'admin', 0, 0, 81);
INSERT INTO `ticket_ticketuser` VALUES (140, '', '2021-07-30 21:51:07', '2021-07-30 21:51:07', 0, '', 1, 0, 81);
INSERT INTO `ticket_ticketuser` VALUES (141, '', '2021-07-30 21:52:18', '2021-07-30 21:52:18', 0, 'admin', 0, 0, 82);
INSERT INTO `ticket_ticketuser` VALUES (142, '', '2021-07-30 21:52:18', '2021-07-30 21:52:18', 0, '', 1, 0, 82);
INSERT INTO `ticket_ticketuser` VALUES (143, '', '2021-07-30 21:52:20', '2021-07-30 21:52:20', 0, 'admin', 0, 0, 83);
INSERT INTO `ticket_ticketuser` VALUES (144, '', '2021-07-30 21:52:20', '2021-07-30 21:52:20', 0, '', 1, 0, 83);
INSERT INTO `ticket_ticketuser` VALUES (145, '', '2021-07-30 21:52:20', '2021-07-30 21:52:20', 0, 'admin', 0, 0, 84);
INSERT INTO `ticket_ticketuser` VALUES (146, '', '2021-07-30 21:52:20', '2021-07-30 21:52:20', 0, '', 1, 0, 84);
INSERT INTO `ticket_ticketuser` VALUES (147, '', '2021-07-30 21:52:20', '2021-07-30 21:52:20', 0, 'admin', 0, 0, 85);
INSERT INTO `ticket_ticketuser` VALUES (148, '', '2021-07-30 21:52:20', '2021-07-30 21:52:20', 0, '', 1, 0, 85);
INSERT INTO `ticket_ticketuser` VALUES (149, '', '2021-07-30 21:52:21', '2021-07-30 21:52:21', 0, 'admin', 0, 0, 86);
INSERT INTO `ticket_ticketuser` VALUES (150, '', '2021-07-30 21:52:21', '2021-07-30 21:52:21', 0, '', 1, 0, 86);
INSERT INTO `ticket_ticketuser` VALUES (151, '', '2021-07-30 21:53:39', '2021-07-30 21:53:39', 0, 'admin', 0, 0, 87);
INSERT INTO `ticket_ticketuser` VALUES (152, '', '2021-07-30 21:53:39', '2021-07-30 21:53:39', 0, '', 1, 0, 87);
INSERT INTO `ticket_ticketuser` VALUES (153, '', '2021-07-30 21:53:42', '2021-07-30 21:53:42', 0, 'admin', 0, 0, 88);
INSERT INTO `ticket_ticketuser` VALUES (154, '', '2021-07-30 21:53:42', '2021-07-30 21:53:42', 0, '', 1, 0, 88);
INSERT INTO `ticket_ticketuser` VALUES (155, '', '2021-07-30 22:01:29', '2021-07-30 22:01:29', 0, 'admin', 0, 0, 89);
INSERT INTO `ticket_ticketuser` VALUES (156, '', '2021-07-30 22:01:29', '2021-07-30 22:01:29', 0, '', 1, 0, 89);
INSERT INTO `ticket_ticketuser` VALUES (157, '', '2021-07-30 22:06:37', '2021-07-30 22:06:37', 0, 'admin', 0, 0, 90);
INSERT INTO `ticket_ticketuser` VALUES (158, '', '2021-07-30 22:06:37', '2021-07-30 22:06:37', 0, '', 1, 0, 90);
INSERT INTO `ticket_ticketuser` VALUES (159, '', '2021-07-30 22:08:22', '2021-07-30 22:08:22', 0, 'test', 0, 0, 91);
INSERT INTO `ticket_ticketuser` VALUES (160, '', '2021-07-30 22:08:22', '2021-07-30 22:08:22', 0, '', 1, 0, 91);
INSERT INTO `ticket_ticketuser` VALUES (161, '', '2021-07-30 22:43:46', '2021-07-30 22:43:46', 0, 'test', 0, 0, 92);
INSERT INTO `ticket_ticketuser` VALUES (162, '', '2021-07-30 22:43:46', '2021-07-30 22:43:46', 0, '', 1, 0, 92);
INSERT INTO `ticket_ticketuser` VALUES (163, '', '2021-07-30 22:43:54', '2021-07-30 22:43:54', 0, 'test', 0, 0, 93);
INSERT INTO `ticket_ticketuser` VALUES (164, '', '2021-07-30 22:43:54', '2021-07-30 22:43:54', 0, '', 1, 0, 93);
INSERT INTO `ticket_ticketuser` VALUES (165, '', '2021-07-30 22:44:30', '2021-07-30 22:44:30', 0, 'test2', 0, 0, 94);
INSERT INTO `ticket_ticketuser` VALUES (166, '', '2021-07-30 22:44:30', '2021-07-31 18:46:41', 0, '', 0, 0, 94);
INSERT INTO `ticket_ticketuser` VALUES (167, '', '2021-07-31 10:02:45', '2021-07-31 10:02:45', 0, 'admin', 0, 0, 95);
INSERT INTO `ticket_ticketuser` VALUES (168, '', '2021-07-31 10:02:45', '2021-07-31 10:02:45', 0, '', 1, 0, 95);
INSERT INTO `ticket_ticketuser` VALUES (169, '', '2021-07-31 10:03:11', '2021-07-31 10:03:11', 0, 'admin', 0, 0, 96);
INSERT INTO `ticket_ticketuser` VALUES (170, '', '2021-07-31 10:03:11', '2021-07-31 10:03:11', 0, '', 1, 0, 96);
INSERT INTO `ticket_ticketuser` VALUES (171, '', '2021-07-31 10:03:40', '2021-07-31 10:03:40', 0, 'admin', 0, 0, 97);
INSERT INTO `ticket_ticketuser` VALUES (172, '', '2021-07-31 10:03:40', '2021-07-31 10:03:40', 0, '', 1, 0, 97);
INSERT INTO `ticket_ticketuser` VALUES (173, '', '2021-07-31 10:10:30', '2021-07-31 10:10:30', 0, 'admin', 0, 0, 98);
INSERT INTO `ticket_ticketuser` VALUES (174, '', '2021-07-31 10:10:30', '2021-07-31 10:10:30', 0, '', 1, 0, 98);
INSERT INTO `ticket_ticketuser` VALUES (175, '', '2021-07-31 10:10:40', '2021-07-31 10:10:40', 0, 'admin', 0, 0, 99);
INSERT INTO `ticket_ticketuser` VALUES (176, '', '2021-07-31 10:10:40', '2021-07-31 10:10:40', 0, '', 1, 0, 99);
INSERT INTO `ticket_ticketuser` VALUES (177, '', '2021-07-31 10:11:38', '2021-07-31 10:11:38', 0, 'test', 0, 0, 100);
INSERT INTO `ticket_ticketuser` VALUES (178, '', '2021-07-31 10:11:38', '2021-07-31 12:29:50', 0, '', 1, 0, 100);
INSERT INTO `ticket_ticketuser` VALUES (179, '', '2021-07-31 10:44:57', '2021-07-31 10:44:57', 0, 'test', 0, 0, 101);
INSERT INTO `ticket_ticketuser` VALUES (180, '', '2021-07-31 10:44:57', '2021-07-31 10:44:57', 0, '', 1, 0, 101);
INSERT INTO `ticket_ticketuser` VALUES (181, '', '2021-07-31 10:45:20', '2021-07-31 10:45:20', 0, 'test', 0, 0, 102);
INSERT INTO `ticket_ticketuser` VALUES (182, '', '2021-07-31 10:45:20', '2021-07-31 10:45:20', 0, '', 1, 0, 102);
INSERT INTO `ticket_ticketuser` VALUES (183, '', '2021-07-31 10:45:27', '2021-07-31 10:45:27', 0, 'test', 0, 0, 103);
INSERT INTO `ticket_ticketuser` VALUES (184, '', '2021-07-31 10:45:27', '2021-07-31 10:45:27', 0, '', 1, 0, 103);
INSERT INTO `ticket_ticketuser` VALUES (185, '', '2021-07-31 10:47:10', '2021-07-31 10:47:10', 0, 'test', 0, 0, 104);
INSERT INTO `ticket_ticketuser` VALUES (186, '', '2021-07-31 10:47:10', '2021-07-31 10:47:10', 0, '', 1, 0, 104);
INSERT INTO `ticket_ticketuser` VALUES (187, '', '2021-07-31 10:48:34', '2021-07-31 10:48:34', 0, 'test', 0, 0, 105);
INSERT INTO `ticket_ticketuser` VALUES (188, '', '2021-07-31 10:48:34', '2021-07-31 10:48:34', 0, '', 1, 0, 105);
INSERT INTO `ticket_ticketuser` VALUES (189, '', '2021-07-31 10:48:41', '2021-07-31 10:48:41', 0, 'test', 0, 0, 106);
INSERT INTO `ticket_ticketuser` VALUES (190, '', '2021-07-31 10:48:41', '2021-07-31 10:48:41', 0, '', 1, 0, 106);
INSERT INTO `ticket_ticketuser` VALUES (191, '', '2021-07-31 10:50:43', '2021-07-31 10:50:43', 0, 'test', 0, 0, 107);
INSERT INTO `ticket_ticketuser` VALUES (192, '', '2021-07-31 10:50:43', '2021-07-31 10:50:43', 0, '', 1, 0, 107);
INSERT INTO `ticket_ticketuser` VALUES (193, '', '2021-07-31 10:52:16', '2021-07-31 10:52:16', 0, 'test', 0, 0, 108);
INSERT INTO `ticket_ticketuser` VALUES (194, '', '2021-07-31 10:52:16', '2021-07-31 10:52:16', 0, '', 1, 0, 108);
INSERT INTO `ticket_ticketuser` VALUES (195, '', '2021-07-31 11:09:03', '2021-07-31 11:09:03', 0, 'admin', 0, 0, 109);
INSERT INTO `ticket_ticketuser` VALUES (196, '', '2021-07-31 11:09:03', '2021-07-31 11:09:03', 0, '', 1, 0, 109);
INSERT INTO `ticket_ticketuser` VALUES (197, '', '2021-07-31 11:09:28', '2021-07-31 11:09:28', 0, 'admin', 0, 0, 110);
INSERT INTO `ticket_ticketuser` VALUES (198, '', '2021-07-31 11:09:28', '2021-07-31 11:09:28', 0, '', 1, 0, 110);
INSERT INTO `ticket_ticketuser` VALUES (199, '', '2021-07-31 11:09:46', '2021-07-31 11:09:46', 0, 'admin', 0, 0, 111);
INSERT INTO `ticket_ticketuser` VALUES (200, '', '2021-07-31 11:09:46', '2021-07-31 11:09:46', 0, '', 1, 0, 111);
INSERT INTO `ticket_ticketuser` VALUES (201, '', '2021-07-31 11:11:40', '2021-07-31 11:11:40', 0, 'admin', 0, 0, 112);
INSERT INTO `ticket_ticketuser` VALUES (202, '', '2021-07-31 11:11:40', '2021-07-31 11:11:40', 0, '', 1, 0, 112);
INSERT INTO `ticket_ticketuser` VALUES (203, '', '2021-07-31 11:12:18', '2021-07-31 11:12:18', 0, 'admin', 0, 0, 113);
INSERT INTO `ticket_ticketuser` VALUES (204, '', '2021-07-31 11:12:18', '2021-07-31 11:12:18', 0, '', 1, 0, 113);
INSERT INTO `ticket_ticketuser` VALUES (205, '', '2021-07-31 11:30:50', '2021-07-31 12:29:50', 0, 'admin', 0, 0, 100);
INSERT INTO `ticket_ticketuser` VALUES (206, '', '2021-07-31 11:43:56', '2021-07-31 15:15:19', 0, 'test', 0, 0, 114);
INSERT INTO `ticket_ticketuser` VALUES (207, '', '2021-07-31 11:43:56', '2021-07-31 15:15:19', 0, '23424', 0, 0, 114);
INSERT INTO `ticket_ticketuser` VALUES (208, '', '2021-07-31 11:43:56', '2021-07-31 15:15:53', 0, 'laoshi', 1, 1, 114);
INSERT INTO `ticket_ticketuser` VALUES (209, '', '2021-07-31 11:43:56', '2021-07-31 15:15:19', 0, 'fdsfds', 0, 0, 114);
INSERT INTO `ticket_ticketuser` VALUES (210, '', '2021-07-31 11:43:56', '2021-07-31 15:15:19', 0, 'test2', 0, 0, 114);
INSERT INTO `ticket_ticketuser` VALUES (211, '', '2021-07-31 11:43:56', '2021-07-31 15:15:19', 0, 'test1111', 0, 0, 114);
INSERT INTO `ticket_ticketuser` VALUES (212, '', '2021-07-31 11:43:56', '2021-07-31 15:15:19', 0, 'laoshia', 0, 0, 114);
INSERT INTO `ticket_ticketuser` VALUES (213, '', '2021-07-31 11:43:56', '2021-07-31 15:15:19', 0, '3333', 0, 0, 114);
INSERT INTO `ticket_ticketuser` VALUES (214, '', '2021-07-31 11:43:56', '2021-07-31 15:15:19', 0, 'dsfsffsdf', 0, 0, 114);
INSERT INTO `ticket_ticketuser` VALUES (215, '', '2021-07-31 11:43:56', '2021-07-31 15:15:19', 0, 'aaaa', 0, 0, 114);
INSERT INTO `ticket_ticketuser` VALUES (216, '', '2021-07-31 11:43:56', '2021-07-31 15:15:19', 0, 'admin', 0, 0, 114);
INSERT INTO `ticket_ticketuser` VALUES (217, '', '2021-07-31 11:43:56', '2021-07-31 15:15:19', 0, 'fewf', 0, 0, 114);
INSERT INTO `ticket_ticketuser` VALUES (218, '', '2021-07-31 13:14:32', '2021-07-31 13:14:35', 0, '', 0, 0, 114);
INSERT INTO `ticket_ticketuser` VALUES (219, '', '2021-07-31 13:49:10', '2021-07-31 15:07:06', 0, 'admin', 0, 0, 115);
INSERT INTO `ticket_ticketuser` VALUES (220, '', '2021-07-31 13:49:10', '2021-07-31 15:07:06', 0, '23424', 0, 0, 115);
INSERT INTO `ticket_ticketuser` VALUES (221, '', '2021-07-31 13:49:10', '2021-07-31 15:13:30', 0, 'laoshi', 1, 1, 115);
INSERT INTO `ticket_ticketuser` VALUES (222, '', '2021-07-31 13:49:10', '2021-07-31 15:07:06', 0, 'fdsfds', 0, 0, 115);
INSERT INTO `ticket_ticketuser` VALUES (223, '', '2021-07-31 13:49:10', '2021-07-31 15:07:06', 0, 'test', 0, 0, 115);
INSERT INTO `ticket_ticketuser` VALUES (224, '', '2021-07-31 13:49:10', '2021-07-31 15:07:06', 0, 'test2', 0, 0, 115);
INSERT INTO `ticket_ticketuser` VALUES (225, '', '2021-07-31 13:49:10', '2021-07-31 15:07:06', 0, 'test1111', 0, 0, 115);
INSERT INTO `ticket_ticketuser` VALUES (226, '', '2021-07-31 13:49:10', '2021-07-31 15:07:06', 0, 'laoshia', 0, 0, 115);
INSERT INTO `ticket_ticketuser` VALUES (227, '', '2021-07-31 13:49:10', '2021-07-31 15:07:06', 0, '3333', 0, 0, 115);
INSERT INTO `ticket_ticketuser` VALUES (228, '', '2021-07-31 13:49:10', '2021-07-31 15:07:06', 0, 'dsfsffsdf', 0, 0, 115);
INSERT INTO `ticket_ticketuser` VALUES (229, '', '2021-07-31 13:49:10', '2021-07-31 15:07:06', 0, 'aaaa', 0, 0, 115);
INSERT INTO `ticket_ticketuser` VALUES (230, '', '2021-07-31 13:49:10', '2021-07-31 15:07:06', 0, 'fewf', 0, 0, 115);
INSERT INTO `ticket_ticketuser` VALUES (231, '', '2021-07-31 13:52:11', '2021-07-31 15:06:11', 0, 'test', 0, 0, 116);
INSERT INTO `ticket_ticketuser` VALUES (232, '', '2021-07-31 13:52:11', '2021-07-31 15:06:11', 0, '23424', 0, 0, 116);
INSERT INTO `ticket_ticketuser` VALUES (233, '', '2021-07-31 13:52:11', '2021-07-31 15:06:19', 0, 'laoshi', 1, 1, 116);
INSERT INTO `ticket_ticketuser` VALUES (234, '', '2021-07-31 13:52:11', '2021-07-31 15:06:11', 0, 'fdsfds', 0, 0, 116);
INSERT INTO `ticket_ticketuser` VALUES (235, '', '2021-07-31 13:52:11', '2021-07-31 15:06:11', 0, 'test2', 0, 0, 116);
INSERT INTO `ticket_ticketuser` VALUES (236, '', '2021-07-31 13:52:11', '2021-07-31 15:06:11', 0, 'test1111', 0, 0, 116);
INSERT INTO `ticket_ticketuser` VALUES (237, '', '2021-07-31 13:52:11', '2021-07-31 15:06:11', 0, 'laoshia', 0, 0, 116);
INSERT INTO `ticket_ticketuser` VALUES (238, '', '2021-07-31 13:52:11', '2021-07-31 15:06:11', 0, '3333', 0, 0, 116);
INSERT INTO `ticket_ticketuser` VALUES (239, '', '2021-07-31 13:52:11', '2021-07-31 15:06:11', 0, 'dsfsffsdf', 0, 0, 116);
INSERT INTO `ticket_ticketuser` VALUES (240, '', '2021-07-31 13:52:11', '2021-07-31 15:06:11', 0, 'aaaa', 0, 0, 116);
INSERT INTO `ticket_ticketuser` VALUES (241, '', '2021-07-31 13:52:11', '2021-07-31 15:06:11', 0, 'admin', 0, 0, 116);
INSERT INTO `ticket_ticketuser` VALUES (242, '', '2021-07-31 13:52:11', '2021-07-31 15:06:11', 0, 'fewf', 0, 0, 116);
INSERT INTO `ticket_ticketuser` VALUES (243, '', '2021-07-31 15:19:43', '2021-07-31 15:28:48', 0, 'test', 0, 0, 117);
INSERT INTO `ticket_ticketuser` VALUES (244, '', '2021-07-31 15:19:43', '2021-07-31 15:28:48', 0, '23424', 0, 0, 117);
INSERT INTO `ticket_ticketuser` VALUES (245, '', '2021-07-31 15:19:43', '2021-07-31 15:29:41', 0, 'laoshi', 1, 1, 117);
INSERT INTO `ticket_ticketuser` VALUES (246, '', '2021-07-31 15:19:43', '2021-07-31 15:28:48', 0, 'fdsfds', 0, 0, 117);
INSERT INTO `ticket_ticketuser` VALUES (247, '', '2021-07-31 15:19:43', '2021-07-31 15:28:48', 0, 'test2', 0, 0, 117);
INSERT INTO `ticket_ticketuser` VALUES (248, '', '2021-07-31 15:19:43', '2021-07-31 15:28:48', 0, 'test1111', 0, 0, 117);
INSERT INTO `ticket_ticketuser` VALUES (249, '', '2021-07-31 15:19:43', '2021-07-31 15:28:48', 0, 'laoshia', 0, 0, 117);
INSERT INTO `ticket_ticketuser` VALUES (250, '', '2021-07-31 15:19:43', '2021-07-31 15:28:48', 0, '3333', 0, 0, 117);
INSERT INTO `ticket_ticketuser` VALUES (251, '', '2021-07-31 15:19:43', '2021-07-31 15:28:48', 0, 'dsfsffsdf', 0, 0, 117);
INSERT INTO `ticket_ticketuser` VALUES (252, '', '2021-07-31 15:19:43', '2021-07-31 15:28:48', 0, 'aaaa', 0, 0, 117);
INSERT INTO `ticket_ticketuser` VALUES (253, '', '2021-07-31 15:19:43', '2021-07-31 15:28:48', 0, 'admin', 0, 0, 117);
INSERT INTO `ticket_ticketuser` VALUES (254, '', '2021-07-31 15:19:43', '2021-07-31 15:28:48', 0, 'fewf', 0, 0, 117);
INSERT INTO `ticket_ticketuser` VALUES (255, '', '2021-07-31 15:31:45', '2021-07-31 15:32:18', 0, 'test', 0, 0, 118);
INSERT INTO `ticket_ticketuser` VALUES (256, '', '2021-07-31 15:31:45', '2021-07-31 15:32:18', 0, '23424', 0, 0, 118);
INSERT INTO `ticket_ticketuser` VALUES (257, '', '2021-07-31 15:31:45', '2021-07-31 15:36:31', 0, 'laoshi', 1, 1, 118);
INSERT INTO `ticket_ticketuser` VALUES (258, '', '2021-07-31 15:31:45', '2021-07-31 15:32:18', 0, 'fdsfds', 0, 0, 118);
INSERT INTO `ticket_ticketuser` VALUES (259, '', '2021-07-31 15:31:45', '2021-07-31 15:32:18', 0, 'test2', 0, 0, 118);
INSERT INTO `ticket_ticketuser` VALUES (260, '', '2021-07-31 15:31:45', '2021-07-31 15:32:18', 0, 'test1111', 0, 0, 118);
INSERT INTO `ticket_ticketuser` VALUES (261, '', '2021-07-31 15:31:45', '2021-07-31 15:32:18', 0, 'laoshia', 0, 0, 118);
INSERT INTO `ticket_ticketuser` VALUES (262, '', '2021-07-31 15:31:45', '2021-07-31 15:32:18', 0, '3333', 0, 0, 118);
INSERT INTO `ticket_ticketuser` VALUES (263, '', '2021-07-31 15:31:45', '2021-07-31 15:32:18', 0, 'dsfsffsdf', 0, 0, 118);
INSERT INTO `ticket_ticketuser` VALUES (264, '', '2021-07-31 15:31:45', '2021-07-31 15:32:18', 0, 'aaaa', 0, 0, 118);
INSERT INTO `ticket_ticketuser` VALUES (265, '', '2021-07-31 15:31:45', '2021-07-31 15:32:18', 0, 'admin', 0, 0, 118);
INSERT INTO `ticket_ticketuser` VALUES (266, '', '2021-07-31 15:31:45', '2021-07-31 15:32:18', 0, 'fewf', 0, 0, 118);
INSERT INTO `ticket_ticketuser` VALUES (267, '', '2021-07-31 15:37:13', '2021-07-31 15:37:49', 0, 'test', 0, 0, 119);
INSERT INTO `ticket_ticketuser` VALUES (268, '', '2021-07-31 15:37:13', '2021-07-31 15:37:49', 0, '23424', 0, 0, 119);
INSERT INTO `ticket_ticketuser` VALUES (269, '', '2021-07-31 15:37:13', '2021-07-31 15:38:00', 0, 'laoshi', 1, 1, 119);
INSERT INTO `ticket_ticketuser` VALUES (270, '', '2021-07-31 15:37:13', '2021-07-31 15:37:49', 0, 'fdsfds', 0, 0, 119);
INSERT INTO `ticket_ticketuser` VALUES (271, '', '2021-07-31 15:37:13', '2021-07-31 15:37:49', 0, 'test2', 0, 0, 119);
INSERT INTO `ticket_ticketuser` VALUES (272, '', '2021-07-31 15:37:13', '2021-07-31 15:37:49', 0, 'test1111', 0, 0, 119);
INSERT INTO `ticket_ticketuser` VALUES (273, '', '2021-07-31 15:37:13', '2021-07-31 15:37:49', 0, 'laoshia', 0, 0, 119);
INSERT INTO `ticket_ticketuser` VALUES (274, '', '2021-07-31 15:37:13', '2021-07-31 15:37:49', 0, '3333', 0, 0, 119);
INSERT INTO `ticket_ticketuser` VALUES (275, '', '2021-07-31 15:37:13', '2021-07-31 15:37:49', 0, 'dsfsffsdf', 0, 0, 119);
INSERT INTO `ticket_ticketuser` VALUES (276, '', '2021-07-31 15:37:13', '2021-07-31 15:37:49', 0, 'aaaa', 0, 0, 119);
INSERT INTO `ticket_ticketuser` VALUES (277, '', '2021-07-31 15:37:13', '2021-07-31 15:37:49', 0, 'admin', 0, 0, 119);
INSERT INTO `ticket_ticketuser` VALUES (278, '', '2021-07-31 15:37:13', '2021-07-31 15:37:49', 0, 'fewf', 0, 0, 119);
INSERT INTO `ticket_ticketuser` VALUES (279, '', '2021-07-31 15:41:11', '2021-07-31 15:41:25', 0, 'test', 0, 0, 120);
INSERT INTO `ticket_ticketuser` VALUES (280, '', '2021-07-31 15:41:11', '2021-07-31 15:41:25', 0, '23424', 0, 0, 120);
INSERT INTO `ticket_ticketuser` VALUES (281, '', '2021-07-31 15:41:11', '2021-07-31 15:52:46', 0, 'laoshi', 0, 0, 120);
INSERT INTO `ticket_ticketuser` VALUES (282, '', '2021-07-31 15:41:11', '2021-07-31 15:41:25', 0, 'fdsfds', 0, 0, 120);
INSERT INTO `ticket_ticketuser` VALUES (283, '', '2021-07-31 15:41:11', '2021-07-31 15:41:25', 0, 'test2', 0, 0, 120);
INSERT INTO `ticket_ticketuser` VALUES (284, '', '2021-07-31 15:41:11', '2021-07-31 15:41:25', 0, 'test1111', 0, 0, 120);
INSERT INTO `ticket_ticketuser` VALUES (285, '', '2021-07-31 15:41:11', '2021-07-31 15:41:25', 0, 'laoshia', 0, 0, 120);
INSERT INTO `ticket_ticketuser` VALUES (286, '', '2021-07-31 15:41:11', '2021-07-31 15:41:25', 0, '3333', 0, 0, 120);
INSERT INTO `ticket_ticketuser` VALUES (287, '', '2021-07-31 15:41:11', '2021-07-31 15:41:25', 0, 'dsfsffsdf', 0, 0, 120);
INSERT INTO `ticket_ticketuser` VALUES (288, '', '2021-07-31 15:41:11', '2021-07-31 15:41:25', 0, 'aaaa', 0, 0, 120);
INSERT INTO `ticket_ticketuser` VALUES (289, '', '2021-07-31 15:41:11', '2021-07-31 15:41:25', 0, 'admin', 0, 0, 120);
INSERT INTO `ticket_ticketuser` VALUES (290, '', '2021-07-31 15:41:11', '2021-07-31 15:41:25', 0, 'fewf', 0, 0, 120);
INSERT INTO `ticket_ticketuser` VALUES (291, '', '2021-07-31 15:41:43', '2021-07-31 15:41:43', 0, 'laoshi', 0, 0, 121);
INSERT INTO `ticket_ticketuser` VALUES (292, '', '2021-07-31 15:41:43', '2021-07-31 15:53:51', 0, 'zhangsan', 0, 0, 121);
INSERT INTO `ticket_ticketuser` VALUES (293, '', '2021-07-31 15:41:43', '2021-07-31 15:53:51', 0, 'admin', 0, 0, 121);
INSERT INTO `ticket_ticketuser` VALUES (294, '', '2021-07-31 15:59:34', '2021-07-31 15:59:33', 0, 'admin', 1, 0, 122);
INSERT INTO `ticket_ticketuser` VALUES (295, '', '2021-07-31 15:59:34', '2021-07-31 15:59:34', 0, '23424', 1, 0, 122);
INSERT INTO `ticket_ticketuser` VALUES (296, '', '2021-07-31 15:59:34', '2021-07-31 15:59:34', 0, 'laoshi', 1, 0, 122);
INSERT INTO `ticket_ticketuser` VALUES (297, '', '2021-07-31 15:59:34', '2021-07-31 15:59:34', 0, 'fdsfds', 1, 0, 122);
INSERT INTO `ticket_ticketuser` VALUES (298, '', '2021-07-31 15:59:34', '2021-07-31 15:59:34', 0, 'test', 1, 0, 122);
INSERT INTO `ticket_ticketuser` VALUES (299, '', '2021-07-31 15:59:34', '2021-07-31 15:59:34', 0, 'test2', 1, 0, 122);
INSERT INTO `ticket_ticketuser` VALUES (300, '', '2021-07-31 15:59:34', '2021-07-31 15:59:34', 0, 'test1111', 1, 0, 122);
INSERT INTO `ticket_ticketuser` VALUES (301, '', '2021-07-31 15:59:34', '2021-07-31 15:59:34', 0, 'laoshia', 1, 0, 122);
INSERT INTO `ticket_ticketuser` VALUES (302, '', '2021-07-31 15:59:34', '2021-07-31 15:59:34', 0, '3333', 1, 0, 122);
INSERT INTO `ticket_ticketuser` VALUES (303, '', '2021-07-31 15:59:34', '2021-07-31 15:59:34', 0, 'dsfsffsdf', 1, 0, 122);
INSERT INTO `ticket_ticketuser` VALUES (304, '', '2021-07-31 15:59:34', '2021-07-31 15:59:34', 0, 'aaaa', 1, 0, 122);
INSERT INTO `ticket_ticketuser` VALUES (305, '', '2021-07-31 15:59:34', '2021-07-31 15:59:34', 0, 'fewf', 1, 0, 122);
INSERT INTO `ticket_ticketuser` VALUES (306, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'admin', 1, 0, 123);
INSERT INTO `ticket_ticketuser` VALUES (307, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, '23424', 1, 0, 123);
INSERT INTO `ticket_ticketuser` VALUES (308, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'laoshi', 1, 0, 123);
INSERT INTO `ticket_ticketuser` VALUES (309, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'fdsfds', 1, 0, 123);
INSERT INTO `ticket_ticketuser` VALUES (310, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'test', 1, 0, 123);
INSERT INTO `ticket_ticketuser` VALUES (311, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'test2', 1, 0, 123);
INSERT INTO `ticket_ticketuser` VALUES (312, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'test1111', 1, 0, 123);
INSERT INTO `ticket_ticketuser` VALUES (313, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'laoshia', 1, 0, 123);
INSERT INTO `ticket_ticketuser` VALUES (314, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, '3333', 1, 0, 123);
INSERT INTO `ticket_ticketuser` VALUES (315, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'dsfsffsdf', 1, 0, 123);
INSERT INTO `ticket_ticketuser` VALUES (316, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'aaaa', 1, 0, 123);
INSERT INTO `ticket_ticketuser` VALUES (317, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'fewf', 1, 0, 123);
INSERT INTO `ticket_ticketuser` VALUES (318, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'admin', 1, 0, 124);
INSERT INTO `ticket_ticketuser` VALUES (319, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, '23424', 1, 0, 124);
INSERT INTO `ticket_ticketuser` VALUES (320, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'laoshi', 1, 0, 124);
INSERT INTO `ticket_ticketuser` VALUES (321, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'fdsfds', 1, 0, 124);
INSERT INTO `ticket_ticketuser` VALUES (322, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'test', 1, 0, 124);
INSERT INTO `ticket_ticketuser` VALUES (323, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'test2', 1, 0, 124);
INSERT INTO `ticket_ticketuser` VALUES (324, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'test1111', 1, 0, 124);
INSERT INTO `ticket_ticketuser` VALUES (325, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'laoshia', 1, 0, 124);
INSERT INTO `ticket_ticketuser` VALUES (326, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, '3333', 1, 0, 124);
INSERT INTO `ticket_ticketuser` VALUES (327, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'dsfsffsdf', 1, 0, 124);
INSERT INTO `ticket_ticketuser` VALUES (328, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'aaaa', 1, 0, 124);
INSERT INTO `ticket_ticketuser` VALUES (329, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'fewf', 1, 0, 124);
INSERT INTO `ticket_ticketuser` VALUES (330, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'admin', 1, 0, 125);
INSERT INTO `ticket_ticketuser` VALUES (331, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, '23424', 1, 0, 125);
INSERT INTO `ticket_ticketuser` VALUES (332, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'laoshi', 1, 0, 125);
INSERT INTO `ticket_ticketuser` VALUES (333, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'fdsfds', 1, 0, 125);
INSERT INTO `ticket_ticketuser` VALUES (334, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'test', 1, 0, 125);
INSERT INTO `ticket_ticketuser` VALUES (335, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'test2', 1, 0, 125);
INSERT INTO `ticket_ticketuser` VALUES (336, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'test1111', 1, 0, 125);
INSERT INTO `ticket_ticketuser` VALUES (337, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'laoshia', 1, 0, 125);
INSERT INTO `ticket_ticketuser` VALUES (338, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, '3333', 1, 0, 125);
INSERT INTO `ticket_ticketuser` VALUES (339, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'dsfsffsdf', 1, 0, 125);
INSERT INTO `ticket_ticketuser` VALUES (340, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'aaaa', 1, 0, 125);
INSERT INTO `ticket_ticketuser` VALUES (341, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'fewf', 1, 0, 125);
INSERT INTO `ticket_ticketuser` VALUES (342, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'admin', 1, 0, 126);
INSERT INTO `ticket_ticketuser` VALUES (343, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, '23424', 1, 0, 126);
INSERT INTO `ticket_ticketuser` VALUES (344, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'laoshi', 1, 0, 126);
INSERT INTO `ticket_ticketuser` VALUES (345, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'fdsfds', 1, 0, 126);
INSERT INTO `ticket_ticketuser` VALUES (346, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'test', 1, 0, 126);
INSERT INTO `ticket_ticketuser` VALUES (347, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'test2', 1, 0, 126);
INSERT INTO `ticket_ticketuser` VALUES (348, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'test1111', 1, 0, 126);
INSERT INTO `ticket_ticketuser` VALUES (349, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'laoshia', 1, 0, 126);
INSERT INTO `ticket_ticketuser` VALUES (350, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, '3333', 1, 0, 126);
INSERT INTO `ticket_ticketuser` VALUES (351, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'dsfsffsdf', 1, 0, 126);
INSERT INTO `ticket_ticketuser` VALUES (352, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'aaaa', 1, 0, 126);
INSERT INTO `ticket_ticketuser` VALUES (353, '', '2021-07-31 15:59:35', '2021-07-31 15:59:35', 0, 'fewf', 1, 0, 126);
INSERT INTO `ticket_ticketuser` VALUES (354, '', '2021-07-31 16:00:41', '2021-07-31 16:00:40', 0, 'admin', 1, 0, 127);
INSERT INTO `ticket_ticketuser` VALUES (355, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, '23424', 1, 0, 127);
INSERT INTO `ticket_ticketuser` VALUES (356, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'laoshi', 1, 0, 127);
INSERT INTO `ticket_ticketuser` VALUES (357, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'fdsfds', 1, 0, 127);
INSERT INTO `ticket_ticketuser` VALUES (358, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'test', 1, 0, 127);
INSERT INTO `ticket_ticketuser` VALUES (359, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'test2', 1, 0, 127);
INSERT INTO `ticket_ticketuser` VALUES (360, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'test1111', 1, 0, 127);
INSERT INTO `ticket_ticketuser` VALUES (361, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'laoshia', 1, 0, 127);
INSERT INTO `ticket_ticketuser` VALUES (362, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, '3333', 1, 0, 127);
INSERT INTO `ticket_ticketuser` VALUES (363, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'dsfsffsdf', 1, 0, 127);
INSERT INTO `ticket_ticketuser` VALUES (364, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'aaaa', 1, 0, 127);
INSERT INTO `ticket_ticketuser` VALUES (365, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'fewf', 1, 0, 127);
INSERT INTO `ticket_ticketuser` VALUES (366, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'admin', 1, 0, 128);
INSERT INTO `ticket_ticketuser` VALUES (367, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, '23424', 1, 0, 128);
INSERT INTO `ticket_ticketuser` VALUES (368, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'laoshi', 1, 0, 128);
INSERT INTO `ticket_ticketuser` VALUES (369, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'fdsfds', 1, 0, 128);
INSERT INTO `ticket_ticketuser` VALUES (370, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'test', 1, 0, 128);
INSERT INTO `ticket_ticketuser` VALUES (371, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'test2', 1, 0, 128);
INSERT INTO `ticket_ticketuser` VALUES (372, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'test1111', 1, 0, 128);
INSERT INTO `ticket_ticketuser` VALUES (373, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'laoshia', 1, 0, 128);
INSERT INTO `ticket_ticketuser` VALUES (374, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, '3333', 1, 0, 128);
INSERT INTO `ticket_ticketuser` VALUES (375, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'dsfsffsdf', 1, 0, 128);
INSERT INTO `ticket_ticketuser` VALUES (376, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'aaaa', 1, 0, 128);
INSERT INTO `ticket_ticketuser` VALUES (377, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'fewf', 1, 0, 128);
INSERT INTO `ticket_ticketuser` VALUES (378, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'admin', 1, 0, 129);
INSERT INTO `ticket_ticketuser` VALUES (379, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, '23424', 1, 0, 129);
INSERT INTO `ticket_ticketuser` VALUES (380, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'laoshi', 1, 0, 129);
INSERT INTO `ticket_ticketuser` VALUES (381, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'fdsfds', 1, 0, 129);
INSERT INTO `ticket_ticketuser` VALUES (382, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'test', 1, 0, 129);
INSERT INTO `ticket_ticketuser` VALUES (383, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'test2', 1, 0, 129);
INSERT INTO `ticket_ticketuser` VALUES (384, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'test1111', 1, 0, 129);
INSERT INTO `ticket_ticketuser` VALUES (385, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'laoshia', 1, 0, 129);
INSERT INTO `ticket_ticketuser` VALUES (386, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, '3333', 1, 0, 129);
INSERT INTO `ticket_ticketuser` VALUES (387, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'dsfsffsdf', 1, 0, 129);
INSERT INTO `ticket_ticketuser` VALUES (388, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'aaaa', 1, 0, 129);
INSERT INTO `ticket_ticketuser` VALUES (389, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'fewf', 1, 0, 129);
INSERT INTO `ticket_ticketuser` VALUES (390, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'admin', 1, 0, 130);
INSERT INTO `ticket_ticketuser` VALUES (391, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, '23424', 1, 0, 130);
INSERT INTO `ticket_ticketuser` VALUES (392, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'laoshi', 1, 0, 130);
INSERT INTO `ticket_ticketuser` VALUES (393, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'fdsfds', 1, 0, 130);
INSERT INTO `ticket_ticketuser` VALUES (394, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'test', 1, 0, 130);
INSERT INTO `ticket_ticketuser` VALUES (395, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'test2', 1, 0, 130);
INSERT INTO `ticket_ticketuser` VALUES (396, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'test1111', 1, 0, 130);
INSERT INTO `ticket_ticketuser` VALUES (397, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'laoshia', 1, 0, 130);
INSERT INTO `ticket_ticketuser` VALUES (398, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, '3333', 1, 0, 130);
INSERT INTO `ticket_ticketuser` VALUES (399, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'dsfsffsdf', 1, 0, 130);
INSERT INTO `ticket_ticketuser` VALUES (400, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'aaaa', 1, 0, 130);
INSERT INTO `ticket_ticketuser` VALUES (401, '', '2021-07-31 16:00:41', '2021-07-31 16:00:41', 0, 'fewf', 1, 0, 130);
INSERT INTO `ticket_ticketuser` VALUES (402, '', '2021-07-31 16:00:42', '2021-07-31 16:00:41', 0, 'admin', 1, 0, 131);
INSERT INTO `ticket_ticketuser` VALUES (403, '', '2021-07-31 16:00:42', '2021-07-31 16:00:42', 0, '23424', 1, 0, 131);
INSERT INTO `ticket_ticketuser` VALUES (404, '', '2021-07-31 16:00:42', '2021-07-31 16:00:42', 0, 'laoshi', 1, 0, 131);
INSERT INTO `ticket_ticketuser` VALUES (405, '', '2021-07-31 16:00:42', '2021-07-31 16:00:42', 0, 'fdsfds', 1, 0, 131);
INSERT INTO `ticket_ticketuser` VALUES (406, '', '2021-07-31 16:00:42', '2021-07-31 16:00:42', 0, 'test', 1, 0, 131);
INSERT INTO `ticket_ticketuser` VALUES (407, '', '2021-07-31 16:00:42', '2021-07-31 16:00:42', 0, 'test2', 1, 0, 131);
INSERT INTO `ticket_ticketuser` VALUES (408, '', '2021-07-31 16:00:42', '2021-07-31 16:00:42', 0, 'test1111', 1, 0, 131);
INSERT INTO `ticket_ticketuser` VALUES (409, '', '2021-07-31 16:00:42', '2021-07-31 16:00:42', 0, 'laoshia', 1, 0, 131);
INSERT INTO `ticket_ticketuser` VALUES (410, '', '2021-07-31 16:00:42', '2021-07-31 16:00:42', 0, '3333', 1, 0, 131);
INSERT INTO `ticket_ticketuser` VALUES (411, '', '2021-07-31 16:00:42', '2021-07-31 16:00:42', 0, 'dsfsffsdf', 1, 0, 131);
INSERT INTO `ticket_ticketuser` VALUES (412, '', '2021-07-31 16:00:42', '2021-07-31 16:00:42', 0, 'aaaa', 1, 0, 131);
INSERT INTO `ticket_ticketuser` VALUES (413, '', '2021-07-31 16:00:42', '2021-07-31 16:00:42', 0, 'fewf', 1, 0, 131);
INSERT INTO `ticket_ticketuser` VALUES (414, '', '2021-07-31 16:01:30', '2021-07-31 16:01:29', 0, 'admin', 1, 0, 132);
INSERT INTO `ticket_ticketuser` VALUES (415, '', '2021-07-31 16:01:30', '2021-07-31 16:01:30', 0, '23424', 1, 0, 132);
INSERT INTO `ticket_ticketuser` VALUES (416, '', '2021-07-31 16:01:30', '2021-07-31 16:01:30', 0, 'laoshi', 1, 0, 132);
INSERT INTO `ticket_ticketuser` VALUES (417, '', '2021-07-31 16:01:30', '2021-07-31 16:01:30', 0, 'fdsfds', 1, 0, 132);
INSERT INTO `ticket_ticketuser` VALUES (418, '', '2021-07-31 16:01:30', '2021-07-31 16:01:30', 0, 'test', 1, 0, 132);
INSERT INTO `ticket_ticketuser` VALUES (419, '', '2021-07-31 16:01:30', '2021-07-31 16:01:30', 0, 'test2', 1, 0, 132);
INSERT INTO `ticket_ticketuser` VALUES (420, '', '2021-07-31 16:01:30', '2021-07-31 16:01:30', 0, 'test1111', 1, 0, 132);
INSERT INTO `ticket_ticketuser` VALUES (421, '', '2021-07-31 16:01:30', '2021-07-31 16:01:30', 0, 'laoshia', 1, 0, 132);
INSERT INTO `ticket_ticketuser` VALUES (422, '', '2021-07-31 16:01:30', '2021-07-31 16:01:30', 0, '3333', 1, 0, 132);
INSERT INTO `ticket_ticketuser` VALUES (423, '', '2021-07-31 16:01:30', '2021-07-31 16:01:30', 0, 'dsfsffsdf', 1, 0, 132);
INSERT INTO `ticket_ticketuser` VALUES (424, '', '2021-07-31 16:01:30', '2021-07-31 16:01:30', 0, 'aaaa', 1, 0, 132);
INSERT INTO `ticket_ticketuser` VALUES (425, '', '2021-07-31 16:01:30', '2021-07-31 16:01:30', 0, 'fewf', 1, 0, 132);
INSERT INTO `ticket_ticketuser` VALUES (426, '', '2021-07-31 16:01:31', '2021-07-31 16:01:30', 0, 'admin', 1, 0, 133);
INSERT INTO `ticket_ticketuser` VALUES (427, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, '23424', 1, 0, 133);
INSERT INTO `ticket_ticketuser` VALUES (428, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'laoshi', 1, 0, 133);
INSERT INTO `ticket_ticketuser` VALUES (429, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'fdsfds', 1, 0, 133);
INSERT INTO `ticket_ticketuser` VALUES (430, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'test', 1, 0, 133);
INSERT INTO `ticket_ticketuser` VALUES (431, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'test2', 1, 0, 133);
INSERT INTO `ticket_ticketuser` VALUES (432, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'test1111', 1, 0, 133);
INSERT INTO `ticket_ticketuser` VALUES (433, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'laoshia', 1, 0, 133);
INSERT INTO `ticket_ticketuser` VALUES (434, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, '3333', 1, 0, 133);
INSERT INTO `ticket_ticketuser` VALUES (435, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'dsfsffsdf', 1, 0, 133);
INSERT INTO `ticket_ticketuser` VALUES (436, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'aaaa', 1, 0, 133);
INSERT INTO `ticket_ticketuser` VALUES (437, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'fewf', 1, 0, 133);
INSERT INTO `ticket_ticketuser` VALUES (438, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'admin', 1, 0, 134);
INSERT INTO `ticket_ticketuser` VALUES (439, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, '23424', 1, 0, 134);
INSERT INTO `ticket_ticketuser` VALUES (440, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'laoshi', 1, 0, 134);
INSERT INTO `ticket_ticketuser` VALUES (441, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'fdsfds', 1, 0, 134);
INSERT INTO `ticket_ticketuser` VALUES (442, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'test', 1, 0, 134);
INSERT INTO `ticket_ticketuser` VALUES (443, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'test2', 1, 0, 134);
INSERT INTO `ticket_ticketuser` VALUES (444, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'test1111', 1, 0, 134);
INSERT INTO `ticket_ticketuser` VALUES (445, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'laoshia', 1, 0, 134);
INSERT INTO `ticket_ticketuser` VALUES (446, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, '3333', 1, 0, 134);
INSERT INTO `ticket_ticketuser` VALUES (447, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'dsfsffsdf', 1, 0, 134);
INSERT INTO `ticket_ticketuser` VALUES (448, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'aaaa', 1, 0, 134);
INSERT INTO `ticket_ticketuser` VALUES (449, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'fewf', 1, 0, 134);
INSERT INTO `ticket_ticketuser` VALUES (450, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'admin', 1, 0, 135);
INSERT INTO `ticket_ticketuser` VALUES (451, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, '23424', 1, 0, 135);
INSERT INTO `ticket_ticketuser` VALUES (452, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'laoshi', 1, 0, 135);
INSERT INTO `ticket_ticketuser` VALUES (453, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'fdsfds', 1, 0, 135);
INSERT INTO `ticket_ticketuser` VALUES (454, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'test', 1, 0, 135);
INSERT INTO `ticket_ticketuser` VALUES (455, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'test2', 1, 0, 135);
INSERT INTO `ticket_ticketuser` VALUES (456, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'test1111', 1, 0, 135);
INSERT INTO `ticket_ticketuser` VALUES (457, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'laoshia', 1, 0, 135);
INSERT INTO `ticket_ticketuser` VALUES (458, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, '3333', 1, 0, 135);
INSERT INTO `ticket_ticketuser` VALUES (459, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'dsfsffsdf', 1, 0, 135);
INSERT INTO `ticket_ticketuser` VALUES (460, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'aaaa', 1, 0, 135);
INSERT INTO `ticket_ticketuser` VALUES (461, '', '2021-07-31 16:01:31', '2021-07-31 16:01:31', 0, 'fewf', 1, 0, 135);
INSERT INTO `ticket_ticketuser` VALUES (462, '', '2021-07-31 16:02:18', '2021-07-31 16:02:17', 0, 'admin', 1, 0, 136);
INSERT INTO `ticket_ticketuser` VALUES (463, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, '23424', 1, 0, 136);
INSERT INTO `ticket_ticketuser` VALUES (464, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'laoshi', 1, 0, 136);
INSERT INTO `ticket_ticketuser` VALUES (465, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'fdsfds', 1, 0, 136);
INSERT INTO `ticket_ticketuser` VALUES (466, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'test', 1, 0, 136);
INSERT INTO `ticket_ticketuser` VALUES (467, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'test2', 1, 0, 136);
INSERT INTO `ticket_ticketuser` VALUES (468, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'test1111', 1, 0, 136);
INSERT INTO `ticket_ticketuser` VALUES (469, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'laoshia', 1, 0, 136);
INSERT INTO `ticket_ticketuser` VALUES (470, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, '3333', 1, 0, 136);
INSERT INTO `ticket_ticketuser` VALUES (471, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'dsfsffsdf', 1, 0, 136);
INSERT INTO `ticket_ticketuser` VALUES (472, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'aaaa', 1, 0, 136);
INSERT INTO `ticket_ticketuser` VALUES (473, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'fewf', 1, 0, 136);
INSERT INTO `ticket_ticketuser` VALUES (474, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'admin', 1, 0, 137);
INSERT INTO `ticket_ticketuser` VALUES (475, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, '23424', 1, 0, 137);
INSERT INTO `ticket_ticketuser` VALUES (476, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'laoshi', 1, 0, 137);
INSERT INTO `ticket_ticketuser` VALUES (477, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'fdsfds', 1, 0, 137);
INSERT INTO `ticket_ticketuser` VALUES (478, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'test', 1, 0, 137);
INSERT INTO `ticket_ticketuser` VALUES (479, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'test2', 1, 0, 137);
INSERT INTO `ticket_ticketuser` VALUES (480, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'test1111', 1, 0, 137);
INSERT INTO `ticket_ticketuser` VALUES (481, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'laoshia', 1, 0, 137);
INSERT INTO `ticket_ticketuser` VALUES (482, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, '3333', 1, 0, 137);
INSERT INTO `ticket_ticketuser` VALUES (483, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'dsfsffsdf', 1, 0, 137);
INSERT INTO `ticket_ticketuser` VALUES (484, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'aaaa', 1, 0, 137);
INSERT INTO `ticket_ticketuser` VALUES (485, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'fewf', 1, 0, 137);
INSERT INTO `ticket_ticketuser` VALUES (486, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'admin', 1, 0, 138);
INSERT INTO `ticket_ticketuser` VALUES (487, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, '23424', 1, 0, 138);
INSERT INTO `ticket_ticketuser` VALUES (488, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'laoshi', 1, 0, 138);
INSERT INTO `ticket_ticketuser` VALUES (489, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'fdsfds', 1, 0, 138);
INSERT INTO `ticket_ticketuser` VALUES (490, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'test', 1, 0, 138);
INSERT INTO `ticket_ticketuser` VALUES (491, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'test2', 1, 0, 138);
INSERT INTO `ticket_ticketuser` VALUES (492, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'test1111', 1, 0, 138);
INSERT INTO `ticket_ticketuser` VALUES (493, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'laoshia', 1, 0, 138);
INSERT INTO `ticket_ticketuser` VALUES (494, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, '3333', 1, 0, 138);
INSERT INTO `ticket_ticketuser` VALUES (495, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'dsfsffsdf', 1, 0, 138);
INSERT INTO `ticket_ticketuser` VALUES (496, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'aaaa', 1, 0, 138);
INSERT INTO `ticket_ticketuser` VALUES (497, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'fewf', 1, 0, 138);
INSERT INTO `ticket_ticketuser` VALUES (498, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'admin', 1, 0, 139);
INSERT INTO `ticket_ticketuser` VALUES (499, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, '23424', 1, 0, 139);
INSERT INTO `ticket_ticketuser` VALUES (500, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'laoshi', 1, 0, 139);
INSERT INTO `ticket_ticketuser` VALUES (501, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'fdsfds', 1, 0, 139);
INSERT INTO `ticket_ticketuser` VALUES (502, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'test', 1, 0, 139);
INSERT INTO `ticket_ticketuser` VALUES (503, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'test2', 1, 0, 139);
INSERT INTO `ticket_ticketuser` VALUES (504, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'test1111', 1, 0, 139);
INSERT INTO `ticket_ticketuser` VALUES (505, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'laoshia', 1, 0, 139);
INSERT INTO `ticket_ticketuser` VALUES (506, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, '3333', 1, 0, 139);
INSERT INTO `ticket_ticketuser` VALUES (507, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'dsfsffsdf', 1, 0, 139);
INSERT INTO `ticket_ticketuser` VALUES (508, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'aaaa', 1, 0, 139);
INSERT INTO `ticket_ticketuser` VALUES (509, '', '2021-07-31 16:02:18', '2021-07-31 16:02:18', 0, 'fewf', 1, 0, 139);
INSERT INTO `ticket_ticketuser` VALUES (510, '', '2021-07-31 16:02:22', '2021-07-31 16:02:21', 0, 'test', 1, 0, 140);
INSERT INTO `ticket_ticketuser` VALUES (511, '', '2021-07-31 16:02:22', '2021-07-31 16:02:22', 0, '23424', 1, 0, 140);
INSERT INTO `ticket_ticketuser` VALUES (512, '', '2021-07-31 16:02:22', '2021-07-31 16:02:22', 0, 'laoshi', 1, 0, 140);
INSERT INTO `ticket_ticketuser` VALUES (513, '', '2021-07-31 16:02:22', '2021-07-31 16:02:22', 0, 'fdsfds', 1, 0, 140);
INSERT INTO `ticket_ticketuser` VALUES (514, '', '2021-07-31 16:02:22', '2021-07-31 16:02:22', 0, 'test2', 1, 0, 140);
INSERT INTO `ticket_ticketuser` VALUES (515, '', '2021-07-31 16:02:22', '2021-07-31 16:02:22', 0, 'test1111', 1, 0, 140);
INSERT INTO `ticket_ticketuser` VALUES (516, '', '2021-07-31 16:02:22', '2021-07-31 16:02:22', 0, 'laoshia', 1, 0, 140);
INSERT INTO `ticket_ticketuser` VALUES (517, '', '2021-07-31 16:02:22', '2021-07-31 16:02:22', 0, '3333', 1, 0, 140);
INSERT INTO `ticket_ticketuser` VALUES (518, '', '2021-07-31 16:02:22', '2021-07-31 16:02:22', 0, 'dsfsffsdf', 1, 0, 140);
INSERT INTO `ticket_ticketuser` VALUES (519, '', '2021-07-31 16:02:22', '2021-07-31 16:02:22', 0, 'aaaa', 1, 0, 140);
INSERT INTO `ticket_ticketuser` VALUES (520, '', '2021-07-31 16:02:22', '2021-07-31 16:02:22', 0, 'admin', 1, 0, 140);
INSERT INTO `ticket_ticketuser` VALUES (521, '', '2021-07-31 16:02:22', '2021-07-31 16:02:22', 0, 'fewf', 1, 0, 140);
INSERT INTO `ticket_ticketuser` VALUES (522, '', '2021-07-31 16:02:55', '2021-07-31 16:02:55', 0, 'admin', 1, 0, 141);
INSERT INTO `ticket_ticketuser` VALUES (523, '', '2021-07-31 16:02:55', '2021-07-31 16:02:55', 0, '23424', 1, 0, 141);
INSERT INTO `ticket_ticketuser` VALUES (524, '', '2021-07-31 16:02:55', '2021-07-31 16:02:55', 0, 'laoshi', 1, 0, 141);
INSERT INTO `ticket_ticketuser` VALUES (525, '', '2021-07-31 16:02:55', '2021-07-31 16:02:55', 0, 'fdsfds', 1, 0, 141);
INSERT INTO `ticket_ticketuser` VALUES (526, '', '2021-07-31 16:02:55', '2021-07-31 16:02:55', 0, 'test', 1, 0, 141);
INSERT INTO `ticket_ticketuser` VALUES (527, '', '2021-07-31 16:02:55', '2021-07-31 16:02:55', 0, 'test2', 1, 0, 141);
INSERT INTO `ticket_ticketuser` VALUES (528, '', '2021-07-31 16:02:55', '2021-07-31 16:02:55', 0, 'test1111', 1, 0, 141);
INSERT INTO `ticket_ticketuser` VALUES (529, '', '2021-07-31 16:02:55', '2021-07-31 16:02:55', 0, 'laoshia', 1, 0, 141);
INSERT INTO `ticket_ticketuser` VALUES (530, '', '2021-07-31 16:02:55', '2021-07-31 16:02:55', 0, '3333', 1, 0, 141);
INSERT INTO `ticket_ticketuser` VALUES (531, '', '2021-07-31 16:02:55', '2021-07-31 16:02:55', 0, 'dsfsffsdf', 1, 0, 141);
INSERT INTO `ticket_ticketuser` VALUES (532, '', '2021-07-31 16:02:55', '2021-07-31 16:02:55', 0, 'aaaa', 1, 0, 141);
INSERT INTO `ticket_ticketuser` VALUES (533, '', '2021-07-31 16:02:55', '2021-07-31 16:02:55', 0, 'fewf', 1, 0, 141);
INSERT INTO `ticket_ticketuser` VALUES (534, '', '2021-07-31 16:02:56', '2021-07-31 16:02:55', 0, 'admin', 1, 0, 142);
INSERT INTO `ticket_ticketuser` VALUES (535, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, '23424', 1, 0, 142);
INSERT INTO `ticket_ticketuser` VALUES (536, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'laoshi', 1, 0, 142);
INSERT INTO `ticket_ticketuser` VALUES (537, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'fdsfds', 1, 0, 142);
INSERT INTO `ticket_ticketuser` VALUES (538, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'test', 1, 0, 142);
INSERT INTO `ticket_ticketuser` VALUES (539, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'test2', 1, 0, 142);
INSERT INTO `ticket_ticketuser` VALUES (540, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'test1111', 1, 0, 142);
INSERT INTO `ticket_ticketuser` VALUES (541, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'laoshia', 1, 0, 142);
INSERT INTO `ticket_ticketuser` VALUES (542, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, '3333', 1, 0, 142);
INSERT INTO `ticket_ticketuser` VALUES (543, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'dsfsffsdf', 1, 0, 142);
INSERT INTO `ticket_ticketuser` VALUES (544, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'aaaa', 1, 0, 142);
INSERT INTO `ticket_ticketuser` VALUES (545, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'fewf', 1, 0, 142);
INSERT INTO `ticket_ticketuser` VALUES (546, '', '2021-07-31 16:02:56', '2021-07-31 16:02:55', 0, 'admin', 1, 0, 143);
INSERT INTO `ticket_ticketuser` VALUES (547, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, '23424', 1, 0, 143);
INSERT INTO `ticket_ticketuser` VALUES (548, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'laoshi', 1, 0, 143);
INSERT INTO `ticket_ticketuser` VALUES (549, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'fdsfds', 1, 0, 143);
INSERT INTO `ticket_ticketuser` VALUES (550, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'test', 1, 0, 143);
INSERT INTO `ticket_ticketuser` VALUES (551, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'test2', 1, 0, 143);
INSERT INTO `ticket_ticketuser` VALUES (552, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'test1111', 1, 0, 143);
INSERT INTO `ticket_ticketuser` VALUES (553, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'laoshia', 1, 0, 143);
INSERT INTO `ticket_ticketuser` VALUES (554, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, '3333', 1, 0, 143);
INSERT INTO `ticket_ticketuser` VALUES (555, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'dsfsffsdf', 1, 0, 143);
INSERT INTO `ticket_ticketuser` VALUES (556, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'aaaa', 1, 0, 143);
INSERT INTO `ticket_ticketuser` VALUES (557, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'fewf', 1, 0, 143);
INSERT INTO `ticket_ticketuser` VALUES (558, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'admin', 1, 0, 144);
INSERT INTO `ticket_ticketuser` VALUES (559, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, '23424', 1, 0, 144);
INSERT INTO `ticket_ticketuser` VALUES (560, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'laoshi', 1, 0, 144);
INSERT INTO `ticket_ticketuser` VALUES (561, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'fdsfds', 1, 0, 144);
INSERT INTO `ticket_ticketuser` VALUES (562, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'test', 1, 0, 144);
INSERT INTO `ticket_ticketuser` VALUES (563, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'test2', 1, 0, 144);
INSERT INTO `ticket_ticketuser` VALUES (564, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'test1111', 1, 0, 144);
INSERT INTO `ticket_ticketuser` VALUES (565, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'laoshia', 1, 0, 144);
INSERT INTO `ticket_ticketuser` VALUES (566, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, '3333', 1, 0, 144);
INSERT INTO `ticket_ticketuser` VALUES (567, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'dsfsffsdf', 1, 0, 144);
INSERT INTO `ticket_ticketuser` VALUES (568, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'aaaa', 1, 0, 144);
INSERT INTO `ticket_ticketuser` VALUES (569, '', '2021-07-31 16:02:56', '2021-07-31 16:02:56', 0, 'fewf', 1, 0, 144);
INSERT INTO `ticket_ticketuser` VALUES (570, '', '2021-07-31 16:04:13', '2021-07-31 16:04:12', 0, 'admin', 1, 0, 145);
INSERT INTO `ticket_ticketuser` VALUES (571, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, '23424', 1, 0, 145);
INSERT INTO `ticket_ticketuser` VALUES (572, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, 'laoshi', 1, 0, 145);
INSERT INTO `ticket_ticketuser` VALUES (573, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, 'fdsfds', 1, 0, 145);
INSERT INTO `ticket_ticketuser` VALUES (574, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, 'test', 1, 0, 145);
INSERT INTO `ticket_ticketuser` VALUES (575, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, 'test2', 1, 0, 145);
INSERT INTO `ticket_ticketuser` VALUES (576, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, 'test1111', 1, 0, 145);
INSERT INTO `ticket_ticketuser` VALUES (577, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, 'laoshia', 1, 0, 145);
INSERT INTO `ticket_ticketuser` VALUES (578, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, '3333', 1, 0, 145);
INSERT INTO `ticket_ticketuser` VALUES (579, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, 'dsfsffsdf', 1, 0, 145);
INSERT INTO `ticket_ticketuser` VALUES (580, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, 'aaaa', 1, 0, 145);
INSERT INTO `ticket_ticketuser` VALUES (581, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, 'fewf', 1, 0, 145);
INSERT INTO `ticket_ticketuser` VALUES (582, '', '2021-07-31 16:04:13', '2021-07-31 16:04:12', 0, 'admin', 1, 0, 146);
INSERT INTO `ticket_ticketuser` VALUES (583, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, '23424', 1, 0, 146);
INSERT INTO `ticket_ticketuser` VALUES (584, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, 'laoshi', 1, 0, 146);
INSERT INTO `ticket_ticketuser` VALUES (585, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, 'fdsfds', 1, 0, 146);
INSERT INTO `ticket_ticketuser` VALUES (586, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, 'test', 1, 0, 146);
INSERT INTO `ticket_ticketuser` VALUES (587, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, 'test2', 1, 0, 146);
INSERT INTO `ticket_ticketuser` VALUES (588, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, 'test1111', 1, 0, 146);
INSERT INTO `ticket_ticketuser` VALUES (589, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, 'laoshia', 1, 0, 146);
INSERT INTO `ticket_ticketuser` VALUES (590, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, '3333', 1, 0, 146);
INSERT INTO `ticket_ticketuser` VALUES (591, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, 'dsfsffsdf', 1, 0, 146);
INSERT INTO `ticket_ticketuser` VALUES (592, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, 'aaaa', 1, 0, 146);
INSERT INTO `ticket_ticketuser` VALUES (593, '', '2021-07-31 16:04:13', '2021-07-31 16:04:13', 0, 'fewf', 1, 0, 146);
INSERT INTO `ticket_ticketuser` VALUES (594, '', '2021-07-31 16:04:57', '2021-07-31 16:04:56', 0, 'admin', 1, 0, 147);
INSERT INTO `ticket_ticketuser` VALUES (595, '', '2021-07-31 16:04:57', '2021-07-31 16:04:57', 0, '23424', 1, 0, 147);
INSERT INTO `ticket_ticketuser` VALUES (596, '', '2021-07-31 16:04:57', '2021-07-31 16:04:57', 0, 'laoshi', 1, 0, 147);
INSERT INTO `ticket_ticketuser` VALUES (597, '', '2021-07-31 16:04:57', '2021-07-31 16:04:57', 0, 'fdsfds', 1, 0, 147);
INSERT INTO `ticket_ticketuser` VALUES (598, '', '2021-07-31 16:04:57', '2021-07-31 16:04:57', 0, 'test', 1, 0, 147);
INSERT INTO `ticket_ticketuser` VALUES (599, '', '2021-07-31 16:04:57', '2021-07-31 16:04:57', 0, 'test2', 1, 0, 147);
INSERT INTO `ticket_ticketuser` VALUES (600, '', '2021-07-31 16:04:57', '2021-07-31 16:04:57', 0, 'test1111', 1, 0, 147);
INSERT INTO `ticket_ticketuser` VALUES (601, '', '2021-07-31 16:04:57', '2021-07-31 16:04:57', 0, 'laoshia', 1, 0, 147);
INSERT INTO `ticket_ticketuser` VALUES (602, '', '2021-07-31 16:04:57', '2021-07-31 16:04:57', 0, '3333', 1, 0, 147);
INSERT INTO `ticket_ticketuser` VALUES (603, '', '2021-07-31 16:04:57', '2021-07-31 16:04:57', 0, 'dsfsffsdf', 1, 0, 147);
INSERT INTO `ticket_ticketuser` VALUES (604, '', '2021-07-31 16:04:57', '2021-07-31 16:04:57', 0, 'aaaa', 1, 0, 147);
INSERT INTO `ticket_ticketuser` VALUES (605, '', '2021-07-31 16:04:57', '2021-07-31 16:04:57', 0, 'fewf', 1, 0, 147);
INSERT INTO `ticket_ticketuser` VALUES (606, '', '2021-07-31 16:05:00', '2021-07-31 16:04:59', 0, 'admin', 1, 0, 148);
INSERT INTO `ticket_ticketuser` VALUES (607, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, '23424', 1, 0, 148);
INSERT INTO `ticket_ticketuser` VALUES (608, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'laoshi', 1, 0, 148);
INSERT INTO `ticket_ticketuser` VALUES (609, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'fdsfds', 1, 0, 148);
INSERT INTO `ticket_ticketuser` VALUES (610, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'test', 1, 0, 148);
INSERT INTO `ticket_ticketuser` VALUES (611, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'test2', 1, 0, 148);
INSERT INTO `ticket_ticketuser` VALUES (612, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'test1111', 1, 0, 148);
INSERT INTO `ticket_ticketuser` VALUES (613, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'laoshia', 1, 0, 148);
INSERT INTO `ticket_ticketuser` VALUES (614, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, '3333', 1, 0, 148);
INSERT INTO `ticket_ticketuser` VALUES (615, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'dsfsffsdf', 1, 0, 148);
INSERT INTO `ticket_ticketuser` VALUES (616, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'aaaa', 1, 0, 148);
INSERT INTO `ticket_ticketuser` VALUES (617, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'fewf', 1, 0, 148);
INSERT INTO `ticket_ticketuser` VALUES (618, '', '2021-07-31 16:05:00', '2021-07-31 16:04:59', 0, 'admin', 1, 0, 149);
INSERT INTO `ticket_ticketuser` VALUES (619, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, '23424', 1, 0, 149);
INSERT INTO `ticket_ticketuser` VALUES (620, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'laoshi', 1, 0, 149);
INSERT INTO `ticket_ticketuser` VALUES (621, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'fdsfds', 1, 0, 149);
INSERT INTO `ticket_ticketuser` VALUES (622, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'test', 1, 0, 149);
INSERT INTO `ticket_ticketuser` VALUES (623, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'test2', 1, 0, 149);
INSERT INTO `ticket_ticketuser` VALUES (624, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'test1111', 1, 0, 149);
INSERT INTO `ticket_ticketuser` VALUES (625, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'laoshia', 1, 0, 149);
INSERT INTO `ticket_ticketuser` VALUES (626, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, '3333', 1, 0, 149);
INSERT INTO `ticket_ticketuser` VALUES (627, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'dsfsffsdf', 1, 0, 149);
INSERT INTO `ticket_ticketuser` VALUES (628, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'aaaa', 1, 0, 149);
INSERT INTO `ticket_ticketuser` VALUES (629, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'fewf', 1, 0, 149);
INSERT INTO `ticket_ticketuser` VALUES (630, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'admin', 1, 0, 150);
INSERT INTO `ticket_ticketuser` VALUES (631, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, '23424', 1, 0, 150);
INSERT INTO `ticket_ticketuser` VALUES (632, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'laoshi', 1, 0, 150);
INSERT INTO `ticket_ticketuser` VALUES (633, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'fdsfds', 1, 0, 150);
INSERT INTO `ticket_ticketuser` VALUES (634, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'test', 1, 0, 150);
INSERT INTO `ticket_ticketuser` VALUES (635, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'test2', 1, 0, 150);
INSERT INTO `ticket_ticketuser` VALUES (636, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'test1111', 1, 0, 150);
INSERT INTO `ticket_ticketuser` VALUES (637, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'laoshia', 1, 0, 150);
INSERT INTO `ticket_ticketuser` VALUES (638, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, '3333', 1, 0, 150);
INSERT INTO `ticket_ticketuser` VALUES (639, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'dsfsffsdf', 1, 0, 150);
INSERT INTO `ticket_ticketuser` VALUES (640, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'aaaa', 1, 0, 150);
INSERT INTO `ticket_ticketuser` VALUES (641, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'fewf', 1, 0, 150);
INSERT INTO `ticket_ticketuser` VALUES (642, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'admin', 1, 0, 151);
INSERT INTO `ticket_ticketuser` VALUES (643, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, '23424', 1, 0, 151);
INSERT INTO `ticket_ticketuser` VALUES (644, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'laoshi', 1, 0, 151);
INSERT INTO `ticket_ticketuser` VALUES (645, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'fdsfds', 1, 0, 151);
INSERT INTO `ticket_ticketuser` VALUES (646, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'test', 1, 0, 151);
INSERT INTO `ticket_ticketuser` VALUES (647, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'test2', 1, 0, 151);
INSERT INTO `ticket_ticketuser` VALUES (648, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'test1111', 1, 0, 151);
INSERT INTO `ticket_ticketuser` VALUES (649, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'laoshia', 1, 0, 151);
INSERT INTO `ticket_ticketuser` VALUES (650, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, '3333', 1, 0, 151);
INSERT INTO `ticket_ticketuser` VALUES (651, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'dsfsffsdf', 1, 0, 151);
INSERT INTO `ticket_ticketuser` VALUES (652, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'aaaa', 1, 0, 151);
INSERT INTO `ticket_ticketuser` VALUES (653, '', '2021-07-31 16:05:00', '2021-07-31 16:05:00', 0, 'fewf', 1, 0, 151);
INSERT INTO `ticket_ticketuser` VALUES (654, '', '2021-07-31 16:05:55', '2021-07-31 16:52:34', 0, 'admin', 0, 0, 152);
INSERT INTO `ticket_ticketuser` VALUES (655, '', '2021-07-31 16:05:55', '2021-07-31 16:52:34', 0, '23424', 0, 0, 152);
INSERT INTO `ticket_ticketuser` VALUES (656, '', '2021-07-31 16:05:55', '2021-07-31 16:52:34', 0, 'laoshi', 0, 0, 152);
INSERT INTO `ticket_ticketuser` VALUES (657, '', '2021-07-31 16:05:55', '2021-07-31 16:52:34', 0, 'fdsfds', 0, 0, 152);
INSERT INTO `ticket_ticketuser` VALUES (658, '', '2021-07-31 16:05:55', '2021-07-31 16:52:34', 0, 'test', 0, 0, 152);
INSERT INTO `ticket_ticketuser` VALUES (659, '', '2021-07-31 16:05:55', '2021-07-31 16:52:34', 0, 'test2', 0, 0, 152);
INSERT INTO `ticket_ticketuser` VALUES (660, '', '2021-07-31 16:05:55', '2021-07-31 16:52:34', 0, 'test1111', 0, 0, 152);
INSERT INTO `ticket_ticketuser` VALUES (661, '', '2021-07-31 16:05:55', '2021-07-31 16:52:34', 0, 'laoshia', 0, 0, 152);
INSERT INTO `ticket_ticketuser` VALUES (662, '', '2021-07-31 16:05:55', '2021-07-31 16:52:34', 0, '3333', 0, 0, 152);
INSERT INTO `ticket_ticketuser` VALUES (663, '', '2021-07-31 16:05:55', '2021-07-31 16:52:34', 0, 'dsfsffsdf', 0, 0, 152);
INSERT INTO `ticket_ticketuser` VALUES (664, '', '2021-07-31 16:05:55', '2021-07-31 16:52:34', 0, 'aaaa', 0, 0, 152);
INSERT INTO `ticket_ticketuser` VALUES (665, '', '2021-07-31 16:05:55', '2021-07-31 16:52:34', 0, 'fewf', 0, 0, 152);
INSERT INTO `ticket_ticketuser` VALUES (666, '', '2021-07-31 16:08:02', '2021-07-31 16:08:01', 0, 'admin', 1, 0, 153);
INSERT INTO `ticket_ticketuser` VALUES (667, '', '2021-07-31 16:08:02', '2021-07-31 16:08:02', 0, '23424', 1, 0, 153);
INSERT INTO `ticket_ticketuser` VALUES (668, '', '2021-07-31 16:08:02', '2021-07-31 16:08:02', 0, 'laoshi', 1, 0, 153);
INSERT INTO `ticket_ticketuser` VALUES (669, '', '2021-07-31 16:08:02', '2021-07-31 16:08:02', 0, 'fdsfds', 1, 0, 153);
INSERT INTO `ticket_ticketuser` VALUES (670, '', '2021-07-31 16:08:02', '2021-07-31 16:08:02', 0, 'test', 1, 0, 153);
INSERT INTO `ticket_ticketuser` VALUES (671, '', '2021-07-31 16:08:02', '2021-07-31 16:08:02', 0, 'test2', 1, 0, 153);
INSERT INTO `ticket_ticketuser` VALUES (672, '', '2021-07-31 16:08:02', '2021-07-31 16:08:02', 0, 'test1111', 1, 0, 153);
INSERT INTO `ticket_ticketuser` VALUES (673, '', '2021-07-31 16:08:02', '2021-07-31 16:08:02', 0, 'laoshia', 1, 0, 153);
INSERT INTO `ticket_ticketuser` VALUES (674, '', '2021-07-31 16:08:02', '2021-07-31 16:08:02', 0, '3333', 1, 0, 153);
INSERT INTO `ticket_ticketuser` VALUES (675, '', '2021-07-31 16:08:02', '2021-07-31 16:08:02', 0, 'dsfsffsdf', 1, 0, 153);
INSERT INTO `ticket_ticketuser` VALUES (676, '', '2021-07-31 16:08:02', '2021-07-31 16:08:02', 0, 'aaaa', 1, 0, 153);
INSERT INTO `ticket_ticketuser` VALUES (677, '', '2021-07-31 16:08:02', '2021-07-31 16:08:02', 0, 'fewf', 1, 0, 153);
INSERT INTO `ticket_ticketuser` VALUES (678, '', '2021-07-31 16:25:04', '2021-07-31 16:25:04', 0, 'test', 1, 0, 154);
INSERT INTO `ticket_ticketuser` VALUES (679, '', '2021-07-31 16:25:04', '2021-07-31 16:25:04', 0, '23424', 1, 0, 154);
INSERT INTO `ticket_ticketuser` VALUES (680, '', '2021-07-31 16:25:04', '2021-07-31 16:25:04', 0, 'laoshi', 1, 0, 154);
INSERT INTO `ticket_ticketuser` VALUES (681, '', '2021-07-31 16:25:04', '2021-07-31 16:25:04', 0, 'fdsfds', 1, 0, 154);
INSERT INTO `ticket_ticketuser` VALUES (682, '', '2021-07-31 16:25:04', '2021-07-31 16:25:04', 0, 'test2', 1, 0, 154);
INSERT INTO `ticket_ticketuser` VALUES (683, '', '2021-07-31 16:25:04', '2021-07-31 16:25:04', 0, 'test1111', 1, 0, 154);
INSERT INTO `ticket_ticketuser` VALUES (684, '', '2021-07-31 16:25:04', '2021-07-31 16:25:04', 0, 'laoshia', 1, 0, 154);
INSERT INTO `ticket_ticketuser` VALUES (685, '', '2021-07-31 16:25:04', '2021-07-31 16:25:04', 0, '3333', 1, 0, 154);
INSERT INTO `ticket_ticketuser` VALUES (686, '', '2021-07-31 16:25:04', '2021-07-31 16:25:04', 0, 'dsfsffsdf', 1, 0, 154);
INSERT INTO `ticket_ticketuser` VALUES (687, '', '2021-07-31 16:25:04', '2021-07-31 16:25:04', 0, 'aaaa', 1, 0, 154);
INSERT INTO `ticket_ticketuser` VALUES (688, '', '2021-07-31 16:25:04', '2021-07-31 16:25:04', 0, 'admin', 1, 0, 154);
INSERT INTO `ticket_ticketuser` VALUES (689, '', '2021-07-31 16:25:04', '2021-07-31 16:25:04', 0, 'fewf', 1, 0, 154);
INSERT INTO `ticket_ticketuser` VALUES (690, '', '2021-07-31 16:25:08', '2021-07-31 16:25:08', 0, 'test', 1, 0, 155);
INSERT INTO `ticket_ticketuser` VALUES (691, '', '2021-07-31 16:25:08', '2021-07-31 16:25:08', 0, '23424', 1, 0, 155);
INSERT INTO `ticket_ticketuser` VALUES (692, '', '2021-07-31 16:25:08', '2021-07-31 16:25:08', 0, 'laoshi', 1, 0, 155);
INSERT INTO `ticket_ticketuser` VALUES (693, '', '2021-07-31 16:25:08', '2021-07-31 16:25:08', 0, 'fdsfds', 1, 0, 155);
INSERT INTO `ticket_ticketuser` VALUES (694, '', '2021-07-31 16:25:08', '2021-07-31 16:25:08', 0, 'test2', 1, 0, 155);
INSERT INTO `ticket_ticketuser` VALUES (695, '', '2021-07-31 16:25:08', '2021-07-31 16:25:08', 0, 'test1111', 1, 0, 155);
INSERT INTO `ticket_ticketuser` VALUES (696, '', '2021-07-31 16:25:08', '2021-07-31 16:25:08', 0, 'laoshia', 1, 0, 155);
INSERT INTO `ticket_ticketuser` VALUES (697, '', '2021-07-31 16:25:08', '2021-07-31 16:25:08', 0, '3333', 1, 0, 155);
INSERT INTO `ticket_ticketuser` VALUES (698, '', '2021-07-31 16:25:08', '2021-07-31 16:25:08', 0, 'dsfsffsdf', 1, 0, 155);
INSERT INTO `ticket_ticketuser` VALUES (699, '', '2021-07-31 16:25:08', '2021-07-31 16:25:08', 0, 'aaaa', 1, 0, 155);
INSERT INTO `ticket_ticketuser` VALUES (700, '', '2021-07-31 16:25:08', '2021-07-31 16:25:08', 0, 'admin', 1, 0, 155);
INSERT INTO `ticket_ticketuser` VALUES (701, '', '2021-07-31 16:25:08', '2021-07-31 16:25:08', 0, 'fewf', 1, 0, 155);
INSERT INTO `ticket_ticketuser` VALUES (702, '', '2021-07-31 16:25:11', '2021-07-31 17:12:30', 0, 'test', 0, 0, 156);
INSERT INTO `ticket_ticketuser` VALUES (703, '', '2021-07-31 16:25:11', '2021-07-31 17:12:30', 0, '23424', 0, 0, 156);
INSERT INTO `ticket_ticketuser` VALUES (704, '', '2021-07-31 16:25:11', '2021-07-31 17:12:30', 0, 'laoshi', 0, 0, 156);
INSERT INTO `ticket_ticketuser` VALUES (705, '', '2021-07-31 16:25:11', '2021-07-31 17:12:30', 0, 'fdsfds', 0, 0, 156);
INSERT INTO `ticket_ticketuser` VALUES (706, '', '2021-07-31 16:25:11', '2021-07-31 17:12:30', 0, 'test2', 0, 0, 156);
INSERT INTO `ticket_ticketuser` VALUES (707, '', '2021-07-31 16:25:11', '2021-07-31 17:12:30', 0, 'test1111', 0, 0, 156);
INSERT INTO `ticket_ticketuser` VALUES (708, '', '2021-07-31 16:25:11', '2021-07-31 17:12:30', 0, 'laoshia', 0, 0, 156);
INSERT INTO `ticket_ticketuser` VALUES (709, '', '2021-07-31 16:25:11', '2021-07-31 17:12:30', 0, '3333', 0, 0, 156);
INSERT INTO `ticket_ticketuser` VALUES (710, '', '2021-07-31 16:25:11', '2021-07-31 17:12:30', 0, 'dsfsffsdf', 0, 0, 156);
INSERT INTO `ticket_ticketuser` VALUES (711, '', '2021-07-31 16:25:11', '2021-07-31 17:12:30', 0, 'aaaa', 0, 0, 156);
INSERT INTO `ticket_ticketuser` VALUES (712, '', '2021-07-31 16:25:11', '2021-07-31 17:12:30', 0, 'admin', 0, 0, 156);
INSERT INTO `ticket_ticketuser` VALUES (713, '', '2021-07-31 16:25:11', '2021-07-31 17:12:30', 0, 'fewf', 0, 0, 156);
INSERT INTO `ticket_ticketuser` VALUES (714, '', '2021-07-31 16:25:21', '2021-07-31 16:50:35', 0, 'test', 0, 0, 157);
INSERT INTO `ticket_ticketuser` VALUES (715, '', '2021-07-31 16:25:21', '2021-07-31 16:50:35', 0, '23424', 0, 0, 157);
INSERT INTO `ticket_ticketuser` VALUES (716, '', '2021-07-31 16:25:21', '2021-07-31 16:50:35', 0, 'laoshi', 0, 0, 157);
INSERT INTO `ticket_ticketuser` VALUES (717, '', '2021-07-31 16:25:21', '2021-07-31 16:50:35', 0, 'fdsfds', 0, 0, 157);
INSERT INTO `ticket_ticketuser` VALUES (718, '', '2021-07-31 16:25:21', '2021-07-31 16:50:35', 0, 'test2', 0, 0, 157);
INSERT INTO `ticket_ticketuser` VALUES (719, '', '2021-07-31 16:25:21', '2021-07-31 16:50:35', 0, 'test1111', 0, 0, 157);
INSERT INTO `ticket_ticketuser` VALUES (720, '', '2021-07-31 16:25:21', '2021-07-31 16:50:35', 0, 'laoshia', 0, 0, 157);
INSERT INTO `ticket_ticketuser` VALUES (721, '', '2021-07-31 16:25:21', '2021-07-31 16:50:35', 0, '3333', 0, 0, 157);
INSERT INTO `ticket_ticketuser` VALUES (722, '', '2021-07-31 16:25:21', '2021-07-31 16:50:35', 0, 'dsfsffsdf', 0, 0, 157);
INSERT INTO `ticket_ticketuser` VALUES (723, '', '2021-07-31 16:25:21', '2021-07-31 16:50:35', 0, 'aaaa', 0, 0, 157);
INSERT INTO `ticket_ticketuser` VALUES (724, '', '2021-07-31 16:25:21', '2021-07-31 16:50:35', 0, 'admin', 0, 0, 157);
INSERT INTO `ticket_ticketuser` VALUES (725, '', '2021-07-31 16:25:21', '2021-07-31 16:50:35', 0, 'fewf', 0, 0, 157);
INSERT INTO `ticket_ticketuser` VALUES (726, '', '2021-07-31 16:31:51', '2021-07-31 16:31:50', 0, 'admin', 1, 0, 158);
INSERT INTO `ticket_ticketuser` VALUES (727, '', '2021-07-31 16:31:51', '2021-07-31 16:31:51', 0, '23424', 1, 0, 158);
INSERT INTO `ticket_ticketuser` VALUES (728, '', '2021-07-31 16:31:51', '2021-07-31 16:31:51', 0, 'laoshi', 1, 0, 158);
INSERT INTO `ticket_ticketuser` VALUES (729, '', '2021-07-31 16:31:51', '2021-07-31 16:31:51', 0, 'fdsfds', 1, 0, 158);
INSERT INTO `ticket_ticketuser` VALUES (730, '', '2021-07-31 16:31:51', '2021-07-31 16:31:51', 0, 'test', 1, 0, 158);
INSERT INTO `ticket_ticketuser` VALUES (731, '', '2021-07-31 16:31:51', '2021-07-31 16:31:51', 0, 'test2', 1, 0, 158);
INSERT INTO `ticket_ticketuser` VALUES (732, '', '2021-07-31 16:31:51', '2021-07-31 16:31:51', 0, 'test1111', 1, 0, 158);
INSERT INTO `ticket_ticketuser` VALUES (733, '', '2021-07-31 16:31:51', '2021-07-31 16:31:51', 0, 'laoshia', 1, 0, 158);
INSERT INTO `ticket_ticketuser` VALUES (734, '', '2021-07-31 16:31:51', '2021-07-31 16:31:51', 0, '3333', 1, 0, 158);
INSERT INTO `ticket_ticketuser` VALUES (735, '', '2021-07-31 16:31:51', '2021-07-31 16:31:51', 0, 'dsfsffsdf', 1, 0, 158);
INSERT INTO `ticket_ticketuser` VALUES (736, '', '2021-07-31 16:31:51', '2021-07-31 16:31:51', 0, 'aaaa', 1, 0, 158);
INSERT INTO `ticket_ticketuser` VALUES (737, '', '2021-07-31 16:31:51', '2021-07-31 16:31:51', 0, 'fewf', 1, 0, 158);
INSERT INTO `ticket_ticketuser` VALUES (738, '', '2021-07-31 16:31:52', '2021-07-31 16:31:52', 0, 'admin', 1, 0, 159);
INSERT INTO `ticket_ticketuser` VALUES (739, '', '2021-07-31 16:31:52', '2021-07-31 16:31:52', 0, '23424', 1, 0, 159);
INSERT INTO `ticket_ticketuser` VALUES (740, '', '2021-07-31 16:31:52', '2021-07-31 16:31:52', 0, 'laoshi', 1, 0, 159);
INSERT INTO `ticket_ticketuser` VALUES (741, '', '2021-07-31 16:31:52', '2021-07-31 16:31:52', 0, 'fdsfds', 1, 0, 159);
INSERT INTO `ticket_ticketuser` VALUES (742, '', '2021-07-31 16:31:52', '2021-07-31 16:31:52', 0, 'test', 1, 0, 159);
INSERT INTO `ticket_ticketuser` VALUES (743, '', '2021-07-31 16:31:52', '2021-07-31 16:31:52', 0, 'test2', 1, 0, 159);
INSERT INTO `ticket_ticketuser` VALUES (744, '', '2021-07-31 16:31:52', '2021-07-31 16:31:52', 0, 'test1111', 1, 0, 159);
INSERT INTO `ticket_ticketuser` VALUES (745, '', '2021-07-31 16:31:52', '2021-07-31 16:31:52', 0, 'laoshia', 1, 0, 159);
INSERT INTO `ticket_ticketuser` VALUES (746, '', '2021-07-31 16:31:52', '2021-07-31 16:31:52', 0, '3333', 1, 0, 159);
INSERT INTO `ticket_ticketuser` VALUES (747, '', '2021-07-31 16:31:52', '2021-07-31 16:31:52', 0, 'dsfsffsdf', 1, 0, 159);
INSERT INTO `ticket_ticketuser` VALUES (748, '', '2021-07-31 16:31:52', '2021-07-31 16:31:52', 0, 'aaaa', 1, 0, 159);
INSERT INTO `ticket_ticketuser` VALUES (749, '', '2021-07-31 16:31:52', '2021-07-31 16:31:52', 0, 'fewf', 1, 0, 159);
INSERT INTO `ticket_ticketuser` VALUES (750, '', '2021-07-31 16:31:54', '2021-07-31 16:31:54', 0, 'admin', 1, 0, 160);
INSERT INTO `ticket_ticketuser` VALUES (751, '', '2021-07-31 16:31:54', '2021-07-31 16:31:54', 0, '23424', 1, 0, 160);
INSERT INTO `ticket_ticketuser` VALUES (752, '', '2021-07-31 16:31:54', '2021-07-31 16:31:54', 0, 'laoshi', 1, 0, 160);
INSERT INTO `ticket_ticketuser` VALUES (753, '', '2021-07-31 16:31:54', '2021-07-31 16:31:54', 0, 'fdsfds', 1, 0, 160);
INSERT INTO `ticket_ticketuser` VALUES (754, '', '2021-07-31 16:31:54', '2021-07-31 16:31:54', 0, 'test', 1, 0, 160);
INSERT INTO `ticket_ticketuser` VALUES (755, '', '2021-07-31 16:31:54', '2021-07-31 16:31:54', 0, 'test2', 1, 0, 160);
INSERT INTO `ticket_ticketuser` VALUES (756, '', '2021-07-31 16:31:54', '2021-07-31 16:31:54', 0, 'test1111', 1, 0, 160);
INSERT INTO `ticket_ticketuser` VALUES (757, '', '2021-07-31 16:31:54', '2021-07-31 16:31:54', 0, 'laoshia', 1, 0, 160);
INSERT INTO `ticket_ticketuser` VALUES (758, '', '2021-07-31 16:31:54', '2021-07-31 16:31:54', 0, '3333', 1, 0, 160);
INSERT INTO `ticket_ticketuser` VALUES (759, '', '2021-07-31 16:31:54', '2021-07-31 16:31:54', 0, 'dsfsffsdf', 1, 0, 160);
INSERT INTO `ticket_ticketuser` VALUES (760, '', '2021-07-31 16:31:54', '2021-07-31 16:31:54', 0, 'aaaa', 1, 0, 160);
INSERT INTO `ticket_ticketuser` VALUES (761, '', '2021-07-31 16:31:54', '2021-07-31 16:31:54', 0, 'fewf', 1, 0, 160);
INSERT INTO `ticket_ticketuser` VALUES (762, '', '2021-07-31 16:32:34', '2021-07-31 16:32:33', 0, 'admin', 1, 0, 161);
INSERT INTO `ticket_ticketuser` VALUES (763, '', '2021-07-31 16:32:34', '2021-07-31 16:32:34', 0, '23424', 1, 0, 161);
INSERT INTO `ticket_ticketuser` VALUES (764, '', '2021-07-31 16:32:34', '2021-07-31 16:32:34', 0, 'laoshi', 1, 0, 161);
INSERT INTO `ticket_ticketuser` VALUES (765, '', '2021-07-31 16:32:34', '2021-07-31 16:32:34', 0, 'fdsfds', 1, 0, 161);
INSERT INTO `ticket_ticketuser` VALUES (766, '', '2021-07-31 16:32:34', '2021-07-31 16:32:34', 0, 'test', 1, 0, 161);
INSERT INTO `ticket_ticketuser` VALUES (767, '', '2021-07-31 16:32:34', '2021-07-31 16:32:34', 0, 'test2', 1, 0, 161);
INSERT INTO `ticket_ticketuser` VALUES (768, '', '2021-07-31 16:32:34', '2021-07-31 16:32:34', 0, 'test1111', 1, 0, 161);
INSERT INTO `ticket_ticketuser` VALUES (769, '', '2021-07-31 16:32:34', '2021-07-31 16:32:34', 0, 'laoshia', 1, 0, 161);
INSERT INTO `ticket_ticketuser` VALUES (770, '', '2021-07-31 16:32:34', '2021-07-31 16:32:34', 0, '3333', 1, 0, 161);
INSERT INTO `ticket_ticketuser` VALUES (771, '', '2021-07-31 16:32:34', '2021-07-31 16:32:34', 0, 'dsfsffsdf', 1, 0, 161);
INSERT INTO `ticket_ticketuser` VALUES (772, '', '2021-07-31 16:32:34', '2021-07-31 16:32:34', 0, 'aaaa', 1, 0, 161);
INSERT INTO `ticket_ticketuser` VALUES (773, '', '2021-07-31 16:32:34', '2021-07-31 16:32:34', 0, 'fewf', 1, 0, 161);
INSERT INTO `ticket_ticketuser` VALUES (774, '', '2021-07-31 16:33:25', '2021-07-31 16:33:25', 0, 'admin', 1, 0, 162);
INSERT INTO `ticket_ticketuser` VALUES (775, '', '2021-07-31 16:33:25', '2021-07-31 16:33:25', 0, '23424', 1, 0, 162);
INSERT INTO `ticket_ticketuser` VALUES (776, '', '2021-07-31 16:33:25', '2021-07-31 16:33:25', 0, 'laoshi', 1, 0, 162);
INSERT INTO `ticket_ticketuser` VALUES (777, '', '2021-07-31 16:33:25', '2021-07-31 16:33:25', 0, 'fdsfds', 1, 0, 162);
INSERT INTO `ticket_ticketuser` VALUES (778, '', '2021-07-31 16:33:25', '2021-07-31 16:33:25', 0, 'test', 1, 0, 162);
INSERT INTO `ticket_ticketuser` VALUES (779, '', '2021-07-31 16:33:25', '2021-07-31 16:33:25', 0, 'test2', 1, 0, 162);
INSERT INTO `ticket_ticketuser` VALUES (780, '', '2021-07-31 16:33:25', '2021-07-31 16:33:25', 0, 'test1111', 1, 0, 162);
INSERT INTO `ticket_ticketuser` VALUES (781, '', '2021-07-31 16:33:25', '2021-07-31 16:33:25', 0, 'laoshia', 1, 0, 162);
INSERT INTO `ticket_ticketuser` VALUES (782, '', '2021-07-31 16:33:25', '2021-07-31 16:33:25', 0, '3333', 1, 0, 162);
INSERT INTO `ticket_ticketuser` VALUES (783, '', '2021-07-31 16:33:25', '2021-07-31 16:33:25', 0, 'dsfsffsdf', 1, 0, 162);
INSERT INTO `ticket_ticketuser` VALUES (784, '', '2021-07-31 16:33:25', '2021-07-31 16:33:25', 0, 'aaaa', 1, 0, 162);
INSERT INTO `ticket_ticketuser` VALUES (785, '', '2021-07-31 16:33:25', '2021-07-31 16:33:25', 0, 'fewf', 1, 0, 162);
INSERT INTO `ticket_ticketuser` VALUES (786, '', '2021-07-31 16:34:09', '2021-07-31 17:04:20', 0, 'admin', 1, 1, 163);
INSERT INTO `ticket_ticketuser` VALUES (787, '', '2021-07-31 16:34:09', '2021-07-31 17:04:18', 0, '23424', 0, 0, 163);
INSERT INTO `ticket_ticketuser` VALUES (788, '', '2021-07-31 16:34:09', '2021-07-31 17:04:18', 0, 'laoshi', 0, 0, 163);
INSERT INTO `ticket_ticketuser` VALUES (789, '', '2021-07-31 16:34:09', '2021-07-31 17:04:18', 0, 'fdsfds', 0, 0, 163);
INSERT INTO `ticket_ticketuser` VALUES (790, '', '2021-07-31 16:34:09', '2021-07-31 17:04:18', 0, 'test', 0, 0, 163);
INSERT INTO `ticket_ticketuser` VALUES (791, '', '2021-07-31 16:34:09', '2021-07-31 17:04:18', 0, 'test2', 0, 0, 163);
INSERT INTO `ticket_ticketuser` VALUES (792, '', '2021-07-31 16:34:09', '2021-07-31 17:04:18', 0, 'test1111', 0, 0, 163);
INSERT INTO `ticket_ticketuser` VALUES (793, '', '2021-07-31 16:34:09', '2021-07-31 17:04:18', 0, 'laoshia', 0, 0, 163);
INSERT INTO `ticket_ticketuser` VALUES (794, '', '2021-07-31 16:34:09', '2021-07-31 17:04:18', 0, '3333', 0, 0, 163);
INSERT INTO `ticket_ticketuser` VALUES (795, '', '2021-07-31 16:34:09', '2021-07-31 17:04:18', 0, 'dsfsffsdf', 0, 0, 163);
INSERT INTO `ticket_ticketuser` VALUES (796, '', '2021-07-31 16:34:09', '2021-07-31 17:04:18', 0, 'aaaa', 0, 0, 163);
INSERT INTO `ticket_ticketuser` VALUES (797, '', '2021-07-31 16:34:09', '2021-07-31 17:04:18', 0, 'fewf', 0, 0, 163);
INSERT INTO `ticket_ticketuser` VALUES (798, '', '2021-07-31 16:34:57', '2021-07-31 16:34:56', 0, 'admin', 1, 0, 164);
INSERT INTO `ticket_ticketuser` VALUES (799, '', '2021-07-31 16:34:57', '2021-07-31 16:34:57', 0, '23424', 1, 0, 164);
INSERT INTO `ticket_ticketuser` VALUES (800, '', '2021-07-31 16:34:57', '2021-07-31 16:34:57', 0, 'laoshi', 1, 0, 164);
INSERT INTO `ticket_ticketuser` VALUES (801, '', '2021-07-31 16:34:57', '2021-07-31 16:34:57', 0, 'fdsfds', 1, 0, 164);
INSERT INTO `ticket_ticketuser` VALUES (802, '', '2021-07-31 16:34:57', '2021-07-31 16:34:57', 0, 'test', 1, 0, 164);
INSERT INTO `ticket_ticketuser` VALUES (803, '', '2021-07-31 16:34:57', '2021-07-31 16:34:57', 0, 'test2', 1, 0, 164);
INSERT INTO `ticket_ticketuser` VALUES (804, '', '2021-07-31 16:34:57', '2021-07-31 16:34:57', 0, 'test1111', 1, 0, 164);
INSERT INTO `ticket_ticketuser` VALUES (805, '', '2021-07-31 16:34:57', '2021-07-31 16:34:57', 0, 'laoshia', 1, 0, 164);
INSERT INTO `ticket_ticketuser` VALUES (806, '', '2021-07-31 16:34:57', '2021-07-31 16:34:57', 0, '3333', 1, 0, 164);
INSERT INTO `ticket_ticketuser` VALUES (807, '', '2021-07-31 16:34:57', '2021-07-31 16:34:57', 0, 'dsfsffsdf', 1, 0, 164);
INSERT INTO `ticket_ticketuser` VALUES (808, '', '2021-07-31 16:34:57', '2021-07-31 16:34:57', 0, 'aaaa', 1, 0, 164);
INSERT INTO `ticket_ticketuser` VALUES (809, '', '2021-07-31 16:34:57', '2021-07-31 16:34:57', 0, 'fewf', 1, 0, 164);
INSERT INTO `ticket_ticketuser` VALUES (810, '', '2021-07-31 16:36:11', '2021-07-31 16:36:11', 0, 'admin', 1, 0, 165);
INSERT INTO `ticket_ticketuser` VALUES (811, '', '2021-07-31 16:36:11', '2021-07-31 16:36:11', 0, '23424', 1, 0, 165);
INSERT INTO `ticket_ticketuser` VALUES (812, '', '2021-07-31 16:36:11', '2021-07-31 16:36:11', 0, 'laoshi', 1, 0, 165);
INSERT INTO `ticket_ticketuser` VALUES (813, '', '2021-07-31 16:36:11', '2021-07-31 16:36:11', 0, 'fdsfds', 1, 0, 165);
INSERT INTO `ticket_ticketuser` VALUES (814, '', '2021-07-31 16:36:11', '2021-07-31 16:36:11', 0, 'test', 1, 0, 165);
INSERT INTO `ticket_ticketuser` VALUES (815, '', '2021-07-31 16:36:11', '2021-07-31 16:36:11', 0, 'test2', 1, 0, 165);
INSERT INTO `ticket_ticketuser` VALUES (816, '', '2021-07-31 16:36:11', '2021-07-31 16:36:11', 0, 'test1111', 1, 0, 165);
INSERT INTO `ticket_ticketuser` VALUES (817, '', '2021-07-31 16:36:11', '2021-07-31 16:36:11', 0, 'laoshia', 1, 0, 165);
INSERT INTO `ticket_ticketuser` VALUES (818, '', '2021-07-31 16:36:11', '2021-07-31 16:36:11', 0, '3333', 1, 0, 165);
INSERT INTO `ticket_ticketuser` VALUES (819, '', '2021-07-31 16:36:11', '2021-07-31 16:36:11', 0, 'dsfsffsdf', 1, 0, 165);
INSERT INTO `ticket_ticketuser` VALUES (820, '', '2021-07-31 16:36:11', '2021-07-31 16:36:11', 0, 'aaaa', 1, 0, 165);
INSERT INTO `ticket_ticketuser` VALUES (821, '', '2021-07-31 16:36:11', '2021-07-31 16:36:11', 0, 'fewf', 1, 0, 165);
INSERT INTO `ticket_ticketuser` VALUES (822, '', '2021-07-31 16:36:14', '2021-07-31 16:36:14', 0, 'admin', 1, 0, 166);
INSERT INTO `ticket_ticketuser` VALUES (823, '', '2021-07-31 16:36:14', '2021-07-31 16:36:14', 0, '23424', 1, 0, 166);
INSERT INTO `ticket_ticketuser` VALUES (824, '', '2021-07-31 16:36:14', '2021-07-31 16:36:14', 0, 'laoshi', 1, 0, 166);
INSERT INTO `ticket_ticketuser` VALUES (825, '', '2021-07-31 16:36:14', '2021-07-31 16:36:14', 0, 'fdsfds', 1, 0, 166);
INSERT INTO `ticket_ticketuser` VALUES (826, '', '2021-07-31 16:36:14', '2021-07-31 16:36:14', 0, 'test', 1, 0, 166);
INSERT INTO `ticket_ticketuser` VALUES (827, '', '2021-07-31 16:36:14', '2021-07-31 16:36:14', 0, 'test2', 1, 0, 166);
INSERT INTO `ticket_ticketuser` VALUES (828, '', '2021-07-31 16:36:14', '2021-07-31 16:36:14', 0, 'test1111', 1, 0, 166);
INSERT INTO `ticket_ticketuser` VALUES (829, '', '2021-07-31 16:36:14', '2021-07-31 16:36:14', 0, 'laoshia', 1, 0, 166);
INSERT INTO `ticket_ticketuser` VALUES (830, '', '2021-07-31 16:36:14', '2021-07-31 16:36:14', 0, '3333', 1, 0, 166);
INSERT INTO `ticket_ticketuser` VALUES (831, '', '2021-07-31 16:36:14', '2021-07-31 16:36:14', 0, 'dsfsffsdf', 1, 0, 166);
INSERT INTO `ticket_ticketuser` VALUES (832, '', '2021-07-31 16:36:14', '2021-07-31 16:36:14', 0, 'aaaa', 1, 0, 166);
INSERT INTO `ticket_ticketuser` VALUES (833, '', '2021-07-31 16:36:14', '2021-07-31 16:36:14', 0, 'fewf', 1, 0, 166);
INSERT INTO `ticket_ticketuser` VALUES (834, '', '2021-07-31 16:36:23', '2021-07-31 16:36:23', 0, 'admin', 1, 0, 167);
INSERT INTO `ticket_ticketuser` VALUES (835, '', '2021-07-31 16:36:23', '2021-07-31 16:36:23', 0, '23424', 1, 0, 167);
INSERT INTO `ticket_ticketuser` VALUES (836, '', '2021-07-31 16:36:23', '2021-07-31 16:36:23', 0, 'laoshi', 1, 0, 167);
INSERT INTO `ticket_ticketuser` VALUES (837, '', '2021-07-31 16:36:23', '2021-07-31 16:36:23', 0, 'fdsfds', 1, 0, 167);
INSERT INTO `ticket_ticketuser` VALUES (838, '', '2021-07-31 16:36:23', '2021-07-31 16:36:23', 0, 'test', 1, 0, 167);
INSERT INTO `ticket_ticketuser` VALUES (839, '', '2021-07-31 16:36:23', '2021-07-31 16:36:23', 0, 'test2', 1, 0, 167);
INSERT INTO `ticket_ticketuser` VALUES (840, '', '2021-07-31 16:36:23', '2021-07-31 16:36:23', 0, 'test1111', 1, 0, 167);
INSERT INTO `ticket_ticketuser` VALUES (841, '', '2021-07-31 16:36:23', '2021-07-31 16:36:23', 0, 'laoshia', 1, 0, 167);
INSERT INTO `ticket_ticketuser` VALUES (842, '', '2021-07-31 16:36:23', '2021-07-31 16:36:23', 0, '3333', 1, 0, 167);
INSERT INTO `ticket_ticketuser` VALUES (843, '', '2021-07-31 16:36:23', '2021-07-31 16:36:23', 0, 'dsfsffsdf', 1, 0, 167);
INSERT INTO `ticket_ticketuser` VALUES (844, '', '2021-07-31 16:36:23', '2021-07-31 16:36:23', 0, 'aaaa', 1, 0, 167);
INSERT INTO `ticket_ticketuser` VALUES (845, '', '2021-07-31 16:36:23', '2021-07-31 16:36:23', 0, 'fewf', 1, 0, 167);
INSERT INTO `ticket_ticketuser` VALUES (846, '', '2021-07-31 16:36:47', '2021-07-31 16:36:46', 0, 'admin', 1, 0, 168);
INSERT INTO `ticket_ticketuser` VALUES (847, '', '2021-07-31 16:36:47', '2021-07-31 16:58:53', 0, '23424', 0, 0, 168);
INSERT INTO `ticket_ticketuser` VALUES (848, '', '2021-07-31 16:36:47', '2021-07-31 16:58:53', 0, 'laoshi', 0, 0, 168);
INSERT INTO `ticket_ticketuser` VALUES (849, '', '2021-07-31 16:36:47', '2021-07-31 16:58:53', 0, 'fdsfds', 0, 0, 168);
INSERT INTO `ticket_ticketuser` VALUES (850, '', '2021-07-31 16:36:47', '2021-07-31 16:58:53', 0, 'test', 0, 0, 168);
INSERT INTO `ticket_ticketuser` VALUES (851, '', '2021-07-31 16:36:47', '2021-07-31 16:58:53', 0, 'test2', 0, 0, 168);
INSERT INTO `ticket_ticketuser` VALUES (852, '', '2021-07-31 16:36:47', '2021-07-31 16:58:53', 0, 'test1111', 0, 0, 168);
INSERT INTO `ticket_ticketuser` VALUES (853, '', '2021-07-31 16:36:47', '2021-07-31 16:58:53', 0, 'laoshia', 0, 0, 168);
INSERT INTO `ticket_ticketuser` VALUES (854, '', '2021-07-31 16:36:47', '2021-07-31 16:58:53', 0, '3333', 0, 0, 168);
INSERT INTO `ticket_ticketuser` VALUES (855, '', '2021-07-31 16:36:47', '2021-07-31 16:58:53', 0, 'dsfsffsdf', 0, 0, 168);
INSERT INTO `ticket_ticketuser` VALUES (856, '', '2021-07-31 16:36:47', '2021-07-31 16:58:53', 0, 'aaaa', 0, 0, 168);
INSERT INTO `ticket_ticketuser` VALUES (857, '', '2021-07-31 16:36:47', '2021-07-31 16:58:53', 0, 'fewf', 0, 0, 168);
INSERT INTO `ticket_ticketuser` VALUES (858, '', '2021-07-31 16:37:04', '2021-07-31 16:37:03', 0, 'admin', 1, 0, 169);
INSERT INTO `ticket_ticketuser` VALUES (859, '', '2021-07-31 16:37:04', '2021-07-31 16:37:04', 0, '23424', 1, 0, 169);
INSERT INTO `ticket_ticketuser` VALUES (860, '', '2021-07-31 16:37:04', '2021-07-31 16:37:04', 0, 'laoshi', 1, 0, 169);
INSERT INTO `ticket_ticketuser` VALUES (861, '', '2021-07-31 16:37:04', '2021-07-31 16:37:04', 0, 'fdsfds', 1, 0, 169);
INSERT INTO `ticket_ticketuser` VALUES (862, '', '2021-07-31 16:37:04', '2021-07-31 16:37:04', 0, 'test', 1, 0, 169);
INSERT INTO `ticket_ticketuser` VALUES (863, '', '2021-07-31 16:37:04', '2021-07-31 16:37:04', 0, 'test2', 1, 0, 169);
INSERT INTO `ticket_ticketuser` VALUES (864, '', '2021-07-31 16:37:04', '2021-07-31 16:37:04', 0, 'test1111', 1, 0, 169);
INSERT INTO `ticket_ticketuser` VALUES (865, '', '2021-07-31 16:37:04', '2021-07-31 16:37:04', 0, 'laoshia', 1, 0, 169);
INSERT INTO `ticket_ticketuser` VALUES (866, '', '2021-07-31 16:37:04', '2021-07-31 16:37:04', 0, '3333', 1, 0, 169);
INSERT INTO `ticket_ticketuser` VALUES (867, '', '2021-07-31 16:37:04', '2021-07-31 16:37:04', 0, 'dsfsffsdf', 1, 0, 169);
INSERT INTO `ticket_ticketuser` VALUES (868, '', '2021-07-31 16:37:04', '2021-07-31 16:37:04', 0, 'aaaa', 1, 0, 169);
INSERT INTO `ticket_ticketuser` VALUES (869, '', '2021-07-31 16:37:04', '2021-07-31 16:37:04', 0, 'fewf', 1, 0, 169);
INSERT INTO `ticket_ticketuser` VALUES (870, '', '2021-07-31 16:39:46', '2021-07-31 16:39:46', 0, 'admin', 1, 0, 170);
INSERT INTO `ticket_ticketuser` VALUES (871, '', '2021-07-31 16:39:46', '2021-07-31 16:39:46', 0, '23424', 1, 0, 170);
INSERT INTO `ticket_ticketuser` VALUES (872, '', '2021-07-31 16:39:46', '2021-07-31 16:39:46', 0, 'laoshi', 1, 0, 170);
INSERT INTO `ticket_ticketuser` VALUES (873, '', '2021-07-31 16:39:46', '2021-07-31 16:39:46', 0, 'fdsfds', 1, 0, 170);
INSERT INTO `ticket_ticketuser` VALUES (874, '', '2021-07-31 16:39:46', '2021-07-31 16:39:46', 0, 'test', 1, 0, 170);
INSERT INTO `ticket_ticketuser` VALUES (875, '', '2021-07-31 16:39:46', '2021-07-31 16:39:46', 0, 'test2', 1, 0, 170);
INSERT INTO `ticket_ticketuser` VALUES (876, '', '2021-07-31 16:39:46', '2021-07-31 16:39:46', 0, 'test1111', 1, 0, 170);
INSERT INTO `ticket_ticketuser` VALUES (877, '', '2021-07-31 16:39:46', '2021-07-31 16:39:46', 0, 'laoshia', 1, 0, 170);
INSERT INTO `ticket_ticketuser` VALUES (878, '', '2021-07-31 16:39:46', '2021-07-31 16:39:46', 0, '3333', 1, 0, 170);
INSERT INTO `ticket_ticketuser` VALUES (879, '', '2021-07-31 16:39:46', '2021-07-31 16:39:46', 0, 'dsfsffsdf', 1, 0, 170);
INSERT INTO `ticket_ticketuser` VALUES (880, '', '2021-07-31 16:39:46', '2021-07-31 16:39:46', 0, 'aaaa', 1, 0, 170);
INSERT INTO `ticket_ticketuser` VALUES (881, '', '2021-07-31 16:39:46', '2021-07-31 16:39:46', 0, 'fewf', 1, 0, 170);
INSERT INTO `ticket_ticketuser` VALUES (882, '', '2021-07-31 16:39:47', '2021-07-31 16:39:46', 0, 'admin', 1, 0, 171);
INSERT INTO `ticket_ticketuser` VALUES (883, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, '23424', 1, 0, 171);
INSERT INTO `ticket_ticketuser` VALUES (884, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'laoshi', 1, 0, 171);
INSERT INTO `ticket_ticketuser` VALUES (885, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'fdsfds', 1, 0, 171);
INSERT INTO `ticket_ticketuser` VALUES (886, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'test', 1, 0, 171);
INSERT INTO `ticket_ticketuser` VALUES (887, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'test2', 1, 0, 171);
INSERT INTO `ticket_ticketuser` VALUES (888, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'test1111', 1, 0, 171);
INSERT INTO `ticket_ticketuser` VALUES (889, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'laoshia', 1, 0, 171);
INSERT INTO `ticket_ticketuser` VALUES (890, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, '3333', 1, 0, 171);
INSERT INTO `ticket_ticketuser` VALUES (891, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'dsfsffsdf', 1, 0, 171);
INSERT INTO `ticket_ticketuser` VALUES (892, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'aaaa', 1, 0, 171);
INSERT INTO `ticket_ticketuser` VALUES (893, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'fewf', 1, 0, 171);
INSERT INTO `ticket_ticketuser` VALUES (894, '', '2021-07-31 16:39:47', '2021-07-31 16:39:46', 0, 'admin', 1, 0, 172);
INSERT INTO `ticket_ticketuser` VALUES (895, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, '23424', 1, 0, 172);
INSERT INTO `ticket_ticketuser` VALUES (896, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'laoshi', 1, 0, 172);
INSERT INTO `ticket_ticketuser` VALUES (897, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'fdsfds', 1, 0, 172);
INSERT INTO `ticket_ticketuser` VALUES (898, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'test', 1, 0, 172);
INSERT INTO `ticket_ticketuser` VALUES (899, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'test2', 1, 0, 172);
INSERT INTO `ticket_ticketuser` VALUES (900, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'test1111', 1, 0, 172);
INSERT INTO `ticket_ticketuser` VALUES (901, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'laoshia', 1, 0, 172);
INSERT INTO `ticket_ticketuser` VALUES (902, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, '3333', 1, 0, 172);
INSERT INTO `ticket_ticketuser` VALUES (903, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'dsfsffsdf', 1, 0, 172);
INSERT INTO `ticket_ticketuser` VALUES (904, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'aaaa', 1, 0, 172);
INSERT INTO `ticket_ticketuser` VALUES (905, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'fewf', 1, 0, 172);
INSERT INTO `ticket_ticketuser` VALUES (906, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'admin', 1, 0, 173);
INSERT INTO `ticket_ticketuser` VALUES (907, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, '23424', 1, 0, 173);
INSERT INTO `ticket_ticketuser` VALUES (908, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'laoshi', 1, 0, 173);
INSERT INTO `ticket_ticketuser` VALUES (909, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'fdsfds', 1, 0, 173);
INSERT INTO `ticket_ticketuser` VALUES (910, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'test', 1, 0, 173);
INSERT INTO `ticket_ticketuser` VALUES (911, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'test2', 1, 0, 173);
INSERT INTO `ticket_ticketuser` VALUES (912, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'test1111', 1, 0, 173);
INSERT INTO `ticket_ticketuser` VALUES (913, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'laoshia', 1, 0, 173);
INSERT INTO `ticket_ticketuser` VALUES (914, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, '3333', 1, 0, 173);
INSERT INTO `ticket_ticketuser` VALUES (915, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'dsfsffsdf', 1, 0, 173);
INSERT INTO `ticket_ticketuser` VALUES (916, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'aaaa', 1, 0, 173);
INSERT INTO `ticket_ticketuser` VALUES (917, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'fewf', 1, 0, 173);
INSERT INTO `ticket_ticketuser` VALUES (918, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'admin', 1, 0, 174);
INSERT INTO `ticket_ticketuser` VALUES (919, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, '23424', 1, 0, 174);
INSERT INTO `ticket_ticketuser` VALUES (920, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'laoshi', 1, 0, 174);
INSERT INTO `ticket_ticketuser` VALUES (921, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'fdsfds', 1, 0, 174);
INSERT INTO `ticket_ticketuser` VALUES (922, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'test', 1, 0, 174);
INSERT INTO `ticket_ticketuser` VALUES (923, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'test2', 1, 0, 174);
INSERT INTO `ticket_ticketuser` VALUES (924, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'test1111', 1, 0, 174);
INSERT INTO `ticket_ticketuser` VALUES (925, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'laoshia', 1, 0, 174);
INSERT INTO `ticket_ticketuser` VALUES (926, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, '3333', 1, 0, 174);
INSERT INTO `ticket_ticketuser` VALUES (927, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'dsfsffsdf', 1, 0, 174);
INSERT INTO `ticket_ticketuser` VALUES (928, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'aaaa', 1, 0, 174);
INSERT INTO `ticket_ticketuser` VALUES (929, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'fewf', 1, 0, 174);
INSERT INTO `ticket_ticketuser` VALUES (930, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'admin', 1, 0, 175);
INSERT INTO `ticket_ticketuser` VALUES (931, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, '23424', 1, 0, 175);
INSERT INTO `ticket_ticketuser` VALUES (932, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'laoshi', 1, 0, 175);
INSERT INTO `ticket_ticketuser` VALUES (933, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'fdsfds', 1, 0, 175);
INSERT INTO `ticket_ticketuser` VALUES (934, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'test', 1, 0, 175);
INSERT INTO `ticket_ticketuser` VALUES (935, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'test2', 1, 0, 175);
INSERT INTO `ticket_ticketuser` VALUES (936, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'test1111', 1, 0, 175);
INSERT INTO `ticket_ticketuser` VALUES (937, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'laoshia', 1, 0, 175);
INSERT INTO `ticket_ticketuser` VALUES (938, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, '3333', 1, 0, 175);
INSERT INTO `ticket_ticketuser` VALUES (939, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'dsfsffsdf', 1, 0, 175);
INSERT INTO `ticket_ticketuser` VALUES (940, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'aaaa', 1, 0, 175);
INSERT INTO `ticket_ticketuser` VALUES (941, '', '2021-07-31 16:39:47', '2021-07-31 16:39:47', 0, 'fewf', 1, 0, 175);
INSERT INTO `ticket_ticketuser` VALUES (942, '', '2021-07-31 16:39:48', '2021-07-31 16:39:47', 0, 'admin', 1, 0, 176);
INSERT INTO `ticket_ticketuser` VALUES (943, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, '23424', 1, 0, 176);
INSERT INTO `ticket_ticketuser` VALUES (944, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'laoshi', 1, 0, 176);
INSERT INTO `ticket_ticketuser` VALUES (945, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'fdsfds', 1, 0, 176);
INSERT INTO `ticket_ticketuser` VALUES (946, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'test', 1, 0, 176);
INSERT INTO `ticket_ticketuser` VALUES (947, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'test2', 1, 0, 176);
INSERT INTO `ticket_ticketuser` VALUES (948, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'test1111', 1, 0, 176);
INSERT INTO `ticket_ticketuser` VALUES (949, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'laoshia', 1, 0, 176);
INSERT INTO `ticket_ticketuser` VALUES (950, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, '3333', 1, 0, 176);
INSERT INTO `ticket_ticketuser` VALUES (951, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'dsfsffsdf', 1, 0, 176);
INSERT INTO `ticket_ticketuser` VALUES (952, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'aaaa', 1, 0, 176);
INSERT INTO `ticket_ticketuser` VALUES (953, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'fewf', 1, 0, 176);
INSERT INTO `ticket_ticketuser` VALUES (954, '', '2021-07-31 16:39:48', '2021-07-31 16:39:47', 0, 'admin', 1, 0, 177);
INSERT INTO `ticket_ticketuser` VALUES (955, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, '23424', 1, 0, 177);
INSERT INTO `ticket_ticketuser` VALUES (956, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'laoshi', 1, 0, 177);
INSERT INTO `ticket_ticketuser` VALUES (957, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'fdsfds', 1, 0, 177);
INSERT INTO `ticket_ticketuser` VALUES (958, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'test', 1, 0, 177);
INSERT INTO `ticket_ticketuser` VALUES (959, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'test2', 1, 0, 177);
INSERT INTO `ticket_ticketuser` VALUES (960, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'test1111', 1, 0, 177);
INSERT INTO `ticket_ticketuser` VALUES (961, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'laoshia', 1, 0, 177);
INSERT INTO `ticket_ticketuser` VALUES (962, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, '3333', 1, 0, 177);
INSERT INTO `ticket_ticketuser` VALUES (963, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'dsfsffsdf', 1, 0, 177);
INSERT INTO `ticket_ticketuser` VALUES (964, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'aaaa', 1, 0, 177);
INSERT INTO `ticket_ticketuser` VALUES (965, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'fewf', 1, 0, 177);
INSERT INTO `ticket_ticketuser` VALUES (966, '', '2021-07-31 16:39:48', '2021-07-31 16:39:47', 0, 'admin', 1, 0, 178);
INSERT INTO `ticket_ticketuser` VALUES (967, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, '23424', 1, 0, 178);
INSERT INTO `ticket_ticketuser` VALUES (968, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'laoshi', 1, 0, 178);
INSERT INTO `ticket_ticketuser` VALUES (969, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'fdsfds', 1, 0, 178);
INSERT INTO `ticket_ticketuser` VALUES (970, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'test', 1, 0, 178);
INSERT INTO `ticket_ticketuser` VALUES (971, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'test2', 1, 0, 178);
INSERT INTO `ticket_ticketuser` VALUES (972, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'test1111', 1, 0, 178);
INSERT INTO `ticket_ticketuser` VALUES (973, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'laoshia', 1, 0, 178);
INSERT INTO `ticket_ticketuser` VALUES (974, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, '3333', 1, 0, 178);
INSERT INTO `ticket_ticketuser` VALUES (975, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'dsfsffsdf', 1, 0, 178);
INSERT INTO `ticket_ticketuser` VALUES (976, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'aaaa', 1, 0, 178);
INSERT INTO `ticket_ticketuser` VALUES (977, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'fewf', 1, 0, 178);
INSERT INTO `ticket_ticketuser` VALUES (978, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'admin', 1, 0, 179);
INSERT INTO `ticket_ticketuser` VALUES (979, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, '23424', 1, 0, 179);
INSERT INTO `ticket_ticketuser` VALUES (980, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'laoshi', 1, 0, 179);
INSERT INTO `ticket_ticketuser` VALUES (981, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'fdsfds', 1, 0, 179);
INSERT INTO `ticket_ticketuser` VALUES (982, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'test', 1, 0, 179);
INSERT INTO `ticket_ticketuser` VALUES (983, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'test2', 1, 0, 179);
INSERT INTO `ticket_ticketuser` VALUES (984, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'test1111', 1, 0, 179);
INSERT INTO `ticket_ticketuser` VALUES (985, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'laoshia', 1, 0, 179);
INSERT INTO `ticket_ticketuser` VALUES (986, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, '3333', 1, 0, 179);
INSERT INTO `ticket_ticketuser` VALUES (987, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'dsfsffsdf', 1, 0, 179);
INSERT INTO `ticket_ticketuser` VALUES (988, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'aaaa', 1, 0, 179);
INSERT INTO `ticket_ticketuser` VALUES (989, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'fewf', 1, 0, 179);
INSERT INTO `ticket_ticketuser` VALUES (990, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'admin', 1, 0, 180);
INSERT INTO `ticket_ticketuser` VALUES (991, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, '23424', 1, 0, 180);
INSERT INTO `ticket_ticketuser` VALUES (992, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'laoshi', 1, 0, 180);
INSERT INTO `ticket_ticketuser` VALUES (993, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'fdsfds', 1, 0, 180);
INSERT INTO `ticket_ticketuser` VALUES (994, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'test', 1, 0, 180);
INSERT INTO `ticket_ticketuser` VALUES (995, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'test2', 1, 0, 180);
INSERT INTO `ticket_ticketuser` VALUES (996, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'test1111', 1, 0, 180);
INSERT INTO `ticket_ticketuser` VALUES (997, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'laoshia', 1, 0, 180);
INSERT INTO `ticket_ticketuser` VALUES (998, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, '3333', 1, 0, 180);
INSERT INTO `ticket_ticketuser` VALUES (999, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'dsfsffsdf', 1, 0, 180);
INSERT INTO `ticket_ticketuser` VALUES (1000, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'aaaa', 1, 0, 180);
INSERT INTO `ticket_ticketuser` VALUES (1001, '', '2021-07-31 16:39:48', '2021-07-31 16:39:48', 0, 'fewf', 1, 0, 180);
INSERT INTO `ticket_ticketuser` VALUES (1002, '', '2021-07-31 16:39:48', '2021-07-31 16:54:24', 0, 'admin', 0, 0, 181);
INSERT INTO `ticket_ticketuser` VALUES (1003, '', '2021-07-31 16:39:48', '2021-07-31 16:54:24', 0, '23424', 0, 0, 181);
INSERT INTO `ticket_ticketuser` VALUES (1004, '', '2021-07-31 16:39:48', '2021-07-31 16:54:24', 0, 'laoshi', 0, 0, 181);
INSERT INTO `ticket_ticketuser` VALUES (1005, '', '2021-07-31 16:39:48', '2021-07-31 16:54:24', 0, 'fdsfds', 0, 0, 181);
INSERT INTO `ticket_ticketuser` VALUES (1006, '', '2021-07-31 16:39:48', '2021-07-31 16:54:24', 0, 'test', 0, 0, 181);
INSERT INTO `ticket_ticketuser` VALUES (1007, '', '2021-07-31 16:39:48', '2021-07-31 16:54:24', 0, 'test2', 0, 0, 181);
INSERT INTO `ticket_ticketuser` VALUES (1008, '', '2021-07-31 16:39:48', '2021-07-31 16:54:24', 0, 'test1111', 0, 0, 181);
INSERT INTO `ticket_ticketuser` VALUES (1009, '', '2021-07-31 16:39:48', '2021-07-31 16:54:24', 0, 'laoshia', 0, 0, 181);
INSERT INTO `ticket_ticketuser` VALUES (1010, '', '2021-07-31 16:39:48', '2021-07-31 16:54:24', 0, '3333', 0, 0, 181);
INSERT INTO `ticket_ticketuser` VALUES (1011, '', '2021-07-31 16:39:48', '2021-07-31 16:54:24', 0, 'dsfsffsdf', 0, 0, 181);
INSERT INTO `ticket_ticketuser` VALUES (1012, '', '2021-07-31 16:39:48', '2021-07-31 16:54:24', 0, 'aaaa', 0, 0, 181);
INSERT INTO `ticket_ticketuser` VALUES (1013, '', '2021-07-31 16:39:48', '2021-07-31 16:54:24', 0, 'fewf', 0, 0, 181);
INSERT INTO `ticket_ticketuser` VALUES (1014, '', '2021-07-31 16:39:49', '2021-07-31 16:53:12', 0, 'admin', 0, 0, 182);
INSERT INTO `ticket_ticketuser` VALUES (1015, '', '2021-07-31 16:39:49', '2021-07-31 16:53:12', 0, '23424', 0, 0, 182);
INSERT INTO `ticket_ticketuser` VALUES (1016, '', '2021-07-31 16:39:49', '2021-07-31 16:53:12', 0, 'laoshi', 0, 0, 182);
INSERT INTO `ticket_ticketuser` VALUES (1017, '', '2021-07-31 16:39:49', '2021-07-31 16:53:12', 0, 'fdsfds', 0, 0, 182);
INSERT INTO `ticket_ticketuser` VALUES (1018, '', '2021-07-31 16:39:49', '2021-07-31 16:53:12', 0, 'test', 0, 0, 182);
INSERT INTO `ticket_ticketuser` VALUES (1019, '', '2021-07-31 16:39:49', '2021-07-31 16:53:12', 0, 'test2', 0, 0, 182);
INSERT INTO `ticket_ticketuser` VALUES (1020, '', '2021-07-31 16:39:49', '2021-07-31 16:53:12', 0, 'test1111', 0, 0, 182);
INSERT INTO `ticket_ticketuser` VALUES (1021, '', '2021-07-31 16:39:49', '2021-07-31 16:53:12', 0, 'laoshia', 0, 0, 182);
INSERT INTO `ticket_ticketuser` VALUES (1022, '', '2021-07-31 16:39:49', '2021-07-31 16:53:12', 0, '3333', 0, 0, 182);
INSERT INTO `ticket_ticketuser` VALUES (1023, '', '2021-07-31 16:39:49', '2021-07-31 16:53:12', 0, 'dsfsffsdf', 0, 0, 182);
INSERT INTO `ticket_ticketuser` VALUES (1024, '', '2021-07-31 16:39:49', '2021-07-31 16:53:12', 0, 'aaaa', 0, 0, 182);
INSERT INTO `ticket_ticketuser` VALUES (1025, '', '2021-07-31 16:39:49', '2021-07-31 16:53:12', 0, 'fewf', 0, 0, 182);
INSERT INTO `ticket_ticketuser` VALUES (1026, '', '2021-07-31 17:27:27', '2021-07-31 17:27:26', 0, 'admin', 1, 0, 183);
INSERT INTO `ticket_ticketuser` VALUES (1027, '', '2021-07-31 17:27:27', '2021-07-31 17:27:27', 0, '23424', 1, 0, 183);
INSERT INTO `ticket_ticketuser` VALUES (1028, '', '2021-07-31 17:27:27', '2021-07-31 17:27:27', 0, 'laoshi', 1, 0, 183);
INSERT INTO `ticket_ticketuser` VALUES (1029, '', '2021-07-31 17:27:27', '2021-07-31 17:27:27', 0, 'fdsfds', 1, 0, 183);
INSERT INTO `ticket_ticketuser` VALUES (1030, '', '2021-07-31 17:27:27', '2021-07-31 17:27:27', 0, 'test', 1, 0, 183);
INSERT INTO `ticket_ticketuser` VALUES (1031, '', '2021-07-31 17:27:27', '2021-07-31 17:27:27', 0, 'test2', 1, 0, 183);
INSERT INTO `ticket_ticketuser` VALUES (1032, '', '2021-07-31 17:27:27', '2021-07-31 17:27:27', 0, 'test1111', 1, 0, 183);
INSERT INTO `ticket_ticketuser` VALUES (1033, '', '2021-07-31 17:27:27', '2021-07-31 17:27:27', 0, 'laoshia', 1, 0, 183);
INSERT INTO `ticket_ticketuser` VALUES (1034, '', '2021-07-31 17:27:27', '2021-07-31 17:27:27', 0, '3333', 1, 0, 183);
INSERT INTO `ticket_ticketuser` VALUES (1035, '', '2021-07-31 17:27:27', '2021-07-31 17:27:27', 0, 'dsfsffsdf', 1, 0, 183);
INSERT INTO `ticket_ticketuser` VALUES (1036, '', '2021-07-31 17:27:27', '2021-07-31 17:27:27', 0, 'aaaa', 1, 0, 183);
INSERT INTO `ticket_ticketuser` VALUES (1037, '', '2021-07-31 17:27:27', '2021-07-31 17:27:27', 0, 'fewf', 1, 0, 183);
INSERT INTO `ticket_ticketuser` VALUES (1038, '', '2021-07-31 17:27:45', '2021-07-31 17:27:44', 0, 'admin', 1, 0, 184);
INSERT INTO `ticket_ticketuser` VALUES (1039, '', '2021-07-31 17:27:45', '2021-07-31 17:27:45', 0, '23424', 1, 0, 184);
INSERT INTO `ticket_ticketuser` VALUES (1040, '', '2021-07-31 17:27:45', '2021-07-31 17:27:45', 0, 'laoshi', 1, 0, 184);
INSERT INTO `ticket_ticketuser` VALUES (1041, '', '2021-07-31 17:27:45', '2021-07-31 17:27:45', 0, 'fdsfds', 1, 0, 184);
INSERT INTO `ticket_ticketuser` VALUES (1042, '', '2021-07-31 17:27:45', '2021-07-31 17:27:45', 0, 'test', 1, 0, 184);
INSERT INTO `ticket_ticketuser` VALUES (1043, '', '2021-07-31 17:27:45', '2021-07-31 17:27:45', 0, 'test2', 1, 0, 184);
INSERT INTO `ticket_ticketuser` VALUES (1044, '', '2021-07-31 17:27:45', '2021-07-31 17:27:45', 0, 'test1111', 1, 0, 184);
INSERT INTO `ticket_ticketuser` VALUES (1045, '', '2021-07-31 17:27:45', '2021-07-31 17:27:45', 0, 'laoshia', 1, 0, 184);
INSERT INTO `ticket_ticketuser` VALUES (1046, '', '2021-07-31 17:27:45', '2021-07-31 17:27:45', 0, '3333', 1, 0, 184);
INSERT INTO `ticket_ticketuser` VALUES (1047, '', '2021-07-31 17:27:45', '2021-07-31 17:27:45', 0, 'dsfsffsdf', 1, 0, 184);
INSERT INTO `ticket_ticketuser` VALUES (1048, '', '2021-07-31 17:27:45', '2021-07-31 17:27:45', 0, 'aaaa', 1, 0, 184);
INSERT INTO `ticket_ticketuser` VALUES (1049, '', '2021-07-31 17:27:45', '2021-07-31 17:27:45', 0, 'fewf', 1, 0, 184);
INSERT INTO `ticket_ticketuser` VALUES (1050, '', '2021-07-31 17:28:18', '2021-07-31 17:28:17', 0, 'admin', 1, 0, 185);
INSERT INTO `ticket_ticketuser` VALUES (1051, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, '23424', 1, 0, 185);
INSERT INTO `ticket_ticketuser` VALUES (1052, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, 'laoshi', 1, 0, 185);
INSERT INTO `ticket_ticketuser` VALUES (1053, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, 'fdsfds', 1, 0, 185);
INSERT INTO `ticket_ticketuser` VALUES (1054, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, 'test', 1, 0, 185);
INSERT INTO `ticket_ticketuser` VALUES (1055, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, 'test2', 1, 0, 185);
INSERT INTO `ticket_ticketuser` VALUES (1056, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, 'test1111', 1, 0, 185);
INSERT INTO `ticket_ticketuser` VALUES (1057, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, 'laoshia', 1, 0, 185);
INSERT INTO `ticket_ticketuser` VALUES (1058, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, '3333', 1, 0, 185);
INSERT INTO `ticket_ticketuser` VALUES (1059, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, 'dsfsffsdf', 1, 0, 185);
INSERT INTO `ticket_ticketuser` VALUES (1060, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, 'aaaa', 1, 0, 185);
INSERT INTO `ticket_ticketuser` VALUES (1061, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, 'fewf', 1, 0, 185);
INSERT INTO `ticket_ticketuser` VALUES (1062, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, 'admin', 1, 0, 186);
INSERT INTO `ticket_ticketuser` VALUES (1063, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, '23424', 1, 0, 186);
INSERT INTO `ticket_ticketuser` VALUES (1064, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, 'laoshi', 1, 0, 186);
INSERT INTO `ticket_ticketuser` VALUES (1065, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, 'fdsfds', 1, 0, 186);
INSERT INTO `ticket_ticketuser` VALUES (1066, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, 'test', 1, 0, 186);
INSERT INTO `ticket_ticketuser` VALUES (1067, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, 'test2', 1, 0, 186);
INSERT INTO `ticket_ticketuser` VALUES (1068, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, 'test1111', 1, 0, 186);
INSERT INTO `ticket_ticketuser` VALUES (1069, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, 'laoshia', 1, 0, 186);
INSERT INTO `ticket_ticketuser` VALUES (1070, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, '3333', 1, 0, 186);
INSERT INTO `ticket_ticketuser` VALUES (1071, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, 'dsfsffsdf', 1, 0, 186);
INSERT INTO `ticket_ticketuser` VALUES (1072, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, 'aaaa', 1, 0, 186);
INSERT INTO `ticket_ticketuser` VALUES (1073, '', '2021-07-31 17:28:18', '2021-07-31 17:28:18', 0, 'fewf', 1, 0, 186);
INSERT INTO `ticket_ticketuser` VALUES (1074, '', '2021-07-31 17:28:21', '2021-07-31 17:28:20', 0, 'admin', 1, 0, 187);
INSERT INTO `ticket_ticketuser` VALUES (1075, '', '2021-07-31 17:28:21', '2021-07-31 17:28:21', 0, '23424', 1, 0, 187);
INSERT INTO `ticket_ticketuser` VALUES (1076, '', '2021-07-31 17:28:21', '2021-07-31 17:28:21', 0, 'laoshi', 1, 0, 187);
INSERT INTO `ticket_ticketuser` VALUES (1077, '', '2021-07-31 17:28:21', '2021-07-31 17:28:21', 0, 'fdsfds', 1, 0, 187);
INSERT INTO `ticket_ticketuser` VALUES (1078, '', '2021-07-31 17:28:21', '2021-07-31 17:28:21', 0, 'test', 1, 0, 187);
INSERT INTO `ticket_ticketuser` VALUES (1079, '', '2021-07-31 17:28:21', '2021-07-31 17:28:21', 0, 'test2', 1, 0, 187);
INSERT INTO `ticket_ticketuser` VALUES (1080, '', '2021-07-31 17:28:21', '2021-07-31 17:28:21', 0, 'test1111', 1, 0, 187);
INSERT INTO `ticket_ticketuser` VALUES (1081, '', '2021-07-31 17:28:21', '2021-07-31 17:28:21', 0, 'laoshia', 1, 0, 187);
INSERT INTO `ticket_ticketuser` VALUES (1082, '', '2021-07-31 17:28:21', '2021-07-31 17:28:21', 0, '3333', 1, 0, 187);
INSERT INTO `ticket_ticketuser` VALUES (1083, '', '2021-07-31 17:28:21', '2021-07-31 17:28:21', 0, 'dsfsffsdf', 1, 0, 187);
INSERT INTO `ticket_ticketuser` VALUES (1084, '', '2021-07-31 17:28:21', '2021-07-31 17:28:21', 0, 'aaaa', 1, 0, 187);
INSERT INTO `ticket_ticketuser` VALUES (1085, '', '2021-07-31 17:28:21', '2021-07-31 17:28:21', 0, 'fewf', 1, 0, 187);
INSERT INTO `ticket_ticketuser` VALUES (1086, '', '2021-07-31 17:28:30', '2021-07-31 17:28:29', 0, 'admin', 1, 0, 188);
INSERT INTO `ticket_ticketuser` VALUES (1087, '', '2021-07-31 17:28:30', '2021-07-31 17:28:30', 0, '23424', 1, 0, 188);
INSERT INTO `ticket_ticketuser` VALUES (1088, '', '2021-07-31 17:28:30', '2021-07-31 17:28:30', 0, 'laoshi', 1, 0, 188);
INSERT INTO `ticket_ticketuser` VALUES (1089, '', '2021-07-31 17:28:30', '2021-07-31 17:28:30', 0, 'fdsfds', 1, 0, 188);
INSERT INTO `ticket_ticketuser` VALUES (1090, '', '2021-07-31 17:28:30', '2021-07-31 17:28:30', 0, 'test', 1, 0, 188);
INSERT INTO `ticket_ticketuser` VALUES (1091, '', '2021-07-31 17:28:30', '2021-07-31 17:28:30', 0, 'test2', 1, 0, 188);
INSERT INTO `ticket_ticketuser` VALUES (1092, '', '2021-07-31 17:28:30', '2021-07-31 17:28:30', 0, 'test1111', 1, 0, 188);
INSERT INTO `ticket_ticketuser` VALUES (1093, '', '2021-07-31 17:28:30', '2021-07-31 17:28:30', 0, 'laoshia', 1, 0, 188);
INSERT INTO `ticket_ticketuser` VALUES (1094, '', '2021-07-31 17:28:30', '2021-07-31 17:28:30', 0, '3333', 1, 0, 188);
INSERT INTO `ticket_ticketuser` VALUES (1095, '', '2021-07-31 17:28:30', '2021-07-31 17:28:30', 0, 'dsfsffsdf', 1, 0, 188);
INSERT INTO `ticket_ticketuser` VALUES (1096, '', '2021-07-31 17:28:30', '2021-07-31 17:28:30', 0, 'aaaa', 1, 0, 188);
INSERT INTO `ticket_ticketuser` VALUES (1097, '', '2021-07-31 17:28:30', '2021-07-31 17:28:30', 0, 'fewf', 1, 0, 188);
INSERT INTO `ticket_ticketuser` VALUES (1098, '', '2021-07-31 17:28:32', '2021-07-31 17:28:31', 0, 'admin', 1, 0, 189);
INSERT INTO `ticket_ticketuser` VALUES (1099, '', '2021-07-31 17:28:32', '2021-07-31 17:28:32', 0, '23424', 1, 0, 189);
INSERT INTO `ticket_ticketuser` VALUES (1100, '', '2021-07-31 17:28:32', '2021-07-31 17:28:32', 0, 'laoshi', 1, 0, 189);
INSERT INTO `ticket_ticketuser` VALUES (1101, '', '2021-07-31 17:28:32', '2021-07-31 17:28:32', 0, 'fdsfds', 1, 0, 189);
INSERT INTO `ticket_ticketuser` VALUES (1102, '', '2021-07-31 17:28:32', '2021-07-31 17:28:32', 0, 'test', 1, 0, 189);
INSERT INTO `ticket_ticketuser` VALUES (1103, '', '2021-07-31 17:28:32', '2021-07-31 17:28:32', 0, 'test2', 1, 0, 189);
INSERT INTO `ticket_ticketuser` VALUES (1104, '', '2021-07-31 17:28:32', '2021-07-31 17:28:32', 0, 'test1111', 1, 0, 189);
INSERT INTO `ticket_ticketuser` VALUES (1105, '', '2021-07-31 17:28:32', '2021-07-31 17:28:32', 0, 'laoshia', 1, 0, 189);
INSERT INTO `ticket_ticketuser` VALUES (1106, '', '2021-07-31 17:28:32', '2021-07-31 17:28:32', 0, '3333', 1, 0, 189);
INSERT INTO `ticket_ticketuser` VALUES (1107, '', '2021-07-31 17:28:32', '2021-07-31 17:28:32', 0, 'dsfsffsdf', 1, 0, 189);
INSERT INTO `ticket_ticketuser` VALUES (1108, '', '2021-07-31 17:28:32', '2021-07-31 17:28:32', 0, 'aaaa', 1, 0, 189);
INSERT INTO `ticket_ticketuser` VALUES (1109, '', '2021-07-31 17:28:32', '2021-07-31 17:28:32', 0, 'fewf', 1, 0, 189);
INSERT INTO `ticket_ticketuser` VALUES (1110, '', '2021-07-31 17:28:39', '2021-07-31 17:28:38', 0, 'admin', 1, 0, 190);
INSERT INTO `ticket_ticketuser` VALUES (1111, '', '2021-07-31 17:28:39', '2021-07-31 17:28:39', 0, '23424', 1, 0, 190);
INSERT INTO `ticket_ticketuser` VALUES (1112, '', '2021-07-31 17:28:39', '2021-07-31 17:28:39', 0, 'laoshi', 1, 0, 190);
INSERT INTO `ticket_ticketuser` VALUES (1113, '', '2021-07-31 17:28:39', '2021-07-31 17:28:39', 0, 'fdsfds', 1, 0, 190);
INSERT INTO `ticket_ticketuser` VALUES (1114, '', '2021-07-31 17:28:39', '2021-07-31 17:28:39', 0, 'test', 1, 0, 190);
INSERT INTO `ticket_ticketuser` VALUES (1115, '', '2021-07-31 17:28:39', '2021-07-31 17:28:39', 0, 'test2', 1, 0, 190);
INSERT INTO `ticket_ticketuser` VALUES (1116, '', '2021-07-31 17:28:39', '2021-07-31 17:28:39', 0, 'test1111', 1, 0, 190);
INSERT INTO `ticket_ticketuser` VALUES (1117, '', '2021-07-31 17:28:39', '2021-07-31 17:28:39', 0, 'laoshia', 1, 0, 190);
INSERT INTO `ticket_ticketuser` VALUES (1118, '', '2021-07-31 17:28:39', '2021-07-31 17:28:39', 0, '3333', 1, 0, 190);
INSERT INTO `ticket_ticketuser` VALUES (1119, '', '2021-07-31 17:28:39', '2021-07-31 17:28:39', 0, 'dsfsffsdf', 1, 0, 190);
INSERT INTO `ticket_ticketuser` VALUES (1120, '', '2021-07-31 17:28:39', '2021-07-31 17:28:39', 0, 'aaaa', 1, 0, 190);
INSERT INTO `ticket_ticketuser` VALUES (1121, '', '2021-07-31 17:28:39', '2021-07-31 17:28:39', 0, 'fewf', 1, 0, 190);
INSERT INTO `ticket_ticketuser` VALUES (1122, '', '2021-07-31 17:28:56', '2021-07-31 17:28:55', 0, 'admin', 1, 0, 191);
INSERT INTO `ticket_ticketuser` VALUES (1123, '', '2021-07-31 17:28:56', '2021-07-31 17:28:56', 0, '23424', 1, 0, 191);
INSERT INTO `ticket_ticketuser` VALUES (1124, '', '2021-07-31 17:28:56', '2021-07-31 17:28:56', 0, 'laoshi', 1, 0, 191);
INSERT INTO `ticket_ticketuser` VALUES (1125, '', '2021-07-31 17:28:56', '2021-07-31 17:28:56', 0, 'fdsfds', 1, 0, 191);
INSERT INTO `ticket_ticketuser` VALUES (1126, '', '2021-07-31 17:28:56', '2021-07-31 17:28:56', 0, 'test', 1, 0, 191);
INSERT INTO `ticket_ticketuser` VALUES (1127, '', '2021-07-31 17:28:56', '2021-07-31 17:28:56', 0, 'test2', 1, 0, 191);
INSERT INTO `ticket_ticketuser` VALUES (1128, '', '2021-07-31 17:28:56', '2021-07-31 17:28:56', 0, 'test1111', 1, 0, 191);
INSERT INTO `ticket_ticketuser` VALUES (1129, '', '2021-07-31 17:28:56', '2021-07-31 17:28:56', 0, 'laoshia', 1, 0, 191);
INSERT INTO `ticket_ticketuser` VALUES (1130, '', '2021-07-31 17:28:56', '2021-07-31 17:28:56', 0, '3333', 1, 0, 191);
INSERT INTO `ticket_ticketuser` VALUES (1131, '', '2021-07-31 17:28:56', '2021-07-31 17:28:56', 0, 'dsfsffsdf', 1, 0, 191);
INSERT INTO `ticket_ticketuser` VALUES (1132, '', '2021-07-31 17:28:56', '2021-07-31 17:28:56', 0, 'aaaa', 1, 0, 191);
INSERT INTO `ticket_ticketuser` VALUES (1133, '', '2021-07-31 17:28:56', '2021-07-31 17:28:56', 0, 'fewf', 1, 0, 191);
INSERT INTO `ticket_ticketuser` VALUES (1134, '', '2021-07-31 17:28:57', '2021-07-31 17:28:56', 0, 'admin', 1, 0, 192);
INSERT INTO `ticket_ticketuser` VALUES (1135, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, '23424', 1, 0, 192);
INSERT INTO `ticket_ticketuser` VALUES (1136, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'laoshi', 1, 0, 192);
INSERT INTO `ticket_ticketuser` VALUES (1137, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'fdsfds', 1, 0, 192);
INSERT INTO `ticket_ticketuser` VALUES (1138, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'test', 1, 0, 192);
INSERT INTO `ticket_ticketuser` VALUES (1139, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'test2', 1, 0, 192);
INSERT INTO `ticket_ticketuser` VALUES (1140, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'test1111', 1, 0, 192);
INSERT INTO `ticket_ticketuser` VALUES (1141, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'laoshia', 1, 0, 192);
INSERT INTO `ticket_ticketuser` VALUES (1142, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, '3333', 1, 0, 192);
INSERT INTO `ticket_ticketuser` VALUES (1143, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'dsfsffsdf', 1, 0, 192);
INSERT INTO `ticket_ticketuser` VALUES (1144, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'aaaa', 1, 0, 192);
INSERT INTO `ticket_ticketuser` VALUES (1145, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'fewf', 1, 0, 192);
INSERT INTO `ticket_ticketuser` VALUES (1146, '', '2021-07-31 17:28:57', '2021-07-31 17:28:56', 0, 'admin', 1, 0, 193);
INSERT INTO `ticket_ticketuser` VALUES (1147, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, '23424', 1, 0, 193);
INSERT INTO `ticket_ticketuser` VALUES (1148, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'laoshi', 1, 0, 193);
INSERT INTO `ticket_ticketuser` VALUES (1149, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'fdsfds', 1, 0, 193);
INSERT INTO `ticket_ticketuser` VALUES (1150, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'test', 1, 0, 193);
INSERT INTO `ticket_ticketuser` VALUES (1151, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'test2', 1, 0, 193);
INSERT INTO `ticket_ticketuser` VALUES (1152, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'test1111', 1, 0, 193);
INSERT INTO `ticket_ticketuser` VALUES (1153, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'laoshia', 1, 0, 193);
INSERT INTO `ticket_ticketuser` VALUES (1154, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, '3333', 1, 0, 193);
INSERT INTO `ticket_ticketuser` VALUES (1155, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'dsfsffsdf', 1, 0, 193);
INSERT INTO `ticket_ticketuser` VALUES (1156, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'aaaa', 1, 0, 193);
INSERT INTO `ticket_ticketuser` VALUES (1157, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'fewf', 1, 0, 193);
INSERT INTO `ticket_ticketuser` VALUES (1158, '', '2021-07-31 17:28:57', '2021-07-31 17:28:56', 0, 'admin', 1, 0, 194);
INSERT INTO `ticket_ticketuser` VALUES (1159, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, '23424', 1, 0, 194);
INSERT INTO `ticket_ticketuser` VALUES (1160, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'laoshi', 1, 0, 194);
INSERT INTO `ticket_ticketuser` VALUES (1161, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'fdsfds', 1, 0, 194);
INSERT INTO `ticket_ticketuser` VALUES (1162, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'test', 1, 0, 194);
INSERT INTO `ticket_ticketuser` VALUES (1163, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'test2', 1, 0, 194);
INSERT INTO `ticket_ticketuser` VALUES (1164, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'test1111', 1, 0, 194);
INSERT INTO `ticket_ticketuser` VALUES (1165, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'laoshia', 1, 0, 194);
INSERT INTO `ticket_ticketuser` VALUES (1166, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, '3333', 1, 0, 194);
INSERT INTO `ticket_ticketuser` VALUES (1167, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'dsfsffsdf', 1, 0, 194);
INSERT INTO `ticket_ticketuser` VALUES (1168, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'aaaa', 1, 0, 194);
INSERT INTO `ticket_ticketuser` VALUES (1169, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'fewf', 1, 0, 194);
INSERT INTO `ticket_ticketuser` VALUES (1170, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'admin', 1, 0, 195);
INSERT INTO `ticket_ticketuser` VALUES (1171, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, '23424', 1, 0, 195);
INSERT INTO `ticket_ticketuser` VALUES (1172, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'laoshi', 1, 0, 195);
INSERT INTO `ticket_ticketuser` VALUES (1173, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'fdsfds', 1, 0, 195);
INSERT INTO `ticket_ticketuser` VALUES (1174, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'test', 1, 0, 195);
INSERT INTO `ticket_ticketuser` VALUES (1175, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'test2', 1, 0, 195);
INSERT INTO `ticket_ticketuser` VALUES (1176, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'test1111', 1, 0, 195);
INSERT INTO `ticket_ticketuser` VALUES (1177, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'laoshia', 1, 0, 195);
INSERT INTO `ticket_ticketuser` VALUES (1178, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, '3333', 1, 0, 195);
INSERT INTO `ticket_ticketuser` VALUES (1179, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'dsfsffsdf', 1, 0, 195);
INSERT INTO `ticket_ticketuser` VALUES (1180, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'aaaa', 1, 0, 195);
INSERT INTO `ticket_ticketuser` VALUES (1181, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'fewf', 1, 0, 195);
INSERT INTO `ticket_ticketuser` VALUES (1182, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'admin', 1, 0, 196);
INSERT INTO `ticket_ticketuser` VALUES (1183, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, '23424', 1, 0, 196);
INSERT INTO `ticket_ticketuser` VALUES (1184, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'laoshi', 1, 0, 196);
INSERT INTO `ticket_ticketuser` VALUES (1185, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'fdsfds', 1, 0, 196);
INSERT INTO `ticket_ticketuser` VALUES (1186, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'test', 1, 0, 196);
INSERT INTO `ticket_ticketuser` VALUES (1187, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'test2', 1, 0, 196);
INSERT INTO `ticket_ticketuser` VALUES (1188, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'test1111', 1, 0, 196);
INSERT INTO `ticket_ticketuser` VALUES (1189, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'laoshia', 1, 0, 196);
INSERT INTO `ticket_ticketuser` VALUES (1190, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, '3333', 1, 0, 196);
INSERT INTO `ticket_ticketuser` VALUES (1191, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'dsfsffsdf', 1, 0, 196);
INSERT INTO `ticket_ticketuser` VALUES (1192, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'aaaa', 1, 0, 196);
INSERT INTO `ticket_ticketuser` VALUES (1193, '', '2021-07-31 17:28:57', '2021-07-31 17:28:57', 0, 'fewf', 1, 0, 196);
INSERT INTO `ticket_ticketuser` VALUES (1194, '', '2021-07-31 17:29:04', '2021-07-31 17:29:03', 0, 'admin', 1, 0, 197);
INSERT INTO `ticket_ticketuser` VALUES (1195, '', '2021-07-31 17:29:04', '2021-07-31 17:29:04', 0, '23424', 1, 0, 197);
INSERT INTO `ticket_ticketuser` VALUES (1196, '', '2021-07-31 17:29:04', '2021-07-31 17:29:04', 0, 'laoshi', 1, 0, 197);
INSERT INTO `ticket_ticketuser` VALUES (1197, '', '2021-07-31 17:29:04', '2021-07-31 17:29:04', 0, 'fdsfds', 1, 0, 197);
INSERT INTO `ticket_ticketuser` VALUES (1198, '', '2021-07-31 17:29:04', '2021-07-31 17:29:04', 0, 'test', 1, 0, 197);
INSERT INTO `ticket_ticketuser` VALUES (1199, '', '2021-07-31 17:29:04', '2021-07-31 17:29:04', 0, 'test2', 1, 0, 197);
INSERT INTO `ticket_ticketuser` VALUES (1200, '', '2021-07-31 17:29:04', '2021-07-31 17:29:04', 0, 'test1111', 1, 0, 197);
INSERT INTO `ticket_ticketuser` VALUES (1201, '', '2021-07-31 17:29:04', '2021-07-31 17:29:04', 0, 'laoshia', 1, 0, 197);
INSERT INTO `ticket_ticketuser` VALUES (1202, '', '2021-07-31 17:29:04', '2021-07-31 17:29:04', 0, '3333', 1, 0, 197);
INSERT INTO `ticket_ticketuser` VALUES (1203, '', '2021-07-31 17:29:04', '2021-07-31 17:29:04', 0, 'dsfsffsdf', 1, 0, 197);
INSERT INTO `ticket_ticketuser` VALUES (1204, '', '2021-07-31 17:29:04', '2021-07-31 17:29:04', 0, 'aaaa', 1, 0, 197);
INSERT INTO `ticket_ticketuser` VALUES (1205, '', '2021-07-31 17:29:04', '2021-07-31 17:29:04', 0, 'fewf', 1, 0, 197);
INSERT INTO `ticket_ticketuser` VALUES (1206, '', '2021-07-31 17:29:04', '2021-07-31 20:54:49', 0, 'admin', 1, 1, 198);
INSERT INTO `ticket_ticketuser` VALUES (1207, '', '2021-07-31 17:29:04', '2021-07-31 20:40:21', 0, '23424', 0, 0, 198);
INSERT INTO `ticket_ticketuser` VALUES (1208, '', '2021-07-31 17:29:04', '2021-07-31 20:40:21', 0, 'laoshi', 0, 0, 198);
INSERT INTO `ticket_ticketuser` VALUES (1209, '', '2021-07-31 17:29:04', '2021-07-31 20:40:21', 0, 'fdsfds', 0, 0, 198);
INSERT INTO `ticket_ticketuser` VALUES (1210, '', '2021-07-31 17:29:04', '2021-07-31 20:40:21', 0, 'test', 0, 0, 198);
INSERT INTO `ticket_ticketuser` VALUES (1211, '', '2021-07-31 17:29:04', '2021-07-31 20:40:21', 0, 'test2', 0, 0, 198);
INSERT INTO `ticket_ticketuser` VALUES (1212, '', '2021-07-31 17:29:04', '2021-07-31 20:40:21', 0, 'test1111', 0, 0, 198);
INSERT INTO `ticket_ticketuser` VALUES (1213, '', '2021-07-31 17:29:04', '2021-07-31 20:40:21', 0, 'laoshia', 0, 0, 198);
INSERT INTO `ticket_ticketuser` VALUES (1214, '', '2021-07-31 17:29:04', '2021-07-31 20:40:21', 0, '3333', 0, 0, 198);
INSERT INTO `ticket_ticketuser` VALUES (1215, '', '2021-07-31 17:29:04', '2021-07-31 20:40:21', 0, 'dsfsffsdf', 0, 0, 198);
INSERT INTO `ticket_ticketuser` VALUES (1216, '', '2021-07-31 17:29:04', '2021-07-31 20:40:21', 0, 'aaaa', 0, 0, 198);
INSERT INTO `ticket_ticketuser` VALUES (1217, '', '2021-07-31 17:29:04', '2021-07-31 20:40:21', 0, 'fewf', 0, 0, 198);
INSERT INTO `ticket_ticketuser` VALUES (1218, '', '2021-07-31 17:29:13', '2021-07-31 19:30:44', 0, 'admin', 0, 0, 199);
INSERT INTO `ticket_ticketuser` VALUES (1219, '', '2021-07-31 17:29:13', '2021-07-31 19:30:44', 0, '23424', 0, 0, 199);
INSERT INTO `ticket_ticketuser` VALUES (1220, '', '2021-07-31 17:29:13', '2021-07-31 19:30:44', 0, 'laoshi', 0, 0, 199);
INSERT INTO `ticket_ticketuser` VALUES (1221, '', '2021-07-31 17:29:13', '2021-07-31 19:30:44', 0, 'fdsfds', 0, 0, 199);
INSERT INTO `ticket_ticketuser` VALUES (1222, '', '2021-07-31 17:29:13', '2021-07-31 19:30:44', 0, 'test', 0, 0, 199);
INSERT INTO `ticket_ticketuser` VALUES (1223, '', '2021-07-31 17:29:13', '2021-07-31 19:30:44', 0, 'test2', 0, 0, 199);
INSERT INTO `ticket_ticketuser` VALUES (1224, '', '2021-07-31 17:29:13', '2021-07-31 19:30:44', 0, 'test1111', 0, 0, 199);
INSERT INTO `ticket_ticketuser` VALUES (1225, '', '2021-07-31 17:29:13', '2021-07-31 19:30:44', 0, 'laoshia', 0, 0, 199);
INSERT INTO `ticket_ticketuser` VALUES (1226, '', '2021-07-31 17:29:13', '2021-07-31 19:30:44', 0, '3333', 0, 0, 199);
INSERT INTO `ticket_ticketuser` VALUES (1227, '', '2021-07-31 17:29:13', '2021-07-31 19:30:44', 0, 'dsfsffsdf', 0, 0, 199);
INSERT INTO `ticket_ticketuser` VALUES (1228, '', '2021-07-31 17:29:13', '2021-07-31 19:30:44', 0, 'aaaa', 0, 0, 199);
INSERT INTO `ticket_ticketuser` VALUES (1229, '', '2021-07-31 17:29:13', '2021-07-31 19:30:44', 0, 'fewf', 0, 0, 199);
INSERT INTO `ticket_ticketuser` VALUES (1230, '', '2021-07-31 17:29:44', '2021-07-31 18:54:03', 0, 'admin', 0, 0, 200);
INSERT INTO `ticket_ticketuser` VALUES (1231, '', '2021-07-31 17:29:44', '2021-07-31 18:54:03', 0, '23424', 0, 0, 200);
INSERT INTO `ticket_ticketuser` VALUES (1232, '', '2021-07-31 17:29:44', '2021-07-31 18:54:03', 0, 'laoshi', 0, 0, 200);
INSERT INTO `ticket_ticketuser` VALUES (1233, '', '2021-07-31 17:29:44', '2021-07-31 18:54:03', 0, 'fdsfds', 0, 0, 200);
INSERT INTO `ticket_ticketuser` VALUES (1234, '', '2021-07-31 17:29:44', '2021-07-31 18:54:03', 0, 'test', 0, 0, 200);
INSERT INTO `ticket_ticketuser` VALUES (1235, '', '2021-07-31 17:29:44', '2021-07-31 18:54:03', 0, 'test2', 0, 0, 200);
INSERT INTO `ticket_ticketuser` VALUES (1236, '', '2021-07-31 17:29:44', '2021-07-31 18:54:03', 0, 'test1111', 0, 0, 200);
INSERT INTO `ticket_ticketuser` VALUES (1237, '', '2021-07-31 17:29:44', '2021-07-31 18:54:03', 0, 'laoshia', 0, 0, 200);
INSERT INTO `ticket_ticketuser` VALUES (1238, '', '2021-07-31 17:29:44', '2021-07-31 18:54:03', 0, '3333', 0, 0, 200);
INSERT INTO `ticket_ticketuser` VALUES (1239, '', '2021-07-31 17:29:44', '2021-07-31 18:54:03', 0, 'dsfsffsdf', 0, 0, 200);
INSERT INTO `ticket_ticketuser` VALUES (1240, '', '2021-07-31 17:29:44', '2021-07-31 18:54:03', 0, 'aaaa', 0, 0, 200);
INSERT INTO `ticket_ticketuser` VALUES (1241, '', '2021-07-31 17:29:44', '2021-07-31 18:54:03', 0, 'fewf', 0, 0, 200);
INSERT INTO `ticket_ticketuser` VALUES (1242, '', '2021-07-31 17:30:10', '2021-07-31 18:19:32', 0, 'admin', 0, 0, 201);
INSERT INTO `ticket_ticketuser` VALUES (1243, '', '2021-07-31 17:30:10', '2021-07-31 18:19:32', 0, '23424', 0, 0, 201);
INSERT INTO `ticket_ticketuser` VALUES (1244, '', '2021-07-31 17:30:10', '2021-07-31 18:19:32', 0, 'laoshi', 0, 0, 201);
INSERT INTO `ticket_ticketuser` VALUES (1245, '', '2021-07-31 17:30:10', '2021-07-31 18:19:32', 0, 'fdsfds', 0, 0, 201);
INSERT INTO `ticket_ticketuser` VALUES (1246, '', '2021-07-31 17:30:10', '2021-07-31 18:19:32', 0, 'test', 0, 0, 201);
INSERT INTO `ticket_ticketuser` VALUES (1247, '', '2021-07-31 17:30:10', '2021-07-31 18:19:32', 0, 'test2', 0, 0, 201);
INSERT INTO `ticket_ticketuser` VALUES (1248, '', '2021-07-31 17:30:10', '2021-07-31 18:19:32', 0, 'test1111', 0, 0, 201);
INSERT INTO `ticket_ticketuser` VALUES (1249, '', '2021-07-31 17:30:10', '2021-07-31 18:19:32', 0, 'laoshia', 0, 0, 201);
INSERT INTO `ticket_ticketuser` VALUES (1250, '', '2021-07-31 17:30:10', '2021-07-31 18:19:32', 0, '3333', 0, 0, 201);
INSERT INTO `ticket_ticketuser` VALUES (1251, '', '2021-07-31 17:30:10', '2021-07-31 18:19:32', 0, 'dsfsffsdf', 0, 0, 201);
INSERT INTO `ticket_ticketuser` VALUES (1252, '', '2021-07-31 17:30:10', '2021-07-31 18:19:32', 0, 'aaaa', 0, 0, 201);
INSERT INTO `ticket_ticketuser` VALUES (1253, '', '2021-07-31 17:30:10', '2021-07-31 18:19:32', 0, 'fewf', 0, 0, 201);
INSERT INTO `ticket_ticketuser` VALUES (1254, '', '2021-07-31 17:30:27', '2021-07-31 18:18:54', 0, 'admin', 0, 0, 202);
INSERT INTO `ticket_ticketuser` VALUES (1255, '', '2021-07-31 17:30:27', '2021-07-31 18:18:54', 0, '23424', 0, 0, 202);
INSERT INTO `ticket_ticketuser` VALUES (1256, '', '2021-07-31 17:30:27', '2021-07-31 18:18:54', 0, 'laoshi', 0, 0, 202);
INSERT INTO `ticket_ticketuser` VALUES (1257, '', '2021-07-31 17:30:27', '2021-07-31 18:18:54', 0, 'fdsfds', 0, 0, 202);
INSERT INTO `ticket_ticketuser` VALUES (1258, '', '2021-07-31 17:30:27', '2021-07-31 18:18:54', 0, 'test', 0, 0, 202);
INSERT INTO `ticket_ticketuser` VALUES (1259, '', '2021-07-31 17:30:27', '2021-07-31 18:18:54', 0, 'test2', 0, 0, 202);
INSERT INTO `ticket_ticketuser` VALUES (1260, '', '2021-07-31 17:30:27', '2021-07-31 18:18:54', 0, 'test1111', 0, 0, 202);
INSERT INTO `ticket_ticketuser` VALUES (1261, '', '2021-07-31 17:30:27', '2021-07-31 18:18:54', 0, 'laoshia', 0, 0, 202);
INSERT INTO `ticket_ticketuser` VALUES (1262, '', '2021-07-31 17:30:27', '2021-07-31 18:18:54', 0, '3333', 0, 0, 202);
INSERT INTO `ticket_ticketuser` VALUES (1263, '', '2021-07-31 17:30:27', '2021-07-31 18:18:54', 0, 'dsfsffsdf', 0, 0, 202);
INSERT INTO `ticket_ticketuser` VALUES (1264, '', '2021-07-31 17:30:27', '2021-07-31 18:18:54', 0, 'aaaa', 0, 0, 202);
INSERT INTO `ticket_ticketuser` VALUES (1265, '', '2021-07-31 17:30:27', '2021-07-31 18:18:54', 0, 'fewf', 0, 0, 202);
INSERT INTO `ticket_ticketuser` VALUES (1266, '', '2021-07-31 17:30:43', '2021-07-31 18:18:13', 0, 'admin', 0, 0, 203);
INSERT INTO `ticket_ticketuser` VALUES (1267, '', '2021-07-31 17:30:43', '2021-07-31 18:18:13', 0, '23424', 0, 0, 203);
INSERT INTO `ticket_ticketuser` VALUES (1268, '', '2021-07-31 17:30:43', '2021-07-31 18:18:13', 0, 'laoshi', 0, 0, 203);
INSERT INTO `ticket_ticketuser` VALUES (1269, '', '2021-07-31 17:30:43', '2021-07-31 18:18:13', 0, 'fdsfds', 0, 0, 203);
INSERT INTO `ticket_ticketuser` VALUES (1270, '', '2021-07-31 17:30:43', '2021-07-31 18:18:13', 0, 'test', 0, 0, 203);
INSERT INTO `ticket_ticketuser` VALUES (1271, '', '2021-07-31 17:30:43', '2021-07-31 18:18:13', 0, 'test2', 0, 0, 203);
INSERT INTO `ticket_ticketuser` VALUES (1272, '', '2021-07-31 17:30:43', '2021-07-31 18:18:13', 0, 'test1111', 0, 0, 203);
INSERT INTO `ticket_ticketuser` VALUES (1273, '', '2021-07-31 17:30:43', '2021-07-31 18:18:13', 0, 'laoshia', 0, 0, 203);
INSERT INTO `ticket_ticketuser` VALUES (1274, '', '2021-07-31 17:30:43', '2021-07-31 18:18:13', 0, '3333', 0, 0, 203);
INSERT INTO `ticket_ticketuser` VALUES (1275, '', '2021-07-31 17:30:43', '2021-07-31 18:18:13', 0, 'dsfsffsdf', 0, 0, 203);
INSERT INTO `ticket_ticketuser` VALUES (1276, '', '2021-07-31 17:30:43', '2021-07-31 18:18:13', 0, 'aaaa', 0, 0, 203);
INSERT INTO `ticket_ticketuser` VALUES (1277, '', '2021-07-31 17:30:43', '2021-07-31 18:18:13', 0, 'fewf', 0, 0, 203);
INSERT INTO `ticket_ticketuser` VALUES (1278, '', '2021-07-31 18:22:49', '2021-07-31 18:39:41', 0, 'admin', 0, 0, 204);
INSERT INTO `ticket_ticketuser` VALUES (1279, '', '2021-07-31 18:22:49', '2021-07-31 18:39:41', 0, 'test1111', 0, 0, 204);
INSERT INTO `ticket_ticketuser` VALUES (1280, '', '2021-07-31 18:22:49', '2021-07-31 18:39:41', 0, 'fdsfds', 0, 0, 204);
INSERT INTO `ticket_ticketuser` VALUES (1281, '', '2021-07-31 18:22:49', '2021-07-31 18:39:41', 0, 'aaaa', 0, 0, 204);
INSERT INTO `ticket_ticketuser` VALUES (1282, '', '2021-07-31 18:22:49', '2021-07-31 18:39:41', 0, 'dsfsffsdf', 0, 0, 204);
INSERT INTO `ticket_ticketuser` VALUES (1283, '', '2021-07-31 18:22:49', '2021-07-31 18:39:41', 0, '23424', 0, 0, 204);
INSERT INTO `ticket_ticketuser` VALUES (1284, '', '2021-07-31 18:22:49', '2021-07-31 18:39:41', 0, 'test2', 0, 0, 204);
INSERT INTO `ticket_ticketuser` VALUES (1285, '', '2021-07-31 18:22:49', '2021-07-31 18:39:41', 0, '3333', 0, 0, 204);
INSERT INTO `ticket_ticketuser` VALUES (1286, '', '2021-07-31 18:22:49', '2021-07-31 18:39:41', 0, 'test', 0, 0, 204);
INSERT INTO `ticket_ticketuser` VALUES (1287, '', '2021-07-31 18:22:49', '2021-07-31 18:39:41', 0, 'laoshia', 0, 0, 204);
INSERT INTO `ticket_ticketuser` VALUES (1288, '', '2021-07-31 18:22:49', '2021-07-31 18:39:41', 0, 'laoshi', 0, 0, 204);
INSERT INTO `ticket_ticketuser` VALUES (1289, '', '2021-07-31 18:22:49', '2021-07-31 18:39:41', 0, 'fewf', 0, 0, 204);
INSERT INTO `ticket_ticketuser` VALUES (1290, '', '2021-07-31 18:48:23', '2021-07-31 18:49:23', 0, 'test2', 0, 0, 205);
INSERT INTO `ticket_ticketuser` VALUES (1291, '', '2021-07-31 18:48:23', '2021-07-31 18:49:23', 0, '23424', 0, 0, 205);
INSERT INTO `ticket_ticketuser` VALUES (1292, '', '2021-07-31 18:48:23', '2021-07-31 18:49:23', 0, 'fdsfds', 0, 0, 205);
INSERT INTO `ticket_ticketuser` VALUES (1293, '', '2021-07-31 18:48:23', '2021-07-31 18:49:23', 0, 'test', 0, 0, 205);
INSERT INTO `ticket_ticketuser` VALUES (1294, '', '2021-07-31 18:48:23', '2021-07-31 18:49:43', 0, 'laoshi', 1, 1, 205);
INSERT INTO `ticket_ticketuser` VALUES (1295, '', '2021-07-31 18:48:23', '2021-07-31 18:49:23', 0, 'aaaa', 0, 0, 205);
INSERT INTO `ticket_ticketuser` VALUES (1296, '', '2021-07-31 18:48:23', '2021-07-31 18:49:23', 0, 'laoshia', 0, 0, 205);
INSERT INTO `ticket_ticketuser` VALUES (1297, '', '2021-07-31 18:48:23', '2021-07-31 18:49:23', 0, 'fewf', 0, 0, 205);
INSERT INTO `ticket_ticketuser` VALUES (1298, '', '2021-07-31 18:48:23', '2021-07-31 18:49:23', 0, 'dsfsffsdf', 0, 0, 205);
INSERT INTO `ticket_ticketuser` VALUES (1299, '', '2021-07-31 18:48:23', '2021-07-31 18:49:23', 0, '3333', 0, 0, 205);
INSERT INTO `ticket_ticketuser` VALUES (1300, '', '2021-07-31 18:48:23', '2021-07-31 18:49:23', 0, 'admin', 0, 0, 205);
INSERT INTO `ticket_ticketuser` VALUES (1301, '', '2021-07-31 18:48:23', '2021-07-31 18:49:23', 0, 'test1111', 0, 0, 205);
INSERT INTO `ticket_ticketuser` VALUES (1302, '', '2021-07-31 18:55:43', '2021-07-31 20:34:51', 0, 'admin', 0, 0, 206);
INSERT INTO `ticket_ticketuser` VALUES (1303, '', '2021-07-31 18:55:43', '2021-07-31 20:34:51', 0, '23424', 0, 0, 206);
INSERT INTO `ticket_ticketuser` VALUES (1304, '', '2021-07-31 18:55:43', '2021-07-31 20:34:51', 0, 'fdsfds', 0, 0, 206);
INSERT INTO `ticket_ticketuser` VALUES (1305, '', '2021-07-31 18:55:43', '2021-07-31 20:34:51', 0, 'test', 0, 0, 206);
INSERT INTO `ticket_ticketuser` VALUES (1306, '', '2021-07-31 18:55:43', '2021-07-31 20:34:51', 0, 'laoshi', 0, 0, 206);
INSERT INTO `ticket_ticketuser` VALUES (1307, '', '2021-07-31 18:55:43', '2021-07-31 20:34:51', 0, 'aaaa', 0, 0, 206);
INSERT INTO `ticket_ticketuser` VALUES (1308, '', '2021-07-31 18:55:43', '2021-07-31 20:34:51', 0, 'test2', 0, 0, 206);
INSERT INTO `ticket_ticketuser` VALUES (1309, '', '2021-07-31 18:55:43', '2021-07-31 20:34:51', 0, 'laoshia', 0, 0, 206);
INSERT INTO `ticket_ticketuser` VALUES (1310, '', '2021-07-31 18:55:43', '2021-07-31 20:34:51', 0, 'fewf', 0, 0, 206);
INSERT INTO `ticket_ticketuser` VALUES (1311, '', '2021-07-31 18:55:43', '2021-07-31 20:34:51', 0, 'dsfsffsdf', 0, 0, 206);
INSERT INTO `ticket_ticketuser` VALUES (1312, '', '2021-07-31 18:55:43', '2021-07-31 20:34:51', 0, '3333', 0, 0, 206);
INSERT INTO `ticket_ticketuser` VALUES (1313, '', '2021-07-31 18:55:43', '2021-07-31 20:34:51', 0, 'test1111', 0, 0, 206);
INSERT INTO `ticket_ticketuser` VALUES (1314, '', '2021-07-31 19:22:57', '2021-07-31 19:23:44', 0, 'admin', 1, 1, 207);
INSERT INTO `ticket_ticketuser` VALUES (1315, '', '2021-07-31 19:22:57', '2021-07-31 19:23:40', 0, '23424', 0, 0, 207);
INSERT INTO `ticket_ticketuser` VALUES (1316, '', '2021-07-31 19:22:57', '2021-07-31 19:23:40', 0, 'fdsfds', 0, 0, 207);
INSERT INTO `ticket_ticketuser` VALUES (1317, '', '2021-07-31 19:22:57', '2021-07-31 19:23:40', 0, 'test', 0, 0, 207);
INSERT INTO `ticket_ticketuser` VALUES (1318, '', '2021-07-31 19:22:57', '2021-07-31 19:23:40', 0, 'laoshi', 0, 0, 207);
INSERT INTO `ticket_ticketuser` VALUES (1319, '', '2021-07-31 19:22:57', '2021-07-31 19:23:40', 0, 'aaaa', 0, 0, 207);
INSERT INTO `ticket_ticketuser` VALUES (1320, '', '2021-07-31 19:22:57', '2021-07-31 19:23:40', 0, 'test2', 0, 0, 207);
INSERT INTO `ticket_ticketuser` VALUES (1321, '', '2021-07-31 19:22:57', '2021-07-31 19:23:40', 0, 'laoshia', 0, 0, 207);
INSERT INTO `ticket_ticketuser` VALUES (1322, '', '2021-07-31 19:22:57', '2021-07-31 19:23:40', 0, 'fewf', 0, 0, 207);
INSERT INTO `ticket_ticketuser` VALUES (1323, '', '2021-07-31 19:22:57', '2021-07-31 19:23:40', 0, 'dsfsffsdf', 0, 0, 207);
INSERT INTO `ticket_ticketuser` VALUES (1324, '', '2021-07-31 19:22:57', '2021-07-31 19:23:40', 0, '3333', 0, 0, 207);
INSERT INTO `ticket_ticketuser` VALUES (1325, '', '2021-07-31 19:22:57', '2021-07-31 19:23:40', 0, 'test1111', 0, 0, 207);
INSERT INTO `ticket_ticketuser` VALUES (1326, '', '2021-07-31 20:56:43', '2021-07-31 20:56:43', 0, 'admin', 1, 0, 208);
INSERT INTO `ticket_ticketuser` VALUES (1327, '', '2021-07-31 20:56:43', '2021-07-31 20:56:43', 0, 'fdsfds', 1, 0, 208);
INSERT INTO `ticket_ticketuser` VALUES (1328, '', '2021-07-31 20:56:43', '2021-07-31 20:56:43', 0, 'dsfsffsdf', 1, 0, 208);
INSERT INTO `ticket_ticketuser` VALUES (1329, '', '2021-07-31 20:56:43', '2021-07-31 20:56:43', 0, 'aaaa', 1, 0, 208);
INSERT INTO `ticket_ticketuser` VALUES (1330, '', '2021-07-31 20:56:43', '2021-07-31 20:56:43', 0, 'laoshia', 1, 0, 208);
INSERT INTO `ticket_ticketuser` VALUES (1331, '', '2021-07-31 20:56:43', '2021-07-31 20:56:43', 0, 'test2', 1, 0, 208);
INSERT INTO `ticket_ticketuser` VALUES (1332, '', '2021-07-31 20:56:43', '2021-07-31 20:56:43', 0, 'laoshi', 1, 0, 208);
INSERT INTO `ticket_ticketuser` VALUES (1333, '', '2021-07-31 20:56:43', '2021-07-31 20:56:43', 0, '3333', 1, 0, 208);
INSERT INTO `ticket_ticketuser` VALUES (1334, '', '2021-07-31 20:56:43', '2021-07-31 20:56:43', 0, 'test1111', 1, 0, 208);
INSERT INTO `ticket_ticketuser` VALUES (1335, '', '2021-07-31 20:56:43', '2021-07-31 20:56:43', 0, '23424', 1, 0, 208);
INSERT INTO `ticket_ticketuser` VALUES (1336, '', '2021-07-31 20:56:43', '2021-07-31 20:56:43', 0, 'fewf', 1, 0, 208);
INSERT INTO `ticket_ticketuser` VALUES (1337, '', '2021-07-31 20:56:43', '2021-07-31 20:56:43', 0, 'test', 1, 0, 208);
INSERT INTO `ticket_ticketuser` VALUES (1338, '', '2021-08-01 12:11:22', '2021-08-01 12:12:09', 0, 'admin', 0, 0, 209);
INSERT INTO `ticket_ticketuser` VALUES (1339, '', '2021-08-01 12:11:22', '2021-08-01 12:12:09', 0, 'aaaa', 0, 0, 209);
INSERT INTO `ticket_ticketuser` VALUES (1340, '', '2021-08-01 12:11:22', '2021-08-01 12:12:09', 0, 'dsfsffsdf', 0, 0, 209);
INSERT INTO `ticket_ticketuser` VALUES (1341, '', '2021-08-01 12:11:22', '2021-08-01 12:12:09', 0, 'test', 0, 0, 209);
INSERT INTO `ticket_ticketuser` VALUES (1342, '', '2021-08-01 12:11:22', '2021-08-01 12:12:09', 0, 'fewf', 0, 0, 209);
INSERT INTO `ticket_ticketuser` VALUES (1343, '', '2021-08-01 12:11:22', '2021-08-01 12:12:09', 0, 'test1111', 0, 0, 209);
INSERT INTO `ticket_ticketuser` VALUES (1344, '', '2021-08-01 12:11:22', '2021-08-01 12:12:09', 0, 'test2', 0, 0, 209);
INSERT INTO `ticket_ticketuser` VALUES (1345, '', '2021-08-01 12:11:22', '2021-08-01 12:12:09', 0, 'fdsfds', 0, 0, 209);
INSERT INTO `ticket_ticketuser` VALUES (1346, '', '2021-08-01 12:11:22', '2021-08-01 12:12:09', 0, '3333', 0, 0, 209);
INSERT INTO `ticket_ticketuser` VALUES (1347, '', '2021-08-01 12:11:22', '2021-08-01 12:12:09', 0, '23424', 0, 0, 209);
INSERT INTO `ticket_ticketuser` VALUES (1348, '', '2021-08-01 12:11:22', '2021-08-01 12:12:09', 0, 'laoshia', 0, 0, 209);
INSERT INTO `ticket_ticketuser` VALUES (1349, '', '2021-08-01 12:11:22', '2021-08-01 12:11:22', 0, 'laoshi', 1, 0, 209);
INSERT INTO `ticket_ticketuser` VALUES (1350, '', '2021-08-01 12:40:41', '2021-08-01 12:41:02', 0, 'test', 0, 0, 210);
INSERT INTO `ticket_ticketuser` VALUES (1351, '', '2021-08-01 12:40:41', '2021-08-01 12:41:02', 0, 'fdsfds', 0, 0, 210);
INSERT INTO `ticket_ticketuser` VALUES (1352, '', '2021-08-01 12:40:41', '2021-08-01 12:41:02', 0, 'admin', 0, 0, 210);
INSERT INTO `ticket_ticketuser` VALUES (1353, '', '2021-08-01 12:40:41', '2021-08-01 12:41:02', 0, 'laoshia', 0, 0, 210);
INSERT INTO `ticket_ticketuser` VALUES (1354, '', '2021-08-01 12:40:41', '2021-08-01 12:41:02', 0, '23424', 0, 0, 210);
INSERT INTO `ticket_ticketuser` VALUES (1355, '', '2021-08-01 12:40:41', '2021-08-01 12:41:02', 0, '3333', 0, 0, 210);
INSERT INTO `ticket_ticketuser` VALUES (1356, '', '2021-08-01 12:40:41', '2021-08-01 12:41:02', 0, 'laoshi', 0, 0, 210);
INSERT INTO `ticket_ticketuser` VALUES (1357, '', '2021-08-01 12:40:41', '2021-08-01 12:41:02', 0, 'dsfsffsdf', 0, 0, 210);
INSERT INTO `ticket_ticketuser` VALUES (1358, '', '2021-08-01 12:40:41', '2021-08-01 12:41:02', 0, 'test2', 0, 0, 210);
INSERT INTO `ticket_ticketuser` VALUES (1359, '', '2021-08-01 12:40:41', '2021-08-01 12:41:02', 0, 'fewf', 0, 0, 210);
INSERT INTO `ticket_ticketuser` VALUES (1360, '', '2021-08-01 12:40:41', '2021-08-01 12:41:02', 0, 'test1111', 0, 0, 210);
INSERT INTO `ticket_ticketuser` VALUES (1361, '', '2021-08-01 12:40:41', '2021-08-01 12:41:02', 0, 'aaaa', 0, 0, 210);
INSERT INTO `ticket_ticketuser` VALUES (1362, '', '2021-08-01 12:43:31', '2021-08-01 12:44:06', 0, 'test', 0, 0, 211);
INSERT INTO `ticket_ticketuser` VALUES (1363, '', '2021-08-01 12:43:31', '2021-08-01 12:44:06', 0, 'fdsfds', 0, 0, 211);
INSERT INTO `ticket_ticketuser` VALUES (1364, '', '2021-08-01 12:43:31', '2021-08-01 12:44:06', 0, 'admin', 0, 0, 211);
INSERT INTO `ticket_ticketuser` VALUES (1365, '', '2021-08-01 12:43:31', '2021-08-01 12:44:06', 0, 'laoshia', 0, 0, 211);
INSERT INTO `ticket_ticketuser` VALUES (1366, '', '2021-08-01 12:43:31', '2021-08-01 12:44:06', 0, '23424', 0, 0, 211);
INSERT INTO `ticket_ticketuser` VALUES (1367, '', '2021-08-01 12:43:31', '2021-08-01 12:44:06', 0, '3333', 0, 0, 211);
INSERT INTO `ticket_ticketuser` VALUES (1368, '', '2021-08-01 12:43:31', '2021-08-01 12:44:20', 0, 'laoshi', 1, 1, 211);
INSERT INTO `ticket_ticketuser` VALUES (1369, '', '2021-08-01 12:43:31', '2021-08-01 12:44:06', 0, 'dsfsffsdf', 0, 0, 211);
INSERT INTO `ticket_ticketuser` VALUES (1370, '', '2021-08-01 12:43:31', '2021-08-01 12:44:06', 0, 'test2', 0, 0, 211);
INSERT INTO `ticket_ticketuser` VALUES (1371, '', '2021-08-01 12:43:31', '2021-08-01 12:44:06', 0, 'fewf', 0, 0, 211);
INSERT INTO `ticket_ticketuser` VALUES (1372, '', '2021-08-01 12:43:31', '2021-08-01 12:44:06', 0, 'test1111', 0, 0, 211);
INSERT INTO `ticket_ticketuser` VALUES (1373, '', '2021-08-01 12:43:31', '2021-08-01 12:44:06', 0, 'aaaa', 0, 0, 211);
INSERT INTO `ticket_ticketuser` VALUES (1374, '', '2021-08-01 12:47:25', '2021-08-01 12:52:51', 0, 'test', 0, 0, 212);
INSERT INTO `ticket_ticketuser` VALUES (1375, '', '2021-08-01 12:47:25', '2021-08-01 12:52:51', 0, '3333', 0, 0, 212);
INSERT INTO `ticket_ticketuser` VALUES (1376, '', '2021-08-01 12:47:25', '2021-08-01 12:47:25', 0, 'laoshi', 1, 0, 212);
INSERT INTO `ticket_ticketuser` VALUES (1377, '', '2021-08-01 12:47:25', '2021-08-01 12:52:51', 0, 'laoshia', 0, 0, 212);
INSERT INTO `ticket_ticketuser` VALUES (1378, '', '2021-08-01 12:47:25', '2021-08-01 12:52:51', 0, '23424', 0, 0, 212);
INSERT INTO `ticket_ticketuser` VALUES (1379, '', '2021-08-01 12:47:25', '2021-08-01 12:52:51', 0, 'dsfsffsdf', 0, 0, 212);
INSERT INTO `ticket_ticketuser` VALUES (1380, '', '2021-08-01 12:47:25', '2021-08-01 12:52:51', 0, 'test1111', 0, 0, 212);
INSERT INTO `ticket_ticketuser` VALUES (1381, '', '2021-08-01 12:47:25', '2021-08-01 12:52:51', 0, 'test2', 0, 0, 212);
INSERT INTO `ticket_ticketuser` VALUES (1382, '', '2021-08-01 12:47:25', '2021-08-01 12:52:51', 0, 'fdsfds', 0, 0, 212);
INSERT INTO `ticket_ticketuser` VALUES (1383, '', '2021-08-01 12:47:25', '2021-08-01 12:52:51', 0, 'fewf', 0, 0, 212);
INSERT INTO `ticket_ticketuser` VALUES (1384, '', '2021-08-01 12:47:25', '2021-08-01 12:52:51', 0, 'aaaa', 0, 0, 212);
INSERT INTO `ticket_ticketuser` VALUES (1385, '', '2021-08-01 12:47:25', '2021-08-01 12:52:51', 0, 'admin', 0, 0, 212);
INSERT INTO `ticket_ticketuser` VALUES (1386, '', '2021-08-01 12:47:34', '2021-08-01 12:53:04', 0, 'test', 0, 0, 213);
INSERT INTO `ticket_ticketuser` VALUES (1387, '', '2021-08-01 12:47:34', '2021-08-01 12:53:04', 0, '3333', 0, 0, 213);
INSERT INTO `ticket_ticketuser` VALUES (1388, '', '2021-08-01 12:47:34', '2021-08-01 13:00:50', 0, 'laoshi', 1, 1, 213);
INSERT INTO `ticket_ticketuser` VALUES (1389, '', '2021-08-01 12:47:34', '2021-08-01 12:53:04', 0, 'laoshia', 0, 0, 213);
INSERT INTO `ticket_ticketuser` VALUES (1390, '', '2021-08-01 12:47:34', '2021-08-01 12:53:04', 0, '23424', 0, 0, 213);
INSERT INTO `ticket_ticketuser` VALUES (1391, '', '2021-08-01 12:47:34', '2021-08-01 12:53:04', 0, 'dsfsffsdf', 0, 0, 213);
INSERT INTO `ticket_ticketuser` VALUES (1392, '', '2021-08-01 12:47:34', '2021-08-01 12:53:04', 0, 'test1111', 0, 0, 213);
INSERT INTO `ticket_ticketuser` VALUES (1393, '', '2021-08-01 12:47:34', '2021-08-01 12:53:04', 0, 'test2', 0, 0, 213);
INSERT INTO `ticket_ticketuser` VALUES (1394, '', '2021-08-01 12:47:34', '2021-08-01 12:53:04', 0, 'fdsfds', 0, 0, 213);
INSERT INTO `ticket_ticketuser` VALUES (1395, '', '2021-08-01 12:47:34', '2021-08-01 12:53:04', 0, 'fewf', 0, 0, 213);
INSERT INTO `ticket_ticketuser` VALUES (1396, '', '2021-08-01 12:47:34', '2021-08-01 12:53:04', 0, 'aaaa', 0, 0, 213);
INSERT INTO `ticket_ticketuser` VALUES (1397, '', '2021-08-01 12:47:34', '2021-08-01 12:53:04', 0, 'admin', 0, 0, 213);
INSERT INTO `ticket_ticketuser` VALUES (1398, '', '2021-08-01 12:55:35', '2021-08-01 12:56:03', 0, 'test', 0, 0, 214);
INSERT INTO `ticket_ticketuser` VALUES (1399, '', '2021-08-01 12:55:35', '2021-08-01 12:56:03', 0, '3333', 0, 0, 214);
INSERT INTO `ticket_ticketuser` VALUES (1400, '', '2021-08-01 12:55:35', '2021-08-01 12:59:54', 0, 'laoshi', 1, 1, 214);
INSERT INTO `ticket_ticketuser` VALUES (1401, '', '2021-08-01 12:55:35', '2021-08-01 12:56:03', 0, 'laoshia', 0, 0, 214);
INSERT INTO `ticket_ticketuser` VALUES (1402, '', '2021-08-01 12:55:35', '2021-08-01 12:56:03', 0, '23424', 0, 0, 214);
INSERT INTO `ticket_ticketuser` VALUES (1403, '', '2021-08-01 12:55:35', '2021-08-01 12:56:03', 0, 'dsfsffsdf', 0, 0, 214);
INSERT INTO `ticket_ticketuser` VALUES (1404, '', '2021-08-01 12:55:35', '2021-08-01 12:56:03', 0, 'test1111', 0, 0, 214);
INSERT INTO `ticket_ticketuser` VALUES (1405, '', '2021-08-01 12:55:35', '2021-08-01 12:56:03', 0, 'test2', 0, 0, 214);
INSERT INTO `ticket_ticketuser` VALUES (1406, '', '2021-08-01 12:55:35', '2021-08-01 12:56:03', 0, 'fdsfds', 0, 0, 214);
INSERT INTO `ticket_ticketuser` VALUES (1407, '', '2021-08-01 12:55:35', '2021-08-01 12:56:03', 0, 'fewf', 0, 0, 214);
INSERT INTO `ticket_ticketuser` VALUES (1408, '', '2021-08-01 12:55:35', '2021-08-01 12:56:03', 0, 'aaaa', 0, 0, 214);
INSERT INTO `ticket_ticketuser` VALUES (1409, '', '2021-08-01 12:55:35', '2021-08-01 12:56:03', 0, 'admin', 0, 0, 214);
INSERT INTO `ticket_ticketuser` VALUES (1410, '', '2021-08-01 13:01:15', '2021-08-01 13:01:27', 0, 'test', 0, 0, 215);
INSERT INTO `ticket_ticketuser` VALUES (1411, '', '2021-08-01 13:01:15', '2021-08-01 13:01:27', 0, 'aaaa', 0, 0, 215);
INSERT INTO `ticket_ticketuser` VALUES (1412, '', '2021-08-01 13:01:15', '2021-08-01 13:01:27', 0, 'test2', 0, 0, 215);
INSERT INTO `ticket_ticketuser` VALUES (1413, '', '2021-08-01 13:01:15', '2021-08-01 13:01:27', 0, 'laoshia', 0, 0, 215);
INSERT INTO `ticket_ticketuser` VALUES (1414, '', '2021-08-01 13:01:15', '2021-08-01 13:01:27', 0, 'test1111', 0, 0, 215);
INSERT INTO `ticket_ticketuser` VALUES (1415, '', '2021-08-01 13:01:15', '2021-08-01 13:01:27', 0, 'fewf', 0, 0, 215);
INSERT INTO `ticket_ticketuser` VALUES (1416, '', '2021-08-01 13:01:15', '2021-08-01 13:01:27', 0, 'admin', 0, 0, 215);
INSERT INTO `ticket_ticketuser` VALUES (1417, '', '2021-08-01 13:01:15', '2021-08-01 13:01:27', 0, '3333', 0, 0, 215);
INSERT INTO `ticket_ticketuser` VALUES (1418, '', '2021-08-01 13:01:15', '2021-08-01 13:01:36', 0, 'laoshi', 1, 1, 215);
INSERT INTO `ticket_ticketuser` VALUES (1419, '', '2021-08-01 13:01:15', '2021-08-01 13:01:27', 0, '23424', 0, 0, 215);
INSERT INTO `ticket_ticketuser` VALUES (1420, '', '2021-08-01 13:01:15', '2021-08-01 13:01:27', 0, 'dsfsffsdf', 0, 0, 215);
INSERT INTO `ticket_ticketuser` VALUES (1421, '', '2021-08-01 13:01:15', '2021-08-01 13:01:27', 0, 'fdsfds', 0, 0, 215);
INSERT INTO `ticket_ticketuser` VALUES (1422, '', '2021-08-01 13:05:31', '2021-08-01 13:05:43', 0, 'test', 0, 0, 216);
INSERT INTO `ticket_ticketuser` VALUES (1423, '', '2021-08-01 13:05:31', '2021-08-01 13:05:43', 0, 'test1111', 0, 0, 216);
INSERT INTO `ticket_ticketuser` VALUES (1424, '', '2021-08-01 13:05:31', '2021-08-01 13:05:43', 0, 'dsfsffsdf', 0, 0, 216);
INSERT INTO `ticket_ticketuser` VALUES (1425, '', '2021-08-01 13:05:31', '2021-08-01 13:05:43', 0, 'test2', 0, 0, 216);
INSERT INTO `ticket_ticketuser` VALUES (1426, '', '2021-08-01 13:05:31', '2021-08-01 13:05:43', 0, 'fewf', 0, 0, 216);
INSERT INTO `ticket_ticketuser` VALUES (1427, '', '2021-08-01 13:05:31', '2021-08-01 13:05:43', 0, 'fdsfds', 0, 0, 216);
INSERT INTO `ticket_ticketuser` VALUES (1428, '', '2021-08-01 13:05:31', '2021-08-01 13:05:43', 0, 'admin', 0, 0, 216);
INSERT INTO `ticket_ticketuser` VALUES (1429, '', '2021-08-01 13:05:31', '2021-08-01 13:05:43', 0, 'laoshi', 1, 1, 216);
INSERT INTO `ticket_ticketuser` VALUES (1430, '', '2021-08-01 13:05:31', '2021-08-01 13:05:43', 0, '3333', 0, 0, 216);
INSERT INTO `ticket_ticketuser` VALUES (1431, '', '2021-08-01 13:05:31', '2021-08-01 13:05:43', 0, 'aaaa', 0, 0, 216);
INSERT INTO `ticket_ticketuser` VALUES (1432, '', '2021-08-01 13:05:31', '2021-08-01 13:05:43', 0, 'laoshia', 0, 0, 216);
INSERT INTO `ticket_ticketuser` VALUES (1433, '', '2021-08-01 13:05:31', '2021-08-01 13:05:43', 0, '23424', 0, 0, 216);
INSERT INTO `ticket_ticketuser` VALUES (1434, '', '2021-08-01 13:07:56', '2021-08-01 13:08:01', 0, 'test', 0, 0, 217);
INSERT INTO `ticket_ticketuser` VALUES (1435, '', '2021-08-01 13:07:56', '2021-08-01 13:08:01', 0, 'test1111', 0, 0, 217);
INSERT INTO `ticket_ticketuser` VALUES (1436, '', '2021-08-01 13:07:56', '2021-08-01 13:08:01', 0, 'dsfsffsdf', 0, 0, 217);
INSERT INTO `ticket_ticketuser` VALUES (1437, '', '2021-08-01 13:07:56', '2021-08-01 13:08:01', 0, 'test2', 0, 0, 217);
INSERT INTO `ticket_ticketuser` VALUES (1438, '', '2021-08-01 13:07:56', '2021-08-01 13:08:01', 0, 'fewf', 0, 0, 217);
INSERT INTO `ticket_ticketuser` VALUES (1439, '', '2021-08-01 13:07:56', '2021-08-01 13:08:01', 0, 'fdsfds', 0, 0, 217);
INSERT INTO `ticket_ticketuser` VALUES (1440, '', '2021-08-01 13:07:56', '2021-08-01 13:08:01', 0, 'admin', 0, 0, 217);
INSERT INTO `ticket_ticketuser` VALUES (1441, '', '2021-08-01 13:07:56', '2021-08-01 15:06:54', 0, 'laoshi', 0, 1, 217);
INSERT INTO `ticket_ticketuser` VALUES (1442, '', '2021-08-01 13:07:56', '2021-08-01 13:08:01', 0, '3333', 0, 0, 217);
INSERT INTO `ticket_ticketuser` VALUES (1443, '', '2021-08-01 13:07:56', '2021-08-01 13:08:01', 0, 'aaaa', 0, 0, 217);
INSERT INTO `ticket_ticketuser` VALUES (1444, '', '2021-08-01 13:07:56', '2021-08-01 13:08:01', 0, 'laoshia', 0, 0, 217);
INSERT INTO `ticket_ticketuser` VALUES (1445, '', '2021-08-01 13:07:56', '2021-08-01 13:08:01', 0, '23424', 0, 0, 217);
INSERT INTO `ticket_ticketuser` VALUES (1446, '', '2021-08-01 13:17:30', '2021-08-01 13:17:29', 0, 'laoshi', 1, 0, 218);
INSERT INTO `ticket_ticketuser` VALUES (1447, '', '2021-08-01 13:17:30', '2021-08-01 13:17:30', 0, 'fewf', 1, 0, 218);
INSERT INTO `ticket_ticketuser` VALUES (1448, '', '2021-08-01 13:17:30', '2021-08-01 13:17:30', 0, 'test1111', 1, 0, 218);
INSERT INTO `ticket_ticketuser` VALUES (1449, '', '2021-08-01 13:17:30', '2021-08-01 13:17:30', 0, 'aaaa', 1, 0, 218);
INSERT INTO `ticket_ticketuser` VALUES (1450, '', '2021-08-01 13:17:30', '2021-08-01 13:17:30', 0, 'test', 1, 0, 218);
INSERT INTO `ticket_ticketuser` VALUES (1451, '', '2021-08-01 13:17:30', '2021-08-01 13:17:30', 0, 'laoshia', 1, 0, 218);
INSERT INTO `ticket_ticketuser` VALUES (1452, '', '2021-08-01 13:17:30', '2021-08-01 13:17:30', 0, 'fdsfds', 1, 0, 218);
INSERT INTO `ticket_ticketuser` VALUES (1453, '', '2021-08-01 13:17:30', '2021-08-01 13:17:30', 0, 'test2', 1, 0, 218);
INSERT INTO `ticket_ticketuser` VALUES (1454, '', '2021-08-01 13:17:30', '2021-08-01 13:17:30', 0, '23424', 1, 0, 218);
INSERT INTO `ticket_ticketuser` VALUES (1455, '', '2021-08-01 13:17:30', '2021-08-01 13:17:30', 0, 'admin', 1, 0, 218);
INSERT INTO `ticket_ticketuser` VALUES (1456, '', '2021-08-01 13:17:30', '2021-08-01 13:17:30', 0, 'dsfsffsdf', 1, 0, 218);
INSERT INTO `ticket_ticketuser` VALUES (1457, '', '2021-08-01 13:17:30', '2021-08-01 13:17:30', 0, '3333', 1, 0, 218);
INSERT INTO `ticket_ticketuser` VALUES (1458, '', '2021-08-01 13:22:42', '2021-08-01 13:22:41', 0, 'laoshi', 1, 0, 219);
INSERT INTO `ticket_ticketuser` VALUES (1459, '', '2021-08-01 13:22:42', '2021-08-01 13:22:42', 0, 'fewf', 1, 0, 219);
INSERT INTO `ticket_ticketuser` VALUES (1460, '', '2021-08-01 13:22:42', '2021-08-01 13:22:42', 0, 'test1111', 1, 0, 219);
INSERT INTO `ticket_ticketuser` VALUES (1461, '', '2021-08-01 13:22:42', '2021-08-01 13:22:42', 0, 'aaaa', 1, 0, 219);
INSERT INTO `ticket_ticketuser` VALUES (1462, '', '2021-08-01 13:22:42', '2021-08-01 13:22:42', 0, 'test', 1, 0, 219);
INSERT INTO `ticket_ticketuser` VALUES (1463, '', '2021-08-01 13:22:42', '2021-08-01 13:22:42', 0, 'laoshia', 1, 0, 219);
INSERT INTO `ticket_ticketuser` VALUES (1464, '', '2021-08-01 13:22:42', '2021-08-01 13:22:42', 0, 'fdsfds', 1, 0, 219);
INSERT INTO `ticket_ticketuser` VALUES (1465, '', '2021-08-01 13:22:42', '2021-08-01 13:22:42', 0, 'test2', 1, 0, 219);
INSERT INTO `ticket_ticketuser` VALUES (1466, '', '2021-08-01 13:22:42', '2021-08-01 13:22:42', 0, '23424', 1, 0, 219);
INSERT INTO `ticket_ticketuser` VALUES (1467, '', '2021-08-01 13:22:42', '2021-08-01 13:22:42', 0, 'admin', 1, 0, 219);
INSERT INTO `ticket_ticketuser` VALUES (1468, '', '2021-08-01 13:22:42', '2021-08-01 13:22:42', 0, 'dsfsffsdf', 1, 0, 219);
INSERT INTO `ticket_ticketuser` VALUES (1469, '', '2021-08-01 13:22:42', '2021-08-01 13:22:42', 0, '3333', 1, 0, 219);
INSERT INTO `ticket_ticketuser` VALUES (1470, '', '2021-08-01 13:22:55', '2021-08-01 13:22:54', 0, 'laoshi', 1, 0, 220);
INSERT INTO `ticket_ticketuser` VALUES (1471, '', '2021-08-01 13:22:55', '2021-08-01 13:22:55', 0, 'fewf', 1, 0, 220);
INSERT INTO `ticket_ticketuser` VALUES (1472, '', '2021-08-01 13:22:55', '2021-08-01 13:22:55', 0, 'test1111', 1, 0, 220);
INSERT INTO `ticket_ticketuser` VALUES (1473, '', '2021-08-01 13:22:55', '2021-08-01 13:22:55', 0, 'aaaa', 1, 0, 220);
INSERT INTO `ticket_ticketuser` VALUES (1474, '', '2021-08-01 13:22:55', '2021-08-01 13:22:55', 0, 'test', 1, 0, 220);
INSERT INTO `ticket_ticketuser` VALUES (1475, '', '2021-08-01 13:22:55', '2021-08-01 13:22:55', 0, 'laoshia', 1, 0, 220);
INSERT INTO `ticket_ticketuser` VALUES (1476, '', '2021-08-01 13:22:55', '2021-08-01 13:22:55', 0, 'fdsfds', 1, 0, 220);
INSERT INTO `ticket_ticketuser` VALUES (1477, '', '2021-08-01 13:22:55', '2021-08-01 13:22:55', 0, 'test2', 1, 0, 220);
INSERT INTO `ticket_ticketuser` VALUES (1478, '', '2021-08-01 13:22:55', '2021-08-01 13:22:55', 0, '23424', 1, 0, 220);
INSERT INTO `ticket_ticketuser` VALUES (1479, '', '2021-08-01 13:22:55', '2021-08-01 13:22:55', 0, 'admin', 1, 0, 220);
INSERT INTO `ticket_ticketuser` VALUES (1480, '', '2021-08-01 13:22:55', '2021-08-01 13:22:55', 0, 'dsfsffsdf', 1, 0, 220);
INSERT INTO `ticket_ticketuser` VALUES (1481, '', '2021-08-01 13:22:55', '2021-08-01 13:22:55', 0, '3333', 1, 0, 220);
INSERT INTO `ticket_ticketuser` VALUES (1482, '', '2021-08-01 13:23:09', '2021-08-01 13:23:08', 0, 'laoshi', 1, 0, 221);
INSERT INTO `ticket_ticketuser` VALUES (1483, '', '2021-08-01 13:23:09', '2021-08-01 13:23:09', 0, 'fewf', 1, 0, 221);
INSERT INTO `ticket_ticketuser` VALUES (1484, '', '2021-08-01 13:23:09', '2021-08-01 13:23:09', 0, 'test1111', 1, 0, 221);
INSERT INTO `ticket_ticketuser` VALUES (1485, '', '2021-08-01 13:23:09', '2021-08-01 13:23:09', 0, 'aaaa', 1, 0, 221);
INSERT INTO `ticket_ticketuser` VALUES (1486, '', '2021-08-01 13:23:09', '2021-08-01 13:23:09', 0, 'test', 1, 0, 221);
INSERT INTO `ticket_ticketuser` VALUES (1487, '', '2021-08-01 13:23:09', '2021-08-01 13:23:09', 0, 'laoshia', 1, 0, 221);
INSERT INTO `ticket_ticketuser` VALUES (1488, '', '2021-08-01 13:23:09', '2021-08-01 13:23:09', 0, 'fdsfds', 1, 0, 221);
INSERT INTO `ticket_ticketuser` VALUES (1489, '', '2021-08-01 13:23:09', '2021-08-01 13:23:09', 0, 'test2', 1, 0, 221);
INSERT INTO `ticket_ticketuser` VALUES (1490, '', '2021-08-01 13:23:09', '2021-08-01 13:23:09', 0, '23424', 1, 0, 221);
INSERT INTO `ticket_ticketuser` VALUES (1491, '', '2021-08-01 13:23:09', '2021-08-01 13:23:09', 0, 'admin', 1, 0, 221);
INSERT INTO `ticket_ticketuser` VALUES (1492, '', '2021-08-01 13:23:09', '2021-08-01 13:23:09', 0, 'dsfsffsdf', 1, 0, 221);
INSERT INTO `ticket_ticketuser` VALUES (1493, '', '2021-08-01 13:23:09', '2021-08-01 13:23:09', 0, '3333', 1, 0, 221);
INSERT INTO `ticket_ticketuser` VALUES (1494, '', '2021-08-01 13:26:59', '2021-08-01 13:26:58', 0, 'laoshi', 1, 0, 222);
INSERT INTO `ticket_ticketuser` VALUES (1495, '', '2021-08-01 13:26:59', '2021-08-01 13:26:59', 0, 'test2', 1, 0, 222);
INSERT INTO `ticket_ticketuser` VALUES (1496, '', '2021-08-01 13:26:59', '2021-08-01 13:26:59', 0, 'aaaa', 1, 0, 222);
INSERT INTO `ticket_ticketuser` VALUES (1497, '', '2021-08-01 13:26:59', '2021-08-01 13:26:59', 0, '23424', 1, 0, 222);
INSERT INTO `ticket_ticketuser` VALUES (1498, '', '2021-08-01 13:26:59', '2021-08-01 13:26:59', 0, 'admin', 1, 0, 222);
INSERT INTO `ticket_ticketuser` VALUES (1499, '', '2021-08-01 13:26:59', '2021-08-01 13:26:59', 0, '3333', 1, 0, 222);
INSERT INTO `ticket_ticketuser` VALUES (1500, '', '2021-08-01 13:26:59', '2021-08-01 13:26:59', 0, 'test1111', 1, 0, 222);
INSERT INTO `ticket_ticketuser` VALUES (1501, '', '2021-08-01 13:26:59', '2021-08-01 13:26:59', 0, 'dsfsffsdf', 1, 0, 222);
INSERT INTO `ticket_ticketuser` VALUES (1502, '', '2021-08-01 13:26:59', '2021-08-01 13:26:59', 0, 'laoshia', 1, 0, 222);
INSERT INTO `ticket_ticketuser` VALUES (1503, '', '2021-08-01 13:26:59', '2021-08-01 13:26:59', 0, 'test', 1, 0, 222);
INSERT INTO `ticket_ticketuser` VALUES (1504, '', '2021-08-01 13:26:59', '2021-08-01 13:26:59', 0, 'fdsfds', 1, 0, 222);
INSERT INTO `ticket_ticketuser` VALUES (1505, '', '2021-08-01 13:26:59', '2021-08-01 13:26:59', 0, 'fewf', 1, 0, 222);
INSERT INTO `ticket_ticketuser` VALUES (1506, '', '2021-08-01 13:33:39', '2021-08-01 13:33:39', 0, 'laoshi', 1, 0, 223);
INSERT INTO `ticket_ticketuser` VALUES (1507, '', '2021-08-01 13:33:39', '2021-08-01 13:33:39', 0, 'test1111', 1, 0, 223);
INSERT INTO `ticket_ticketuser` VALUES (1508, '', '2021-08-01 13:33:39', '2021-08-01 13:33:39', 0, 'fdsfds', 1, 0, 223);
INSERT INTO `ticket_ticketuser` VALUES (1509, '', '2021-08-01 13:33:39', '2021-08-01 13:33:39', 0, 'laoshia', 1, 0, 223);
INSERT INTO `ticket_ticketuser` VALUES (1510, '', '2021-08-01 13:33:39', '2021-08-01 13:33:39', 0, 'test2', 1, 0, 223);
INSERT INTO `ticket_ticketuser` VALUES (1511, '', '2021-08-01 13:33:39', '2021-08-01 13:33:39', 0, 'test', 1, 0, 223);
INSERT INTO `ticket_ticketuser` VALUES (1512, '', '2021-08-01 13:33:39', '2021-08-01 13:33:39', 0, 'fewf', 1, 0, 223);
INSERT INTO `ticket_ticketuser` VALUES (1513, '', '2021-08-01 13:33:39', '2021-08-01 13:33:39', 0, '3333', 1, 0, 223);
INSERT INTO `ticket_ticketuser` VALUES (1514, '', '2021-08-01 13:33:39', '2021-08-01 13:33:39', 0, '23424', 1, 0, 223);
INSERT INTO `ticket_ticketuser` VALUES (1515, '', '2021-08-01 13:33:39', '2021-08-01 13:33:39', 0, 'dsfsffsdf', 1, 0, 223);
INSERT INTO `ticket_ticketuser` VALUES (1516, '', '2021-08-01 13:33:39', '2021-08-01 13:33:39', 0, 'admin', 1, 0, 223);
INSERT INTO `ticket_ticketuser` VALUES (1517, '', '2021-08-01 13:33:39', '2021-08-01 13:33:39', 0, 'aaaa', 1, 0, 223);
INSERT INTO `ticket_ticketuser` VALUES (1518, '', '2021-08-01 13:38:51', '2021-08-01 13:38:50', 0, 'laoshi', 1, 0, 224);
INSERT INTO `ticket_ticketuser` VALUES (1519, '', '2021-08-01 13:38:51', '2021-08-01 13:38:51', 0, 'dsfsffsdf', 1, 0, 224);
INSERT INTO `ticket_ticketuser` VALUES (1520, '', '2021-08-01 13:38:51', '2021-08-01 13:38:51', 0, '3333', 1, 0, 224);
INSERT INTO `ticket_ticketuser` VALUES (1521, '', '2021-08-01 13:38:51', '2021-08-01 13:38:51', 0, '23424', 1, 0, 224);
INSERT INTO `ticket_ticketuser` VALUES (1522, '', '2021-08-01 13:38:51', '2021-08-01 13:38:51', 0, 'test', 1, 0, 224);
INSERT INTO `ticket_ticketuser` VALUES (1523, '', '2021-08-01 13:38:51', '2021-08-01 13:38:51', 0, 'test1111', 1, 0, 224);
INSERT INTO `ticket_ticketuser` VALUES (1524, '', '2021-08-01 13:38:51', '2021-08-01 13:38:51', 0, 'fewf', 1, 0, 224);
INSERT INTO `ticket_ticketuser` VALUES (1525, '', '2021-08-01 13:38:51', '2021-08-01 13:38:51', 0, 'aaaa', 1, 0, 224);
INSERT INTO `ticket_ticketuser` VALUES (1526, '', '2021-08-01 13:38:51', '2021-08-01 13:38:51', 0, 'test2', 1, 0, 224);
INSERT INTO `ticket_ticketuser` VALUES (1527, '', '2021-08-01 13:38:51', '2021-08-01 13:38:51', 0, 'fdsfds', 1, 0, 224);
INSERT INTO `ticket_ticketuser` VALUES (1528, '', '2021-08-01 13:38:51', '2021-08-01 13:38:51', 0, 'admin', 1, 0, 224);
INSERT INTO `ticket_ticketuser` VALUES (1529, '', '2021-08-01 13:38:51', '2021-08-01 13:38:51', 0, 'laoshia', 1, 0, 224);
INSERT INTO `ticket_ticketuser` VALUES (1530, '', '2021-08-01 13:40:22', '2021-08-01 13:40:21', 0, 'laoshi', 1, 0, 225);
INSERT INTO `ticket_ticketuser` VALUES (1531, '', '2021-08-01 13:40:22', '2021-08-01 13:40:22', 0, '3333', 1, 0, 225);
INSERT INTO `ticket_ticketuser` VALUES (1532, '', '2021-08-01 13:40:22', '2021-08-01 13:40:22', 0, 'test2', 1, 0, 225);
INSERT INTO `ticket_ticketuser` VALUES (1533, '', '2021-08-01 13:40:22', '2021-08-01 13:40:22', 0, 'aaaa', 1, 0, 225);
INSERT INTO `ticket_ticketuser` VALUES (1534, '', '2021-08-01 13:40:22', '2021-08-01 13:40:22', 0, '23424', 1, 0, 225);
INSERT INTO `ticket_ticketuser` VALUES (1535, '', '2021-08-01 13:40:22', '2021-08-01 13:40:22', 0, 'fdsfds', 1, 0, 225);
INSERT INTO `ticket_ticketuser` VALUES (1536, '', '2021-08-01 13:40:22', '2021-08-01 13:40:22', 0, 'fewf', 1, 0, 225);
INSERT INTO `ticket_ticketuser` VALUES (1537, '', '2021-08-01 13:40:22', '2021-08-01 13:40:22', 0, 'admin', 1, 0, 225);
INSERT INTO `ticket_ticketuser` VALUES (1538, '', '2021-08-01 13:40:22', '2021-08-01 13:40:22', 0, 'test', 1, 0, 225);
INSERT INTO `ticket_ticketuser` VALUES (1539, '', '2021-08-01 13:40:22', '2021-08-01 13:40:22', 0, 'laoshia', 1, 0, 225);
INSERT INTO `ticket_ticketuser` VALUES (1540, '', '2021-08-01 13:40:22', '2021-08-01 13:40:22', 0, 'test1111', 1, 0, 225);
INSERT INTO `ticket_ticketuser` VALUES (1541, '', '2021-08-01 13:40:22', '2021-08-01 13:40:22', 0, 'dsfsffsdf', 1, 0, 225);
INSERT INTO `ticket_ticketuser` VALUES (1542, '', '2021-08-01 13:41:05', '2021-08-01 13:41:05', 0, 'laoshi', 1, 0, 226);
INSERT INTO `ticket_ticketuser` VALUES (1543, '', '2021-08-01 13:41:05', '2021-08-01 13:41:05', 0, '3333', 1, 0, 226);
INSERT INTO `ticket_ticketuser` VALUES (1544, '', '2021-08-01 13:41:05', '2021-08-01 13:41:05', 0, 'test2', 1, 0, 226);
INSERT INTO `ticket_ticketuser` VALUES (1545, '', '2021-08-01 13:41:05', '2021-08-01 13:41:05', 0, 'aaaa', 1, 0, 226);
INSERT INTO `ticket_ticketuser` VALUES (1546, '', '2021-08-01 13:41:05', '2021-08-01 13:41:05', 0, '23424', 1, 0, 226);
INSERT INTO `ticket_ticketuser` VALUES (1547, '', '2021-08-01 13:41:05', '2021-08-01 13:41:05', 0, 'fdsfds', 1, 0, 226);
INSERT INTO `ticket_ticketuser` VALUES (1548, '', '2021-08-01 13:41:05', '2021-08-01 13:41:05', 0, 'fewf', 1, 0, 226);
INSERT INTO `ticket_ticketuser` VALUES (1549, '', '2021-08-01 13:41:05', '2021-08-01 13:41:05', 0, 'admin', 1, 0, 226);
INSERT INTO `ticket_ticketuser` VALUES (1550, '', '2021-08-01 13:41:05', '2021-08-01 13:41:05', 0, 'test', 1, 0, 226);
INSERT INTO `ticket_ticketuser` VALUES (1551, '', '2021-08-01 13:41:05', '2021-08-01 13:41:05', 0, 'laoshia', 1, 0, 226);
INSERT INTO `ticket_ticketuser` VALUES (1552, '', '2021-08-01 13:41:05', '2021-08-01 13:41:05', 0, 'test1111', 1, 0, 226);
INSERT INTO `ticket_ticketuser` VALUES (1553, '', '2021-08-01 13:41:05', '2021-08-01 13:41:05', 0, 'dsfsffsdf', 1, 0, 226);
INSERT INTO `ticket_ticketuser` VALUES (1554, '', '2021-08-01 13:46:45', '2021-08-01 13:46:44', 0, 'laoshi', 1, 0, 227);
INSERT INTO `ticket_ticketuser` VALUES (1555, '', '2021-08-01 13:46:45', '2021-08-01 13:46:45', 0, 'test1111', 1, 0, 227);
INSERT INTO `ticket_ticketuser` VALUES (1556, '', '2021-08-01 13:46:45', '2021-08-01 13:46:45', 0, '23424', 1, 0, 227);
INSERT INTO `ticket_ticketuser` VALUES (1557, '', '2021-08-01 13:46:45', '2021-08-01 13:46:45', 0, 'fdsfds', 1, 0, 227);
INSERT INTO `ticket_ticketuser` VALUES (1558, '', '2021-08-01 13:46:45', '2021-08-01 13:46:45', 0, 'fewf', 1, 0, 227);
INSERT INTO `ticket_ticketuser` VALUES (1559, '', '2021-08-01 13:46:45', '2021-08-01 13:46:45', 0, 'laoshia', 1, 0, 227);
INSERT INTO `ticket_ticketuser` VALUES (1560, '', '2021-08-01 13:46:45', '2021-08-01 13:46:45', 0, 'test', 1, 0, 227);
INSERT INTO `ticket_ticketuser` VALUES (1561, '', '2021-08-01 13:46:45', '2021-08-01 13:46:45', 0, 'dsfsffsdf', 1, 0, 227);
INSERT INTO `ticket_ticketuser` VALUES (1562, '', '2021-08-01 13:46:45', '2021-08-01 13:46:45', 0, 'admin', 1, 0, 227);
INSERT INTO `ticket_ticketuser` VALUES (1563, '', '2021-08-01 13:46:45', '2021-08-01 13:46:45', 0, 'test2', 1, 0, 227);
INSERT INTO `ticket_ticketuser` VALUES (1564, '', '2021-08-01 13:46:45', '2021-08-01 13:46:45', 0, '3333', 1, 0, 227);
INSERT INTO `ticket_ticketuser` VALUES (1565, '', '2021-08-01 13:46:45', '2021-08-01 13:46:45', 0, 'aaaa', 1, 0, 227);
INSERT INTO `ticket_ticketuser` VALUES (1566, '', '2021-08-01 13:48:01', '2021-08-01 13:48:01', 0, 'laoshi', 1, 0, 228);
INSERT INTO `ticket_ticketuser` VALUES (1567, '', '2021-08-01 13:48:01', '2021-08-01 13:48:01', 0, 'dsfsffsdf', 1, 0, 228);
INSERT INTO `ticket_ticketuser` VALUES (1568, '', '2021-08-01 13:48:01', '2021-08-01 13:48:01', 0, 'test', 1, 0, 228);
INSERT INTO `ticket_ticketuser` VALUES (1569, '', '2021-08-01 13:48:01', '2021-08-01 13:48:01', 0, 'test2', 1, 0, 228);
INSERT INTO `ticket_ticketuser` VALUES (1570, '', '2021-08-01 13:48:01', '2021-08-01 13:48:01', 0, 'laoshia', 1, 0, 228);
INSERT INTO `ticket_ticketuser` VALUES (1571, '', '2021-08-01 13:48:01', '2021-08-01 13:48:01', 0, '23424', 1, 0, 228);
INSERT INTO `ticket_ticketuser` VALUES (1572, '', '2021-08-01 13:48:01', '2021-08-01 13:48:01', 0, 'admin', 1, 0, 228);
INSERT INTO `ticket_ticketuser` VALUES (1573, '', '2021-08-01 13:48:01', '2021-08-01 13:48:01', 0, 'fewf', 1, 0, 228);
INSERT INTO `ticket_ticketuser` VALUES (1574, '', '2021-08-01 13:48:01', '2021-08-01 13:48:01', 0, 'aaaa', 1, 0, 228);
INSERT INTO `ticket_ticketuser` VALUES (1575, '', '2021-08-01 13:48:01', '2021-08-01 13:48:01', 0, '3333', 1, 0, 228);
INSERT INTO `ticket_ticketuser` VALUES (1576, '', '2021-08-01 13:48:01', '2021-08-01 13:48:01', 0, 'fdsfds', 1, 0, 228);
INSERT INTO `ticket_ticketuser` VALUES (1577, '', '2021-08-01 13:48:01', '2021-08-01 13:48:01', 0, 'test1111', 1, 0, 228);
INSERT INTO `ticket_ticketuser` VALUES (1578, '', '2021-08-01 13:48:55', '2021-08-01 13:48:55', 0, 'laoshi', 1, 0, 229);
INSERT INTO `ticket_ticketuser` VALUES (1579, '', '2021-08-01 13:48:55', '2021-08-01 13:48:55', 0, 'dsfsffsdf', 1, 0, 229);
INSERT INTO `ticket_ticketuser` VALUES (1580, '', '2021-08-01 13:48:55', '2021-08-01 13:48:55', 0, 'test', 1, 0, 229);
INSERT INTO `ticket_ticketuser` VALUES (1581, '', '2021-08-01 13:48:55', '2021-08-01 13:48:55', 0, 'test2', 1, 0, 229);
INSERT INTO `ticket_ticketuser` VALUES (1582, '', '2021-08-01 13:48:55', '2021-08-01 13:48:55', 0, 'laoshia', 1, 0, 229);
INSERT INTO `ticket_ticketuser` VALUES (1583, '', '2021-08-01 13:48:55', '2021-08-01 13:48:55', 0, '23424', 1, 0, 229);
INSERT INTO `ticket_ticketuser` VALUES (1584, '', '2021-08-01 13:48:55', '2021-08-01 13:48:55', 0, 'admin', 1, 0, 229);
INSERT INTO `ticket_ticketuser` VALUES (1585, '', '2021-08-01 13:48:55', '2021-08-01 13:48:55', 0, 'fewf', 1, 0, 229);
INSERT INTO `ticket_ticketuser` VALUES (1586, '', '2021-08-01 13:48:55', '2021-08-01 13:48:55', 0, 'aaaa', 1, 0, 229);
INSERT INTO `ticket_ticketuser` VALUES (1587, '', '2021-08-01 13:48:55', '2021-08-01 13:48:55', 0, '3333', 1, 0, 229);
INSERT INTO `ticket_ticketuser` VALUES (1588, '', '2021-08-01 13:48:55', '2021-08-01 13:48:55', 0, 'fdsfds', 1, 0, 229);
INSERT INTO `ticket_ticketuser` VALUES (1589, '', '2021-08-01 13:48:55', '2021-08-01 13:48:55', 0, 'test1111', 1, 0, 229);
INSERT INTO `ticket_ticketuser` VALUES (1590, '', '2021-08-01 13:50:14', '2021-08-01 13:50:14', 0, 'laoshi', 1, 0, 230);
INSERT INTO `ticket_ticketuser` VALUES (1591, '', '2021-08-01 13:50:14', '2021-08-01 13:50:14', 0, 'test', 1, 0, 230);
INSERT INTO `ticket_ticketuser` VALUES (1592, '', '2021-08-01 13:50:14', '2021-08-01 13:50:14', 0, 'fdsfds', 1, 0, 230);
INSERT INTO `ticket_ticketuser` VALUES (1593, '', '2021-08-01 13:50:14', '2021-08-01 13:50:14', 0, 'laoshia', 1, 0, 230);
INSERT INTO `ticket_ticketuser` VALUES (1594, '', '2021-08-01 13:50:14', '2021-08-01 13:50:14', 0, 'dsfsffsdf', 1, 0, 230);
INSERT INTO `ticket_ticketuser` VALUES (1595, '', '2021-08-01 13:50:14', '2021-08-01 13:50:14', 0, '3333', 1, 0, 230);
INSERT INTO `ticket_ticketuser` VALUES (1596, '', '2021-08-01 13:50:14', '2021-08-01 13:50:14', 0, '23424', 1, 0, 230);
INSERT INTO `ticket_ticketuser` VALUES (1597, '', '2021-08-01 13:50:14', '2021-08-01 13:50:14', 0, 'fewf', 1, 0, 230);
INSERT INTO `ticket_ticketuser` VALUES (1598, '', '2021-08-01 13:50:14', '2021-08-01 13:50:14', 0, 'aaaa', 1, 0, 230);
INSERT INTO `ticket_ticketuser` VALUES (1599, '', '2021-08-01 13:50:14', '2021-08-01 13:50:14', 0, 'admin', 1, 0, 230);
INSERT INTO `ticket_ticketuser` VALUES (1600, '', '2021-08-01 13:50:14', '2021-08-01 13:50:14', 0, 'test1111', 1, 0, 230);
INSERT INTO `ticket_ticketuser` VALUES (1601, '', '2021-08-01 13:50:14', '2021-08-01 13:50:14', 0, 'test2', 1, 0, 230);
INSERT INTO `ticket_ticketuser` VALUES (1602, '', '2021-08-01 14:02:25', '2021-08-01 14:02:25', 0, 'laoshi', 1, 0, 231);
INSERT INTO `ticket_ticketuser` VALUES (1603, '', '2021-08-01 14:02:25', '2021-08-01 14:02:25', 0, 'test', 1, 0, 231);
INSERT INTO `ticket_ticketuser` VALUES (1604, '', '2021-08-01 14:02:25', '2021-08-01 14:02:25', 0, 'fdsfds', 1, 0, 231);
INSERT INTO `ticket_ticketuser` VALUES (1605, '', '2021-08-01 14:02:25', '2021-08-01 14:02:25', 0, 'laoshia', 1, 0, 231);
INSERT INTO `ticket_ticketuser` VALUES (1606, '', '2021-08-01 14:02:25', '2021-08-01 14:02:25', 0, 'dsfsffsdf', 1, 0, 231);
INSERT INTO `ticket_ticketuser` VALUES (1607, '', '2021-08-01 14:02:25', '2021-08-01 14:02:25', 0, '3333', 1, 0, 231);
INSERT INTO `ticket_ticketuser` VALUES (1608, '', '2021-08-01 14:02:25', '2021-08-01 14:02:25', 0, '23424', 1, 0, 231);
INSERT INTO `ticket_ticketuser` VALUES (1609, '', '2021-08-01 14:02:25', '2021-08-01 14:02:25', 0, 'fewf', 1, 0, 231);
INSERT INTO `ticket_ticketuser` VALUES (1610, '', '2021-08-01 14:02:25', '2021-08-01 14:02:25', 0, 'aaaa', 1, 0, 231);
INSERT INTO `ticket_ticketuser` VALUES (1611, '', '2021-08-01 14:02:25', '2021-08-01 14:02:25', 0, 'admin', 1, 0, 231);
INSERT INTO `ticket_ticketuser` VALUES (1612, '', '2021-08-01 14:02:25', '2021-08-01 14:02:25', 0, 'test1111', 1, 0, 231);
INSERT INTO `ticket_ticketuser` VALUES (1613, '', '2021-08-01 14:02:25', '2021-08-01 14:02:25', 0, 'test2', 1, 0, 231);
INSERT INTO `ticket_ticketuser` VALUES (1614, '', '2021-08-01 14:06:12', '2021-08-01 14:06:12', 0, 'laoshi', 1, 0, 232);
INSERT INTO `ticket_ticketuser` VALUES (1615, '', '2021-08-01 14:06:12', '2021-08-01 14:06:12', 0, 'test', 1, 0, 232);
INSERT INTO `ticket_ticketuser` VALUES (1616, '', '2021-08-01 14:06:12', '2021-08-01 14:06:12', 0, 'fdsfds', 1, 0, 232);
INSERT INTO `ticket_ticketuser` VALUES (1617, '', '2021-08-01 14:06:12', '2021-08-01 14:06:12', 0, 'laoshia', 1, 0, 232);
INSERT INTO `ticket_ticketuser` VALUES (1618, '', '2021-08-01 14:06:12', '2021-08-01 14:06:12', 0, 'dsfsffsdf', 1, 0, 232);
INSERT INTO `ticket_ticketuser` VALUES (1619, '', '2021-08-01 14:06:12', '2021-08-01 14:06:12', 0, '3333', 1, 0, 232);
INSERT INTO `ticket_ticketuser` VALUES (1620, '', '2021-08-01 14:06:12', '2021-08-01 14:06:12', 0, '23424', 1, 0, 232);
INSERT INTO `ticket_ticketuser` VALUES (1621, '', '2021-08-01 14:06:12', '2021-08-01 14:06:12', 0, 'fewf', 1, 0, 232);
INSERT INTO `ticket_ticketuser` VALUES (1622, '', '2021-08-01 14:06:12', '2021-08-01 14:06:12', 0, 'aaaa', 1, 0, 232);
INSERT INTO `ticket_ticketuser` VALUES (1623, '', '2021-08-01 14:06:12', '2021-08-01 14:06:12', 0, 'admin', 1, 0, 232);
INSERT INTO `ticket_ticketuser` VALUES (1624, '', '2021-08-01 14:06:12', '2021-08-01 14:06:12', 0, 'test1111', 1, 0, 232);
INSERT INTO `ticket_ticketuser` VALUES (1625, '', '2021-08-01 14:06:12', '2021-08-01 14:06:12', 0, 'test2', 1, 0, 232);
INSERT INTO `ticket_ticketuser` VALUES (1626, '', '2021-08-01 14:07:59', '2021-08-01 14:07:59', 0, 'laoshi', 1, 0, 233);
INSERT INTO `ticket_ticketuser` VALUES (1627, '', '2021-08-01 14:07:59', '2021-08-01 14:07:59', 0, '3333', 1, 0, 233);
INSERT INTO `ticket_ticketuser` VALUES (1628, '', '2021-08-01 14:07:59', '2021-08-01 14:07:59', 0, 'dsfsffsdf', 1, 0, 233);
INSERT INTO `ticket_ticketuser` VALUES (1629, '', '2021-08-01 14:07:59', '2021-08-01 14:07:59', 0, 'fewf', 1, 0, 233);
INSERT INTO `ticket_ticketuser` VALUES (1630, '', '2021-08-01 14:07:59', '2021-08-01 14:07:59', 0, 'fdsfds', 1, 0, 233);
INSERT INTO `ticket_ticketuser` VALUES (1631, '', '2021-08-01 14:07:59', '2021-08-01 14:07:59', 0, 'aaaa', 1, 0, 233);
INSERT INTO `ticket_ticketuser` VALUES (1632, '', '2021-08-01 14:07:59', '2021-08-01 14:07:59', 0, 'test', 1, 0, 233);
INSERT INTO `ticket_ticketuser` VALUES (1633, '', '2021-08-01 14:07:59', '2021-08-01 14:07:59', 0, 'laoshia', 1, 0, 233);
INSERT INTO `ticket_ticketuser` VALUES (1634, '', '2021-08-01 14:07:59', '2021-08-01 14:07:59', 0, 'test1111', 1, 0, 233);
INSERT INTO `ticket_ticketuser` VALUES (1635, '', '2021-08-01 14:07:59', '2021-08-01 14:07:59', 0, 'test2', 1, 0, 233);
INSERT INTO `ticket_ticketuser` VALUES (1636, '', '2021-08-01 14:07:59', '2021-08-01 14:07:59', 0, '23424', 1, 0, 233);
INSERT INTO `ticket_ticketuser` VALUES (1637, '', '2021-08-01 14:07:59', '2021-08-01 14:07:59', 0, 'admin', 1, 0, 233);
INSERT INTO `ticket_ticketuser` VALUES (1638, '', '2021-08-01 14:18:24', '2021-08-01 14:18:24', 0, 'laoshi', 1, 0, 234);
INSERT INTO `ticket_ticketuser` VALUES (1639, '', '2021-08-01 14:18:24', '2021-08-01 14:18:24', 0, '3333', 1, 0, 234);
INSERT INTO `ticket_ticketuser` VALUES (1640, '', '2021-08-01 14:18:24', '2021-08-01 14:18:24', 0, 'dsfsffsdf', 1, 0, 234);
INSERT INTO `ticket_ticketuser` VALUES (1641, '', '2021-08-01 14:18:24', '2021-08-01 14:18:24', 0, 'fewf', 1, 0, 234);
INSERT INTO `ticket_ticketuser` VALUES (1642, '', '2021-08-01 14:18:24', '2021-08-01 14:18:24', 0, 'fdsfds', 1, 0, 234);
INSERT INTO `ticket_ticketuser` VALUES (1643, '', '2021-08-01 14:18:24', '2021-08-01 14:18:24', 0, 'aaaa', 1, 0, 234);
INSERT INTO `ticket_ticketuser` VALUES (1644, '', '2021-08-01 14:18:24', '2021-08-01 14:18:24', 0, 'test', 1, 0, 234);
INSERT INTO `ticket_ticketuser` VALUES (1645, '', '2021-08-01 14:18:24', '2021-08-01 14:18:24', 0, 'laoshia', 1, 0, 234);
INSERT INTO `ticket_ticketuser` VALUES (1646, '', '2021-08-01 14:18:24', '2021-08-01 14:18:24', 0, 'test1111', 1, 0, 234);
INSERT INTO `ticket_ticketuser` VALUES (1647, '', '2021-08-01 14:18:24', '2021-08-01 14:18:24', 0, 'test2', 1, 0, 234);
INSERT INTO `ticket_ticketuser` VALUES (1648, '', '2021-08-01 14:18:24', '2021-08-01 14:18:24', 0, '23424', 1, 0, 234);
INSERT INTO `ticket_ticketuser` VALUES (1649, '', '2021-08-01 14:18:24', '2021-08-01 14:18:24', 0, 'admin', 1, 0, 234);
INSERT INTO `ticket_ticketuser` VALUES (1650, '', '2021-08-01 14:18:54', '2021-08-01 14:18:53', 0, 'laoshi', 1, 0, 235);
INSERT INTO `ticket_ticketuser` VALUES (1651, '', '2021-08-01 14:18:54', '2021-08-01 14:18:54', 0, '3333', 1, 0, 235);
INSERT INTO `ticket_ticketuser` VALUES (1652, '', '2021-08-01 14:18:54', '2021-08-01 14:18:54', 0, 'dsfsffsdf', 1, 0, 235);
INSERT INTO `ticket_ticketuser` VALUES (1653, '', '2021-08-01 14:18:54', '2021-08-01 14:18:54', 0, 'fewf', 1, 0, 235);
INSERT INTO `ticket_ticketuser` VALUES (1654, '', '2021-08-01 14:18:54', '2021-08-01 14:18:54', 0, 'fdsfds', 1, 0, 235);
INSERT INTO `ticket_ticketuser` VALUES (1655, '', '2021-08-01 14:18:54', '2021-08-01 14:18:54', 0, 'aaaa', 1, 0, 235);
INSERT INTO `ticket_ticketuser` VALUES (1656, '', '2021-08-01 14:18:54', '2021-08-01 14:18:54', 0, 'test', 1, 0, 235);
INSERT INTO `ticket_ticketuser` VALUES (1657, '', '2021-08-01 14:18:54', '2021-08-01 14:18:54', 0, 'laoshia', 1, 0, 235);
INSERT INTO `ticket_ticketuser` VALUES (1658, '', '2021-08-01 14:18:54', '2021-08-01 14:18:54', 0, 'test1111', 1, 0, 235);
INSERT INTO `ticket_ticketuser` VALUES (1659, '', '2021-08-01 14:18:54', '2021-08-01 14:18:54', 0, 'test2', 1, 0, 235);
INSERT INTO `ticket_ticketuser` VALUES (1660, '', '2021-08-01 14:18:54', '2021-08-01 14:18:54', 0, '23424', 1, 0, 235);
INSERT INTO `ticket_ticketuser` VALUES (1661, '', '2021-08-01 14:18:54', '2021-08-01 14:18:54', 0, 'admin', 1, 0, 235);
INSERT INTO `ticket_ticketuser` VALUES (1662, '', '2021-08-01 14:21:42', '2021-08-01 14:21:42', 0, 'laoshi', 1, 0, 236);
INSERT INTO `ticket_ticketuser` VALUES (1663, '', '2021-08-01 14:21:42', '2021-08-01 14:21:42', 0, '3333', 1, 0, 236);
INSERT INTO `ticket_ticketuser` VALUES (1664, '', '2021-08-01 14:21:42', '2021-08-01 14:21:42', 0, 'dsfsffsdf', 1, 0, 236);
INSERT INTO `ticket_ticketuser` VALUES (1665, '', '2021-08-01 14:21:42', '2021-08-01 14:21:42', 0, 'fewf', 1, 0, 236);
INSERT INTO `ticket_ticketuser` VALUES (1666, '', '2021-08-01 14:21:42', '2021-08-01 14:21:42', 0, 'fdsfds', 1, 0, 236);
INSERT INTO `ticket_ticketuser` VALUES (1667, '', '2021-08-01 14:21:42', '2021-08-01 14:21:42', 0, 'aaaa', 1, 0, 236);
INSERT INTO `ticket_ticketuser` VALUES (1668, '', '2021-08-01 14:21:42', '2021-08-01 14:21:42', 0, 'test', 1, 0, 236);
INSERT INTO `ticket_ticketuser` VALUES (1669, '', '2021-08-01 14:21:42', '2021-08-01 14:21:42', 0, 'laoshia', 1, 0, 236);
INSERT INTO `ticket_ticketuser` VALUES (1670, '', '2021-08-01 14:21:42', '2021-08-01 14:21:42', 0, 'test1111', 1, 0, 236);
INSERT INTO `ticket_ticketuser` VALUES (1671, '', '2021-08-01 14:21:42', '2021-08-01 14:21:42', 0, 'test2', 1, 0, 236);
INSERT INTO `ticket_ticketuser` VALUES (1672, '', '2021-08-01 14:21:42', '2021-08-01 14:21:42', 0, '23424', 1, 0, 236);
INSERT INTO `ticket_ticketuser` VALUES (1673, '', '2021-08-01 14:21:42', '2021-08-01 14:21:42', 0, 'admin', 1, 0, 236);
INSERT INTO `ticket_ticketuser` VALUES (1674, '', '2021-08-01 14:37:14', '2021-08-01 14:37:14', 0, 'laoshi', 1, 0, 237);
INSERT INTO `ticket_ticketuser` VALUES (1675, '', '2021-08-01 14:37:14', '2021-08-01 14:37:14', 0, '3333', 1, 0, 237);
INSERT INTO `ticket_ticketuser` VALUES (1676, '', '2021-08-01 14:37:14', '2021-08-01 14:37:14', 0, 'dsfsffsdf', 1, 0, 237);
INSERT INTO `ticket_ticketuser` VALUES (1677, '', '2021-08-01 14:37:14', '2021-08-01 14:37:14', 0, 'fewf', 1, 0, 237);
INSERT INTO `ticket_ticketuser` VALUES (1678, '', '2021-08-01 14:37:14', '2021-08-01 14:37:14', 0, 'fdsfds', 1, 0, 237);
INSERT INTO `ticket_ticketuser` VALUES (1679, '', '2021-08-01 14:37:14', '2021-08-01 14:37:14', 0, 'aaaa', 1, 0, 237);
INSERT INTO `ticket_ticketuser` VALUES (1680, '', '2021-08-01 14:37:14', '2021-08-01 14:37:14', 0, 'test', 1, 0, 237);
INSERT INTO `ticket_ticketuser` VALUES (1681, '', '2021-08-01 14:37:14', '2021-08-01 14:37:14', 0, 'laoshia', 1, 0, 237);
INSERT INTO `ticket_ticketuser` VALUES (1682, '', '2021-08-01 14:37:14', '2021-08-01 14:37:14', 0, 'test1111', 1, 0, 237);
INSERT INTO `ticket_ticketuser` VALUES (1683, '', '2021-08-01 14:37:14', '2021-08-01 14:37:14', 0, 'test2', 1, 0, 237);
INSERT INTO `ticket_ticketuser` VALUES (1684, '', '2021-08-01 14:37:14', '2021-08-01 14:37:14', 0, '23424', 1, 0, 237);
INSERT INTO `ticket_ticketuser` VALUES (1685, '', '2021-08-01 14:37:14', '2021-08-01 14:37:14', 0, 'admin', 1, 0, 237);
INSERT INTO `ticket_ticketuser` VALUES (1686, '', '2021-08-01 14:39:26', '2021-08-01 14:39:26', 0, 'laoshi', 1, 0, 238);
INSERT INTO `ticket_ticketuser` VALUES (1687, '', '2021-08-01 14:39:26', '2021-08-01 14:39:26', 0, '3333', 1, 0, 238);
INSERT INTO `ticket_ticketuser` VALUES (1688, '', '2021-08-01 14:39:26', '2021-08-01 14:39:26', 0, 'dsfsffsdf', 1, 0, 238);
INSERT INTO `ticket_ticketuser` VALUES (1689, '', '2021-08-01 14:39:26', '2021-08-01 14:39:26', 0, 'fewf', 1, 0, 238);
INSERT INTO `ticket_ticketuser` VALUES (1690, '', '2021-08-01 14:39:26', '2021-08-01 14:39:26', 0, 'fdsfds', 1, 0, 238);
INSERT INTO `ticket_ticketuser` VALUES (1691, '', '2021-08-01 14:39:26', '2021-08-01 14:39:26', 0, 'aaaa', 1, 0, 238);
INSERT INTO `ticket_ticketuser` VALUES (1692, '', '2021-08-01 14:39:26', '2021-08-01 14:39:26', 0, 'test', 1, 0, 238);
INSERT INTO `ticket_ticketuser` VALUES (1693, '', '2021-08-01 14:39:26', '2021-08-01 14:39:26', 0, 'laoshia', 1, 0, 238);
INSERT INTO `ticket_ticketuser` VALUES (1694, '', '2021-08-01 14:39:26', '2021-08-01 14:39:26', 0, 'test1111', 1, 0, 238);
INSERT INTO `ticket_ticketuser` VALUES (1695, '', '2021-08-01 14:39:26', '2021-08-01 14:39:26', 0, 'test2', 1, 0, 238);
INSERT INTO `ticket_ticketuser` VALUES (1696, '', '2021-08-01 14:39:26', '2021-08-01 14:39:26', 0, '23424', 1, 0, 238);
INSERT INTO `ticket_ticketuser` VALUES (1697, '', '2021-08-01 14:39:26', '2021-08-01 14:39:26', 0, 'admin', 1, 0, 238);
INSERT INTO `ticket_ticketuser` VALUES (1698, '', '2021-08-01 14:40:45', '2021-08-01 14:40:44', 0, 'laoshi', 1, 0, 239);
INSERT INTO `ticket_ticketuser` VALUES (1699, '', '2021-08-01 14:40:45', '2021-08-01 14:40:45', 0, '3333', 1, 0, 239);
INSERT INTO `ticket_ticketuser` VALUES (1700, '', '2021-08-01 14:40:45', '2021-08-01 14:40:45', 0, 'dsfsffsdf', 1, 0, 239);
INSERT INTO `ticket_ticketuser` VALUES (1701, '', '2021-08-01 14:40:45', '2021-08-01 14:40:45', 0, 'fewf', 1, 0, 239);
INSERT INTO `ticket_ticketuser` VALUES (1702, '', '2021-08-01 14:40:45', '2021-08-01 14:40:45', 0, 'fdsfds', 1, 0, 239);
INSERT INTO `ticket_ticketuser` VALUES (1703, '', '2021-08-01 14:40:45', '2021-08-01 14:40:45', 0, 'aaaa', 1, 0, 239);
INSERT INTO `ticket_ticketuser` VALUES (1704, '', '2021-08-01 14:40:45', '2021-08-01 14:40:45', 0, 'test', 1, 0, 239);
INSERT INTO `ticket_ticketuser` VALUES (1705, '', '2021-08-01 14:40:45', '2021-08-01 14:40:45', 0, 'laoshia', 1, 0, 239);
INSERT INTO `ticket_ticketuser` VALUES (1706, '', '2021-08-01 14:40:45', '2021-08-01 14:40:45', 0, 'test1111', 1, 0, 239);
INSERT INTO `ticket_ticketuser` VALUES (1707, '', '2021-08-01 14:40:45', '2021-08-01 14:40:45', 0, 'test2', 1, 0, 239);
INSERT INTO `ticket_ticketuser` VALUES (1708, '', '2021-08-01 14:40:45', '2021-08-01 14:40:45', 0, '23424', 1, 0, 239);
INSERT INTO `ticket_ticketuser` VALUES (1709, '', '2021-08-01 14:40:45', '2021-08-01 14:40:45', 0, 'admin', 1, 0, 239);
INSERT INTO `ticket_ticketuser` VALUES (1710, '', '2021-08-01 14:53:02', '2021-08-01 14:53:01', 0, 'laoshi', 1, 0, 240);
INSERT INTO `ticket_ticketuser` VALUES (1711, '', '2021-08-01 14:53:02', '2021-08-01 14:53:02', 0, '3333', 1, 0, 240);
INSERT INTO `ticket_ticketuser` VALUES (1712, '', '2021-08-01 14:53:02', '2021-08-01 14:53:02', 0, 'dsfsffsdf', 1, 0, 240);
INSERT INTO `ticket_ticketuser` VALUES (1713, '', '2021-08-01 14:53:02', '2021-08-01 14:53:02', 0, 'fewf', 1, 0, 240);
INSERT INTO `ticket_ticketuser` VALUES (1714, '', '2021-08-01 14:53:02', '2021-08-01 14:53:02', 0, 'fdsfds', 1, 0, 240);
INSERT INTO `ticket_ticketuser` VALUES (1715, '', '2021-08-01 14:53:02', '2021-08-01 14:53:02', 0, 'aaaa', 1, 0, 240);
INSERT INTO `ticket_ticketuser` VALUES (1716, '', '2021-08-01 14:53:02', '2021-08-01 14:53:02', 0, 'test', 1, 0, 240);
INSERT INTO `ticket_ticketuser` VALUES (1717, '', '2021-08-01 14:53:02', '2021-08-01 14:53:02', 0, 'laoshia', 1, 0, 240);
INSERT INTO `ticket_ticketuser` VALUES (1718, '', '2021-08-01 14:53:02', '2021-08-01 14:53:02', 0, 'test1111', 1, 0, 240);
INSERT INTO `ticket_ticketuser` VALUES (1719, '', '2021-08-01 14:53:02', '2021-08-01 14:53:02', 0, 'test2', 1, 0, 240);
INSERT INTO `ticket_ticketuser` VALUES (1720, '', '2021-08-01 14:53:02', '2021-08-01 14:53:02', 0, '23424', 1, 0, 240);
INSERT INTO `ticket_ticketuser` VALUES (1721, '', '2021-08-01 14:53:02', '2021-08-01 14:53:02', 0, 'admin', 1, 0, 240);
INSERT INTO `ticket_ticketuser` VALUES (1722, '', '2021-08-01 14:54:16', '2021-08-01 14:54:15', 0, 'laoshi', 1, 0, 241);
INSERT INTO `ticket_ticketuser` VALUES (1723, '', '2021-08-01 14:54:16', '2021-08-01 14:54:16', 0, '3333', 1, 0, 241);
INSERT INTO `ticket_ticketuser` VALUES (1724, '', '2021-08-01 14:54:16', '2021-08-01 14:54:16', 0, 'dsfsffsdf', 1, 0, 241);
INSERT INTO `ticket_ticketuser` VALUES (1725, '', '2021-08-01 14:54:16', '2021-08-01 14:54:16', 0, 'fewf', 1, 0, 241);
INSERT INTO `ticket_ticketuser` VALUES (1726, '', '2021-08-01 14:54:16', '2021-08-01 14:54:16', 0, 'fdsfds', 1, 0, 241);
INSERT INTO `ticket_ticketuser` VALUES (1727, '', '2021-08-01 14:54:16', '2021-08-01 14:54:16', 0, 'aaaa', 1, 0, 241);
INSERT INTO `ticket_ticketuser` VALUES (1728, '', '2021-08-01 14:54:16', '2021-08-01 14:54:16', 0, 'test', 1, 0, 241);
INSERT INTO `ticket_ticketuser` VALUES (1729, '', '2021-08-01 14:54:16', '2021-08-01 14:54:16', 0, 'laoshia', 1, 0, 241);
INSERT INTO `ticket_ticketuser` VALUES (1730, '', '2021-08-01 14:54:16', '2021-08-01 14:54:16', 0, 'test1111', 1, 0, 241);
INSERT INTO `ticket_ticketuser` VALUES (1731, '', '2021-08-01 14:54:16', '2021-08-01 14:54:16', 0, 'test2', 1, 0, 241);
INSERT INTO `ticket_ticketuser` VALUES (1732, '', '2021-08-01 14:54:16', '2021-08-01 14:54:16', 0, '23424', 1, 0, 241);
INSERT INTO `ticket_ticketuser` VALUES (1733, '', '2021-08-01 14:54:16', '2021-08-01 14:54:16', 0, 'admin', 1, 0, 241);
INSERT INTO `ticket_ticketuser` VALUES (1734, '', '2021-08-01 14:55:00', '2021-08-01 14:55:00', 0, 'laoshi', 1, 0, 242);
INSERT INTO `ticket_ticketuser` VALUES (1735, '', '2021-08-01 14:55:00', '2021-08-01 14:55:00', 0, '3333', 1, 0, 242);
INSERT INTO `ticket_ticketuser` VALUES (1736, '', '2021-08-01 14:55:00', '2021-08-01 14:55:00', 0, 'dsfsffsdf', 1, 0, 242);
INSERT INTO `ticket_ticketuser` VALUES (1737, '', '2021-08-01 14:55:00', '2021-08-01 14:55:00', 0, 'fewf', 1, 0, 242);
INSERT INTO `ticket_ticketuser` VALUES (1738, '', '2021-08-01 14:55:00', '2021-08-01 14:55:00', 0, 'fdsfds', 1, 0, 242);
INSERT INTO `ticket_ticketuser` VALUES (1739, '', '2021-08-01 14:55:00', '2021-08-01 14:55:00', 0, 'aaaa', 1, 0, 242);
INSERT INTO `ticket_ticketuser` VALUES (1740, '', '2021-08-01 14:55:00', '2021-08-01 14:55:00', 0, 'test', 1, 0, 242);
INSERT INTO `ticket_ticketuser` VALUES (1741, '', '2021-08-01 14:55:00', '2021-08-01 14:55:00', 0, 'laoshia', 1, 0, 242);
INSERT INTO `ticket_ticketuser` VALUES (1742, '', '2021-08-01 14:55:00', '2021-08-01 14:55:00', 0, 'test1111', 1, 0, 242);
INSERT INTO `ticket_ticketuser` VALUES (1743, '', '2021-08-01 14:55:00', '2021-08-01 14:55:00', 0, 'test2', 1, 0, 242);
INSERT INTO `ticket_ticketuser` VALUES (1744, '', '2021-08-01 14:55:00', '2021-08-01 14:55:00', 0, '23424', 1, 0, 242);
INSERT INTO `ticket_ticketuser` VALUES (1745, '', '2021-08-01 14:55:00', '2021-08-01 14:55:00', 0, 'admin', 1, 0, 242);
INSERT INTO `ticket_ticketuser` VALUES (1746, '', '2021-08-01 15:02:29', '2021-08-01 15:03:25', 0, 'laoshi', 1, 1, 243);
INSERT INTO `ticket_ticketuser` VALUES (1747, '', '2021-08-01 15:02:29', '2021-08-01 15:03:25', 0, '3333', 0, 0, 243);
INSERT INTO `ticket_ticketuser` VALUES (1748, '', '2021-08-01 15:02:29', '2021-08-01 15:03:25', 0, 'dsfsffsdf', 0, 0, 243);
INSERT INTO `ticket_ticketuser` VALUES (1749, '', '2021-08-01 15:02:29', '2021-08-01 15:03:25', 0, 'fewf', 0, 0, 243);
INSERT INTO `ticket_ticketuser` VALUES (1750, '', '2021-08-01 15:02:29', '2021-08-01 15:03:25', 0, 'fdsfds', 0, 0, 243);
INSERT INTO `ticket_ticketuser` VALUES (1751, '', '2021-08-01 15:02:29', '2021-08-01 15:03:25', 0, 'aaaa', 0, 0, 243);
INSERT INTO `ticket_ticketuser` VALUES (1752, '', '2021-08-01 15:02:29', '2021-08-01 15:03:25', 0, 'test', 0, 0, 243);
INSERT INTO `ticket_ticketuser` VALUES (1753, '', '2021-08-01 15:02:29', '2021-08-01 15:03:25', 0, 'laoshia', 0, 0, 243);
INSERT INTO `ticket_ticketuser` VALUES (1754, '', '2021-08-01 15:02:29', '2021-08-01 15:03:25', 0, 'test1111', 0, 0, 243);
INSERT INTO `ticket_ticketuser` VALUES (1755, '', '2021-08-01 15:02:29', '2021-08-01 15:03:25', 0, 'test2', 0, 0, 243);
INSERT INTO `ticket_ticketuser` VALUES (1756, '', '2021-08-01 15:02:29', '2021-08-01 15:03:25', 0, '23424', 0, 0, 243);
INSERT INTO `ticket_ticketuser` VALUES (1757, '', '2021-08-01 15:02:29', '2021-08-01 15:03:25', 0, 'admin', 0, 0, 243);
INSERT INTO `ticket_ticketuser` VALUES (1758, '', '2021-08-01 15:08:57', '2021-08-01 15:08:56', 0, 'test', 1, 0, 244);
INSERT INTO `ticket_ticketuser` VALUES (1759, '', '2021-08-01 15:08:57', '2021-08-01 15:08:57', 0, '3333', 1, 0, 244);
INSERT INTO `ticket_ticketuser` VALUES (1760, '', '2021-08-01 15:08:57', '2021-08-01 15:08:57', 0, 'dsfsffsdf', 1, 0, 244);
INSERT INTO `ticket_ticketuser` VALUES (1761, '', '2021-08-01 15:08:57', '2021-08-01 15:08:57', 0, 'fewf', 1, 0, 244);
INSERT INTO `ticket_ticketuser` VALUES (1762, '', '2021-08-01 15:08:57', '2021-08-01 15:08:57', 0, 'fdsfds', 1, 0, 244);
INSERT INTO `ticket_ticketuser` VALUES (1763, '', '2021-08-01 15:08:57', '2021-08-01 15:08:57', 0, 'aaaa', 1, 0, 244);
INSERT INTO `ticket_ticketuser` VALUES (1764, '', '2021-08-01 15:08:57', '2021-08-01 15:08:57', 0, 'laoshi', 1, 0, 244);
INSERT INTO `ticket_ticketuser` VALUES (1765, '', '2021-08-01 15:08:57', '2021-08-01 15:08:57', 0, 'laoshia', 1, 0, 244);
INSERT INTO `ticket_ticketuser` VALUES (1766, '', '2021-08-01 15:08:57', '2021-08-01 15:08:57', 0, 'test1111', 1, 0, 244);
INSERT INTO `ticket_ticketuser` VALUES (1767, '', '2021-08-01 15:08:57', '2021-08-01 15:08:57', 0, 'test2', 1, 0, 244);
INSERT INTO `ticket_ticketuser` VALUES (1768, '', '2021-08-01 15:08:57', '2021-08-01 15:08:57', 0, '23424', 1, 0, 244);
INSERT INTO `ticket_ticketuser` VALUES (1769, '', '2021-08-01 15:08:57', '2021-08-01 15:08:57', 0, 'admin', 1, 0, 244);
INSERT INTO `ticket_ticketuser` VALUES (1770, '', '2021-08-01 15:09:22', '2021-08-01 15:09:22', 0, 'test', 1, 0, 245);
INSERT INTO `ticket_ticketuser` VALUES (1771, '', '2021-08-01 15:09:22', '2021-08-01 15:09:22', 0, '3333', 1, 0, 245);
INSERT INTO `ticket_ticketuser` VALUES (1772, '', '2021-08-01 15:09:22', '2021-08-01 15:09:22', 0, 'dsfsffsdf', 1, 0, 245);
INSERT INTO `ticket_ticketuser` VALUES (1773, '', '2021-08-01 15:09:22', '2021-08-01 15:09:22', 0, 'fewf', 1, 0, 245);
INSERT INTO `ticket_ticketuser` VALUES (1774, '', '2021-08-01 15:09:22', '2021-08-01 15:09:22', 0, 'fdsfds', 1, 0, 245);
INSERT INTO `ticket_ticketuser` VALUES (1775, '', '2021-08-01 15:09:22', '2021-08-01 15:09:22', 0, 'aaaa', 1, 0, 245);
INSERT INTO `ticket_ticketuser` VALUES (1776, '', '2021-08-01 15:09:22', '2021-08-01 15:09:22', 0, 'laoshi', 1, 0, 245);
INSERT INTO `ticket_ticketuser` VALUES (1777, '', '2021-08-01 15:09:22', '2021-08-01 15:09:22', 0, 'laoshia', 1, 0, 245);
INSERT INTO `ticket_ticketuser` VALUES (1778, '', '2021-08-01 15:09:22', '2021-08-01 15:09:22', 0, 'test1111', 1, 0, 245);
INSERT INTO `ticket_ticketuser` VALUES (1779, '', '2021-08-01 15:09:22', '2021-08-01 15:09:22', 0, 'test2', 1, 0, 245);
INSERT INTO `ticket_ticketuser` VALUES (1780, '', '2021-08-01 15:09:22', '2021-08-01 15:09:22', 0, '23424', 1, 0, 245);
INSERT INTO `ticket_ticketuser` VALUES (1781, '', '2021-08-01 15:09:22', '2021-08-01 15:09:22', 0, 'admin', 1, 0, 245);
INSERT INTO `ticket_ticketuser` VALUES (1782, '', '2021-08-01 21:38:55', '2021-08-01 21:38:55', 0, 'laoshi', 1, 0, 246);
INSERT INTO `ticket_ticketuser` VALUES (1783, '', '2021-08-01 21:38:55', '2021-08-01 21:38:55', 0, 'dsfsffsdf', 1, 0, 246);
INSERT INTO `ticket_ticketuser` VALUES (1784, '', '2021-08-01 21:38:55', '2021-08-01 21:38:55', 0, 'fdsfds', 1, 0, 246);
INSERT INTO `ticket_ticketuser` VALUES (1785, '', '2021-08-01 21:38:55', '2021-08-01 21:38:55', 0, 'test2', 1, 0, 246);
INSERT INTO `ticket_ticketuser` VALUES (1786, '', '2021-08-01 21:38:55', '2021-08-01 21:38:55', 0, 'test1111', 1, 0, 246);
INSERT INTO `ticket_ticketuser` VALUES (1787, '', '2021-08-01 21:38:55', '2021-08-01 21:38:55', 0, '23424', 1, 0, 246);
INSERT INTO `ticket_ticketuser` VALUES (1788, '', '2021-08-01 21:38:55', '2021-08-01 21:38:55', 0, 'aaaa', 1, 0, 246);
INSERT INTO `ticket_ticketuser` VALUES (1789, '', '2021-08-01 21:38:55', '2021-08-01 21:38:55', 0, 'fewf', 1, 0, 246);
INSERT INTO `ticket_ticketuser` VALUES (1790, '', '2021-08-01 21:38:55', '2021-08-01 21:38:55', 0, 'admin', 1, 0, 246);
INSERT INTO `ticket_ticketuser` VALUES (1791, '', '2021-08-01 21:38:55', '2021-08-01 21:38:55', 0, 'test', 1, 0, 246);
INSERT INTO `ticket_ticketuser` VALUES (1792, '', '2021-08-01 21:38:55', '2021-08-01 21:38:55', 0, 'laoshia', 1, 0, 246);
INSERT INTO `ticket_ticketuser` VALUES (1793, '', '2021-08-01 21:38:55', '2021-08-01 21:38:55', 0, '3333', 1, 0, 246);
INSERT INTO `ticket_ticketuser` VALUES (1794, '', '2021-08-01 21:39:28', '2021-08-01 21:39:28', 0, 'laoshi', 1, 0, 247);
INSERT INTO `ticket_ticketuser` VALUES (1795, '', '2021-08-01 21:39:28', '2021-08-01 21:39:28', 0, 'dsfsffsdf', 1, 0, 247);
INSERT INTO `ticket_ticketuser` VALUES (1796, '', '2021-08-01 21:39:28', '2021-08-01 21:39:28', 0, 'fdsfds', 1, 0, 247);
INSERT INTO `ticket_ticketuser` VALUES (1797, '', '2021-08-01 21:39:28', '2021-08-01 21:39:28', 0, 'test2', 1, 0, 247);
INSERT INTO `ticket_ticketuser` VALUES (1798, '', '2021-08-01 21:39:28', '2021-08-01 21:39:28', 0, 'test1111', 1, 0, 247);
INSERT INTO `ticket_ticketuser` VALUES (1799, '', '2021-08-01 21:39:28', '2021-08-01 21:39:28', 0, '23424', 1, 0, 247);
INSERT INTO `ticket_ticketuser` VALUES (1800, '', '2021-08-01 21:39:28', '2021-08-01 21:39:28', 0, 'aaaa', 1, 0, 247);
INSERT INTO `ticket_ticketuser` VALUES (1801, '', '2021-08-01 21:39:28', '2021-08-01 21:39:28', 0, 'fewf', 1, 0, 247);
INSERT INTO `ticket_ticketuser` VALUES (1802, '', '2021-08-01 21:39:28', '2021-08-01 21:39:28', 0, 'admin', 1, 0, 247);
INSERT INTO `ticket_ticketuser` VALUES (1803, '', '2021-08-01 21:39:28', '2021-08-01 21:39:28', 0, 'test', 1, 0, 247);
INSERT INTO `ticket_ticketuser` VALUES (1804, '', '2021-08-01 21:39:28', '2021-08-01 21:39:28', 0, 'laoshia', 1, 0, 247);
INSERT INTO `ticket_ticketuser` VALUES (1805, '', '2021-08-01 21:39:28', '2021-08-01 21:39:28', 0, '3333', 1, 0, 247);
INSERT INTO `ticket_ticketuser` VALUES (1806, '', '2021-08-01 21:40:14', '2021-08-01 21:40:13', 0, 'laoshi', 1, 0, 248);
INSERT INTO `ticket_ticketuser` VALUES (1807, '', '2021-08-01 21:40:14', '2021-08-01 21:40:14', 0, 'dsfsffsdf', 1, 0, 248);
INSERT INTO `ticket_ticketuser` VALUES (1808, '', '2021-08-01 21:40:14', '2021-08-01 21:40:14', 0, 'fdsfds', 1, 0, 248);
INSERT INTO `ticket_ticketuser` VALUES (1809, '', '2021-08-01 21:40:14', '2021-08-01 21:40:14', 0, 'test2', 1, 0, 248);
INSERT INTO `ticket_ticketuser` VALUES (1810, '', '2021-08-01 21:40:14', '2021-08-01 21:40:14', 0, 'test1111', 1, 0, 248);
INSERT INTO `ticket_ticketuser` VALUES (1811, '', '2021-08-01 21:40:14', '2021-08-01 21:40:14', 0, '23424', 1, 0, 248);
INSERT INTO `ticket_ticketuser` VALUES (1812, '', '2021-08-01 21:40:14', '2021-08-01 21:40:14', 0, 'aaaa', 1, 0, 248);
INSERT INTO `ticket_ticketuser` VALUES (1813, '', '2021-08-01 21:40:14', '2021-08-01 21:40:14', 0, 'fewf', 1, 0, 248);
INSERT INTO `ticket_ticketuser` VALUES (1814, '', '2021-08-01 21:40:14', '2021-08-01 21:40:14', 0, 'admin', 1, 0, 248);
INSERT INTO `ticket_ticketuser` VALUES (1815, '', '2021-08-01 21:40:14', '2021-08-01 21:40:14', 0, 'test', 1, 0, 248);
INSERT INTO `ticket_ticketuser` VALUES (1816, '', '2021-08-01 21:40:14', '2021-08-01 21:40:14', 0, 'laoshia', 1, 0, 248);
INSERT INTO `ticket_ticketuser` VALUES (1817, '', '2021-08-01 21:40:14', '2021-08-01 21:40:14', 0, '3333', 1, 0, 248);
INSERT INTO `ticket_ticketuser` VALUES (1818, '', '2021-08-01 21:40:35', '2021-08-01 21:40:34', 0, 'laoshi', 1, 0, 249);
INSERT INTO `ticket_ticketuser` VALUES (1819, '', '2021-08-01 21:40:35', '2021-08-01 21:40:35', 0, 'dsfsffsdf', 1, 0, 249);
INSERT INTO `ticket_ticketuser` VALUES (1820, '', '2021-08-01 21:40:35', '2021-08-01 21:40:35', 0, 'fdsfds', 1, 0, 249);
INSERT INTO `ticket_ticketuser` VALUES (1821, '', '2021-08-01 21:40:35', '2021-08-01 21:40:35', 0, 'test2', 1, 0, 249);
INSERT INTO `ticket_ticketuser` VALUES (1822, '', '2021-08-01 21:40:35', '2021-08-01 21:40:35', 0, 'test1111', 1, 0, 249);
INSERT INTO `ticket_ticketuser` VALUES (1823, '', '2021-08-01 21:40:35', '2021-08-01 21:40:35', 0, '23424', 1, 0, 249);
INSERT INTO `ticket_ticketuser` VALUES (1824, '', '2021-08-01 21:40:35', '2021-08-01 21:40:35', 0, 'aaaa', 1, 0, 249);
INSERT INTO `ticket_ticketuser` VALUES (1825, '', '2021-08-01 21:40:35', '2021-08-01 21:40:35', 0, 'fewf', 1, 0, 249);
INSERT INTO `ticket_ticketuser` VALUES (1826, '', '2021-08-01 21:40:35', '2021-08-01 21:40:35', 0, 'admin', 1, 0, 249);
INSERT INTO `ticket_ticketuser` VALUES (1827, '', '2021-08-01 21:40:35', '2021-08-01 21:40:35', 0, 'test', 1, 0, 249);
INSERT INTO `ticket_ticketuser` VALUES (1828, '', '2021-08-01 21:40:35', '2021-08-01 21:40:35', 0, 'laoshia', 1, 0, 249);
INSERT INTO `ticket_ticketuser` VALUES (1829, '', '2021-08-01 21:40:35', '2021-08-01 21:40:35', 0, '3333', 1, 0, 249);
INSERT INTO `ticket_ticketuser` VALUES (1830, '', '2021-08-01 21:43:22', '2021-08-01 21:43:22', 0, 'laoshi', 1, 0, 250);
INSERT INTO `ticket_ticketuser` VALUES (1831, '', '2021-08-01 21:43:22', '2021-08-01 21:43:22', 0, 'dsfsffsdf', 1, 0, 250);
INSERT INTO `ticket_ticketuser` VALUES (1832, '', '2021-08-01 21:43:22', '2021-08-01 21:43:22', 0, 'fdsfds', 1, 0, 250);
INSERT INTO `ticket_ticketuser` VALUES (1833, '', '2021-08-01 21:43:22', '2021-08-01 21:43:22', 0, 'test2', 1, 0, 250);
INSERT INTO `ticket_ticketuser` VALUES (1834, '', '2021-08-01 21:43:22', '2021-08-01 21:43:22', 0, 'test1111', 1, 0, 250);
INSERT INTO `ticket_ticketuser` VALUES (1835, '', '2021-08-01 21:43:22', '2021-08-01 21:43:22', 0, '23424', 1, 0, 250);
INSERT INTO `ticket_ticketuser` VALUES (1836, '', '2021-08-01 21:43:22', '2021-08-01 21:43:22', 0, 'aaaa', 1, 0, 250);
INSERT INTO `ticket_ticketuser` VALUES (1837, '', '2021-08-01 21:43:22', '2021-08-01 21:43:22', 0, 'fewf', 1, 0, 250);
INSERT INTO `ticket_ticketuser` VALUES (1838, '', '2021-08-01 21:43:22', '2021-08-01 21:43:22', 0, 'admin', 1, 0, 250);
INSERT INTO `ticket_ticketuser` VALUES (1839, '', '2021-08-01 21:43:22', '2021-08-01 21:43:22', 0, 'test', 1, 0, 250);
INSERT INTO `ticket_ticketuser` VALUES (1840, '', '2021-08-01 21:43:22', '2021-08-01 21:43:22', 0, 'laoshia', 1, 0, 250);
INSERT INTO `ticket_ticketuser` VALUES (1841, '', '2021-08-01 21:43:22', '2021-08-01 21:43:22', 0, '3333', 1, 0, 250);
INSERT INTO `ticket_ticketuser` VALUES (1842, '', '2021-08-01 21:53:59', '2021-08-01 21:56:10', 0, 'test', 0, 0, 251);
INSERT INTO `ticket_ticketuser` VALUES (1843, '', '2021-08-01 21:53:59', '2021-08-01 21:56:10', 0, 'dsfsffsdf', 0, 0, 251);
INSERT INTO `ticket_ticketuser` VALUES (1844, '', '2021-08-01 21:53:59', '2021-08-01 21:56:10', 0, 'fdsfds', 0, 0, 251);
INSERT INTO `ticket_ticketuser` VALUES (1845, '', '2021-08-01 21:53:59', '2021-08-01 21:56:10', 0, 'test2', 0, 0, 251);
INSERT INTO `ticket_ticketuser` VALUES (1846, '', '2021-08-01 21:53:59', '2021-08-01 21:56:10', 0, 'test1111', 0, 0, 251);
INSERT INTO `ticket_ticketuser` VALUES (1847, '', '2021-08-01 21:53:59', '2021-08-01 21:56:10', 0, '23424', 0, 0, 251);
INSERT INTO `ticket_ticketuser` VALUES (1848, '', '2021-08-01 21:53:59', '2021-08-01 21:56:10', 0, 'aaaa', 0, 0, 251);
INSERT INTO `ticket_ticketuser` VALUES (1849, '', '2021-08-01 21:53:59', '2021-08-01 21:56:10', 0, 'fewf', 0, 0, 251);
INSERT INTO `ticket_ticketuser` VALUES (1850, '', '2021-08-01 21:53:59', '2021-08-01 21:56:10', 0, 'admin', 0, 0, 251);
INSERT INTO `ticket_ticketuser` VALUES (1851, '', '2021-08-01 21:53:59', '2021-08-01 21:56:10', 0, 'laoshi', 1, 1, 251);
INSERT INTO `ticket_ticketuser` VALUES (1852, '', '2021-08-01 21:53:59', '2021-08-01 21:56:10', 0, 'laoshia', 0, 0, 251);
INSERT INTO `ticket_ticketuser` VALUES (1853, '', '2021-08-01 21:53:59', '2021-08-01 21:56:10', 0, '3333', 0, 0, 251);

-- ----------------------------
-- Table structure for workflow_customfield
-- ----------------------------
DROP TABLE IF EXISTS `workflow_customfield`;
CREATE TABLE `workflow_customfield`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `workflow_id` int(11) NOT NULL,
  `field_type_id` int(11) NOT NULL,
  `field_key` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `field_name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `order_id` int(11) NOT NULL,
  `default_value` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `description` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `field_template` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `boolean_field_display` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `creator` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `field_choice` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `label` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `placeholder` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 26 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of workflow_customfield
-- ----------------------------
INSERT INTO `workflow_customfield` VALUES (1, 1, 30, 'leave_start', '开始时间', 20, '', '', '', '{}', 'admin', '2018-04-23 20:56:25.940486', '2018-05-11 07:31:11.133782', 0, '{}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (2, 1, 30, 'leave_end', '结束时间', 25, NULL, '', '', '{}', 'admin', '2018-05-10 07:41:03.717540', '2018-05-11 07:31:19.923554', 0, '{}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (4, 1, 60, 'leave_proxy', '代理人', 35, NULL, '请假期间的代理人', '', '{}', 'admin', '2018-05-11 07:31:01.068850', '2018-05-11 07:31:35.323117', 1, '{}', '', '');
INSERT INTO `workflow_customfield` VALUES (5, 1, 35, 'leave_type', '请假类型', 40, '', '', '', '{}', 'admin', '2018-05-11 07:34:29.608579', '2018-05-23 22:38:57.324916', 0, '{\"1\":\"事假\",\"2\":\"病假\"}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (6, 1, 10, 'leave_reason', '请假原因及相关附件', 45, '', '', '病假请提供证明拍照附件， 婚假请提供结婚证拍照附件', '{}', 'admin', '2018-05-11 07:36:41.882377', '2018-05-11 07:36:41.882413', 1, '{}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (7, 2, 55, 'vpn_reason', '申请原因', 110, '请填写申请vpn的理由', '', '', '{}', 'admin', '2018-05-12 10:02:31.501142', '2018-05-12 10:02:31.501189', 0, '{}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (8, 1, 20, 'bool_field', '布尔字段', 0, '', '', '', '{\"1\":\"正确\", \"2\":\"错误\"}', 'admin', '2020-08-15 15:50:14.707215', '2020-08-15 15:50:14.707247', 1, '{}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (9, 1, 25, 'date_filed', '日期字段', 0, '', '', '', '{}', 'admin', '2020-08-15 15:54:19.619379', '2020-08-15 15:54:19.619409', 1, '{}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (10, 1, 30, 'datetime_field', '日期时间字段', 0, '', '', '', '{}', 'admin', '2020-08-15 15:54:33.396096', '2020-08-15 15:54:33.396127', 0, '{}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (11, 1, 35, 'checkbox_field', '单选字段', 0, '', '', '', '{}', 'admin', '2020-08-15 15:55:43.617371', '2020-08-15 15:55:43.617394', 1, '{\"1\":\"中国\",\"2\":\"美国\",\"3\":\"英国\"}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (12, 1, 40, 'multi_checkbox_field', '多选字段', 0, '', '', '', '{}', 'admin', '2020-08-15 15:56:33.283712', '2020-08-15 15:56:33.283801', 1, '{\"1\":\"中国\", \"2\":\"美国\", \"3\":\"英国\"}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (13, 1, 45, 'select_field', '下拉选择字段', 0, '', '', '', '{}', 'admin', '2020-08-15 15:57:04.427730', '2020-08-15 15:57:04.427762', 1, '{\"1\":\"中国\", \"2\":\"美国\", \"3\":\"英国\"}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (14, 1, 50, 'multi_select_field', '多选下拉列表', 0, '', '', '', '{}', 'admin', '2020-08-15 15:57:25.586297', '2020-08-15 15:57:25.586346', 1, '{\"1\":\"中国\",\"2\":\"美国\",\"3\":\"英国\"}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (15, 1, 55, 'text_field', '标题', 0, '', '', '', '{}', 'admin', '2020-08-15 15:57:56.756983', '2020-08-15 15:57:56.757009', 1, '{}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (16, 1, 60, 'user_fleld', '用户选择字段', 0, '', '', '', '{}', 'admin', '2020-08-15 15:58:30.818408', '2020-08-15 15:58:30.818457', 1, '{}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (17, 1, 70, 'multi_user_field', '多选用户字段', 0, '', '', '', '{}', 'admin', '2020-08-15 15:58:52.338369', '2020-08-15 15:58:52.338431', 1, '{}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (18, 1, 80, 'attachment_field', '附件字段', 0, '', '', '', '{}', 'admin', '2020-08-15 15:59:31.269502', '2020-08-15 15:59:31.269533', 0, '{}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (19, 1, 35, 'fw', 'fds', 23, 'sd', 'dsfs', 'fee', '{}', 'admin', '2020-10-27 06:59:50.901725', '2020-10-27 06:59:50.901821', 1, '{}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (20, 1, 35, '2r', 'dfsf', 2, '', '', '', '{}', 'admin', '2020-10-28 07:39:50.412037', '2020-10-28 07:39:50.412132', 1, '{}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (21, 1, 5, 'title', '标题', 0, '', '', '', '{}', 'admin', '2021-07-30 19:22:01.753452', '2021-07-30 19:22:01.753475', 1, '{}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (22, 1, 5, 'title', '标题', 20, '', '', '', '{}', 'admin', '2021-07-30 19:30:04.896043', '2021-07-30 19:30:04.896066', 1, '{}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (23, 1, 10, 'days', '请假天数', 0, '', '', '', '{}', 'admin', '2021-07-30 19:44:05.093076', '2021-07-30 19:44:05.093118', 0, '{}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (24, 1, 55, 'text_desp', '请假理由', 0, '', '', '', '{}', 'admin', '2021-07-30 19:57:18.122623', '2021-07-30 19:57:18.122665', 0, '{}', '{}', '');
INSERT INTO `workflow_customfield` VALUES (25, 1, 80, 'filename', '附件', 0, '', '', '', '{}', 'admin', '2021-08-01 12:22:26.169140', '2021-08-01 12:22:26.169163', 0, '{}', '{}', '');

-- ----------------------------
-- Table structure for workflow_customnotice
-- ----------------------------
DROP TABLE IF EXISTS `workflow_customnotice`;
CREATE TABLE `workflow_customnotice`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `description` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `creator` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `hook_url` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT 'hook_url',
  `hook_token` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT 'hook_token',
  `appkey` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `appsecret` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `corpid` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `corpsecret` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `type_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of workflow_customnotice
-- ----------------------------
INSERT INTO `workflow_customnotice` VALUES (1, '通知1', 'fdsf', 'admin', '2019-02-12 22:45:20.765495', '2019-02-12 22:45:20.765587', 0, '222', '222', '', '', '', '', 1);
INSERT INTO `workflow_customnotice` VALUES (2, 'fdsfs', 'fsdfsd', 'admin', '2020-09-05 22:16:43.661081', '2020-09-05 22:16:43.661305', 1, 'dsfsdf', 'sdfdsfs', '', '', '', '', 1);
INSERT INTO `workflow_customnotice` VALUES (3, '23', '333', 'admin', '2020-09-07 23:41:33.792284', '2020-09-07 23:41:33.792526', 1, '', '', '', '', 'fds', '332323', 2);
INSERT INTO `workflow_customnotice` VALUES (4, 'test', '222', 'admin', '2020-09-08 06:35:20.027469', '2020-09-08 06:35:20.027744', 1, '', '', 'fdsf', 'fdsfs', '', '', 3);
INSERT INTO `workflow_customnotice` VALUES (5, '2323', 'dfsf', 'admin', '2020-09-08 06:38:05.143667', '2020-09-08 06:38:05.143866', 1, '', '', 'fdsfs', 'dfsf', '', '', 3);
INSERT INTO `workflow_customnotice` VALUES (6, '2233342', '', 'admin', '2020-09-08 06:38:33.228658', '2020-09-08 06:38:33.228952', 1, '', '', '', '', 'dfs', 'fdsf', 2);

-- ----------------------------
-- Table structure for workflow_state
-- ----------------------------
DROP TABLE IF EXISTS `workflow_state`;
CREATE TABLE `workflow_state`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `workflow_id` int(11) NOT NULL,
  `is_hidden` tinyint(1) NOT NULL,
  `order_id` int(11) NOT NULL,
  `type_id` int(11) NOT NULL,
  `participant_type_id` int(11) NOT NULL,
  `participant` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `distribute_type_id` int(11) NOT NULL,
  `state_field_str` longtext CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `label` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `creator` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `remember_last_man_enable` tinyint(1) NOT NULL,
  `enable_retreat` tinyint(1) UNSIGNED NOT NULL DEFAULT 0 COMMENT '允许撤回',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 30 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of workflow_state
-- ----------------------------
INSERT INTO `workflow_state` VALUES (1, '发起人-新建中', 1, 0, 1, 1, 0, '', 1, '{\"leave_type\":3,\"days\":3,\"leave_start\":3,\"leave_end\":3,\"text_desp\":3,\"title\":3,\"filename\":3}', '{}', 'admin', '2018-04-23 20:53:33.052134', '2018-05-13 11:42:11.273695', 0, 0, 0);
INSERT INTO `workflow_state` VALUES (2, '发起人-编辑中', 1, 1, 2, 0, 5, 'creator', 1, '{\"leave_end\":2,\"leave_days\":2,\"sn\":1,\"state.state_name\":1,\"leave_proxy\":2,\"title\":2,\"gmt_created\":1,\"creator\":1,\"leave_start\":2,\"leave_reason\":2,\"leave_type\":2}', '{}', 'admin', '2018-04-30 15:45:48.976712', '2018-05-14 06:44:10.661777', 1, 0, 0);
INSERT INTO `workflow_state` VALUES (3, '教师审批', 1, 0, 2, 0, 3, '2', 1, '{\"leave_type\":3,\"days\":3,\"leave_start\":3,\"leave_end\":3,\"text_desp\":3,\"title\":3,\"filename\":3}', '{}', 'admin', '2018-04-30 15:46:42.184252', '2018-11-27 07:20:33.209705', 0, 1, 0);
INSERT INTO `workflow_state` VALUES (4, '人事部门-处理中', 1, 0, 4, 0, 1, 'jack', 1, '{\"sn\":1,  \"title\":1, \"leave_start\": 1,  \"leave_end\":1,  \"leave_days\":1,  \"leave_proxy\":1,  \"leave_type\":1, \"creator\":1, \"gmt_created\":1,  \"leave_reason\":1}', '{}', 'admin', '2018-04-30 15:47:58.790510', '2018-05-13 11:42:59.834440', 1, 0, 0);
INSERT INTO `workflow_state` VALUES (5, '结束', 1, 0, 3, 2, 0, '', 1, '{\"leave_type\":3,\"days\":3,\"leave_start\":3,\"leave_end\":3,\"text_desp\":3,\"title\":3,\"filename\":3}', '{}', 'admin', '2018-04-30 15:51:41.260309', '2018-05-11 06:52:39.799922', 0, 0, 0);
INSERT INTO `workflow_state` VALUES (6, '发起人-新建中', 2, 0, 1, 1, 5, 'creator', 1, '{\"vpn_reason\":2, \"title\":2}', '{}', 'admin', '2018-05-10 07:34:45.302697', '2018-05-15 07:13:06.599270', 0, 0, 0);
INSERT INTO `workflow_state` VALUES (7, '发起人tl-审批中', 2, 0, 2, 0, 2, 'zhangsan,admin', 4, '{\"sn\":1,\"title\":1,\"creator\":1,\"gmt_created\":1,\"vpn_reason\":1}', '{}', 'admin', '2018-05-11 06:47:36.381658', '2018-05-15 07:19:16.038155', 0, 0, 0);
INSERT INTO `workflow_state` VALUES (8, '运维人员-审批中', 2, 0, 3, 0, 3, '3', 1, '{\"sn\":1,  \"title\":1, \"creator\":1, \"gmt_created\":1,\"vpn_reason\":1,\"participant_info.participant_alias\":1,\"participant_info.participant_name\":1}', '{}', 'admin', '2018-05-11 06:48:26.945117', '2018-11-05 23:37:58.618022', 0, 0, 0);
INSERT INTO `workflow_state` VALUES (9, '授权脚本-自动执行中', 2, 0, 4, 0, 10, '{}', 1, '{}', '{}', 'admin', '2018-05-11 06:50:09.416344', '2018-05-11 07:10:25.197748', 0, 0, 0);
INSERT INTO `workflow_state` VALUES (10, '发起人-确认中', 2, 0, 6, 0, 5, 'creator', 1, '{\"sn\":1,\"participant_info.participant_name\":1,\"state.state_name\":1,\"workflow.workflow_name\":1}', '{}', 'admin', '2018-05-11 06:51:02.913212', '2018-05-22 22:21:51.867707', 0, 0, 0);
INSERT INTO `workflow_state` VALUES (11, '结束', 2, 0, 7, 2, 0, '', 1, '{}', '{}', 'admin', '2018-05-11 07:11:53.076731', '2018-05-11 07:11:53.076766', 0, 0, 0);
INSERT INTO `workflow_state` VALUES (19, 'test', 1, 0, 0, 0, 1, '', 2, '{\"title\":2}', '{}', 'admin', '2019-04-07 17:48:09.224566', '2019-04-07 17:48:09.224621', 1, 1, 0);
INSERT INTO `workflow_state` VALUES (20, 'testt', 1, 0, 0, 0, 1, '', 2, '{\"title\":2}', '{}', 'admin', '2019-04-07 21:24:17.078594', '2019-04-07 21:24:17.078638', 1, 0, 0);
INSERT INTO `workflow_state` VALUES (21, '11111111', 1, 0, 0, 0, 1, '', 2, '{\"title\":2}', '{}', 'admin', '2019-04-07 22:10:52.603902', '2019-04-07 22:10:52.603963', 1, 0, 0);
INSERT INTO `workflow_state` VALUES (22, 'ttttttttt', 1, 0, 0, 0, 1, '', 2, '{\"title\":2}', '{}', 'admin', '2019-06-13 23:01:34.696459', '2019-06-13 23:01:34.696492', 1, 0, 0);
INSERT INTO `workflow_state` VALUES (23, '11111', 1, 0, 0, 0, 1, '', 2, '{\"title\":2}', '{}', 'admin', '2019-06-15 21:34:19.035126', '2019-06-15 21:34:19.035160', 1, 0, 0);
INSERT INTO `workflow_state` VALUES (24, '222', 1, 0, 0, 0, 1, '', 2, '{\"title\":2}', '{}', 'admin', '2019-06-15 21:46:16.037190', '2019-06-15 21:46:16.037219', 1, 0, 0);
INSERT INTO `workflow_state` VALUES (25, 'tttt', 1, 0, 0, 0, 1, '', 2, '{\"title\":2}', '{}', 'admin', '2019-09-20 15:21:24.144219', '2019-09-20 15:21:24.144252', 1, 0, 0);
INSERT INTO `workflow_state` VALUES (26, 'tttttt', 1, 0, 0, 0, 1, '', 2, '{\"title\":2}', '{}', 'admin', '2019-09-20 15:21:31.081869', '2019-09-20 15:21:31.081910', 1, 0, 0);
INSERT INTO `workflow_state` VALUES (27, 'fsfsf', 1, 0, 0, 0, 1, '', 2, '{\"title\":2}', '{}', 'admin', '2019-09-20 15:21:37.180213', '2019-09-20 15:21:37.180244', 1, 0, 0);
INSERT INTO `workflow_state` VALUES (28, 'fdf', 1, 0, 1, 0, 1, 'fa', 1, '{\"gmt_created\":1}', '{}', 'admin', '2020-11-03 07:40:02.729021', '2020-11-03 07:40:02.729875', 1, 0, 0);
INSERT INTO `workflow_state` VALUES (29, 'test', 1, 0, 0, 0, 2, 'test', 2, '{}', '{}', 'admin', '2020-11-09 07:20:10.977897', '2020-11-09 07:20:10.978040', 1, 0, 0);

-- ----------------------------
-- Table structure for workflow_transition
-- ----------------------------
DROP TABLE IF EXISTS `workflow_transition`;
CREATE TABLE `workflow_transition`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `workflow_id` int(11) NOT NULL,
  `transition_type_id` int(11) NOT NULL,
  `source_state_id` int(11) NOT NULL,
  `destination_state_id` int(11) NOT NULL,
  `alert_enable` tinyint(1) NOT NULL,
  `alert_text` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `creator` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `field_require_check` tinyint(1) NOT NULL,
  `timer` int(11) NOT NULL,
  `attribute_type_id` int(11) NOT NULL,
  `condition_expression` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 29 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of workflow_transition
-- ----------------------------
INSERT INTO `workflow_transition` VALUES (1, '提交', 1, 1, 1, 3, 0, '', 'admin', '2018-04-24 07:09:25.922814', '2018-04-30 15:48:57.047369', 1, 1, 0, 1, '[]');
INSERT INTO `workflow_transition` VALUES (2, '保存', 1, 1, 1, 1, 0, '', 'admin', '2018-04-30 15:30:25.650813', '2018-04-30 15:48:52.372363', 1, 1, 0, 2, '[]');
INSERT INTO `workflow_transition` VALUES (3, '同意', 1, 1, 3, 4, 0, '', 'admin', '2018-04-30 15:49:23.451582', '2018-04-30 15:49:23.451627', 1, 1, 0, 1, '[]');
INSERT INTO `workflow_transition` VALUES (4, '拒绝', 1, 1, 3, 1, 0, 'fdsfdsfsf', 'admin', '2018-04-30 15:54:32.069649', '2018-05-11 07:00:24.370322', 1, 0, 0, 1, '[]');
INSERT INTO `workflow_transition` VALUES (5, '同意', 1, 1, 4, 5, 0, '', 'admin', '2018-04-30 15:55:00.072437', '2018-05-11 07:03:29.349770', 1, 1, 0, 1, '[]');
INSERT INTO `workflow_transition` VALUES (6, '退回', 1, 1, 4, 1, 0, '', 'admin', '2018-05-11 06:58:43.395655', '2018-05-11 07:04:14.896678', 1, 0, 0, 1, '[]');
INSERT INTO `workflow_transition` VALUES (7, '提交', 2, 1, 6, 7, 0, '', 'admin', '2018-05-11 07:06:22.745312', '2018-05-11 07:06:22.745342', 0, 1, 0, 1, '[]');
INSERT INTO `workflow_transition` VALUES (8, '同意', 2, 1, 7, 8, 0, '', 'admin', '2018-05-11 07:07:33.213731', '2018-05-11 07:07:33.213760', 0, 1, 0, 1, '[]');
INSERT INTO `workflow_transition` VALUES (9, '同意', 2, 1, 8, 9, 0, '', 'admin', '2018-05-11 07:12:53.036037', '2018-05-11 07:12:53.036077', 0, 1, 0, 1, '[]');
INSERT INTO `workflow_transition` VALUES (10, '脚本执行完成', 2, 1, 9, 10, 0, '', 'admin', '2018-05-11 07:13:12.070223', '2018-05-11 07:13:12.070254', 0, 1, 0, 1, '[]');
INSERT INTO `workflow_transition` VALUES (11, '确认完成', 2, 1, 10, 11, 0, '', 'admin', '2018-05-11 07:13:52.427815', '2018-05-11 07:13:52.427844', 0, 1, 0, 1, '[]');
INSERT INTO `workflow_transition` VALUES (12, '未生效', 2, 1, 10, 8, 1, '是否真的退回？  请查看vpn使用文档保证使用姿势正确，再退回', 'admin', '2018-05-11 07:16:26.826525', '2018-05-11 07:16:36.072876', 0, 0, 0, 1, '[]');
INSERT INTO `workflow_transition` VALUES (25, 'tttt', 2, 1, 28, 6, 0, '', 'admin', '2019-12-08 16:46:06.801015', '2019-12-08 16:46:06.801074', 1, 0, 0, 1, '[]');
INSERT INTO `workflow_transition` VALUES (26, 'tet', 1, 0, 1, 4, 0, '', 'admin', '2020-11-14 15:57:37.758568', '2020-11-14 15:57:37.758662', 1, 1, 0, 1, '[]');
INSERT INTO `workflow_transition` VALUES (27, '提交', 1, 1, 1, 3, 0, '', 'admin', '2021-07-30 20:43:54.869857', '2021-07-30 20:43:54.869948', 0, 0, 0, 1, '[]');
INSERT INTO `workflow_transition` VALUES (28, '结束', 1, 1, 3, 5, 0, '', 'admin', '2021-07-30 21:01:42.759809', '2021-07-30 21:01:42.759847', 0, 0, 0, 1, '[]');

-- ----------------------------
-- Table structure for workflow_workflow
-- ----------------------------
DROP TABLE IF EXISTS `workflow_workflow`;
CREATE TABLE `workflow_workflow`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `description` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `display_form_str` varchar(10000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `creator` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `view_permission_check` tinyint(1) NOT NULL,
  `limit_expression` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `notices` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `title_template` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '标题模板',
  `content_template` varchar(1000) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '内容模板',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of workflow_workflow
-- ----------------------------
INSERT INTO `workflow_workflow` VALUES (1, '请假申请', '请假申请测试', '[\"leave_type\",\"days\",\"leave_start\",\"leave_end\",\"text_desp\",\"title\", \"filename\"]', 'admin', '2018-04-23 20:49:32.229386', '2018-10-22 08:05:15.574860', 0, 0, '{}', '1', '{title}', '标题:{title}, 创建时间:{gmt_created}');
INSERT INTO `workflow_workflow` VALUES (2, 'vpn申请', 'vpn权限申请', '[\"sn\", \"title\", \"model\", \"gmt_created\",\"participant.participant_alias\",\"vpn_reason\"]', 'admin', '2018-05-06 12:32:36.690665', '2018-11-05 23:32:57.667206', 0, 1, '{}', '', '', '');

-- ----------------------------
-- Table structure for workflow_workflowadmin
-- ----------------------------
DROP TABLE IF EXISTS `workflow_workflowadmin`;
CREATE TABLE `workflow_workflowadmin`  (
  `id` int(11) NOT NULL AUTO_INCREMENT COMMENT '主键id',
  `creator` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT 'admin' COMMENT '创建人',
  `gmt_created` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `gmt_modified` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `is_deleted` tinyint(1) NOT NULL DEFAULT 0 COMMENT '已删除',
  `username` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '' COMMENT '用户名',
  `workflow_id` int(11) NOT NULL DEFAULT 0 COMMENT '工作流id',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_workflow_id`(`workflow_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 4 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of workflow_workflowadmin
-- ----------------------------
INSERT INTO `workflow_workflowadmin` VALUES (1, 'admin', '2020-04-10 20:08:17', '2020-04-10 20:08:17', 0, 'admin', 30);
INSERT INTO `workflow_workflowadmin` VALUES (2, 'admin', '2020-04-11 09:41:35', '2020-04-11 09:41:35', 0, 'guiji', 31);
INSERT INTO `workflow_workflowadmin` VALUES (3, 'admin', '2020-04-11 09:47:13', '2020-04-11 09:47:13', 0, 'guiji', 35);

-- ----------------------------
-- Table structure for workflow_workflowscript
-- ----------------------------
DROP TABLE IF EXISTS `workflow_workflowscript`;
CREATE TABLE `workflow_workflowscript`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `saved_name` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `description` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `creator` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of workflow_workflowscript
-- ----------------------------
INSERT INTO `workflow_workflowscript` VALUES (1, '创建虚拟机', 'workflow_script/create_vm.py', '用于创建虚拟机的脚本', 1, 'admin', '2019-03-08 07:05:49.613264', '2019-03-08 07:05:49.613315', 0);
INSERT INTO `workflow_workflowscript` VALUES (2, 'werer', 'workflow_script/e5939be6-4b64-11e9-a255-784f437daad6.py', 'erewrewrw2222', 1, 'admin', '2019-03-10 10:06:37.450850', '2019-03-10 10:06:37.450991', 1);
INSERT INTO `workflow_workflowscript` VALUES (3, 'teste2221', 'workflow_script/83b3a57e-42db-11e9-8e30-784f437daad6.py', 'estt', 1, 'admin', '2019-03-10 10:23:38.640143', '2019-03-10 10:23:38.640325', 1);
INSERT INTO `workflow_workflowscript` VALUES (4, '111', 'workflow_script/7401155a-434c-11e9-8621-784f437daad6.py', '222', 1, 'admin', '2019-03-10 23:52:05.449189', '2019-03-10 23:52:05.449298', 1);
INSERT INTO `workflow_workflowscript` VALUES (5, '1313', 'workflow_script/d5d39ad4-4386-11e9-ac68-784f437daad6.py', '13132', 1, 'admin', '2019-03-11 06:50:29.009754', '2019-03-11 06:50:29.009916', 1);
INSERT INTO `workflow_workflowscript` VALUES (6, 'fsdf1', 'workflow_script/08bb0dec-4387-11e9-af6c-784f437daad6.py', 'dfdsf1', 1, 'admin', '2019-03-11 06:51:28.891797', '2019-03-11 06:51:28.891862', 1);
INSERT INTO `workflow_workflowscript` VALUES (7, '12', 'workflow_script/bc560c22-438b-11e9-8720-784f437daad6.py', '122222', 1, 'admin', '2019-03-11 07:25:14.244269', '2019-03-11 07:25:14.244333', 1);
INSERT INTO `workflow_workflowscript` VALUES (8, '12', 'workflow_script/e4bbfec2-438b-11e9-a471-784f437daad6.py', '22', 0, 'admin', '2019-03-11 07:26:12.872996', '2019-03-11 07:26:12.873112', 1);
INSERT INTO `workflow_workflowscript` VALUES (9, '121', 'workflow_script/6be756dc-438c-11e9-866a-784f437daad6.py', '21212', 0, 'admin', '2019-03-11 07:29:59.633154', '2019-03-11 07:29:59.633211', 1);
INSERT INTO `workflow_workflowscript` VALUES (10, '121', 'workflow_script/743df598-438c-11e9-875b-784f437daad6.py', '21212', 0, 'admin', '2019-03-11 07:30:13.623816', '2019-03-11 07:30:13.623875', 1);
INSERT INTO `workflow_workflowscript` VALUES (11, '121', 'workflow_script/aa4f5030-438c-11e9-9ac4-784f437daad6.py', '2121', 0, 'admin', '2019-03-11 07:31:44.335415', '2019-03-11 07:44:31.483375', 1);
INSERT INTO `workflow_workflowscript` VALUES (12, 'fefef222', 'workflow_script/8dae6968-4b64-11e9-9404-784f437daad6.py', '1222222222', 1, 'admin', '2019-03-21 07:04:45.767163', '2019-03-21 07:04:45.767269', 1);
INSERT INTO `workflow_workflowscript` VALUES (13, 'ses222211122222', 'workflow_script/b07acb78-4b64-11e9-9300-784f437daad6.py', '1222222222', 1, 'admin', '2019-03-21 07:05:44.117895', '2019-03-21 07:05:44.117953', 1);
INSERT INTO `workflow_workflowscript` VALUES (14, 'werer', 'workflow_script/e1109ee8-4b64-11e9-bd64-784f437daad6.py', 'erewrewrw', 1, 'admin', '2019-03-21 07:07:05.629952', '2019-03-21 07:07:05.630006', 1);
INSERT INTO `workflow_workflowscript` VALUES (15, 'wf', 'workflow_script/12f69d08-4c30-11e9-bfd8-784f437daad6.py', 'sdfsfs', 1, 'admin', '2019-03-22 07:21:37.181812', '2019-03-22 07:21:37.181870', 1);

-- ----------------------------
-- Table structure for workflow_workflowuserpermission
-- ----------------------------
DROP TABLE IF EXISTS `workflow_workflowuserpermission`;
CREATE TABLE `workflow_workflowuserpermission`  (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `creator` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `gmt_created` datetime(6) NOT NULL,
  `gmt_modified` datetime(6) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `permission` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `user_type` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `user` varchar(100) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,
  `workflow_id` int(11) NOT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `workflow_workflowuserpermission_workflow_id_id_0221212d`(`workflow_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of workflow_workflowuserpermission
-- ----------------------------
INSERT INTO `workflow_workflowuserpermission` VALUES (1, '', '2021-07-30 18:50:30.185234', '2021-07-30 18:50:30.185259', 1, 'api', 'app', 'admin', 1);
INSERT INTO `workflow_workflowuserpermission` VALUES (2, '', '2021-07-30 19:38:36.783856', '2021-07-30 19:38:36.783905', 1, 'api', 'app', 'admin', 1);
INSERT INTO `workflow_workflowuserpermission` VALUES (3, '', '2021-07-30 20:58:51.223924', '2021-07-30 20:58:51.223949', 1, 'api', 'app', 'admin', 2);
INSERT INTO `workflow_workflowuserpermission` VALUES (4, '', '2021-07-30 22:06:14.766068', '2021-07-30 22:06:14.766114', 1, 'api', 'app', 'admin', 1);
INSERT INTO `workflow_workflowuserpermission` VALUES (5, '', '2021-07-31 10:31:43.645654', '2021-07-31 10:31:43.645677', 1, 'api', 'app', 'admin', 1);
INSERT INTO `workflow_workflowuserpermission` VALUES (6, '', '2021-07-31 13:48:36.711167', '2021-07-31 13:48:36.711187', 1, 'api', 'app', 'admin', 1);
INSERT INTO `workflow_workflowuserpermission` VALUES (7, '', '2021-08-01 12:36:28.748373', '2021-08-01 12:36:28.748403', 0, 'api', 'app', 'admin', 1);

SET FOREIGN_KEY_CHECKS = 1;
