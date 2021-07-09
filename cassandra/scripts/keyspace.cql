CREATE KEYSPACE IF NOT EXISTS water_leak
	with replication = {'class' : 'SimpleStrategy', 'replication_factor' : 3};
	
CREATE TABLE IF NOT EXISTS sensor_by_status
(
	status boolean, 
	PRIMARY KEY id uuid,
	soil_moisture double,
	time timeuuid,
	sensor_location text,
	idtable int)


CREATE TABLE IF NOT EXISTS user_by_role
(
	username text,
	 id uuid, 
	 emailAdress text,
	 password text,
	 Admin_key text,
	 idtable int
	)



