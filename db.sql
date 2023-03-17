-- create the mysql data base 

create table if not exists aquaRob (
  id int not null auto_increment,
  temperature float set default -1, 
  latitude float,
  longitude float,
  altitude float,
  rssi float 
  PRIMARY KEY(id)
)
