Create Database RoomBooking;
Use RoomBooking;

Create Table Student
(
	student_id int Primary Key,
	first_name varchar(25),
	last_name varchar(25),
	email varchar(50),
	phone_number varchar(15),
	DOB date,
	Gender varchar(15)
);

Create Table Rooms
(
	room_id int Primary Key,
    room_number varchar(10),
	building_id int,
	furnishings_id int,
	total_occupancy int,
	size varchar(15),
	floor_id int,
	Foreign Key (furnishings_id) references Furnishing(furnishings_id),
	Foreign Key (floor_id) references Floors(floor_id)
);

Create Table Furnishings
(
	furnishings_id int Primary Key,
	furnishing_type varchar(50),
	availability varchar(25)
);

Create Table Floors
(
	floor_id int Primary Key
);

Create Table MaintenanceWorker
(
	maintenance_id int Primary Key,
	first_name varchar(25),
	last_name varchar(25),
	email varchar(50),
	phone_number varchar(15)
);

Create Table Administrator
(
	admin_id int Primary Key,
	first_name varchar(25),
	last_name varchar(25),
	email varchar(50),
	phone_number varchar(15)
);

Create Table MaintenanceRequest
(
	request_id int Primary Key,
	room_id int,
	issue text,
	request_date date,
	Foreign Key (room_id) references Rooms(room_id)
);

Create Table RoomApplication
(
    application_id int Primary Key,
    student_id int,
    room_id int,
    application_status varchar(25),
    Foreign Key (student_id) references Student(student_id),
    Foreign Key (room_id) references Rooms(room_id)
);

Create Table Roommates
(
    student1_id int,
    student2_id int,
    Primary Key (student1_id, student2_id),
    Foreign Key (student1_id) references Student(student_id),
    Foreign Key (student2_id) references Student(student_id)
);