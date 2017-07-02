/*
create domain Genre as varchar
check (value in 
			'Alternative Music',
            'Blues',
            'Classical Music',
            'Country Music',
            'Dance Music',
            'Easy Listening',
            'Electronic Music',
            'European Music',
            'Disco Music'
            'Folk',
            'Pop',
            'Hip Hop',
            'Rap',
            'Indie Pop',
            'Inspirational',
            'Gospel',
            'Asian Pop',
            'Jazz',
            'Latin Music',
            'New Age',
            'Opera',
            'Pop (Popular music)',
            'R&B',
            'Soul',
            'Reggae',
            'Rock',
            'Singer',
            'Songwriter',
            'World Music',
            'Beats',
            'Metal',
            'Hard Rock',
            'psychedelic',

);
*/
drop domain if exists Type_product, Bill_type;
drop table if exists client, instrument, solist, solist_play, band, band_component, band_component_play, Product, Track, Cover,
	bill, concerning;
create domain Type_product as varchar(3) check ( value in ('CD', 'DVD'));
create domain Bill_type as varchar check ( value in ('mastercard', 'visa', 'paypal'));
create table Genre (
	name varchar(50) primary key
);
create table Client (
	username varchar(50) primary key,
	password VARCHAR(20) NOT NULL,
	city varchar(30) not null, 
	fiscalCode char(16) not null UNIQUE check (fiscalCode similar to '[0-9a-zA-Z]{16}'),
	name varchar(50) not null,
	surname varchar(50) not null,
	phone varchar(30) not null check (phone similar to '[+]?[0-9]+'),
	mobilePhone varchar(30) check (mobilePhone similar to '[+]?[0-9]+'),
	favoriteGenre varchar(50) references Genre
);
create table Instrument (
	instrument varchar(50) primary key
);
create table Solist(
	stageName varchar(50) PRIMARY KEY, 
	mainGenre genre not null,
	birthday date not null
);

create table solist_play (
	solist varchar(50) references Solist (stageName),
	instrument varchar(50) references Instrument,
	primary key (solist, instrument)
);

create table Band (
	bandName varchar(50) primary key
);
create table band_component (
	name varchar(40),
	surname varchar(40),
	bandName varchar (50) references Band,
	primary key (name, surname, bandName)
);
create table band_component_play (
	name varchar(40),
	surname varchar(40), 
	bandName varchar(50),
	instrument varchar(50) references Instrument,
	FOREIGN KEY(name,surname,bandName) 
			REFERENCES band_component(name,surname,bandName),
	primary key (name, surname, bandName, instrument) 
);

create table Product (
	id serial primary key,
	title varchar(50) not null, 
	price decimal(7,2) not null,
	storedDate date not null,
	description text not null,
	type Type_product not null,
	solist varchar(50) references Solist(stageName),
	bandName varchar(50) references Band
);
create table Track (
	title varchar(50),
	Product integer references Product(id),
	primary key ( title, Product)
);
create table Cover (
	url_cover varchar primary key, /* oppure data ? */
	Product integer not null references Product(id)
);
create table Bill (
	id serial primary key, 
	data date not null,
	ip_pc varchar(30) not null check ( ip_pc similar to '[0-9]?[0-9]?[0-9].[0-9]?[0-9]?[0-9].[0-9]?[0-9]?[0-9].[0-9]?[0-9]?[0-9]'), -- '[0-9]?[0-9]?[0-9].[0-9]?[0-9]?[0-9].[0-9]?[0-9]?[0-9].[0-9]?[0-9]?[0-9]'
	type Bill_type not null,
	client varchar(50) references Client(username)
);

create table  concerning (
	bill integer references Bill(id),
	Product integer references Product(id),
	primary key (bill, Product)
);








