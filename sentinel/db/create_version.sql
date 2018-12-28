create table version
(
    major int4 not null,
    minor int4 not null,
    patch int4 not null,

    created_at timestamp not null default timestamp 'now',
    updated_at timestamp
);

insert into version values(2, 0, 0);

create trigger on_update
before update on version
for each row
execute procedure on_update();
