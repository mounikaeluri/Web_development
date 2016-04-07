use jadrn034;




drop table if exists products;
drop table if exists vendor;
drop table if exists category;


create table vendor(id int auto_increment, name varchar(255) not null, primary key(id));
create table category(id int auto_increment, name varchar(255) not null, primary key(id));
create table products(sku varchar(7), vendorid int, catid int, mfdid varchar(255), description text, features text, cost decimal(13,2), retail varchar(15), primary key(sku), foreign key(vendorid) references vendor(id), foreign key(catid) references category(id));

insert into vendor(name) values('Canon');
insert into vendor(name) values('Fujifilm');
insert into vendor(name) values ('Kodak');
insert into vendor(name) values ('LG');
insert into vendor(name) values ('Nikon');
insert into vendor(name) values ('Olympus');
insert into vendor(name) values ('Panasonic');
insert into vendor(name) values ('Samsung');
insert into vendor(name) values ('Sony');

insert into category(name) values ('Compact');
insert into category(name) values ('DSLR');
insert into category(name) values ('Interchangeable Lens');
insert into category(name) values ('Kids');
insert into category(name) values ('Point and Shoot');
insert into category(name) values ('Superzoom bridge');
insert into category(name) values ('Underwater');


