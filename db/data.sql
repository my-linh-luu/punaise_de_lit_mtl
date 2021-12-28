create table declarations_ville (
    ID integer primary key,
    NO_DECLARATION integer,
    DATE_DECLARATION text,
    DATE_INSP_VISPRE text,
    NBR_EXTERMIN integer,
    DATE_DEBUTTRAIT text,
    DATE_FINTRAIT text,
    No_QR varchar(5),
    NOM_QR varchar(50),
    NOM_ARROND varchar(50),
    COORD_X real,
    COORD_Y real,
    LONGITUDE real,
    LATITUDE real
);

create table declarations_internes (
    id integer primary key,
    nom_quartier varchar(50),
    nom_arrondissement varchar(50),
    adresse varchar(100),
    date_visite text,
    nom_resident varchar(50),
    prenom_resident varchar(50),
    description text
);

create table declarations_supprimees (
    no_declaration integer
);

create table users (
    id integer primary key,
    utilisateur varchar(50),
    hashed_password varchar(128),
    courriel varchar(100),
    quartiers_a_surveiller varchar(100),
    salt varchar(128),
    pic_id varchar(32)
);

create table pictures (
    id varchar(32) primary key,
    data blob
);

create table session (
    id integer primary key,
    id_session varchar(32),
    utilisateur varchar(50)
);