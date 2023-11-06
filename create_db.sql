CREATE TABLE Book (
    b_bookkey int not null,
    b_authorkey int not null,
    b_genre text[] not null,
    title varchar(255) not null
);

CREATE TABLE User (
    u_userkey int not null,
    u_username varchar(255) not null,
    u_password varchar(255) not null,
);

CREATE TABLE List (
    l_listkey int auto_increment primary key not null,
    l_name varchar(255) not null
);

CREATE TABLE ListBook (
    lb_listkey int not null,
    lb_bookkey int not null,
    lb_userkey int not null
);

CREATE TABLE Rating (
    r_ratingkey int not null,
    stars int not null,
    r_userkey int not null,
    r_bookkey int not null,
    comment varchar(1000)
);

CREATE TABLE Author (
    a_authorkey int not null,
    a_authorname varchar(255) not null
);

-- CREATE TABLE Genre (
--     g_genrekey int not null,
--     g_genrename varchar(255) not null
-- );

