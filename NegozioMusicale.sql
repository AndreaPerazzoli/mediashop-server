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
create domain Bill_type as varchar check ( value in ('Bankwire', 'Credit Card', 'Paypal'));
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
    mobilePhone varchar(30) check ( mobilePhone IS NULL OR mobilePhone similar to '[+]{0,1}[0-9]+')

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
    main_genre varchar(50) not null references Genre , 
    quantity integer not null CHECK(quantity >= 0),
    description text not null,
    type Type_product not null,
    soloist varchar(50) references Soloist(stageName),
    bandName varchar(50) references Band
);
create table Track (
    title varchar(50) not null,
    track_order integer,
    Product integer references Product(id),
    primary key ( track_order, Product)
);
create table Cover(
    product integer primary key references Product(id),
    url_cover text  /* oppure data ? */

);
create table Bill(
    id serial primary key,
    data TIMESTAMP ,
    ip_pc varchar(30) not null check ( ip_pc similar to '[0-9]?[0-9]?[0-9].[0-9]?[0-9]?[0-9].[0-9]?[0-9]?[0-9].[0-9]?[0-9]?[0-9]'), -- '[0-9]?[0-9]?[0-9].[0-9]?[0-9]?[0-9].[0-9]?[0-9]?[0-9].[0-9]?[0-9]?[0-9]'
    type Bill_type not null,
    quantity integer not null check( quantity > 0), 
    client varchar(50) not null references Client(username)
);
create table  Concerning(
    billId integer references Bill(id),
    Product integer references Product(id),
    PRIMARY key (billid, Product)
);
insert into genre values ('Nessuno');
insert into genre values ('Jazz');
insert into genre values ('Classica');
insert into genre values ('Rock');
insert into genre values ('Rap');
insert into genre values ('Pop');
insert into client values ('enrico', 'asdasdasd','verona','asdasdasdasdasda','enrico','gigante','+98878778','+2312313123' );
insert into client values ('andrea', 'asdasdasd','verona','asdasdasdbsdasda','andrea','perazzoli','+988234328778','+2312313123' );
insert into client values ('turo', 'asdasdasd','napoli','asdasdnsdasdasda','cristian','turetta','+98878778','+2312313123' );
insert into client values ('fabio', 'asdasdasd','roma','asfasdasdasdasda','fabio','tagliaferro','+988234378','+2312313123' );
insert into instrument (instrument) values ('Basso'),('chitarra'),('clarinetto'),('viola'),('arpa'),('Voice'), ('Guitar');
insert into soloist (stageName, mainGenre, birthday) values ('Vasco','Rock', '12/12/1950'),('Arisa','Pop','12/12/1970'),('Cristian Zacarias', 'Classica', '12/12/1950'), ('Frank Zappa','Rock', '12/12/1950');
insert into soloist_play ( soloist, instrument) values ('Vasco','Voice'),('Arisa','Voice'), ('Frank Zappa','Guitar');



INSERT INTO Band(bandname) VALUES ('Pink Floid'), ('Genesis'), ('The Beatles');
INSERT INTO band_component(name, surname, bandname)
        VALUES ('Rosso','Carminio','Pink Floid'),
         ('Rosso','Acceso','Pink Floid'),
         ('Bianco','Puro','Genesis'),
         ('Bianco','Acceso','Genesis'),
         ('Bianco','Spento','Genesis'),
         ('Viola', 'Spento', 'The Beatles'),
         ('Viola', 'Sfumatura', 'The Beatles'),
         ('Viola', 'Daltonico', 'The Beatles');
INSERT INTO band_component_play(name,surname,bandName,instrument)
        VALUES ('Rosso','Carminio','Pink Floid','Basso'),
         ('Rosso','Acceso','Pink Floid','chitarra'),
         ('Bianco','Puro','Genesis','Basso'),
         ('Bianco','Acceso','Genesis','Basso'),
         ('Bianco','Spento','Genesis','Basso'),
         ('Viola','Spento','The Beatles','Basso'),
         ('Viola','Sfumatura','The Beatles','Basso'),
         ('Viola','Daltonico','The Beatles','Basso');
         
