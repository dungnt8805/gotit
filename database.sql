create database if not exists gotit;

use gotit;

create table if not exists users (
	id int primary key auto_increment,
	email varchar(150) UNIQUE,
	account_from ENUM('facebook', 'google'),
	full_name varchar(255) null,
	phone_number varchar(20) null,
	occupations varchar(255) NULL,
	created_at TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_at TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW()
) engine=innodb;

create table if not exists blogs (
	id int primary key auto_increment,
	user_id int not null,
	title varchar(255) not null,
	content text not null,
	created_at TIMESTAMP NOT NULL DEFAULT NOW(),
	updated_at TIMESTAMP NOT NULL DEFAULT NOW() ON UPDATE NOW(),
	constraint `fk_user_id` foreign key (`user_id`) references `users`(`id`)
) engine=innodb;

create table if not exists blogs_likes (
	id int primary key auto_increment,
	user_id int not null,
	blog_id int not null,
	constraint `fk_pivot_user_id` foreign key (`user_id`) references `users`(`id`),
	constraint `fk_pivot_blog_id` foreign key (`blog_id`) references `blogs`(`id`)
) engine=innodb;


INSERT INTO `users`(`email`, `account_from`, `full_name`, `phone_number`, `occupations`)
values
		('test@gmail.com', 'facebook', '', '',''),
		('test1@gmail.com', 'google', '','', ''),
		('test2@gmail.com', 'facebook','','','');

INSERT INTO `blogs`(`title`, `user_id`, `content`)
values
		('Mùa hè', 1, 'Mùa hè rất nóng'),
		('Mùa đông', 2, 'Mùa đông rất lạnh'),
		('Mùa hè', 1, 'Mùa thu mát mẻ'),
		('Mùa xuân', 1, 'Mùa xuân mưa nhiều');

INSERT INTO `blogs_likes`(`user_id`, `blog_id`)
values
		(1, 2), (1, 3), (1,4), (2,2), (2,3), (2,4), (3,2), (3,3), (3,4);
