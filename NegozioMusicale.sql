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
            'Psychedelic',
);
*/
drop table if exists client, instrument, soloist, soloist_play, band, band_component, band_component_play, Product, Track, Cover,
    bill, concerning, genre CASCADE ;
drop domain if exists Type_product, Bill_type;
create domain Type_product as varchar(3) check ( value in ('CD', 'DVD'));
create domain Bill_type as varchar check ( value in ('Mastercard', 'Visa', 'Paypal'));
create table Genre (
    name varchar(50) primary key
);
create table Client (
    username varchar(50) primary key,
    password VARCHAR(20) NOT NULL CHECK(LENGTH(password) BETWEEN 8 AND 20),
    city varchar(30) not null,
    fiscalCode char(16) not null UNIQUE check (fiscalCode similar to '[0-9a-zA-Z]{16}'),
    name varchar(50) not null,
    surname varchar(50) not null,
    phone varchar(30) not null check (phone similar to '[+]{0,1}[0-9]+'),
    mobilePhone varchar(30) check (mobilePhone similar to '[+]{0,1}[0-9]+'),
    favouriteGenre varchar(50) references Genre
);
create table Instrument (
    instrument varchar(50) primary key
);
create table Soloist(
    stageName varchar(50) PRIMARY KEY,
    mainGenre varchar(50) not null references Genre,
    birthday date not null
);
create table soloist_play (
    soloist varchar(50) references Soloist (stageName),
    instrument varchar(50) references Instrument,
    primary key (soloist, instrument)
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
    soloist varchar(50) references Soloist(stageName),
    bandName varchar(50) references Band
);
create table Track (
    title varchar(50),
    Product integer references Product(id),
    primary key ( title, Product)
);
create table Cover(
    product integer primary key references Product(id),
    data_cover bytea not null, /* oppure data ? */
    type_cover varchar not null

);
create table Bill(
    id serial primary key,
    data TIMESTAMP ,
    ip_pc varchar(30) not null check ( ip_pc similar to '[0-9]?[0-9]?[0-9].[0-9]?[0-9]?[0-9].[0-9]?[0-9]?[0-9].[0-9]?[0-9]?[0-9]'), -- '[0-9]?[0-9]?[0-9].[0-9]?[0-9]?[0-9].[0-9]?[0-9]?[0-9].[0-9]?[0-9]?[0-9]'
    type Bill_type not null,
    client varchar(50) references Client(username)
);
create table  Concerning(
    billId integer references Bill(id),
    Product integer references Product(id),
    PRIMARY key (billid, Product)
);
insert into genre values ('Jazz');
insert into genre values ('Classica');
insert into genre values ('Rock');
insert into genre values ('Rap');
insert into genre values ('Pop');
insert into client values ('enrico', 'asdasdasd','verona','asdasdasdasdasda','enrico','gigante','+98878778','+2312313123','Jazz' );
insert into client values ('andrea', 'asdasdasd','verona','asdasdasdbsdasda','andrea','perazzoli','+988234328778','+2312313123','Rap' );
insert into client values ('turo', 'asdasdasd','napoli','asdasdnsdasdasda','cristian','turetta','+98878778','+2312313123','Pop' );
insert into client values ('fabio', 'asdasdasd','roma','asfasdasdasdasda','fabio','tagliaferro','+988234378','+2312313123','Rock' );
insert into instrument (instrument) values ('Basso'),('chitarra'),('clarinetto'),('viola'),('arpa'),('Voice');
insert into soloist (stageName, mainGenre, birthday) values ('Vasco','Rock', '12/12/1950'),('Arisa','Pop','12/12/1970');
insert into soloist_play ( soloist, instrument) values ('Vasco','Voice'),('Arisa','Voice');
insert into product (title, price, storedDate, description, type, soloist, bandName) values ('Domenica Al Bar', 45.12, '2000/12/22',
    'una domenica al bar con Vasco', 'CD','Vasco', null);
insert into product (title, price, storedDate, description, type, soloist, bandName) values ('Carotone al Pub', 20.12, '2000/12/31',
    'una domenica al bar con Vasco', 'DVD','Arisa', null);
insert into track (title, product) values ('Sole', 1);
insert into track (title, product) values ('Mare', 1);
insert into track (title, product) values ('Pioggia',1);
insert into track (title, product) values ('Cuore', 2);
insert into track (title, product) values ('Martino', 2);
insert into track (title, product) values ('Stella',2);
INSERT INTO Band(bandname) VALUES ('I rossi'), ('I bianchi'), ('I viola');
INSERT INTO band_component(name, surname, bandname)
        VALUES ('Rosso','Carminio','I rossi'),
         ('Rosso','Acceso','I rossi'),
         ('Bianco','Puro','I bianchi'),
         ('Bianco','Acceso','I bianchi'),
         ('Bianco','Spento','I bianchi'),
         ('Viola', 'Spento', 'I viola'),
         ('Viola', 'Sfumatura', 'I viola'),
         ('Viola', 'Daltonico', 'I viola');
INSERT INTO band_component_play(name,surname,bandName,instrument)
        VALUES ('Rosso','Carminio','I rossi','Basso'),
         ('Rosso','Acceso','I rossi','chitarra'),
         ('Bianco','Puro','I bianchi','Basso'),
         ('Bianco','Acceso','I bianchi','Basso'),
         ('Bianco','Spento','I bianchi','Basso'),
         ('Viola','Spento','I viola','Basso'),
         ('Viola','Sfumatura','I viola','Basso'),
         ('Viola','Daltonico','I viola','Basso');
