
create table processing_state
(
    id int4,

    name text not null,

    created_at timestamp not null default now(),
    updated_at timestamp,

    constraint processing_state_pk primary key (id)
);

create trigger on_update
before update on processing_state
for each row
execute procedure on_update();

insert into processing_state(id, name) values(1, 'Pending');
insert into processing_state(id, name) values(2, 'Processing');
insert into processing_state(id, name) values(3, 'Done');
