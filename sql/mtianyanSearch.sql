/*
 Navicat Premium Data Transfer

 Source Server         : mtianyan_mac_local
 Source Server Type    : MySQL
 Source Server Version : 80016
 Source Host           : localhost:3306
 Source Schema         : mtianyanSearch

 Target Server Type    : MySQL
 Target Server Version : 80016
 File Encoding         : 65001

 Date: 09/10/2020 20:43:19
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of auth_group
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
BEGIN;
INSERT INTO `auth_permission` VALUES (1, 'Can add permission', 1, 'add_permission');
INSERT INTO `auth_permission` VALUES (2, 'Can change permission', 1, 'change_permission');
INSERT INTO `auth_permission` VALUES (3, 'Can delete permission', 1, 'delete_permission');
INSERT INTO `auth_permission` VALUES (4, 'Can view permission', 1, 'view_permission');
INSERT INTO `auth_permission` VALUES (5, 'Can add group', 2, 'add_group');
INSERT INTO `auth_permission` VALUES (6, 'Can change group', 2, 'change_group');
INSERT INTO `auth_permission` VALUES (7, 'Can delete group', 2, 'delete_group');
INSERT INTO `auth_permission` VALUES (8, 'Can view group', 2, 'view_group');
INSERT INTO `auth_permission` VALUES (9, 'Can add content type', 3, 'add_contenttype');
INSERT INTO `auth_permission` VALUES (10, 'Can change content type', 3, 'change_contenttype');
INSERT INTO `auth_permission` VALUES (11, 'Can delete content type', 3, 'delete_contenttype');
INSERT INTO `auth_permission` VALUES (12, 'Can view content type', 3, 'view_contenttype');
INSERT INTO `auth_permission` VALUES (13, 'Can add session', 4, 'add_session');
INSERT INTO `auth_permission` VALUES (14, 'Can change session', 4, 'change_session');
INSERT INTO `auth_permission` VALUES (15, 'Can delete session', 4, 'delete_session');
INSERT INTO `auth_permission` VALUES (16, 'Can view session', 4, 'view_session');
INSERT INTO `auth_permission` VALUES (17, 'Can add 用户信息', 5, 'add_userprofile');
INSERT INTO `auth_permission` VALUES (18, 'Can change 用户信息', 5, 'change_userprofile');
INSERT INTO `auth_permission` VALUES (19, 'Can delete 用户信息', 5, 'delete_userprofile');
INSERT INTO `auth_permission` VALUES (20, 'Can view 用户信息', 5, 'view_userprofile');
INSERT INTO `auth_permission` VALUES (21, 'Can add 关键词word2vec', 6, 'add_keyword2vec');
INSERT INTO `auth_permission` VALUES (22, 'Can change 关键词word2vec', 6, 'change_keyword2vec');
INSERT INTO `auth_permission` VALUES (23, 'Can delete 关键词word2vec', 6, 'delete_keyword2vec');
INSERT INTO `auth_permission` VALUES (24, 'Can view 关键词word2vec', 6, 'view_keyword2vec');
COMMIT;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
BEGIN;
INSERT INTO `django_content_type` VALUES (2, 'auth', 'group');
INSERT INTO `django_content_type` VALUES (1, 'auth', 'permission');
INSERT INTO `django_content_type` VALUES (3, 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES (4, 'sessions', 'session');
INSERT INTO `django_content_type` VALUES (6, 'user', 'keyword2vec');
INSERT INTO `django_content_type` VALUES (5, 'user', 'userprofile');
COMMIT;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_general_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
BEGIN;
INSERT INTO `django_migrations` VALUES (1, 'contenttypes', '0001_initial', '2020-10-09 11:28:52.168164');
INSERT INTO `django_migrations` VALUES (2, 'contenttypes', '0002_remove_content_type_name', '2020-10-09 11:28:52.193721');
INSERT INTO `django_migrations` VALUES (3, 'auth', '0001_initial', '2020-10-09 11:28:52.224033');
INSERT INTO `django_migrations` VALUES (4, 'auth', '0002_alter_permission_name_max_length', '2020-10-09 11:28:52.286536');
INSERT INTO `django_migrations` VALUES (5, 'auth', '0003_alter_user_email_max_length', '2020-10-09 11:28:52.290729');
INSERT INTO `django_migrations` VALUES (6, 'auth', '0004_alter_user_username_opts', '2020-10-09 11:28:52.295986');
INSERT INTO `django_migrations` VALUES (7, 'auth', '0005_alter_user_last_login_null', '2020-10-09 11:28:52.300359');
INSERT INTO `django_migrations` VALUES (8, 'auth', '0006_require_contenttypes_0002', '2020-10-09 11:28:52.301588');
INSERT INTO `django_migrations` VALUES (9, 'auth', '0007_alter_validators_add_error_messages', '2020-10-09 11:28:52.305658');
INSERT INTO `django_migrations` VALUES (10, 'auth', '0008_alter_user_username_max_length', '2020-10-09 11:28:52.310277');
INSERT INTO `django_migrations` VALUES (11, 'auth', '0009_alter_user_last_name_max_length', '2020-10-09 11:28:52.314661');
INSERT INTO `django_migrations` VALUES (12, 'auth', '0010_alter_group_name_max_length', '2020-10-09 11:28:52.322570');
INSERT INTO `django_migrations` VALUES (13, 'auth', '0011_update_proxy_permissions', '2020-10-09 11:28:52.327047');
INSERT INTO `django_migrations` VALUES (14, 'auth', '0012_alter_user_first_name_max_length', '2020-10-09 11:28:52.331585');
INSERT INTO `django_migrations` VALUES (15, 'sessions', '0001_initial', '2020-10-09 11:28:52.340615');
INSERT INTO `django_migrations` VALUES (16, 'user', '0001_initial', '2020-10-09 11:28:52.388988');
INSERT INTO `django_migrations` VALUES (17, 'user', '0002_auto_20190408_1440', '2020-10-09 11:28:52.612008');
INSERT INTO `django_migrations` VALUES (18, 'user', '0003_auto_20190408_1441', '2020-10-09 11:28:52.616821');
INSERT INTO `django_migrations` VALUES (19, 'user', '0004_auto_20190408_1444', '2020-10-09 11:28:52.631422');
INSERT INTO `django_migrations` VALUES (20, 'user', '0005_auto_20201009_1128', '2020-10-09 11:28:52.652815');
COMMIT;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_general_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_general_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of django_session
-- ----------------------------
BEGIN;
INSERT INTO `django_session` VALUES ('pmeeqwno92kppesvqj9gyglat89j7j1i', '.eJxVjEEOwiAQRe_C2pACQwGX7j0DGZhBqoYmpV0Z765NutDtf-_9l4i4rTVunZc4kTgLJU6_W8L84LYDumO7zTLPbV2mJHdFHrTL60z8vBzu30HFXr-1ZwdWD4kNICNTMbYoKsUwBC7OjwMlFUYk1AkMZM1KW8wIPkDh7MT7Awo8OPQ:1kQr17:KK5gZrygr6BTpsCwiHHNoC9IFGwe0wdmQ0J71cvQlhU', '2020-10-23 11:56:57.418092');
COMMIT;

-- ----------------------------
-- Table structure for user_keyword2vec
-- ----------------------------
DROP TABLE IF EXISTS `user_keyword2vec`;
CREATE TABLE `user_keyword2vec` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keyword` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `keyword_word2vec` varchar(256) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of user_keyword2vec
-- ----------------------------
BEGIN;
INSERT INTO `user_keyword2vec` VALUES (1, '老公', '过,妈妈,发现,丑,讲');
COMMIT;

-- ----------------------------
-- Table structure for user_userprofile
-- ----------------------------
DROP TABLE IF EXISTS `user_userprofile`;
CREATE TABLE `user_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_general_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_general_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `history` varchar(128) COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of user_userprofile
-- ----------------------------
BEGIN;
INSERT INTO `user_userprofile` VALUES (1, 'pbkdf2_sha256$216000$A1lGhuOOsxRn$71PJYSoFW6dtnwxPi8rLfM8Nzeki48zz4J+x3y77fps=', '2020-10-09 11:56:57.416118', 0, '1147727180@qq.com', '', '', '1147727180@qq.com', 0, 1, '2020-10-09 11:56:51.609500', ',老公,如何看待华为 HR 胡玲于 2019-10-30 在华为内部论坛心声社,Apple,如何看待 2019 年 12 月 17 日我国第一艘国产航母「山东舰」');
COMMIT;

-- ----------------------------
-- Table structure for user_userprofile_groups
-- ----------------------------
DROP TABLE IF EXISTS `user_userprofile_groups`;
CREATE TABLE `user_userprofile_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userprofile_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_userprofile_groups_userprofile_id_group_id_52847a61_uniq` (`userprofile_id`,`group_id`),
  KEY `user_userprofile_groups_group_id_98cc4038_fk_auth_group_id` (`group_id`),
  CONSTRAINT `user_userprofile_gro_userprofile_id_49724c40_fk_user_user` FOREIGN KEY (`userprofile_id`) REFERENCES `user_userprofile` (`id`),
  CONSTRAINT `user_userprofile_groups_group_id_98cc4038_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of user_userprofile_groups
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for user_userprofile_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `user_userprofile_user_permissions`;
CREATE TABLE `user_userprofile_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userprofile_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_userprofile_user_pe_userprofile_id_permissio_2e86ceca_uniq` (`userprofile_id`,`permission_id`),
  KEY `user_userprofile_use_permission_id_7f559b23_fk_auth_perm` (`permission_id`),
  CONSTRAINT `user_userprofile_use_permission_id_7f559b23_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_userprofile_use_userprofile_id_68dc814c_fk_user_user` FOREIGN KEY (`userprofile_id`) REFERENCES `user_userprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of user_userprofile_user_permissions
-- ----------------------------
BEGIN;
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
