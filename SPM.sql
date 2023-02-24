create database SPM;
use SPM;
create table SPM(
Id int primary key auto_increment,
Owner_Name varchar(300),
Password varchar (200),
CnicNumber int (13),
FlatNumber int (3),
Block varchar (2),
admin BOOLEAN,
confirmed BOOLEAN,
confirmed_on varchar(80)
);