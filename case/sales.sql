/*
SQLyog Community v13.2.1 (64 bit)
MySQL - 8.0.30 : Database - sales
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`sales` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `sales`;

/*Table structure for table `api_customer` */

DROP TABLE IF EXISTS `api_customer`;

CREATE TABLE `api_customer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `api_customer` */

insert  into `api_customer`(`id`,`customer_name`) values 
(1,'CUSTOMER A'),
(2,'CUSTOMER B'),
(3,'CUSTOMER C'),
(4,'CUSTOMER D'),
(5,'CUSTOMER E'),
(6,'CUSTOMER F'),
(7,'Customer G');

/*Table structure for table `api_products` */

DROP TABLE IF EXISTS `api_products`;

CREATE TABLE `api_products` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_code` varchar(15) DEFAULT NULL,
  `product_name` varchar(250) DEFAULT NULL,
  `product_price` double DEFAULT NULL,
  `product_status` varchar(11) NOT NULL,
  `product_stock` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `api_products` */

insert  into `api_products`(`id`,`product_code`,`product_name`,`product_price`,`product_status`,`product_stock`) values 
(1,'PRD0000000001','NASI GORENG',13000,'Active',28),
(2,'PRD0000000002','BAKMI AYAM',12000,'Active',181),
(3,'PRD0000000003','NASI PADANG',17000,'Active',293),
(4,'PRD0000000004','AYAM PENYET',18000,'Active',396),
(5,'PRD0000000005','PECEL AYAM',22000,'Active',120),
(6,'PRD0000000006','PECEL BEBEK',30000,'Active',130),
(7,'PRD0000000007','PECEL LELE',18000,'Active',140),
(8,'PRD0000000008','JAGUNG BAKAR',7000,'Active',150),
(9,'PRD0000000009','TEH HANGAT',5000,'Active',160),
(10,'PRD0000000010','JAHE HANGAT',8000,'Active',170),
(11,'PRD0000000011','AIR MINERAL MERK A',4000,'Active',180),
(12,'PRD0000000012','KOPI HITAM',3000,'Active',190),
(13,'PRD0000000013','TEH HUJAU',9000,'hold',220),
(14,'PRD0000000014','TELUR REBUS',4000,'hold',0),
(15,'PRD0000000015','KAMBING GULING',120000,'hold',3);

/*Table structure for table `api_sale_items` */

DROP TABLE IF EXISTS `api_sale_items`;

CREATE TABLE `api_sale_items` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_price` double NOT NULL,
  `item_qty` int NOT NULL,
  `is_verify` int NOT NULL,
  `product_id_id` bigint DEFAULT NULL,
  `sale_id_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_sale_items_product_id_id_fae361b1_fk_api_products_id` (`product_id_id`),
  KEY `api_sale_items_sale_id_id_cba17e5c_fk_api_sales_id` (`sale_id_id`),
  CONSTRAINT `api_sale_items_product_id_id_fae361b1_fk_api_products_id` FOREIGN KEY (`product_id_id`) REFERENCES `api_products` (`id`),
  CONSTRAINT `api_sale_items_sale_id_id_cba17e5c_fk_api_sales_id` FOREIGN KEY (`sale_id_id`) REFERENCES `api_sales` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `api_sale_items` */

insert  into `api_sale_items`(`id`,`product_price`,`item_qty`,`is_verify`,`product_id_id`,`sale_id_id`) values 
(13,13000,2,0,1,7),
(14,12000,1,0,2,7),
(16,13000,3,0,1,8),
(17,12000,2,0,2,8),
(18,17000,3,0,3,8),
(19,13000,5,0,1,9),
(20,12000,10,0,2,9),
(21,17000,4,0,3,9),
(22,18000,4,0,4,9);

/*Table structure for table `api_sales` */

DROP TABLE IF EXISTS `api_sales`;

CREATE TABLE `api_sales` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `sale_date` datetime(6) DEFAULT NULL,
  `sale_items_total` int NOT NULL,
  `sale_customer_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `api_sales_sale_customer_id_1a6a815c_fk_api_customer_id` (`sale_customer_id`),
  CONSTRAINT `api_sales_sale_customer_id_1a6a815c_fk_api_customer_id` FOREIGN KEY (`sale_customer_id`) REFERENCES `api_customer` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `api_sales` */

