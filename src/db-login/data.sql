# cat data.sql
-- MySQL dump 10.13  Distrib 8.0.26, for Linux (x86_64)
--
-- Create a database using `MYSQL_DATABASE` placeholder
--

-- CREATE DATABASE IF NOT EXISTS `MYSQL_DATABASE`;
USE `users`;

-- CREATE USER 'me'@'mysql';
-- GRANT ALL PRIVILEGES ON MYSQL_DATABSE.* To 'me'@'127.0.0.1' IDENTIFIED BY 'password';


DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `Username` varchar(255) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL
)

INSERT INTO `Users` VALUES ('anas','a');
UNLOCK TABLES;

-- Dump completed on 2022-07-28  1:56:09