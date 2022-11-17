-- bankan.colors definition

CREATE TABLE `colors` (
  `color_id` int(11) NOT NULL AUTO_INCREMENT,
  `color` int(11) NOT NULL,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`color_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- bankan.fonts definition

CREATE TABLE `fonts` (
  `font_id` int(11) NOT NULL AUTO_INCREMENT,
  `font_path` varchar(512) NOT NULL,
  `lang_id` int(11) NOT NULL,
  `name` varchar(32) NOT NULL,
  PRIMARY KEY (`font_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- bankan.guild_stamps definition

CREATE TABLE `guild_stamps` (
  `guild_id` bigint(20) NOT NULL,
  `stamp_id` varchar(100) NOT NULL,
  PRIMARY KEY (`guild_id`,`stamp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- bankan.guild_users definition

CREATE TABLE `guild_users` (
  `user_id` bigint(20) NOT NULL,
  `guild_id` bigint(20) NOT NULL,
  PRIMARY KEY (`user_id`,`guild_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- bankan.image_datas definition

CREATE TABLE `image_datas` (
  `image_id` int(11) NOT NULL AUTO_INCREMENT,
  `image_path` varchar(512) DEFAULT NULL,
  `font_size` int(11) DEFAULT NULL,
  `font_id` int(11) DEFAULT NULL,
  `x` double DEFAULT NULL,
  `y` double DEFAULT NULL,
  `max_width` double DEFAULT NULL,
  `max_vertical` double DEFAULT NULL,
  `color_id` int(11) NOT NULL,
  PRIMARY KEY (`image_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- bankan.image_names definition

CREATE TABLE `image_names` (
  `image_id` int(11) NOT NULL,
  `name` varchar(64) NOT NULL,
  PRIMARY KEY (`image_id`,`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- bankan.langs definition

CREATE TABLE `langs` (
  `lang_id` int(11) NOT NULL AUTO_INCREMENT,
  `lang_name` varchar(32) NOT NULL,
  PRIMARY KEY (`lang_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- bankan.stamps definition

CREATE TABLE `stamps` (
  `stamp_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `url` varchar(512) NOT NULL,
  PRIMARY KEY (`stamp_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;


-- bankan.user_stamps definition

CREATE TABLE `user_stamps` (
  `user_id` bigint(20) NOT NULL,
  `stamp_id` int(11) NOT NULL,
  PRIMARY KEY (`stamp_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;