-- phpMyAdmin SQL Dump
-- version 4.6.6
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: 2018-02-12 09:09:48
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
-- 表的结构 `ding_oa_department`
--

DROP TABLE IF EXISTS `ding_oa_department`;
CREATE TABLE `ding_oa_department` (
  `id` int(50) UNSIGNED NOT NULL,
  `ding_dept_id` varchar(45) NOT NULL COMMENT 'ding中估计为不以0起始的数字',
  `ding_dept_name` varchar(45) NOT NULL COMMENT '钉钉部门名称',
  `oa_org_id` varchar(50) NOT NULL COMMENT 'oa中为0起始的数字',
  `oa_org_shortname` varchar(150) NOT NULL COMMENT 'oa部门名称',
  `oa_org_name` varchar(150) DEFAULT NULL COMMENT '暂不使用',
  `oa_org_update` tinyint(4) NOT NULL DEFAULT '0' COMMENT '-1错误，0无须更新，1已经更新',
  `ding_dept_update` tinyint(4) NOT NULL DEFAULT '0' COMMENT '-1错误，0无须更新，1已经更新',
  `syn_status` tinyint(4) NOT NULL DEFAULT '0' COMMENT '同步状态',
  `find_method` tinyint(4) NOT NULL DEFAULT '0' COMMENT '查找方法：1程序硬编码，2同级别全比对，3相同上级全比对，127手工设置程序忽略',
  `matches` tinyint(4) NOT NULL DEFAULT '0' COMMENT '单条OA数据与钉钉侧数据的匹配次数，不是1的一定是错误行',
  `oa_update_time` datetime DEFAULT NULL COMMENT '如果oa_org_update=1设置这个时间',
  `ding_update_time` datetime DEFAULT NULL COMMENT '如果ding_dept_update=1设置这个时间',
  `last_update` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `ding_oa_user`
--

DROP TABLE IF EXISTS `ding_oa_user`;
CREATE TABLE `ding_oa_user` (
  `id` int(50) UNSIGNED NOT NULL,
  `ding_user_id` varchar(50) NOT NULL COMMENT 'ding中部分人为0起始的数字',
  `email` varchar(50) NOT NULL,
  `oa_user_id` varchar(50) NOT NULL COMMENT 'oa中为字符串',
  `oa_user_update` tinyint(4) NOT NULL DEFAULT '0',
  `ding_user_update` tinyint(4) NOT NULL DEFAULT '0',
  `status` tinyint(4) NOT NULL DEFAULT '0',
  `oa_update_time` datetime DEFAULT NULL,
  `ding_update_time` datetime DEFAULT NULL,
  `last_update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `dingding_department_detail`
--

DROP TABLE IF EXISTS `dingding_department_detail`;
CREATE TABLE `dingding_department_detail` (
  `id` varchar(45) NOT NULL,
  `name` varchar(45) NOT NULL,
  `parentid` varchar(45) NOT NULL,
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
  `id` varchar(45) NOT NULL,
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

-- --------------------------------------------------------

--
-- 表的结构 `syn_log`
--

DROP TABLE IF EXISTS `syn_log`;
CREATE TABLE `syn_log` (
  `id` int(50) UNSIGNED NOT NULL,
  `oa_old` text,
  `oa_new` text,
  `ding_old` text,
  `ding_new` text,
  `syn_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ding_oa_department`
--
ALTER TABLE `ding_oa_department`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `oa_org_id_UNIQUE` (`oa_org_id`);

--
-- Indexes for table `ding_oa_user`
--
ALTER TABLE `ding_oa_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `oa_user_id_UNIQUE` (`oa_user_id`);

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

--
-- Indexes for table `syn_log`
--
ALTER TABLE `syn_log`
  ADD PRIMARY KEY (`id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `ding_oa_department`
--
ALTER TABLE `ding_oa_department`
  MODIFY `id` int(50) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- 使用表AUTO_INCREMENT `ding_oa_user`
--
ALTER TABLE `ding_oa_user`
  MODIFY `id` int(50) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- 使用表AUTO_INCREMENT `syn_log`
--
ALTER TABLE `syn_log`
  MODIFY `id` int(50) UNSIGNED NOT NULL AUTO_INCREMENT;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
