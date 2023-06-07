create table personal_info
(
    id                      bigint auto_increment                          not null,
    idCard                  varchar(255)                                   not null,
    username                varchar(255)                                   not null,
    gender                  varchar(20)                                    not null,
    phone                   varchar(20)                                    not null,
    address                 varchar(255)                                   not null,
    email                   varchar(255)                                   not null,
    community_name          varchar(255)                                   not null,
    building_number         varchar(255)                                   not null,
    unit_number             varchar(255)                                   not null,
    door_number             varchar(255)                                   not null,
    parking_number          varchar(255)                                   not null,
    security_card_number    varchar(255)                                   not null,
    emergency_contact       varchar(255)                                   not null,
    emergency_contact_phone varchar(20)                                    not null,
    avatar_path             varchar(255) default '../../assets/images/userpic.jpg' null,
    faceInfo_path           varchar(255) default '../../assets/images/userpic.jpg' null,
    password                varchar(255)                                   not null comment '登录密码',
    createTime              timestamp                                      null,
    primary key (id, idCard)

);
create index idx_username
    on personal_info (idCard);

create table users_outline
(
    id          bigint       not null
        auto_increment,
    username    varchar(255) not null,
    gender      varchar(20)  not null,
    idCard      varchar(255) not null,
    email       varchar(255) not null,
    address     varchar(255) not null,
    createTime  timestamp    not null,
    status      int          not null,
    avatar_path varchar(255) not null,
    primary key (id, idCard),
    constraint FK_username
        foreign key (id) references personal_info (id)
);


create table security_announcements
(
    id        bigint       not null
        auto_increment,
    title     varchar(255) not null,
    date      date         not null,
    author    varchar(255) not null,
    author_id bigint       not null,
    status    varchar(10)  not null,
    content   text         not null,
    primary key (id),
    constraint FK_author
        foreign key (author_id) references personal_info (id)
);

create index idx_author
    on security_announcements (author_id);

