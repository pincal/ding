-- phpMyAdmin SQL Dump
-- version 2.10.3
-- http://www.phpmyadmin.net
-- 
-- 主机: localhost
-- 生成日期: 2018 年 02 月 03 日 13:57
-- 服务器版本: 5.0.51
-- PHP 版本: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

-- 
-- 数据库: `test`
-- 

-- --------------------------------------------------------

-- 
-- 表的结构 `dingding_department_detail`
-- 
-- 创建时间: 2018 年 02 月 03 日 16:01
-- 

CREATE TABLE IF NOT EXISTS `dingding_department_detail` (
  `id` int(10) unsigned NOT NULL,
  `name` varchar(45) NOT NULL,
  `parentid` int(10) unsigned NOT NULL,
  `order` int(10) unsigned default NULL,
  `createDeptGroup` tinyint(1) NOT NULL,
  `autoAddUser` tinyint(1) NOT NULL,
  `deptHiding` tinyint(1) NOT NULL,
  `deptPerimits` varchar(45) default NULL,
  `userPerimits` varchar(45) default NULL,
  `outerDept` tinyint(1) NOT NULL,
  `outerPermitDepts` varchar(45) default NULL,
  `outerPermitUsers` varchar(45) default NULL,
  `orgDeptOwner` varchar(45) NOT NULL,
  `deptManagerUseridList` varchar(45) default NULL,
  `groupContainSubDept` varchar(45) NOT NULL,
  `syn_timestamp` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

-- 
-- 表的结构 `dingding_department_list`
-- 
-- 创建时间: 2018 年 02 月 03 日 16:01
-- 

CREATE TABLE IF NOT EXISTS `dingding_department_list` (
  `id` int(10) unsigned NOT NULL,
  `name` varchar(45) NOT NULL,
  `parentid` int(10) unsigned default NULL,
  `createDeptGroup` tinyint(1) default NULL,
  `autoAddUser` tinyint(1) default NULL,
  `syn_timestamp` timestamp NOT NULL default CURRENT_TIMESTAMP,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

-- 
-- 表的结构 `dingding_user_detail`
-- 
-- 创建时间: 2018 年 02 月 03 日 16:01
-- 

CREATE TABLE IF NOT EXISTS `dingding_user_detail` (
  `userid` varchar(45) NOT NULL COMMENT '有0开头的userid',
  `name` varchar(45) NOT NULL,
  `tel` varchar(45) default NULL,
  `workPlace` varchar(45) default NULL,
  `remark` varchar(145) default NULL,
  `mobile` varchar(45) NOT NULL,
  `email` varchar(45) default NULL,
  `orgEmail` varchar(45) default NULL,
  `active` tinyint(1) NOT NULL,
  `orderInDepts` varchar(45) default NULL,
  `isAdmin` tinyint(1) NOT NULL,
  `isBoss` tinyint(1) NOT NULL,
  `dingId` varchar(45) default NULL,
  `unionid` varchar(45) default NULL,
  `isLeaderInDepts` varchar(45) NOT NULL,
  `isHide` tinyint(1) NOT NULL,
  `department` varchar(145) NOT NULL,
  `position` varchar(45) default NULL,
  `avatar` varchar(145) default NULL,
  `hiredDate` datetime default NULL,
  `jobnumber` varchar(45) default NULL,
  `extattr` varchar(300) default NULL,
  `syn_timestamp` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  `openId` varchar(45) default NULL,
  `stateCode` varchar(45) default NULL,
  `isSenior` tinyint(1) NOT NULL,
  `roles` varchar(300) default NULL,
  PRIMARY KEY  (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

-- 
-- 表的结构 `dingding_user_list`
-- 
-- 创建时间: 2018 年 02 月 03 日 16:01
-- 

CREATE TABLE IF NOT EXISTS `dingding_user_list` (
  `userid` varchar(45) NOT NULL COMMENT '有0开头的userid',
  `name` varchar(45) NOT NULL,
  `syn_timestamp` timestamp NOT NULL default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP,
  PRIMARY KEY  (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
