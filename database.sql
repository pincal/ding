DROP TABLE IF EXISTS `test`.`dingding_department_detail`;
CREATE TABLE  `test`.`dingding_department_detail` (
  `id` int(10) unsigned NOT NULL,
  `name` varchar(45) NOT NULL,
  `parentid` int(10) unsigned NOT NULL,
  `orders` int(10) unsigned NOT NULL,
  `createDeptGroup` tinyint(1) NOT NULL,
  `autoAddUser` tinyint(1) NOT NULL,
  `deptHiding` tinyint(1) NOT NULL,
  `deptPermits` varchar(45) NOT NULL,
  `userPermits` varchar(45) NOT NULL,
  `outerDept` tinyint(1) NOT NULL,
  `outerPermitDepts` varchar(45) NOT NULL,
  `outerPermitUsers` varchar(45) NOT NULL,
  `orgDeptOwner` varchar(45) NOT NULL,
  `deptManagerUseridList` varchar(45) NOT NULL,
  `syn_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `test`.`dingding_department_list`;
CREATE TABLE  `test`.`dingding_department_list` (
  `id` int(10) unsigned NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `parentid` int(10) unsigned DEFAULT NULL,
  `createDeptGroup` tinyint(1) DEFAULT '0',
  `autoAddUser` tinyint(1) DEFAULT '0',
  `syn_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `test`.`dingding_user_detail`;
CREATE TABLE  `test`.`dingding_user_detail` (
  `userid` varchar(45) NOT NULL COMMENT '有0开头的userid',
  `name` varchar(45) NOT NULL,
  `tel` varchar(45) NOT NULL,
  `workPlace` varchar(45) DEFAULT NULL,
  `remark` varchar(145) DEFAULT NULL,
  `mobile` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `orgEmail` varchar(45) DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `orderInDepts` varchar(45) NOT NULL,
  `isAdmin` tinyint(1) NOT NULL,
  `isBoss` tinyint(1) NOT NULL,
  `dingId` varchar(45) NOT NULL,
  `unionid` varchar(45) DEFAULT NULL,
  `isLeaderInDepts` varchar(45) NOT NULL,
  `isHide` tinyint(1) NOT NULL,
  `department` varchar(145) NOT NULL,
  `uposition` varchar(45) NOT NULL,
  `avatar` varchar(145) NOT NULL,
  `hiredDate` datetime DEFAULT NULL,
  `jobnumber` varchar(45) DEFAULT NULL,
  `extattr` varchar(145) DEFAULT NULL,
  `roles_id` int(10) unsigned DEFAULT NULL,
  `roles_name` varchar(45) DEFAULT NULL,
  `roles_groupName` varchar(45) DEFAULT NULL,
  `syn_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `test`.`dingding_user_list`;
CREATE TABLE  `test`.`dingding_user_list` (
  `userid` varchar(45) NOT NULL COMMENT '有0开头的userid',
  `name` varchar(45) NOT NULL,
  `syn_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;