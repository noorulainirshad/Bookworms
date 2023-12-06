CREATE TABLE Book (
    b_bookkey integer not null,
    b_authorkey integer not null,
    b_genre text[] not null,
    title varchar(255) not null
);

CREATE TABLE User (
    u_userkey integer primary key not null,
    u_username varchar(255) not null,
    u_password varchar(255) not null
);

CREATE TABLE List (
    l_listkey integer primary key not null,
    l_name varchar(255) not null,
    l_userkey integer not null
);

CREATE TABLE ListBook (
    lb_listkey integer not null,
    lb_bookkey integer not null,
    lb_userkey integer not null
);

CREATE TABLE Rating (
    r_ratingkey integer primary key not null,
    stars integer not null,
    r_userkey integer not null,
    r_bookkey integer not null,
    comment varchar(1000)
);

CREATE TABLE Author (
    a_authorkey integer not null,
    a_authorname varchar(255) not null
);

CREATE TRIGGER delete_user_info
BEFORE DELETE ON User
BEGIN
    DELETE FROM ListBook WHERE lb_userkey = OLD.lb_userkey;
    DELETE FROM Rating WHERE r_userkey = OLD.r_userkey;
    DELETE FROM List WHERE l_userkey = OLD.l_userkey;
END;

-- CREATE TABLE Genre (
--     g_genrekey int not null,
--     g_genrename varchar(255) not null
-- );

