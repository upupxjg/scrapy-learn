-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: 2017-08-25 18:32:53
-- 服务器版本： 5.6.28-1ubuntu3
-- PHP Version: 7.0.4-5ubuntu2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `scrapy`
--
CREATE DATABASE IF NOT EXISTS `scrapy` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `scrapy`;

-- --------------------------------------------------------

--
-- 表的结构 `movie_download`
--

CREATE TABLE `movie_download` (
  `dl_id` bigint(20) UNSIGNED NOT NULL,
  `mv_id` bigint(20) UNSIGNED NOT NULL,
  `resolution` int(11) NOT NULL,
  `name` varchar(512) NOT NULL,
  `url` varchar(1024) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `movie_info`
--

CREATE TABLE `movie_info` (
  `mv_id` bigint(20) UNSIGNED NOT NULL,
  `mv_name_zh` varchar(256) NOT NULL COMMENT '中文名',
  `mv_name_en` varchar(256) NOT NULL COMMENT '英文名',
  `mv_period` smallint(5) UNSIGNED DEFAULT NULL COMMENT '年代',
  `mv_lang` varchar(128) DEFAULT NULL COMMENT '语言',
  `mv_region` varchar(128) DEFAULT NULL COMMENT '产地',
  `mv_imdb_score` tinyint(3) UNSIGNED DEFAULT NULL,
  `mv_imdb_url` varchar(512) DEFAULT NULL,
  `mv_douban_score` tinyint(3) UNSIGNED DEFAULT NULL,
  `mv_douban_url` varchar(512) DEFAULT NULL,
  `mv_length` smallint(6) DEFAULT NULL COMMENT '片长',
  `mv_director` varchar(128) DEFAULT NULL COMMENT '导演',
  `mv_actor` varchar(256) DEFAULT NULL COMMENT '主演',
  `mv_desc` varchar(2048) DEFAULT NULL COMMENT '简介'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `movie_type`
--

CREATE TABLE `movie_type` (
  `type_id` int(11) UNSIGNED NOT NULL,
  `type_name` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `movie_type_link`
--

CREATE TABLE `movie_type_link` (
  `link_id` bigint(11) UNSIGNED NOT NULL,
  `movie_id` bigint(20) UNSIGNED NOT NULL,
  `type_id` int(11) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `movie_download`
--
ALTER TABLE `movie_download`
  ADD PRIMARY KEY (`dl_id`),
  ADD KEY `idx_mv_id` (`mv_id`);

--
-- Indexes for table `movie_info`
--
ALTER TABLE `movie_info`
  ADD PRIMARY KEY (`mv_id`),
  ADD KEY `idx_imdb_score` (`mv_imdb_score`),
  ADD KEY `idx_douban_score` (`mv_douban_score`);
ALTER TABLE `movie_info` ADD FULLTEXT KEY `idx_mv_name_zh` (`mv_name_zh`);

--
-- Indexes for table `movie_type`
--
ALTER TABLE `movie_type`
  ADD PRIMARY KEY (`type_id`);

--
-- Indexes for table `movie_type_link`
--
ALTER TABLE `movie_type_link`
  ADD PRIMARY KEY (`link_id`),
  ADD KEY `idx_movie_id` (`movie_id`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `movie_download`
--
ALTER TABLE `movie_download`
  MODIFY `dl_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `movie_info`
--
ALTER TABLE `movie_info`
  MODIFY `mv_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `movie_type`
--
ALTER TABLE `movie_type`
  MODIFY `type_id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `movie_type_link`
--
ALTER TABLE `movie_type_link`
  MODIFY `link_id` bigint(11) UNSIGNED NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
