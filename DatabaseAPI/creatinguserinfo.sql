
use sql_intro;

CREATE TABLE userinfo (
 id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 userid INT UNSIGNED,
 username VARCHAR(50),
 userlocation VARCHAR(50) NOT NULL,
 health VARCHAR(20),
 quest_counter INT
 );