insert  into `api_sales`(`id`,`sale_date`,`sale_items_total`,`sale_customer_id`) values 
(7,'2024-07-15 00:00:00.000000',2,1),
(8,'2024-07-16 00:00:00.000000',3,2),
(9,'2024-07-16 01:00:00.000000',4,3);

/*Table structure for table `auth_group` */

DROP TABLE IF EXISTS `auth_group`;

CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `auth_group` */

/*Table structure for table `auth_group_permissions` */

DROP TABLE IF EXISTS `auth_group_permissions`;

CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `auth_group_permissions` */

/*Table structure for table `auth_permission` */

DROP TABLE IF EXISTS `auth_permission`;

CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `auth_permission` */

insert  into `auth_permission`(`id`,`name`,`content_type_id`,`codename`) values 
(1,'Can add log entry',1,'add_logentry'),
(2,'Can change log entry',1,'change_logentry'),
(3,'Can delete log entry',1,'delete_logentry'),
(4,'Can view log entry',1,'view_logentry'),
(5,'Can add permission',2,'add_permission'),
(6,'Can change permission',2,'change_permission'),
(7,'Can delete permission',2,'delete_permission'),
(8,'Can view permission',2,'view_permission'),
(9,'Can add group',3,'add_group'),
(10,'Can change group',3,'change_group'),
(11,'Can delete group',3,'delete_group'),
(12,'Can view group',3,'view_group'),
(13,'Can add user',4,'add_user'),
(14,'Can change user',4,'change_user'),
(15,'Can delete user',4,'delete_user'),
(16,'Can view user',4,'view_user'),
(17,'Can add content type',5,'add_contenttype'),
(18,'Can change content type',5,'change_contenttype'),
(19,'Can delete content type',5,'delete_contenttype'),
(20,'Can view content type',5,'view_contenttype'),
(21,'Can add session',6,'add_session'),
(22,'Can change session',6,'change_session'),
(23,'Can delete session',6,'delete_session'),
(24,'Can view session',6,'view_session'),
(25,'Can add customer',7,'add_customer'),
(26,'Can change customer',7,'change_customer'),
(27,'Can delete customer',7,'delete_customer'),
(28,'Can view customer',7,'view_customer'),
(29,'Can add products',8,'add_products'),
(30,'Can change products',8,'change_products'),
(31,'Can delete products',8,'delete_products'),
(32,'Can view products',8,'view_products'),
(33,'Can add sales',9,'add_sales'),
(34,'Can change sales',9,'change_sales'),
(35,'Can delete sales',9,'delete_sales'),
(36,'Can view sales',9,'view_sales'),
(37,'Can add sale_ items',10,'add_sale_items'),
(38,'Can change sale_ items',10,'change_sale_items'),
(39,'Can delete sale_ items',10,'delete_sale_items'),
(40,'Can view sale_ items',10,'view_sale_items');

/*Table structure for table `auth_user` */

DROP TABLE IF EXISTS `auth_user`;

CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `auth_user` */

/*Table structure for table `auth_user_groups` */

DROP TABLE IF EXISTS `auth_user_groups`;

CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `auth_user_groups` */

/*Table structure for table `auth_user_user_permissions` */

DROP TABLE IF EXISTS `auth_user_user_permissions`;

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `auth_user_user_permissions` */

/*Table structure for table `customers` */

DROP TABLE IF EXISTS `customers`;

