CREATE TABLE userinfo (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    userid INT UNSIGNED,
    username VARCHAR(50),
    userlocation VARCHAR(50) NOT NULL,
    health float,
    quest_counter INT
 );

 