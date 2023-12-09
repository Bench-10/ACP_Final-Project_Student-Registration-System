-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 08, 2023 at 09:52 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `students_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `STUDID` varchar(200) NOT NULL,
  `FNAME` varchar(200) NOT NULL,
  `LNAME` varchar(200) NOT NULL,
  `ADDRESS` varchar(200) NOT NULL,
  `COURSE` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`STUDID`, `FNAME`, `LNAME`, `ADDRESS`, `COURSE`) VALUES
('22-04617', 'Bench Christian', 'Dela Luna', 'Lumambayan Oriental Mindoro', 'BS Information Technology'),
('22-09374', 'Symon James', 'Gasino', 'San. Isidro,San. Luis, Batangas', 'BS Information Technology');

-- --------------------------------------------------------

--
-- Table structure for table `student_password`
--

CREATE TABLE `student_password` (
  `Username` varchar(50) NOT NULL,
  `Password` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student_password`
--

INSERT INTO `student_password` (`Username`, `Password`) VALUES
('Bench', '1234'),
('BenchPogi', '7654321'),
('Melissa', '123456'),
('Micko', '54321'),
('Symon', '4321'),
('tols', 'tols');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`STUDID`);

--
-- Indexes for table `student_password`
--
ALTER TABLE `student_password`
  ADD PRIMARY KEY (`Username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
