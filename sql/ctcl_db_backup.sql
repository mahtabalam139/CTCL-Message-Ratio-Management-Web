-- MySQL dump 10.13  Distrib 8.0.46, for Linux (x86_64)
--
-- Host: localhost    Database: ctcl_db
-- ------------------------------------------------------
-- Server version       8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `audit_logs`
--

DROP TABLE IF EXISTS `audit_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `audit_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `source` varchar(100) DEFAULT NULL,
  `module` varchar(100) DEFAULT NULL,
  `action` varchar(100) DEFAULT NULL,
  `description` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audit_logs`
--

LOCK TABLES `audit_logs` WRITE;
/*!40000 ALTER TABLE `audit_logs` DISABLE KEYS */;
INSERT INTO `audit_logs` VALUES (1,'admin','WEB','Login','Login','User \'admin\' logged in.','2026-07-27 04:10:52'),(2,'admin','WEB','CTCL','Add Record','New CTCL record added (Exchange IP: 1.1.1.1, Dealer ID: DEALER100)','2026-07-27 04:14:12'),(3,'admin','WEB','CTCL','Save Revision','Exchange IP: 1.1.1.1, Scenario: A2 -> B1, Msg Line: 40 -> 100','2026-07-27 04:14:52');
/*!40000 ALTER TABLE `audit_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ctcl_message_ratio`
--

DROP TABLE IF EXISTS `ctcl_message_ratio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ctcl_message_ratio` (
  `id` int NOT NULL AUTO_INCREMENT,
  `env` varchar(50) DEFAULT NULL,
  `exchange_name` varchar(100) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `dedicated` varchar(50) DEFAULT NULL,
  `system_name` varchar(100) DEFAULT NULL,
  `server_ip` varchar(100) DEFAULT NULL,
  `exchange_ip` varchar(100) DEFAULT NULL,
  `fo_ctcl` varchar(100) DEFAULT NULL,
  `cm_ctcl` varchar(100) DEFAULT NULL,
  `cds_ctcl` varchar(100) DEFAULT NULL,
  `dealer_id` varchar(100) DEFAULT NULL,
  `rack` varchar(100) DEFAULT NULL,
  `scenario` varchar(255) DEFAULT NULL,
  `cm_msgs` int DEFAULT '0',
  `fo_msgs` int DEFAULT '0',
  `cd_msgs` int DEFAULT '0',
  `msg_line` int DEFAULT '0',
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `comments` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ctcl_message_ratio`
--

LOCK TABLES `ctcl_message_ratio` WRITE;
/*!40000 ALTER TABLE `ctcl_message_ratio` DISABLE KEYS */;
INSERT INTO `ctcl_message_ratio` VALUES (1,'PROD','NSE','Mumbai','Yes','APP01','10.0.0.10','10.0.0.20','FO123','CM123','CD123','D001','RACK1','Test Scenario',100,200,50,10,'2026-07-27','2027-07-27','Dummy record'),(2,'Prod','NSE','EH','YES','HFT Platform','10.10.10.101','1.1.1.1','1345','12345','12345','DEALER100','EB17','A2',1,39,0,40,'2026-07-01','2026-07-03','NEW RECORDS ADDED'),(3,'Prod','NSE','EH','YES','HFT Platform','10.10.10.101','1.1.1.1','1345','12345','12345','DEALER100','EB17','B1',1,99,0,100,'2026-07-06','2026-07-31','MCR UPDATED FROM 40 to 100');
/*!40000 ALTER TABLE `ctcl_message_ratio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `role` varchar(100) NOT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','$2b$12$9QsT27tvuV4Yd.iYUtGNn.jjoRHCgWUKbTqwWT30xy3gV4U7l.1Wa','Administrator','admin',1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-07-27  4:16:38
