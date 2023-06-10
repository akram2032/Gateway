CREATE TABLE if not exists users (
  user_id int(4) AUTO_INCREMENT,
  username varchar(25),
  password varchar(25),
  CONSTRAINT pk_users PRIMARY KEY(user_id)
);
create table if not exists devices (
	device_id int(4) auto_increment,
	country varchar(25),
	state varchar(25),
	city varchar(25),
	added_on date DEFAULT CURRENT_DATE,
	added_by int(4),
  Constraint pk_device PRIMARY KEY(device_id),
  Constraint fk_devices Foreign key (added_by) References users (user_id)
);
create table if not exists messages (
  id int(50) not NULL auto_increment,
  device_id int(4),
  date date,
  time Time,
  temperature float,
  longitude double,
  latitude float,
  altitude float,
  depth float,
  rssi int,
  snr double,
  turbidity float,
  CONSTRAINT pk_msg primary key (id),
  CONSTRAINT fk_msg foreign key (device_id) references devices(device_id)
);
