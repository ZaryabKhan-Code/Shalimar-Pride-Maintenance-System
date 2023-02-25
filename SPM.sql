create database SPM;
use SPM;
create table Resident_Information(
id int primary key auto_increment,
resident_name varchar(300),
resident_email varchar (300),
password varchar (200),
self_cnic_number bigint ,
owner_cnic_number bigint,
flat_number varchar (10),
confirmed BOOLEAN,
confirmed_on varchar(80),
registration_count int
);
select * from Resident_Information;
truncate Resident_Information;
create table Resident_Information_Match(
Id int primary key auto_increment,
owner_cnic_number bigint,
flat_number varchar (10)
);

select * from Resident_Information_Match;
insert into Resident_Information_Match value(1,4220133702249,"B-102");
insert into Resident_Information_Match value(2,4220133702244,"A-411");
create table Marquee(
Id int primary key auto_increment,
marquee varchar (500),
confirmed_on varchar(80)
);
select * from Marquee;
