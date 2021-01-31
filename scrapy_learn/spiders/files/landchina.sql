/*
 Navicat Premium Data Transfer

 Source Server         : 腾讯云
 Source Server Type    : MySQL
 Source Server Version : 50729
 Source Host           : 49.234.25.12:3306
 Source Schema         : landchina

 Target Server Type    : MySQL
 Target Server Version : 50729
 File Encoding         : 65001

 Date: 30/01/2021 00:11:29
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for landchina
-- ----------------------------



DROP TABLE IF EXISTS `landc`;
CREATE TABLE `landc` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `xzq` text(1024)  DEFAULT NULL,
  `xmmc` text(1024)  DEFAULT NULL,
  `xmwz` text(1024)  DEFAULT NULL,
  `gymj` text(1024)  DEFAULT NULL,
  `clmj` text(1024)  DEFAULT NULL,
  `gdfs` text(1024)  DEFAULT NULL,
  `tdyt` text(1024)  DEFAULT NULL,
  `synx` text(1024)  DEFAULT NULL,
  `hyfl` text(1024)  DEFAULT NULL,
  `tdjb` text(1024)  DEFAULT NULL,
  `cjjg` text(1024)  DEFAULT NULL,
  `zfqh` text(1024)  DEFAULT NULL,
  `ydzfrq` text(1024)  DEFAULT NULL,
  `ydzfje` text(1024)  DEFAULT NULL,
  `tdsyqr` text(1024)  DEFAULT NULL,
  `bz` text(1024)  DEFAULT NULL,
  `ydrjlx` text(1024)  DEFAULT NULL,
  `ydrjls` text(1024)  DEFAULT NULL,
  `ydjdsj` text(1024)  DEFAULT NULL,
  `ydkgsj` text(1024)  DEFAULT NULL,
  `ydjgsj` text(1024)  DEFAULT NULL,
  `sjkgsj` text(1024)  DEFAULT NULL,
  `sjjgsj` text(1024)  DEFAULT NULL,
  `pzdw` text(1024)  DEFAULT NULL,
  `htqdrq` text(1024)  DEFAULT NULL,
  `url` text(1024)  DEFAULT NULL,
  `create_date` text(1024)  DEFAULT NULL,

  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1  ;



SET FOREIGN_KEY_CHECKS = 1;
