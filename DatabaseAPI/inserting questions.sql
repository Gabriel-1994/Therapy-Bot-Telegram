
/*
CREATE TABLE questions (
   id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
   categoryid INT UNSIGNED,
   category VARCHAR(30) NOT NULL,
   question VARCHAR(350) NOT NULL
);
*/
 
 
-- CATEGORY 1
  INSERT INTO questions (categoryid, category, question)
  VALUES (1, "intro", "Something on your mind today?");
  
  INSERT INTO questions (categoryid, category, question)
  VALUES (1, "intro", "So, tell me about your day so far.");

  INSERT INTO questions (categoryid, category, question)
  VALUES (1, "intro", "So, How is your day going by so far?");



 -- -- CATEGORY 2
  INSERT INTO questions (categoryid, category, question)
  VALUES (2, "follow-up", "What do you think caused this issue?");

  INSERT INTO questions (categoryid, category, question)
  VALUES (2, "follow-up", "Why do you think that happened?");
  
  INSERT INTO questions (categoryid, category, question)
  VALUES (2, "follow-up", "In your opinion, what was the reason behind this?");
  
  -- CATEGORY 4
  INSERT INTO questions (categoryid, category, question)
  VALUES (4, "health-status", "What do you think you can do differently next time around?");

  INSERT INTO questions (categoryid, category, question)
  VALUES (4, "health-status", "If you were to go back in time, what would you have done differently?");
     
  -- CATEGORY 3
  INSERT INTO questions (categoryid, category, question)
  VALUES (3, "Motivation", "Everything will be okay in the end. If it isn’t okay, it isn’t the end");
  
  INSERT INTO questions (categoryid, category, question)
  VALUES (3, "Motivation", "The hard days are what make you stronger");
  
  INSERT INTO questions (categoryid, category, question)
  VALUES (3, "Motivation", "Strive for progress and not perfection");
  
  INSERT INTO questions (categoryid, category, question)
  VALUES (3, "Motivation", "people who wonder if the glass is half empty or full miss the point. The glass is refillable.")