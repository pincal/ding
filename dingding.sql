-- phpMyAdmin SQL Dump
-- version 4.6.6
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: 2018-02-05 06:25:55
-- 服务器版本： 5.7.17-log
-- PHP Version: 5.6.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dingtalk`
--
DROP DATABASE IF EXISTS `dingtalk`;
CREATE DATABASE IF NOT EXISTS `dingtalk` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `dingtalk`;

-- --------------------------------------------------------

--
-- 表的结构 `dingding_department_detail`
--

DROP TABLE IF EXISTS `dingding_department_detail`;
CREATE TABLE `dingding_department_detail` (
  `id` int(10) UNSIGNED NOT NULL,
  `name` varchar(45) NOT NULL,
  `parentid` int(10) UNSIGNED NOT NULL,
  `order` int(10) UNSIGNED DEFAULT NULL,
  `createDeptGroup` tinyint(1) NOT NULL,
  `autoAddUser` tinyint(1) NOT NULL,
  `deptHiding` tinyint(1) NOT NULL,
  `deptPerimits` varchar(45) DEFAULT NULL,
  `userPerimits` varchar(45) DEFAULT NULL,
  `outerDept` tinyint(1) NOT NULL,
  `outerPermitDepts` varchar(45) DEFAULT NULL,
  `outerPermitUsers` varchar(45) DEFAULT NULL,
  `orgDeptOwner` varchar(45) NOT NULL,
  `deptManagerUseridList` varchar(45) DEFAULT NULL,
  `groupContainSubDept` varchar(45) NOT NULL,
  `syn_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `dingding_department_list`
--

DROP TABLE IF EXISTS `dingding_department_list`;
CREATE TABLE `dingding_department_list` (
  `id` int(10) UNSIGNED NOT NULL,
  `name` varchar(45) NOT NULL,
  `parentid` int(10) UNSIGNED DEFAULT NULL,
  `createDeptGroup` tinyint(1) DEFAULT NULL,
  `autoAddUser` tinyint(1) DEFAULT NULL,
  `syn_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `dingding_user_detail`
--

DROP TABLE IF EXISTS `dingding_user_detail`;
CREATE TABLE `dingding_user_detail` (
  `userid` varchar(45) NOT NULL COMMENT '有0开头的userid',
  `name` varchar(45) NOT NULL,
  `tel` varchar(45) DEFAULT NULL,
  `workPlace` varchar(45) DEFAULT NULL,
  `remark` varchar(145) DEFAULT NULL,
  `mobile` varchar(45) NOT NULL,
  `email` varchar(45) DEFAULT NULL,
  `orgEmail` varchar(45) DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `orderInDepts` varchar(145) DEFAULT NULL,
  `isAdmin` tinyint(1) NOT NULL,
  `isBoss` tinyint(1) NOT NULL,
  `dingId` varchar(45) DEFAULT NULL,
  `unionid` varchar(45) DEFAULT NULL,
  `isLeaderInDepts` varchar(45) NOT NULL,
  `isHide` tinyint(1) NOT NULL,
  `department` varchar(145) NOT NULL,
  `position` varchar(45) DEFAULT NULL,
  `avatar` varchar(145) DEFAULT NULL,
  `hiredDate` datetime DEFAULT NULL,
  `jobnumber` varchar(45) DEFAULT NULL,
  `extattr` varchar(300) DEFAULT NULL,
  `openId` varchar(45) DEFAULT NULL,
  `stateCode` varchar(45) DEFAULT NULL,
  `isSenior` tinyint(1) NOT NULL,
  `roles` varchar(300) DEFAULT NULL,
  `syn_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `dingding_user_list`
--

DROP TABLE IF EXISTS `dingding_user_list`;
CREATE TABLE `dingding_user_list` (
  `userid` varchar(45) NOT NULL COMMENT '有0开头的userid',
  `name` varchar(45) NOT NULL,
  `syn_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `dingding_department_detail`
--
ALTER TABLE `dingding_department_detail`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `dingding_department_list`
--
ALTER TABLE `dingding_department_list`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `dingding_user_detail`
--
ALTER TABLE `dingding_user_detail`
  ADD PRIMARY KEY (`userid`);

--
-- Indexes for table `dingding_user_list`
--
ALTER TABLE `dingding_user_list`
  ADD PRIMARY KEY (`userid`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
