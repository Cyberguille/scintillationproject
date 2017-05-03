-- phpMyAdmin SQL Dump
-- version 4.2.12deb2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jun 16, 2016 at 09:00 PM
-- Server version: 5.5.43-0+deb8u1
-- PHP Version: 5.6.7-1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `scintillationdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `data`
--

CREATE TABLE IF NOT EXISTS `data` (
`id` int(11) NOT NULL,
  `datetime` char(16) NOT NULL,
  `value` float NOT NULL,
  `type` int(11) NOT NULL,
  `station_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `primary_data`
--

CREATE TABLE IF NOT EXISTS `primary_data` (
`id` int(11) NOT NULL,
  `datetime` char(20) NOT NULL,
  `hdop` double(2,1) NOT NULL,
  `vdop` double(2,1) NOT NULL,
  `pdop` double(2,1) NOT NULL,
  `latitude` double(13,10) DEFAULT NULL,
  `longitude` double(13,10) DEFAULT NULL,
  `height` double(10,5) DEFAULT NULL,
  `fix` tinyint(1) NOT NULL,
  `nsat` int(11) NOT NULL,
  `station_id` int(11) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=245037 DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `sat_epoch`
--

CREATE TABLE IF NOT EXISTS `sat_epoch` (
`id` int(11) NOT NULL,
  `prn_code` int(2) NOT NULL,
  `obs_id` int(11) NOT NULL,
  `azm` int(3) NOT NULL,
  `elv` int(2) NOT NULL,
  `cno` int(2) NOT NULL,
  `used_fix` tinyint(1) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=2464355 DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `station`
--

CREATE TABLE IF NOT EXISTS `station` (
  `id` int(11) NOT NULL,
  `ref_lat` float NOT NULL,
  `ref_long` float NOT NULL,
  `name` varchar(25) NOT NULL,
  `ref_height` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `station`
--

INSERT INTO `station` (`id`, `ref_lat`, `ref_long`, `name`, `ref_height`) VALUES
(1, 12.3, 13.4, 'RayTest', 23.5);

-- --------------------------------------------------------

--
-- Table structure for table `type`
--

CREATE TABLE IF NOT EXISTS `type` (
  `id` int(11) NOT NULL,
  `name` varchar(25) NOT NULL,
  `unit` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `data`
--
ALTER TABLE `data`
 ADD PRIMARY KEY (`id`), ADD KEY `station_id` (`station_id`), ADD KEY `type` (`type`);

--
-- Indexes for table `primary_data`
--
ALTER TABLE `primary_data`
 ADD PRIMARY KEY (`id`), ADD KEY `station_id` (`station_id`);

--
-- Indexes for table `sat_epoch`
--
ALTER TABLE `sat_epoch`
 ADD PRIMARY KEY (`id`), ADD KEY `obs_id` (`obs_id`);

--
-- Indexes for table `station`
--
ALTER TABLE `station`
 ADD PRIMARY KEY (`id`), ADD KEY `id` (`id`);

--
-- Indexes for table `type`
--
ALTER TABLE `type`
 ADD PRIMARY KEY (`id`), ADD KEY `Id` (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `data`
--
ALTER TABLE `data`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT for table `primary_data`
--
ALTER TABLE `primary_data`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=245037;
--
-- AUTO_INCREMENT for table `sat_epoch`
--
ALTER TABLE `sat_epoch`
MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=2464355;
--
-- Constraints for dumped tables
--

--
-- Constraints for table `data`
--
ALTER TABLE `data`
ADD CONSTRAINT `data_ibfk_1` FOREIGN KEY (`type`) REFERENCES `type` (`Id`),
ADD CONSTRAINT `data_ibfk_2` FOREIGN KEY (`station_id`) REFERENCES `station` (`id`);

--
-- Constraints for table `primary_data`
--
ALTER TABLE `primary_data`
ADD CONSTRAINT `primary_data_ibfk_1` FOREIGN KEY (`station_id`) REFERENCES `station` (`id`);

--
-- Constraints for table `sat_epoch`
--
ALTER TABLE `sat_epoch`
ADD CONSTRAINT `sat_epoch_ibfk_1` FOREIGN KEY (`obs_id`) REFERENCES `primary_data` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
