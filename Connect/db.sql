select * from user_detls;
create database connect;
use connect;
delete from user_detls where user_key = 200;
CREATE TABLE connect.user_details (
  `user_key` int NOT NULL AUTO_INCREMENT,
  `mobile` decimal(10,0) NOT NULL,
  `name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`user_key`,`mobile`)
) ENGINE=InnoDB AUTO_INCREMENT=200 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


ALTER TABLE user_detls AUTO_INCREMENT = 200;


