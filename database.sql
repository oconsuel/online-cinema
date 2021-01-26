-- MySQL dump 10.13  Distrib 8.0.22, for Linux (x86_64)
--
-- Host: std-mysql    Database: std_1001_exam
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.16.04.1

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('a351abd0c853');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_genre_movie`
--

DROP TABLE IF EXISTS `exam_genre_movie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exam_genre_movie` (
  `movie_id` int(11) NOT NULL,
  `genre_id` int(11) NOT NULL,
  PRIMARY KEY (`movie_id`,`genre_id`),
  KEY `fk_exam_genre_movie_genre_id_exam_genres` (`genre_id`),
  CONSTRAINT `fk_exam_genre_movie_genre_id_exam_genres` FOREIGN KEY (`genre_id`) REFERENCES `exam_genres` (`id`),
  CONSTRAINT `fk_exam_genre_movie_movie_id_exam_movies` FOREIGN KEY (`movie_id`) REFERENCES `exam_movies` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_genre_movie`
--

LOCK TABLES `exam_genre_movie` WRITE;
/*!40000 ALTER TABLE `exam_genre_movie` DISABLE KEYS */;
INSERT INTO `exam_genre_movie` VALUES (8,2),(9,4);
/*!40000 ALTER TABLE `exam_genre_movie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_genres`
--

DROP TABLE IF EXISTS `exam_genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exam_genres` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_exam_genres_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_genres`
--

LOCK TABLES `exam_genres` WRITE;
/*!40000 ALTER TABLE `exam_genres` DISABLE KEYS */;
INSERT INTO `exam_genres` VALUES (4,'Детективы'),(2,'Мультфильмы'),(3,'Ужастики'),(1,'Фантастика');
/*!40000 ALTER TABLE `exam_genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_movies`
--

DROP TABLE IF EXISTS `exam_movies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exam_movies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `description` text NOT NULL,
  `production_year` year(4) NOT NULL,
  `country` varchar(128) NOT NULL,
  `producer` varchar(128) NOT NULL,
  `scenarist` varchar(128) NOT NULL,
  `actors` varchar(256) NOT NULL,
  `duration` int(11) NOT NULL,
  `rating_sum` int(11) DEFAULT NULL,
  `rating_num` int(11) DEFAULT NULL,
  `poster_id` varchar(36) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_exam_movies_poster_id_exam_posters` (`poster_id`),
  CONSTRAINT `fk_exam_movies_poster_id_exam_posters` FOREIGN KEY (`poster_id`) REFERENCES `exam_posters` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_movies`
--

LOCK TABLES `exam_movies` WRITE;
/*!40000 ALTER TABLE `exam_movies` DISABLE KEYS */;
INSERT INTO `exam_movies` VALUES (8,'Рик и Морти','Смешные и изобретательные приключения безумного гения и его внука. В озвучке Сыендука',2013,'США','режисер','cw','Actor A.A.',120,0,0,'9a8b5ea9-ddb1-4868-ab04-f7506a290575'),(9,'HBO','wewre',2013,'США','режисер','cw','Actor A.A.',120,0,0,'9a8b5ea9-ddb1-4868-ab04-f7506a290575'),(10,'HBO','wewre',2013,'США','режисер','cw','Actor A.A.',120,0,0,'9a8b5ea9-ddb1-4868-ab04-f7506a290575'),(11,'HBO','wewre',2013,'США','режисер','cw','Actor A.A.',120,0,0,'9a8b5ea9-ddb1-4868-ab04-f7506a290575');
/*!40000 ALTER TABLE `exam_movies` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_posters`
--

DROP TABLE IF EXISTS `exam_posters`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exam_posters` (
  `id` varchar(36) NOT NULL,
  `file_name` varchar(128) NOT NULL,
  `mime_type` varchar(128) NOT NULL,
  `md5_hash` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_exam_posters_md5_hash` (`md5_hash`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_posters`
--

LOCK TABLES `exam_posters` WRITE;
/*!40000 ALTER TABLE `exam_posters` DISABLE KEYS */;
INSERT INTO `exam_posters` VALUES ('1','poster','.jpg','q'),('9a8b5ea9-ddb1-4868-ab04-f7506a290575','poster.jpg','image/jpeg','fa0a60939250145849cbc602f791497d');
/*!40000 ALTER TABLE `exam_posters` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_reviews`
--

DROP TABLE IF EXISTS `exam_reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exam_reviews` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `movie_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  `text` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `fk_exam_reviews_movie_id_exam_movies` (`movie_id`),
  KEY `fk_exam_reviews_user_id_exam_users` (`user_id`),
  CONSTRAINT `fk_exam_reviews_movie_id_exam_movies` FOREIGN KEY (`movie_id`) REFERENCES `exam_movies` (`id`),
  CONSTRAINT `fk_exam_reviews_user_id_exam_users` FOREIGN KEY (`user_id`) REFERENCES `exam_users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_reviews`
--

LOCK TABLES `exam_reviews` WRITE;
/*!40000 ALTER TABLE `exam_reviews` DISABLE KEYS */;
/*!40000 ALTER TABLE `exam_reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_roles`
--

DROP TABLE IF EXISTS `exam_roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exam_roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_roles`
--

LOCK TABLES `exam_roles` WRITE;
/*!40000 ALTER TABLE `exam_roles` DISABLE KEYS */;
INSERT INTO `exam_roles` VALUES (1,'admin','administrator'),(2,'moder','moderator'),(3,'user','user');
/*!40000 ALTER TABLE `exam_roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `exam_users`
--

DROP TABLE IF EXISTS `exam_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `exam_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(128) NOT NULL,
  `password_hash` varchar(128) NOT NULL,
  `last_name` varchar(128) NOT NULL,
  `first_name` varchar(128) NOT NULL,
  `middle_name` varchar(128) DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_exam_users_login` (`login`),
  KEY `fk_exam_users_role_id_exam_roles` (`role_id`),
  CONSTRAINT `fk_exam_users_role_id_exam_roles` FOREIGN KEY (`role_id`) REFERENCES `exam_roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `exam_users`
--

LOCK TABLES `exam_users` WRITE;
/*!40000 ALTER TABLE `exam_users` DISABLE KEYS */;
INSERT INTO `exam_users` VALUES (1,'admin','pbkdf2:sha256:150000$ua09j8my$f840fadc5c5bddf30e44470013868be47a2784c8ae8bcae32f0918326b40a8a1','admin','admin','admin',1);
/*!40000 ALTER TABLE `exam_users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2021-01-26 15:59:14
