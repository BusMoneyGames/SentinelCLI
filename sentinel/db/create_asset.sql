
create table asset_type
(
    id int4,

    name text not null,

    created_at timestamp not null default timestamp 'now',
    updated_at timestamp,

    constraint asset_type_pk primary key (id)
);

create trigger on_update
before update on asset_type
for each row
execute procedure on_update();

--

create table asset
(
    id bigserial,

    name text not null,
    filename text not null,
    asset_type_id int4 not null,
    processing_state_id int4 not null,

    created_at timestamp not null default now(),
    updated_at timestamp,

    constraint asset_pk
        primary key (id),
    constraint asset_fk_asset_type_id
        foreign key (asset_type_id)
        references asset_type
);

create trigger on_update
before update on asset
for each row
execute procedure on_update();

create unique index asset_filename_idx ON asset(filename);

--

create table asset_hash
(
    id bigserial,

    value text not null,

    created_at timestamp not null default now(),
    updated_at timestamp,

    constraint asset_hash_pk
        primary key (id)
);

create trigger on_update
before update on asset_hash
for each row
execute procedure on_update();

--

create table asset_to_asset_hash
(
    asset_id bigint not null,
    asset_hash_id bigint not null,

    created_at timestamp not null default now(),
    updated_at timestamp,

    constraint asset_to_asset_hash_pk
        primary key (asset_id, asset_hash_id),
    constraint asset_to_asset_hash_fk_asset
        foreign key (asset_id)
        references asset,
    constraint asset_to_asset_hash_fk_asset_hash
        foreign key (asset_hash_id)
        references asset_hash
);

create trigger on_update
before update on asset_to_asset_hash
for each row
execute procedure on_update();
