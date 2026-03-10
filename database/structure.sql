/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-12.1.2-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: flight_game
-- ------------------------------------------------------
-- Server version	12.1.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `airport`
--

DROP TABLE IF EXISTS `airport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `airport` (
  `id` int(11) NOT NULL,
  `ident` varchar(40) NOT NULL,
  `name` varchar(40) DEFAULT NULL,
  `iso_country` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`ident`),
  KEY `iso_country` (`iso_country`),
  CONSTRAINT `airport_ibfk_1` FOREIGN KEY (`iso_country`) REFERENCES `country` (`iso_country`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `country`
--

DROP TABLE IF EXISTS `country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `country` (
  `iso_country` varchar(40) NOT NULL,
  `name` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`iso_country`),
  UNIQUE KEY `uq_country_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `false_ticket`
--

DROP TABLE IF EXISTS `false_ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `false_ticket` (
  `ticket_id` int(11) NOT NULL AUTO_INCREMENT,
  `seat` varchar(5) DEFAULT NULL,
  `flight_date` date DEFAULT NULL,
  `departure_airport` varchar(50) DEFAULT NULL,
  `arrival_airport` varchar(50) DEFAULT NULL,
  `flight_time` time DEFAULT NULL,
  `passenger_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`ticket_id`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `game`
--

DROP TABLE IF EXISTS `game`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `game` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `current_day` int(11) DEFAULT NULL,
  `budget` int(11) DEFAULT NULL,
  `energy` int(11) DEFAULT NULL,
  `reputation` int(11) DEFAULT NULL,
  `sustainability` int(11) DEFAULT NULL,
  `location` varchar(40) CHARACTER SET latin1 COLLATE latin1_swedish_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_game_location` (`location`),
  CONSTRAINT `fk_game_location` FOREIGN KEY (`location`) REFERENCES `airport` (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `passenger`
--

DROP TABLE IF EXISTS `passenger`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `passenger` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `game_id` int(11) DEFAULT NULL,
  `true_species` tinyint(1) DEFAULT NULL,
  `first_name` varchar(20) DEFAULT NULL,
  `last_name` varchar(20) DEFAULT NULL,
  `birth_date` date DEFAULT NULL,
  `sex` varchar(1) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `nationality` varchar(50) DEFAULT NULL,
  `place_birth` varchar(50) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `surprise_factor` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `passport`
--

DROP TABLE IF EXISTS `passport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `passport` (
  `passport_ID` int(11) NOT NULL AUTO_INCREMENT,
  `passenger_ID` int(11) DEFAULT NULL,
  `passport_number` varchar(20) DEFAULT NULL,
  `expiration_date` date DEFAULT NULL,
  `issuing_country` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`passport_ID`),
  KEY `idx_passport_passenger` (`passenger_ID`),
  KEY `idx_passport_country` (`issuing_country`),
  CONSTRAINT `1` FOREIGN KEY (`passenger_ID`) REFERENCES `passenger` (`id`),
  CONSTRAINT `fk_passport_country` FOREIGN KEY (`issuing_country`) REFERENCES `country` (`name`),
  CONSTRAINT `fk_passport_passenger` FOREIGN KEY (`passenger_ID`) REFERENCES `passenger` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--Table structure for table 'session'


DROP TABLE IF EXISTS `session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `session` ( 
`id` int NOT NULL AUTO_INCREMENT, 
`passenger_id` int NOT NULL, 
`order_index` int DEFAULT NULL, 
`used` tinyint(1) DEFAULT 0, 
`allowed_in` tinyint(1) DEFAULT NULL, 
PRIMARY KEY (`id`) 
); 
/*!40101 SET character_set_client = @saved_cs_client */;


--
-- Table structure for table `regular_ticket`
--

DROP TABLE IF EXISTS `regular_ticket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `regular_ticket` (
  `ticket_id` int(11) NOT NULL AUTO_INCREMENT,
  `seat` varchar(5) DEFAULT NULL,
  `flight_date` date DEFAULT NULL,
  `departure_airport` varchar(50) DEFAULT NULL,
  `arrival_airport` varchar(50) DEFAULT NULL,
  `flight_time` time DEFAULT NULL,
  `passenger_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`ticket_id`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-03-07 20:25:11
