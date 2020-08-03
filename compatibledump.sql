-- MySQL dump 10.13  Distrib 5.6.48-88.0, for Linux (x86_64)
--
-- Host: localhost    Database: sketchyactivitydb
-- ------------------------------------------------------
-- Server version	5.6.48-88.0
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO,POSTGRESQL' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table "auth_group"
--

DROP TABLE IF EXISTS "auth_group";
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE "auth_group" (
  "id" int(11) NOT NULL,
  "name" varchar(150) NOT NULL,
  PRIMARY KEY ("id"),
  UNIQUE KEY "name" ("name")
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table "auth_group"
--

LOCK TABLES "auth_group" WRITE;
/*!40000 ALTER TABLE "auth_group" DISABLE KEYS */;
/*!40000 ALTER TABLE "auth_group" ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table "auth_group_permissions"
--

DROP TABLE IF EXISTS "auth_group_permissions";
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE "auth_group_permissions" (
  "id" int(11) NOT NULL,
  "group_id" int(11) NOT NULL,
  "permission_id" int(11) NOT NULL,
  PRIMARY KEY ("id"),
  UNIQUE KEY "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ("group_id","permission_id"),
  KEY "auth_group_permissio_permission_id_84c5c92e_fk_auth_perm" ("permission_id"),
  CONSTRAINT "auth_group_permissio_permission_id_84c5c92e_fk_auth_perm" FOREIGN KEY ("permission_id") REFERENCES "auth_permission" ("id"),
  CONSTRAINT "auth_group_permissions_group_id_b120cbf9_fk_auth_group_id" FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id")
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table "auth_group_permissions"
--

LOCK TABLES "auth_group_permissions" WRITE;
/*!40000 ALTER TABLE "auth_group_permissions" DISABLE KEYS */;
/*!40000 ALTER TABLE "auth_group_permissions" ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table "auth_permission"
--

DROP TABLE IF EXISTS "auth_permission";
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE "auth_permission" (
  "id" int(11) NOT NULL,
  "name" varchar(255) NOT NULL,
  "content_type_id" int(11) NOT NULL,
  "codename" varchar(100) NOT NULL,
  PRIMARY KEY ("id"),
  UNIQUE KEY "auth_permission_content_type_id_codename_01ab375a_uniq" ("content_type_id","codename"),
  CONSTRAINT "auth_permission_content_type_id_2f476e4b_fk_django_co" FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id")
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table "auth_permission"
--

LOCK TABLES "auth_permission" WRITE;
/*!40000 ALTER TABLE "auth_permission" DISABLE KEYS */;
INSERT INTO "auth_permission" VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add portfolio item',7,'add_portfolioitem'),(26,'Can change portfolio item',7,'change_portfolioitem'),(27,'Can delete portfolio item',7,'delete_portfolioitem'),(28,'Can view portfolio item',7,'view_portfolioitem'),(29,'Can add user profile',8,'add_userprofile'),(30,'Can change user profile',8,'change_userprofile'),(31,'Can delete user profile',8,'delete_userprofile'),(32,'Can view user profile',8,'view_userprofile');
/*!40000 ALTER TABLE "auth_permission" ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table "auth_user"
--

DROP TABLE IF EXISTS "auth_user";
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE "auth_user" (
  "id" int(11) NOT NULL,
  "password" varchar(128) NOT NULL,
  "last_login" datetime(6) DEFAULT NULL,
  "is_superuser" tinyint(1) NOT NULL,
  "username" varchar(150) NOT NULL,
  "first_name" varchar(30) NOT NULL,
  "last_name" varchar(150) NOT NULL,
  "email" varchar(254) NOT NULL,
  "is_staff" tinyint(1) NOT NULL,
  "is_active" tinyint(1) NOT NULL,
  "date_joined" datetime(6) NOT NULL,
  PRIMARY KEY ("id"),
  UNIQUE KEY "username" ("username")
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table "auth_user"
--

LOCK TABLES "auth_user" WRITE;
/*!40000 ALTER TABLE "auth_user" DISABLE KEYS */;
INSERT INTO "auth_user" VALUES (1,'pbkdf2_sha256$120000$dTSFlWfEzY73$+v2NTW53VJ8GNXz96gVZh3vAtUZ5gpDUm1zSQhDscM0=','2020-07-27 02:52:48.874379',1,'huntaj@cofc.edu','Austin','Hunt','huntaj@cofc.edu',1,1,'2019-09-08 03:42:30.586871'),(7,'pbkdf2_sha256$150000$VTVYzn1XBGD8$4sJoSSC1jDZcpQN+xggZKlUzlMH/eSQ0T1PpjQU1CpY=','2019-09-10 14:03:55.388587',0,'japple@gmail.com','Johnny','Appleseed','japple@gmail.com',0,1,'2019-09-10 14:03:54.735734'),(8,'pbkdf2_sha256$120000$kYGs3a6RYIgf$3vDqqAO0SZUG0wOeZAx00/UnA5I0v/tbQY6c/4HVtYA=','2019-09-11 15:19:17.425803',0,'testuser@gmail','Test','User','testuser@gmail',0,1,'2019-09-10 19:59:28.558825'),(9,'pbkdf2_sha256$120000$oT1F4e4Eosyt$ohDMjlpgKs2exdIidhD7Ydl+1uGDpLknIk+KpVvaDu4=','2019-09-11 19:04:34.766961',0,'catdog@gmail.com','Cat','Dog','catdog@gmail.com',0,1,'2019-09-11 19:04:34.556411'),(10,'pbkdf2_sha256$120000$hDZuWjfChNcC$puKz58kuCMKp6scLL/BNzC2lg5ZSiyITs+x24ZRhwK8=','2019-09-11 19:29:24.287019',0,'lisatullier@gmail.com','Lisa','Hunt','lisatullier@gmail.com',0,1,'2019-09-11 19:29:24.133438'),(11,'pbkdf2_sha256$120000$13z6tN6X6Tye$Rquy5KzrNoLuwkidfdzGHejcQvJVQA5xa8MQHAEXru4=','2019-09-13 20:29:06.274771',0,'newuser@gmail.com','New','User','newuser@gmail.com',0,1,'2019-09-13 20:29:06.107226'),(12,'pbkdf2_sha256$120000$b66UG4dl2GAs$T+pm97DQpMuM9yRQAREqKYG/NjFgVb3vd4ypIk+n4E0=','2019-09-26 20:26:52.881391',0,'ZReese2402@gmail.con','Zander','Reese','ZReese2402@gmail.con',0,1,'2019-09-26 20:26:52.694760');
/*!40000 ALTER TABLE "auth_user" ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table "auth_user_groups"
--

DROP TABLE IF EXISTS "auth_user_groups";
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE "auth_user_groups" (
  "id" int(11) NOT NULL,
  "user_id" int(11) NOT NULL,
  "group_id" int(11) NOT NULL,
  PRIMARY KEY ("id"),
  UNIQUE KEY "auth_user_groups_user_id_group_id_94350c0c_uniq" ("user_id","group_id"),
  KEY "auth_user_groups_group_id_97559544_fk_auth_group_id" ("group_id"),
  CONSTRAINT "auth_user_groups_group_id_97559544_fk_auth_group_id" FOREIGN KEY ("group_id") REFERENCES "auth_group" ("id"),
  CONSTRAINT "auth_user_groups_user_id_6a12ed8b_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id")
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table "auth_user_groups"
--

LOCK TABLES "auth_user_groups" WRITE;
/*!40000 ALTER TABLE "auth_user_groups" DISABLE KEYS */;
/*!40000 ALTER TABLE "auth_user_groups" ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table "auth_user_user_permissions"
--

DROP TABLE IF EXISTS "auth_user_user_permissions";
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE "auth_user_user_permissions" (
  "id" int(11) NOT NULL,
  "user_id" int(11) NOT NULL,
  "permission_id" int(11) NOT NULL,
  PRIMARY KEY ("id"),
  UNIQUE KEY "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ("user_id","permission_id"),
  KEY "auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm" ("permission_id"),
  CONSTRAINT "auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm" FOREIGN KEY ("permission_id") REFERENCES "auth_permission" ("id"),
  CONSTRAINT "auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id")
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table "auth_user_user_permissions"
--

LOCK TABLES "auth_user_user_permissions" WRITE;
/*!40000 ALTER TABLE "auth_user_user_permissions" DISABLE KEYS */;
/*!40000 ALTER TABLE "auth_user_user_permissions" ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table "django_admin_log"
--

DROP TABLE IF EXISTS "django_admin_log";
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE "django_admin_log" (
  "id" int(11) NOT NULL,
  "action_time" datetime(6) NOT NULL,
  "object_id" longtext,
  "object_repr" varchar(200) NOT NULL,
  "action_flag" smallint(5) unsigned NOT NULL,
  "change_message" longtext NOT NULL,
  "content_type_id" int(11) DEFAULT NULL,
  "user_id" int(11) NOT NULL,
  PRIMARY KEY ("id"),
  KEY "django_admin_log_content_type_id_c4bce8eb_fk_django_co" ("content_type_id"),
  KEY "django_admin_log_user_id_c564eba6_fk_auth_user_id" ("user_id"),
  CONSTRAINT "django_admin_log_content_type_id_c4bce8eb_fk_django_co" FOREIGN KEY ("content_type_id") REFERENCES "django_content_type" ("id"),
  CONSTRAINT "django_admin_log_user_id_c564eba6_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id")
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table "django_admin_log"
--

LOCK TABLES "django_admin_log" WRITE;
/*!40000 ALTER TABLE "django_admin_log" DISABLE KEYS */;
/*!40000 ALTER TABLE "django_admin_log" ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table "django_content_type"
--

DROP TABLE IF EXISTS "django_content_type";
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE "django_content_type" (
  "id" int(11) NOT NULL,
  "app_label" varchar(100) NOT NULL,
  "model" varchar(100) NOT NULL,
  PRIMARY KEY ("id"),
  UNIQUE KEY "django_content_type_app_label_model_76bd3d3b_uniq" ("app_label","model")
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table "django_content_type"
--

LOCK TABLES "django_content_type" WRITE;
/*!40000 ALTER TABLE "django_content_type" DISABLE KEYS */;
INSERT INTO "django_content_type" VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(6,'sessions','session'),(7,'sketchyactivity','portfolioitem'),(8,'sketchyactivity','userprofile');
/*!40000 ALTER TABLE "django_content_type" ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table "django_migrations"
--

DROP TABLE IF EXISTS "django_migrations";
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE "django_migrations" (
  "id" int(11) NOT NULL,
  "app" varchar(255) NOT NULL,
  "name" varchar(255) NOT NULL,
  "applied" datetime(6) NOT NULL,
  PRIMARY KEY ("id")
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table "django_migrations"
--

LOCK TABLES "django_migrations" WRITE;
/*!40000 ALTER TABLE "django_migrations" DISABLE KEYS */;
INSERT INTO "django_migrations" VALUES (1,'contenttypes','0001_initial','2019-09-07 20:30:09.878985'),(2,'auth','0001_initial','2019-09-07 20:30:12.235113'),(3,'admin','0001_initial','2019-09-07 20:30:13.975618'),(4,'admin','0002_logentry_remove_auto_add','2019-09-07 20:30:14.280255'),(5,'admin','0003_logentry_add_action_flag_choices','2019-09-07 20:30:14.385418'),(6,'contenttypes','0002_remove_content_type_name','2019-09-07 20:30:14.831283'),(7,'auth','0002_alter_permission_name_max_length','2019-09-07 20:30:15.028084'),(8,'auth','0003_alter_user_email_max_length','2019-09-07 20:30:15.233606'),(9,'auth','0004_alter_user_username_opts','2019-09-07 20:30:15.337065'),(10,'auth','0005_alter_user_last_login_null','2019-09-07 20:30:15.528802'),(11,'auth','0006_require_contenttypes_0002','2019-09-07 20:30:15.627576'),(12,'auth','0007_alter_validators_add_error_messages','2019-09-07 20:30:15.733401'),(13,'auth','0008_alter_user_username_max_length','2019-09-07 20:30:15.937925'),(14,'auth','0009_alter_user_last_name_max_length','2019-09-07 20:30:16.150652'),(15,'auth','0010_alter_group_name_max_length','2019-09-07 20:30:16.356778'),(16,'auth','0011_update_proxy_permissions','2019-09-07 20:30:16.589332'),(17,'sessions','0001_initial','2019-09-07 20:30:16.954812'),(18,'sketchyactivity','0001_initial','2019-09-07 21:29:27.075988'),(19,'sketchyactivity','0002_auto_20190909_1651','2019-09-09 16:51:19.279123'),(20,'sketchyactivity','0003_userprofile','2019-09-10 14:00:26.932160'),(21,'sketchyactivity','0004_portfolioitem_date','2019-09-27 18:04:21.649039'),(22,'sketchyactivity','0005_auto_20190927_1804','2019-09-27 18:04:21.728297'),(23,'sketchyactivity','0004_auto_20190927_1805','2019-09-27 18:05:22.961128');
/*!40000 ALTER TABLE "django_migrations" ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table "django_session"
--

DROP TABLE IF EXISTS "django_session";
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE "django_session" (
  "session_key" varchar(40) NOT NULL,
  "session_data" longtext NOT NULL,
  "expire_date" datetime(6) NOT NULL,
  PRIMARY KEY ("session_key"),
  KEY "django_session_expire_date_a5c62663" ("expire_date")
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table "django_session"
--

LOCK TABLES "django_session" WRITE;
/*!40000 ALTER TABLE "django_session" DISABLE KEYS */;
INSERT INTO "django_session" VALUES ('12tv5vgftt78e7mazp7cxfwskl7h0yvt','ZGU5ZTJmNzE1M2Y1M2ZkYjMyOGFmNzZmNjU4NjgyY2YwN2NiOTY2MDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NDQyMTJlZGFjNTQ1YWQ5MWI4MjZhNzIwZTI4NTI1OTFhOWExNzViIn0=','2019-09-27 20:56:01.741972'),('14c08bz3o8q15yxye92hg6jvqzdyxrj9','MjM2ODlkZDBiMWI5MDEwMDg3OGYzOTg4ZjI1YzA2NDU4ZjUyZGVkZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmNGEwN2M5MTc2OWU1MjQ5ZWUzYjc2ZWNkNTVjYzI0ZWMxYjk4MTZmIn0=','2019-09-27 20:27:47.338339'),('1c3pvcba8fziqsin607lm5g9ks2svhp9','YTU3Y2NhMWRmNjg0N2YzZWQzOTZkYmE5MTk5OWY2NmU5Yjk0NDViODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1OGQzMzNlMWVhNTBiM2FkNTIyMWI5Zjg0MWI5ZDlhYTQxZDI0ZjMxIn0=','2019-09-25 18:06:48.490048'),('3leuhw2quhhiswd5inscc454jvpbee7d','YTU3Y2NhMWRmNjg0N2YzZWQzOTZkYmE5MTk5OWY2NmU5Yjk0NDViODp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1OGQzMzNlMWVhNTBiM2FkNTIyMWI5Zjg0MWI5ZDlhYTQxZDI0ZjMxIn0=','2019-09-25 15:23:21.266326'),('40xjl6dn23lzjw9801ju31xl6nckgp7h','Mjc5ZjZlMWY4NDA4ODI1ZGY1YmQxOGE0OTk3N2UxYjQ1YTI4NWU1ZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwNjE2NzkwYzAzZmFiYWRiNGYwZWYyMDBhY2ZiMmE0YjI4ZjYxYjdjIn0=','2020-06-09 22:37:28.958084'),('5wyleu2zlz8yw4hz5bdcdxzv0hlnq6zh','Mjc5ZjZlMWY4NDA4ODI1ZGY1YmQxOGE0OTk3N2UxYjQ1YTI4NWU1ZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwNjE2NzkwYzAzZmFiYWRiNGYwZWYyMDBhY2ZiMmE0YjI4ZjYxYjdjIn0=','2020-06-12 21:57:22.992669'),('78e0rxpubroksyh50fj8r4eszswl8crj','ZGU5ZTJmNzE1M2Y1M2ZkYjMyOGFmNzZmNjU4NjgyY2YwN2NiOTY2MDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI3NDQyMTJlZGFjNTQ1YWQ5MWI4MjZhNzIwZTI4NTI1OTFhOWExNzViIn0=','2019-09-27 20:34:45.431541'),('apxlh94sxlezjz43w6lkjlwiclguj8ol','OTY0ZThlNDgzZGJlZTUyYWI1ZDIxMzFjYWNkNzUyNzYzMTNiZDY4ZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwNDU2MWIxMTgwY2ZiZjhlOTAxYjI3MmQyZTIxYjc3YTBkNjlkZTljIn0=','2019-09-22 03:49:33.967885'),('frb47rh30i9vzbhq4nm8hin5nz3kye1i','Mjc5ZjZlMWY4NDA4ODI1ZGY1YmQxOGE0OTk3N2UxYjQ1YTI4NWU1ZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwNjE2NzkwYzAzZmFiYWRiNGYwZWYyMDBhY2ZiMmE0YjI4ZjYxYjdjIn0=','2020-04-16 05:08:00.746395'),('hby97mb36w3ngd7szg2cza33oq5vrv39','NzQ1YzUzZGQwNDIzYTc3NzI0ZGZkNzE2ZWVmMzg3MDFhYWVhNDAwYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxZTYyYjE4ZTJmMWE5NThmNzhhMTMyMmJkZDQ2MDEyNTFlMTY3ZjA0In0=','2020-08-10 02:52:48.880622'),('iseesc7foojakxwa0tfmb8k3aujrtp1f','NzQ1YzUzZGQwNDIzYTc3NzI0ZGZkNzE2ZWVmMzg3MDFhYWVhNDAwYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxZTYyYjE4ZTJmMWE5NThmNzhhMTMyMmJkZDQ2MDEyNTFlMTY3ZjA0In0=','2020-08-03 00:28:44.517544'),('isq4aoyp5g6lqrv42228oa01ml7702oe','MmM4OTk1YjgxNWI4MDc2MzVjZjRkN2FiMzliOWVmNTRjN2IxZDFkMzp7Il9hdXRoX3VzZXJfaWQiOiIxMCIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiMTFmNmE0MGQ2MTE1N2UyM2YwZmUwNThmNGMyMTQ5MjNjMTllMmM1OSJ9','2019-09-25 19:29:24.291831'),('j2abbjpc34ydj3a0f2hfo99qs55k77sd','Mjc5ZjZlMWY4NDA4ODI1ZGY1YmQxOGE0OTk3N2UxYjQ1YTI4NWU1ZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwNjE2NzkwYzAzZmFiYWRiNGYwZWYyMDBhY2ZiMmE0YjI4ZjYxYjdjIn0=','2019-10-11 18:46:31.386299'),('j5fa8inj8cb7wj2akahnk7ewd6riqzpj','NzQ1YzUzZGQwNDIzYTc3NzI0ZGZkNzE2ZWVmMzg3MDFhYWVhNDAwYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxZTYyYjE4ZTJmMWE5NThmNzhhMTMyMmJkZDQ2MDEyNTFlMTY3ZjA0In0=','2020-07-04 17:53:45.644119'),('jax5ybtzk13vzvas6cvnxy4lmtu8vo4p','YmE3Y2RiOWQ0MTRmZjhkZmZhN2YzYTM3MzZjY2E0MGI5MGE2MzZkMDp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJmYjY3OTY4YmM3YWY5YjEwYTJmOWIyNGRlYzNiZmRhZDlhNWE0ODliIn0=','2019-09-25 18:51:00.377948'),('jsueoqg88u94rx49turw1batfdsdj79t','YTRmZTA2OTJmZDQ0ZjA5OTVjZjZmNTg1YTI0YzM5MTQ5MmZiMmE5Njp7Il9hdXRoX3VzZXJfaWQiOiIxMiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9oYXNoIjoiYmM5NjkxOWM2ODk0M2YwMmQ0MWZlZGQwYzkyMDg2MDMzYWI1NDg5NiJ9','2019-10-10 20:26:53.095468'),('mevt3kqm0e2tivsgjwqspl8k6a7lw689','Mjc5ZjZlMWY4NDA4ODI1ZGY1YmQxOGE0OTk3N2UxYjQ1YTI4NWU1ZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwNjE2NzkwYzAzZmFiYWRiNGYwZWYyMDBhY2ZiMmE0YjI4ZjYxYjdjIn0=','2020-03-20 15:23:34.536212'),('nwikr00yja2ntnn4trr1ztbe6b6996ey','Mjc5ZjZlMWY4NDA4ODI1ZGY1YmQxOGE0OTk3N2UxYjQ1YTI4NWU1ZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwNjE2NzkwYzAzZmFiYWRiNGYwZWYyMDBhY2ZiMmE0YjI4ZjYxYjdjIn0=','2020-06-08 02:02:47.268670'),('ox92rqwrg7nwk8yj954lqzhp3h17zwrg','Mjc5ZjZlMWY4NDA4ODI1ZGY1YmQxOGE0OTk3N2UxYjQ1YTI4NWU1ZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwNjE2NzkwYzAzZmFiYWRiNGYwZWYyMDBhY2ZiMmE0YjI4ZjYxYjdjIn0=','2020-02-01 05:31:30.338918'),('rcojbn9dkpt857kqz2cnzyxwhcu03n6h','NzQ1YzUzZGQwNDIzYTc3NzI0ZGZkNzE2ZWVmMzg3MDFhYWVhNDAwYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxZTYyYjE4ZTJmMWE5NThmNzhhMTMyMmJkZDQ2MDEyNTFlMTY3ZjA0In0=','2020-07-06 00:41:04.989224'),('rof688e9kfzzaa26kdxu51e6lww4tksc','NzQ1YzUzZGQwNDIzYTc3NzI0ZGZkNzE2ZWVmMzg3MDFhYWVhNDAwYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxZTYyYjE4ZTJmMWE5NThmNzhhMTMyMmJkZDQ2MDEyNTFlMTY3ZjA0In0=','2020-07-04 17:51:50.740322'),('vu3lvh1nn3z11filrz31j0dp4akseg3y','ODkyNzcyZjc0MTJlNDAxNWFiNDdjN2I5NTFiNWM4NjU3MGNiNDk3Nzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI1MzQwNmU4NjM5ZWZmOWRkOTUwNzM4NjhiNTk5YmVhMTlmOWUzZmM5In0=','2019-09-23 16:40:16.888421'),('ws47mb2j13ve7wl9c6ppl46tz1uqy8ht','NzQ1YzUzZGQwNDIzYTc3NzI0ZGZkNzE2ZWVmMzg3MDFhYWVhNDAwYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIxZTYyYjE4ZTJmMWE5NThmNzhhMTMyMmJkZDQ2MDEyNTFlMTY3ZjA0In0=','2020-07-22 03:12:25.770501'),('xjqf9fzz5zpdnb6haksmrzh4m54g1yxs','Mjc5ZjZlMWY4NDA4ODI1ZGY1YmQxOGE0OTk3N2UxYjQ1YTI4NWU1ZTp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIwNjE2NzkwYzAzZmFiYWRiNGYwZWYyMDBhY2ZiMmE0YjI4ZjYxYjdjIn0=','2019-10-11 18:39:42.807340'),('ybn48jmdknjhwv3fjwd5lasapx5baxyq','ZDY5YWY5ODM3ZmY1NWQzYWEzN2U1Y2EyMDNjZTkzNTRhYWViMWUzYzp7Il9hdXRoX3VzZXJfaWQiOiIxIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiIyNzI2YTk5NWNkNjQ3M2UyYmRkOGZkZmZhNzlhMmUyNTBjZTZhNjQ4In0=','2019-10-11 18:31:59.851915');
/*!40000 ALTER TABLE "django_session" ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table "sketchyactivity_metastuff"
--

DROP TABLE IF EXISTS "sketchyactivity_metastuff";
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE "sketchyactivity_metastuff" (
  "id" int(11) NOT NULL,
  "bio" longtext NOT NULL,
  PRIMARY KEY ("id")
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table "sketchyactivity_metastuff"
--

LOCK TABLES "sketchyactivity_metastuff" WRITE;
/*!40000 ALTER TABLE "sketchyactivity_metastuff" DISABLE KEYS */;
INSERT INTO "sketchyactivity_metastuff" VALUES (1,'Hey there, I\'m Austin Hunt, a portrait-drawing, coffee-drinking, code-writing pun slinger based in Charleston, SC. I\'m a 2019 BS Computer Science graduate of the College of Charleston\'s Honors College and I\'ve been working since graduation with the College\'s Enterprise Application Management team with a mix of web- and dev-ops-related responsibilities. Since 2015, I\'ve been a coder, but since 2011, I\'ve been an art guy, and this website is a swirled pool of those interests (as are most of my other hobbies). Built nearly from scratch with just as much love, attention and precision as I put into my sketchbook, this Django-driven site serves as an ongoing, growing collection of my portrait drawings, mostly drawn with pen and paper. I recently bought an iPad so you may notice a new trend toward digital portraiture - major shoutout to the developers of Procreate!\r\nIf you\'d like to commission me, send me an email at huntaj@g.cofc.edu! Or click the big \"COMMISSION ME\" button, because honestly, we both know that\'d be more fun.');
/*!40000 ALTER TABLE "sketchyactivity_metastuff" ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table "sketchyactivity_portfolioitem"
--

DROP TABLE IF EXISTS "sketchyactivity_portfolioitem";
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE "sketchyactivity_portfolioitem" (
  "id" int(11) NOT NULL,
  "tag" varchar(100) NOT NULL,
  "filename" varchar(100) NOT NULL,
  "portrait_name" varchar(100) NOT NULL,
  "date" date DEFAULT NULL,
  PRIMARY KEY ("id")
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table "sketchyactivity_portfolioitem"
--

LOCK TABLES "sketchyactivity_portfolioitem" WRITE;
/*!40000 ALTER TABLE "sketchyactivity_portfolioitem" DISABLE KEYS */;
INSERT INTO "sketchyactivity_portfolioitem" VALUES (1,'Portrait','khalidsketch.jpg','Khalid','2019-07-22'),(2,'Portrait','Saba.JPG','Saba','2019-07-16'),(3,'Portrait','sarahfinal.JPG','Sarah','2018-02-26'),(4,'Portrait','masegodrawingnew.JPG','Masego','2018-02-07'),(6,'Portrait','jennalynn.JPG','Jenna','2017-05-22'),(7,'Portrait','kevin.JPG','Kevin','2016-11-09'),(8,'Portrait','luke.JPG','Luke','2016-11-12'),(9,'Portrait','johncommission.JPG','John','2017-01-15'),(10,'Portrait','cassidy.JPG','Cassidy','2016-08-29'),(11,'Portrait','lane.JPG','Lane','2016-08-28'),(12,'Portrait','john.JPG','John','2016-11-11'),(13,'Portrait','self.jpg','Self','2016-11-26'),(14,'Portrait','kevinhart.JPG','Kevin Hart','2017-01-01'),(15,'Portrait','bailey.JPG','Bailey','2016-09-29'),(16,'Portrait','pat.JPG','Pat','2016-09-10'),(17,'Portrait','freshmanyearfam.JPG','Freshman','2016-02-04'),(18,'Portrait','presley.JPG','Presley','2017-09-02'),(19,'Portrait','cougarclyde.JPG','Cougar','2015-11-06'),(20,'Portrait','lgc.JPG','Cousins','2016-10-08'),(21,'Portrait','sarahdixon.png','Sarah','2017-03-05'),(22,'Portrait','emily.JPG','Emily','2016-10-09'),(23,'Portrait','krystallized.JPG','Krystallized','2016-05-22'),(24,'Portrait','jill.png','Jill','2017-05-03'),(25,'Portrait','anonymous.JPG','Anonymous','2017-02-05'),(26,'Portrait','vienna.JPG','Vienna','2016-12-26'),(27,'Portrait','brbajessie.JPG','Jessie','2014-01-01'),(28,'Portrait','familyportrait.JPG','Family','2018-12-27'),(29,'Portrait','boycommission.JPG','Gavin','2017-01-05'),(30,'Portrait','zander.JPG','Zander','2016-12-22'),(31,'Portrait','daviadrawing.jpg','Davia','2019-02-14'),(32,'Portrait','brbawalt.JPG','Walt,','2014-01-01'),(33,'Portrait','SOA.JPG','SOA','2015-11-01'),(34,'Portrait','chrisfinal.JPG','Chris','2018-06-20'),(35,'Portrait','connor.JPG','Connor','2016-01-01'),(53,'Portrait','C95D0D42-82A1-4B42-8C0E-8DCEA9C1EA7C.jpeg','Bill Withers (WIP)','2019-09-03'),(55,'Portrait','8AEC3509-F986-49BF-8C39-02735665A3B1.jpeg','Bill Withers Final','2019-09-26'),(60,'Portrait','182FD13F-FE7A-4CED-AB1F-9E37C98A4829.jpeg','Don Draper','2019-07-29'),(61,'Portrait','80D7DDAA-210C-408F-BBA8-886E50DF825F.jpeg','Ongo Gablogian, The Art Collector','2019-05-23'),(62,'Portrait','7D047832-596D-4D71-9EC7-161DA3155DC7.jpeg','Mac Miller','2019-07-23'),(63,'Portrait','BEF4CC2A-7064-4CB9-B576-F6690B12CA15.JPG','Commission','2019-11-20'),(65,'Portrait','E6F37700-DC89-4557-9606-1E5910AFCFA1.jpeg','Smino','2020-01-17'),(67,'Portrait','E4144820-C8E3-435A-B0D0-DF1CA12C951E.jpeg','Haley & Weston','2020-01-19'),(68,'Portrait','B125286B-30BC-45E1-A89D-7F752B7DE807.jpeg','Recolored Haley & Weston','2020-01-19'),(70,'Portrait','ACD720C5-B114-4B22-8D22-169A15055DE8.jpeg','Joe Burrow','2020-01-19'),(71,'Portrait','2ECB9B58-B886-44C7-BB0B-336F6396D465.jpeg','Joe Burrow','2020-01-19'),(72,'Portrait','F0B34D27-131C-4954-8D48-149B371DC811.jpeg','Tom Misch','2020-01-20'),(73,'Portrait','80BDCB9C-9D6A-44D5-96BE-03F0E812211C.jpeg','Shia','2020-01-21'),(74,'Portrait','1FCCFBD4-E498-4CC6-AD81-40CE32861B3E.jpeg','Bernie','2020-01-24'),(75,'Portrait','6ADCB312-B9B4-492E-9B95-640C85143389.jpeg','Kobe Bryant','2020-01-26'),(76,'Portrait','5D7BB748-DD76-4C60-A4B8-BB758E6E7B23.jpeg','Bernie Version 2','2020-01-25'),(77,'Portrait','22F2B2B2-24C5-415D-9350-90C6C8C441AE.jpeg','Childish Gambino WIP','2020-02-05'),(79,'Portrait','B6B16289-6AA4-43B1-9CDA-8DAE3D920626.png','Commission WIP','2020-03-06'),(80,'Portrait','DF9D7DEB-4F3E-4EDA-8F60-EADA63CAD0E5.png','Commission Final','2020-03-10'),(81,'Portrait','465A35F6-BBD8-4923-A5F1-032A2F17C74C.jpeg','ThereseCuratolo','2020-04-01'),(82,'Portrait','CFD4E19C-8FF3-4DA1-99DA-B106D772D282.jpeg','Childish Gambino','2020-05-24'),(83,'Portrait','5ADF2200-17CF-4239-B6C5-323DCEC97A75.jpeg','No Reference 1','2020-05-28'),(84,'Portrait','22F442E4-4C6F-4DC6-BF96-C55C50012799.jpeg','NonReference 2','2020-05-29'),(85,'Portrait','E9706502-1369-41DC-B70A-E1792F09BB73.jpeg','Quarantine Mood','2020-05-30'),(86,'Portrait','CB2810C0-5E96-4DDC-A556-16573C45B11E.jpeg','Commission ','2020-05-30'),(87,'Portrait','A1CFB8C0-A3DC-4FD6-BAAB-91E3B69C6CFC.jpeg','CalebCommission','2020-06-07'),(89,'Portrait','AE1DD7EE-868C-45CA-91B0-59C17DDE0A37.jpeg','Ashley','2020-06-04'),(91,'Portrait','F23C3528-77BB-4E7E-90C3-E6B815F2C72F.jpeg','Sarah Commission','2020-06-16'),(92,'Portrait','27FD4C6E-299A-4FF9-9330-C54D7D51A148.jpeg','Grandparents ','2020-06-21'),(93,'Portrait','2418CFC0-550E-4581-BC83-4E8B63DE4613.jpeg','Steven Commission','2020-06-30'),(94,'Portrait','A904E9D7-5C4D-456A-A7F5-6DC1F89B5210.jpeg','Mochi - Jasmine Commission','2020-06-30'),(95,'Portrait','B8C1E7EA-AA07-4EC6-A235-8DEC0BBC40F3.jpeg','quick sketch, single line','2020-07-19'),(96,'Portrait','0E928623-FE43-42BD-8068-8DC271663136.jpeg','Laufey','2020-07-26'),(97,'Portrait','D13A3595-33AB-44EB-840C-27E312905F90.jpeg','Ella Fitzgerald','2020-07-29');
/*!40000 ALTER TABLE "sketchyactivity_portfolioitem" ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table "sketchyactivity_userprofile"
--

DROP TABLE IF EXISTS "sketchyactivity_userprofile";
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE "sketchyactivity_userprofile" (
  "id" int(11) NOT NULL,
  "phone" varchar(20) NOT NULL,
  "user_id" int(11) NOT NULL,
  PRIMARY KEY ("id"),
  UNIQUE KEY "user_id" ("user_id"),
  CONSTRAINT "sketchyactivity_userprofile_user_id_4865617f_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id")
);
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table "sketchyactivity_userprofile"
--

LOCK TABLES "sketchyactivity_userprofile" WRITE;
/*!40000 ALTER TABLE "sketchyactivity_userprofile" DISABLE KEYS */;
INSERT INTO "sketchyactivity_userprofile" VALUES (1,'',7),(2,'',8),(3,'',9),(4,'',10),(5,'',11),(6,'(864)-221-9266',12);
/*!40000 ALTER TABLE "sketchyactivity_userprofile" ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-03 14:56:04