CREATE TABLE `customers` (
  `CUSTOMER_ID` bigint unsigned NOT NULL AUTO_INCREMENT,
  `CUSTOMER_NAME` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`CUSTOMER_ID`),
  UNIQUE KEY `CUSTOMER_ID` (`CUSTOMER_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `customers` */

insert  into `customers`(`CUSTOMER_ID`,`CUSTOMER_NAME`) values 
(1,'CUSTOMER A'),
(2,'CUSTOMER B'),
(3,'CUSTOMER C'),
(4,'CUSTOMER D'),
(5,'CUSTOMER E'),
(6,'CUSTOMER F'),
(7,'CUSTOMER A'),
(8,'CUSTOMER B'),
(9,'CUSTOMER C'),
(10,'CUSTOMER D'),
(11,'CUSTOMER E'),
(12,'CUSTOMER F');

/*Table structure for table `django_admin_log` */

DROP TABLE IF EXISTS `django_admin_log`;

CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `django_admin_log` */

/*Table structure for table `django_content_type` */

DROP TABLE IF EXISTS `django_content_type`;

CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `django_content_type` */

insert  into `django_content_type`(`id`,`app_label`,`model`) values 
(1,'admin','logentry'),
(7,'api','customer'),
(8,'api','products'),
(10,'api','sale_items'),
(9,'api','sales'),
(3,'auth','group'),
(2,'auth','permission'),
(4,'auth','user'),
(5,'contenttypes','contenttype'),
(6,'sessions','session');

/*Table structure for table `django_migrations` */

DROP TABLE IF EXISTS `django_migrations`;

CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `django_migrations` */

insert  into `django_migrations`(`id`,`app`,`name`,`applied`) values 
(1,'contenttypes','0001_initial','2024-07-14 10:59:43.527260'),
(2,'auth','0001_initial','2024-07-14 10:59:44.888788'),
(3,'admin','0001_initial','2024-07-14 10:59:45.233781'),
(4,'admin','0002_logentry_remove_auto_add','2024-07-14 10:59:45.253782'),
(5,'admin','0003_logentry_add_action_flag_choices','2024-07-14 10:59:45.277794'),
(6,'api','0001_initial','2024-07-14 10:59:45.719783'),
(7,'contenttypes','0002_remove_content_type_name','2024-07-14 10:59:45.880780'),
(8,'auth','0002_alter_permission_name_max_length','2024-07-14 10:59:46.004785'),
(9,'auth','0003_alter_user_email_max_length','2024-07-14 10:59:46.057779'),
(10,'auth','0004_alter_user_username_opts','2024-07-14 10:59:46.073779'),
(11,'auth','0005_alter_user_last_login_null','2024-07-14 10:59:46.175779'),
(12,'auth','0006_require_contenttypes_0002','2024-07-14 10:59:46.180792'),
(13,'auth','0007_alter_validators_add_error_messages','2024-07-14 10:59:46.193778'),
(14,'auth','0008_alter_user_username_max_length','2024-07-14 10:59:46.384779'),
(15,'auth','0009_alter_user_last_name_max_length','2024-07-14 10:59:46.498780'),
(16,'auth','0010_alter_group_name_max_length','2024-07-14 10:59:46.541783'),
(17,'auth','0011_update_proxy_permissions','2024-07-14 10:59:46.559780'),
(18,'auth','0012_alter_user_first_name_max_length','2024-07-14 10:59:46.668783'),
(19,'sessions','0001_initial','2024-07-14 10:59:46.737780');

/*Table structure for table `django_session` */

DROP TABLE IF EXISTS `django_session`;

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `django_session` */

/*Table structure for table `products` */

DROP TABLE IF EXISTS `products`;

CREATE TABLE `products` (
  `PRODUCT_ID` bigint unsigned NOT NULL AUTO_INCREMENT,
  `PRODUCT_CODE` varchar(15) DEFAULT NULL,
  `PRODUCT_NAME` varchar(250) DEFAULT NULL,
  `PRODUCT_PRICE` float DEFAULT NULL,
  `PRODUCT_STATUS` varchar(11) DEFAULT '0',
  `PRODUCT_STOCK` int DEFAULT '0',
  PRIMARY KEY (`PRODUCT_ID`),
  UNIQUE KEY `PRODUCT_ID` (`PRODUCT_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `products` */

insert  into `products`(`PRODUCT_ID`,`PRODUCT_CODE`,`PRODUCT_NAME`,`PRODUCT_PRICE`,`PRODUCT_STATUS`,`PRODUCT_STOCK`) values 
(1,'PRD0000000001','NASI GORENG',13000,'Active',50),
(2,'PRD0000000002','BAKMI AYAM',12000,'Active',200),
(3,'PRD0000000003','NASI PADANG',17000,'Active',300),
(4,'PRD0000000004','AYAM PENYET',18000,'Active',400),
(5,'PRD0000000005','PECEL AYAM',22000,'Active',120),
(6,'PRD0000000006','PECEL BEBEK',30000,'Active',130),
(7,'PRD0000000007','PECEL LELE',18000,'Active',140),
(8,'PRD0000000008','JAGUNG BAKAR',7000,'Active',150),
(9,'PRD0000000009','TEH HANGAT',5000,'Active',160),
(10,'PRD0000000010','JAHE HANGAT',8000,'Active',170),
(11,'PRD0000000011','AIR MINERAL MERK A',4000,'Active',180),
(12,'PRD0000000012','KOPI HITAM',3000,'Active',190),
(13,'PRD0000000013','TEH HUJAU',9000,'hold',220),
(14,'PRD0000000014','TELUR REBUS',4000,'hold',0),
(15,'PRD0000000015','KAMBING GULING',120000,'hold',3),
(16,'PRD0000000001','NASI GORENG',13000,'Active',50),
(17,'PRD0000000002','BAKMI AYAM',12000,'Active',200),
(18,'PRD0000000003','NASI PADANG',17000,'Active',300),
(19,'PRD0000000004','AYAM PENYET',18000,'Active',400),
(20,'PRD0000000005','PECEL AYAM',22000,'Active',120),
(21,'PRD0000000006','PECEL BEBEK',30000,'Active',130),
(22,'PRD0000000007','PECEL LELE',18000,'Active',140),
(23,'PRD0000000008','JAGUNG BAKAR',7000,'Active',150),
(24,'PRD0000000009','TEH HANGAT',5000,'Active',160),
(25,'PRD0000000010','JAHE HANGAT',8000,'Active',170),
(26,'PRD0000000011','AIR MINERAL MERK A',4000,'Active',180),
(27,'PRD0000000012','KOPI HITAM',3000,'Active',190),
(28,'PRD0000000013','TEH HIJAU',9000,'hold',220),
(29,'PRD0000000014','TELUR REBUS',4000,'hold',0),
(30,'PRD0000000015','KAMBING GULING',120000,'hold',3),
(31,'PRD0000000001','NASI GORENG',13000,'Active',50),
(32,'PRD0000000002','BAKMI AYAM',12000,'Active',200),
(33,'PRD0000000003','NASI PADANG',17000,'Active',300),
(34,'PRD0000000004','AYAM PENYET',18000,'Active',400),
(35,'PRD0000000005','PECEL AYAM',22000,'Active',120),
(36,'PRD0000000006','PECEL BEBEK',30000,'Active',130),
(37,'PRD0000000007','PECEL LELE',18000,'Active',140),
(38,'PRD0000000008','JAGUNG BAKAR',7000,'Active',150),
(39,'PRD0000000009','TEH HANGAT',5000,'Active',160),
(40,'PRD0000000010','JAHE HANGAT',8000,'Active',170),
(41,'PRD0000000011','AIR MINERAL MERK A',4000,'Active',180),
(42,'PRD0000000012','KOPI HITAM',3000,'Active',190),
(43,'PRD0000000013','TEH HUJAU',9000,'hold',220),
(44,'PRD0000000014','TELUR REBUS',4000,'hold',0),
(45,'PRD0000000015','KAMBING GULING',120000,'hold',3);

/*Table structure for table `sale_items` */

DROP TABLE IF EXISTS `sale_items`;

CREATE TABLE `sale_items` (
  `ITEM_ID` bigint unsigned NOT NULL AUTO_INCREMENT,
  `SALE_ID` int DEFAULT NULL,
  `PRODUCT_ID` int DEFAULT NULL,
  `PRODUCT_PRICE` float DEFAULT NULL,
  `ITEM_QTY` int DEFAULT '0',
  `IS_VERIFY` int DEFAULT '0',
  PRIMARY KEY (`ITEM_ID`),
  UNIQUE KEY `ITEM_ID` (`ITEM_ID`),
  KEY `SALE_ID` (`SALE_ID`),
  KEY `PRODUCT_ID` (`PRODUCT_ID`),
  KEY `SALE_ID_IDX` (`SALE_ID`),
  KEY `PRODUCT_ID_IDX` (`PRODUCT_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `sale_items` */

/*Table structure for table `sales` */

DROP TABLE IF EXISTS `sales`;

CREATE TABLE `sales` (
  `SALE_ID` bigint unsigned NOT NULL AUTO_INCREMENT,
  `SALE_DATE` datetime DEFAULT NULL,
  `CUSTOMER_ID` int DEFAULT NULL,
  `SALE_ITEMS_TOTAL` int DEFAULT '0',
  PRIMARY KEY (`SALE_ID`),
  UNIQUE KEY `SALE_ID` (`SALE_ID`),
  KEY `CUSTOMER_ID` (`CUSTOMER_ID`),
  KEY `CUSTOMER_ID_IDX` (`CUSTOMER_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

/*Data for the table `sales` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
