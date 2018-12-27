
create table rule_violation
(
    id bigserial,

    rule_name text not null,
    rule text not null,
    reason text not null,

    created_at timestamp not null default now(),
    updated_at timestamp,

    constraint rule_violation_pk
        primary key (id)
);

create trigger on_update
before update on rule_violation
for each row
execute procedure on_update();

--

create table asset_to_rule_violation
(
    asset_id bigint not null,
    rule_violation_id bigint not null,

    created_at timestamp not null default now(),
    updated_at timestamp,

    constraint asset_to_rule_violation_pk
        primary key (asset_id, rule_violation_id),
    constraint asset_to_rule_violation_fk_asset
        foreign key (asset_id)
        references asset,
    constraint asset_to_rule_violation_fk_rule_violation
        foreign key (rule_violation_id)
        references rule_violation
);

create trigger on_update
before update on asset_to_rule_violation
for each row
execute procedure on_update();
