Create database ecommerce
Create table userdata(
  userid int auto_increment Primary key,
  username varchar(255) unique not null,
  passuser varchar(255) not null,
  roleuser enum('customer', 'vendor') default 'customer' not null
);

create table stores(
  storeid int auto_increment primary key,
  userid int not null,
  storename varchar(255) not null,
  foreign key (userid) references userdata(userid)
);

create table products(
  productid int auto_increment primary key,
  storeid int not null,
  productname varchar(255) not null,
  price decimal (15,2) not null,
  quantity int not null,
  image_path VARCHAR(255);
  foreign key (storeid) references stores(storeid)
);

create table cart(
  cartid int auto_increment primary key,
  userid int not null,
  checkout datetime default null,
  foreign key(userid) references userdata(userid)
);

create table detail(
  detailid int auto_increment primary key,
  cartid int not null,
  quantity int not null,
  productid int not null,
  price decimal(15,2) not null,
  productname varchar(255) not null,
  foreign key (cartid) references cart(cartid),
  foreign key (productid) references products(productid)
);










