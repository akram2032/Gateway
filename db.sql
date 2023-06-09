---user table---
CREATE TABLE if not exists users (
	user_id int(4) AUTO_INCREMENT,
    username varchar(25),
    password varchar(25),
    CONSTRAINT pk_users PRIMARY KEY(user_id)
);
--- device table----
create table if not exists devices (
	device_id int(4), 
	country varchar(25), 
	state varchar(25),
	city varchar(25),
	added_on date DEFAULT CURRENT_DATE, 
	added_by int(4),
  	Constraint pk_device PRIMARY KEY(device_id),
  	Constraint fk_devices Foreign key (added_by) References users (user_id)
);

--- message tables----
create table if not exists messages (
    id int(50) not NULL auto_increment PRIMARY KEY,
    device_id int(4) not null,
    date date DEFAULT CURRENT_DATE,
    time Time DEFAULT CURRENT_TIME,
    temperature float,
    longitude double,
    latitude float,
    altitude float,
    depth float,
    rssi int,
    snr double,
    turbidite float,
    CONSTRAINT fk_msg foreign key (device_id) references devices(device_id)
);
