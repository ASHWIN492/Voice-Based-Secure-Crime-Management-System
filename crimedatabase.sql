-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.0.17-nt - MySQL Community Edition (GPL)
-- Server OS:                    Win32
-- HeidiSQL Version:             9.4.0.5174
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for crime
CREATE DATABASE IF NOT EXISTS `crime` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `crime`;

-- Dumping structure for table crime.complaints
CREATE TABLE IF NOT EXISTS `complaints` (
  `id` int(11) NOT NULL auto_increment,
  `crimetype` varchar(500) NOT NULL default '0',
  `place` varchar(500) NOT NULL default '0',
  `des` varchar(500) NOT NULL default '0',
  `lat` varchar(500) NOT NULL default '0',
  `longit` varchar(500) NOT NULL default '0',
  `cdate` varchar(500) NOT NULL default '0',
  `ctime` varchar(500) NOT NULL default '0',
  `photo` varchar(500) NOT NULL default '0',
  `video` varchar(500) NOT NULL default '0',
  `status` varchar(500) NOT NULL default '0',
  `uid` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `FK_complaints_users` (`uid`),
  CONSTRAINT `FK_complaints_users` FOREIGN KEY (`uid`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table crime.complaints: ~1 rows (approximately)
/*!40000 ALTER TABLE `complaints` DISABLE KEYS */;
INSERT INTO `complaints` (`id`, `crimetype`, `place`, `des`, `lat`, `longit`, `cdate`, `ctime`, `photo`, `video`, `status`, `uid`) VALUES
	(1, 'robbery', 'Palace', 'nothing', '12.3023928', '76.6564208', '2024-10-29', '09:49:55', 'deepfake.png', 'orig.mp4', 'Accepted', 1);
/*!40000 ALTER TABLE `complaints` ENABLE KEYS */;

-- Dumping structure for table crime.criminals
CREATE TABLE IF NOT EXISTS `criminals` (
  `id` int(11) NOT NULL auto_increment,
  `cname` varchar(150) NOT NULL default '0',
  `crimes` varchar(150) NOT NULL default '0',
  `height` varchar(150) NOT NULL default '0',
  `identification` varchar(500) NOT NULL default '0',
  `description` varchar(500) NOT NULL default '0',
  `img` varchar(500) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table crime.criminals: ~1 rows (approximately)
/*!40000 ALTER TABLE `criminals` DISABLE KEYS */;
INSERT INTO `criminals` (`id`, `cname`, `crimes`, `height`, `identification`, `description`, `img`) VALUES
	(1, 'ABC', 'robbery', '6', 'mole on neck', 'sgseth', 'test.png');
/*!40000 ALTER TABLE `criminals` ENABLE KEYS */;

-- Dumping structure for table crime.police
CREATE TABLE IF NOT EXISTS `police` (
  `id` int(11) NOT NULL auto_increment,
  `email` varchar(150) NOT NULL default '0',
  `password` varchar(150) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table crime.police: ~1 rows (approximately)
/*!40000 ALTER TABLE `police` DISABLE KEYS */;
INSERT INTO `police` (`id`, `email`, `password`) VALUES
	(1, 'police@gmail.com', '123');
/*!40000 ALTER TABLE `police` ENABLE KEYS */;

-- Dumping structure for table crime.sos
CREATE TABLE IF NOT EXISTS `sos` (
  `id` int(11) NOT NULL auto_increment,
  `lat` varchar(100) NOT NULL default '0',
  `longit` varchar(100) NOT NULL default '0',
  `dat` varchar(100) NOT NULL default '0',
  `tim` varchar(100) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table crime.sos: ~2 rows (approximately)
/*!40000 ALTER TABLE `sos` DISABLE KEYS */;
INSERT INTO `sos` (`id`, `lat`, `longit`, `dat`, `tim`) VALUES
	(1, '12.3023928', '76.6564208', '2024-10-29', '09:36:39'),
	(2, '12.3023928', '76.6564208', '2024-10-29', '09:46:51');
/*!40000 ALTER TABLE `sos` ENABLE KEYS */;

-- Dumping structure for table crime.users
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(150) NOT NULL default '0',
  `email` varchar(150) NOT NULL default '0',
  `phone` varchar(10) NOT NULL default '0',
  `gender` varchar(10) NOT NULL default '0',
  `aadno` varchar(15) NOT NULL default '0',
  `password` varchar(20) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table crime.users: ~1 rows (approximately)
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`id`, `name`, `email`, `phone`, `gender`, `aadno`, `password`) VALUES
	(1, 'Arun', 'arun123@gmail.com', '1234567891', 'Male', '123456789123', '123');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