insert into product (title, price, storedDate, main_genre, quantity, description, type, soloist, bandName) values ('Mozart piano Concerto', 20.12, '2000/12/31', 'Classica', 9, 'Piano concerto vol.6 Mozart', 'CD','Cristian Zacarias', null);
insert into product (title, price, storedDate, main_genre, quantity, description, type, soloist, bandName) values ('Non siamo mica gli americani', 45.01, '1987/12/22','Rock', 20, 'Non siamo mica gli americani è il secondo album in studio del cantautore italiano Vasco Rossi uscito nel 1979, pubblicato dalla casa discografica Lotus', 'CD','Vasco', null);
insert into product (title, price, storedDate, main_genre, quantity, description, type, soloist, bandName) values ('Hot rats', 45.12, '1980/12/10','Rock', 20,
    'Hot Rats è il settimo album del musicista statunitense Frank Zappa (il suo secondo da solista) pubblicato negli Stati Uniti il 10 ottobre 1969. Il disco, fortemente influenzato da atmosfere jazz rock, non riscosse nessun successo commerciale in patria mentre in Europa, specialmente in Gran Bretagna (nona posizione) e nei Paesi Bassi (sesta posizione), ebbe un ottimo riscontro di pubblico diventando uno dei suoi dischi più celebri e conosciuti.', 'CD','Frank Zappa', null);
insert into product (title, price, storedDate, main_genre, quantity, description, type, soloist, bandName) values ('Let it be',20.12, '2000/12/31','Pop', 2, 'Let It Be è una canzone dei Beatles del 1970, composta da Paul McCartney anche se viene come da consuetudine attribuita al duo compositivo Lennon/McCartney.', 'CD',null, 'The Beatles');
    
insert into track (title,track_order, product) values ('Sole',1, 1);
insert into track (title,track_order, product) values ('Mare',2, 1);
insert into track (title,track_order, product) values ('Pioggia',3,1);
insert into track (title,track_order, product) values ('Cuore',1, 2);
insert into track (title,track_order, product) values ('Martino',2, 2);
insert into track (title,track_order, product) values ('Stella',3,2);

insert into cover(product, url_cover) values (1, 'https://www.music-bazaar.com/album-images/vol1002/811/811476/2664465-big/Mozart-Piano-Concertos-Vol-6-cover.jpg');
insert into cover(product, url_cover) values (2, 'http://www.vascorossiundio.com/wp-content/uploads/2015/10/vasco-rossi-non-siamo-mica-gli-americani.jpg');
insert into cover(product, url_cover) values (3, 'https://img.discogs.com/OK9dDmCAPSKb5E2mmbHEOhPT5n8=/fit-in/600x598/filters:strip_icc():format(jpeg):mode_rgb():quality(90)/discogs-images/R-584013-1444143009-3942.jpeg.jpg');
insert into cover(product, url_cover) values (4, 'https://upload.wikimedia.org/wikipedia/en/2/25/LetItBe.jpg');




insert into product (title, price, storedDate, main_genre, quantity, description, type, soloist, bandName) values ('Sgt. Peppers Lonely Hearts Club Band',15.75, '2017/3/14','Pop', 2, 'Sgt. Peppers Lonely Hearts Club Band is the eighth studio album by English rock band the Beatles. ', 'CD',null, 'The Beatles');

insert into cover(product, url_cover) values (5, 'https://static.independent.co.uk/s3fs-public/styles/article_small/public/thumbnails/image/2017/05/25/16/sgt-peppers-the-beatles.jpg');

insert into product (title, price, storedDate, main_genre, quantity, description, type, soloist, bandName) values ('Yellow Submarine',10.40, '2017/10/11','Pop', 2, 'Yellow Submarine is the tenth studio album by English rock band the Beatles, released on 13 January 1969', 'CD',null, 'The Beatles');

insert into cover(product, url_cover) values (6, null);

insert into product (title, price, storedDate, main_genre, quantity, description, type, soloist, bandName) values ('Live Shepperton 1973',20.40, '2017/10/12','Rock', 8, 'A great performance by Genesis. Video remastered from the original 16mm footage.', 'DVD',null, 'Genesis');

insert into cover(product, url_cover) values (7, 'http://www.zupimages.net/up/15/48/d7zo.jpg');

insert into product (title, price, storedDate, main_genre, quantity, description, type, soloist, bandName) values ('Vasco Dal Palco',15.60, '2016/10/12','Rock', 9, 'This DVD contains live vidoclips from the tour from 1990 to 2004', 'DVD','Vasco', null);

insert into cover(product, url_cover) values (8, 'http://www.copertinedvd.org/copertine-cd-file/V/vasco_rossi_-_dal_palco.jpg');


insert into product (title, price, storedDate, main_genre, quantity, description, type, soloist, bandName) values ('Toccate Partite',20.00, '2016/10/12','Classica', 9, 'Girolamo Frescobaldi, (Roma, 1º marzo 1643), è stato un compositore, organista e clavicembalista italiano. È ritenuto uno dei maggiori compositori per clavicembalo del XVII secolo.', 'DVD','Vasco', null);

insert into cover(product, url_cover) values (9, 'http://www.concertoclassics.it/wp-content/uploads/CNT2104_Frescobaldi_Cover-high-res.jpg');



    