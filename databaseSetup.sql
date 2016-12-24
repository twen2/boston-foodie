-- set up the database
-- Wendy Wen (twen2) and Sharon Zhang (wzhang2)

use wzhang2_db;

DROP TABLE if exists likes;
DROP TABLE if exists dishes;
DROP TABLE if exists comments;
DROP TABLE if exists users;
DROP TABLE if exists restaurants;

-- users table for login feature
CREATE TABLE users (
	id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	username varchar(50) NOT NULL,
	password varchar(50) NOT NULL
) ENGINE = InnoDB;

-- -- restaurants table
CREATE TABLE restaurants (
	id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name varchar(50) NOT NULL,
	location varchar(50) NOT NULL,
	cuisine_type varchar(50) NOT NULL,
	res_type enum ("cafe", "meal","both")
) ENGINE = InnoDB;

load data LOCAL infile 'restaurants.csv'
 into table restaurants fields terminated by ','lines terminated by '\n';

-- dishes table
CREATE TABLE dishes (
	id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
	name varchar(50) NOT NULL,
	num_of_likes int DEFAULT 0,
	res_id int NOT NULL,
	FOREIGN KEY (res_id) REFERENCES restaurants(id) ON DELETE restrict
) ENGINE = InnoDB;


load data LOCAL infile 'dishes.csv'
 into table dishes fields terminated by ','lines terminated by '\n';
 
-- likes table
-- CREATE TABLE likes (
-- 	user_id int NOT NULL,
-- 	dish_id int NOT NULL,
-- 	FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE restrict,
-- 	FOREIGN KEY (dish_id) REFERENCES dishes(id) ON DELETE restrict
-- ) ENGINE = InnoDB;

CREATE TABLE likes (
	user_id int NOT NULL REFERENCES users(id),
	dish_id int NOT NULL REFERENCES dishes(id),
	PRIMARY KEY (user_id,dish_id)
) ENGINE = InnoDB;

