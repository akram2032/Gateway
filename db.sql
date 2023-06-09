-- create the mysql data base 

-- message---
create table if not exists messages(
  	id int not null auto_increment,
  	device_id int,
  	date date, 
  	time time,
  	temperature float, 
  	latitude double,
  	longitude double,
  	altitude float,
  	depth float,
  	rssi int,
  	snr double,
  	turbidite float,
  	Constraint pk_msg PRIMARY KEY(id),
  	Constraint fk_message Foreign key (device_id) References devices (device_id)
);

create table if not exists devices (
	device_id int(4), 
	country varchar(25), 
	state varchar(25),
	city varchar(25),
	added_on date, 
	added_by int(4),
  	Constraint pk_device PRIMARY KEY(device_id),
  	Constraint fk_devices Foreign key (added_by) References users (user_id)
);

create table if not exists users (
	user_id int(4),
	username varchar(25),
	password varchar(25),
	Constraint pk_usr PRIMARY KEY(user_id)
);
