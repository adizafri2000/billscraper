-- script auto-generated via PyCharm Professional DB SQL Generator Tools
create schema if not exists billing;

create table billing.resident
(
    id          serial
        primary key,
    name        varchar(100) not null,
    mobile      varchar(12),
    joined      date         not null,
    "left"      date,
    created_at  timestamp default now(),
    updated_at  timestamp default now(),
    is_resident boolean generated always as (("left" IS NULL)) stored
);

alter table billing.resident
    owner to postgres;

grant select, update, usage on sequence billing.resident_id_seq to anon;

grant select, update, usage on sequence billing.resident_id_seq to authenticated;

grant select, update, usage on sequence billing.resident_id_seq to service_role;

create trigger update_resident
    before update
    on billing.resident
    for each row
execute procedure public.update_timestamp_function();

grant delete, insert, references, select, trigger, truncate, update on billing.resident to anon;

grant delete, insert, references, select, trigger, truncate, update on billing.resident to authenticated;

grant delete, insert, references, select, trigger, truncate, update on billing.resident to service_role;

create table billing.installment
(
    id          serial
        primary key,
    name        varchar(30) not null,
    is_active   boolean,
    total       numeric,
    period      integer,
    created_at  timestamp default now(),
    updated_at  timestamp default now(),
    resident_id integer
        references billing.resident,
    start_date  date
);

alter table billing.installment
    owner to postgres;

grant select, update, usage on sequence billing.installment_id_seq to anon;

grant select, update, usage on sequence billing.installment_id_seq to authenticated;

grant select, update, usage on sequence billing.installment_id_seq to service_role;

create trigger update_installment
    before update
    on billing.installment
    for each row
execute procedure public.update_timestamp_function();

grant delete, insert, references, select, trigger, truncate, update on billing.installment to anon;

grant delete, insert, references, select, trigger, truncate, update on billing.installment to authenticated;

grant delete, insert, references, select, trigger, truncate, update on billing.installment to service_role;

create table billing.utility
(
    id                       serial
        primary key,
    name                     varchar(30) not null,
    resident_id              integer
        references resident,
    created_at               timestamp default now(),
    updated_at               timestamp default now(),
    price                    numeric,
    is_previous_month_charge boolean     not null
);

alter table billing.utility
    owner to postgres;

grant select, update, usage on sequence billing.utility_id_seq to anon;

grant select, update, usage on sequence billing.utility_id_seq to authenticated;

grant select, update, usage on sequence billing.utility_id_seq to service_role;

create trigger update_utility
    before update
    on billing.utility
    for each row
execute procedure public.update_timestamp_function();

grant delete, insert, references, select, trigger, truncate, update on billing.utility to anon;

grant delete, insert, references, select, trigger, truncate, update on billing.utility to authenticated;

grant delete, insert, references, select, trigger, truncate, update on billing.utility to service_role;

create table billing.statement
(
    id               serial
        primary key,
    name             varchar(30) not null,
    month            date,
    total            numeric,
    active_residents integer,
    split_total      numeric,
    created_at       timestamp default now(),
    updated_at       timestamp default now()
);

alter table billing.statement
    owner to postgres;

grant select, update, usage on sequence billing.statement_id_seq to anon;

grant select, update, usage on sequence billing.statement_id_seq to authenticated;

grant select, update, usage on sequence billing.statement_id_seq to service_role;

create trigger update_statement
    before update
    on billing.statement
    for each row
execute procedure public.update_timestamp_function();

grant delete, insert, references, select, trigger, truncate, update on billing.statement to anon;

grant delete, insert, references, select, trigger, truncate, update on billing.statement to authenticated;

grant delete, insert, references, select, trigger, truncate, update on billing.statement to service_role;

create table billing.monthly_utility
(
    statement_id integer
        references billing.statement,
    utility_id   integer
        references billing.utility,
    total        numeric,
    created_at   timestamp default now(),
    updated_at   timestamp default now()
);

alter table billing.monthly_utility
    owner to postgres;

create trigger update_monthly_utility
    before update
    on billing.monthly_utility
    for each row
execute procedure public.update_timestamp_function();

grant delete, insert, references, select, trigger, truncate, update on billing.monthly_utility to anon;

grant delete, insert, references, select, trigger, truncate, update on billing.monthly_utility to authenticated;

grant delete, insert, references, select, trigger, truncate, update on billing.monthly_utility to service_role;

create table billing.monthly_installment
(
    statement_id   integer
        references billing.statement,
    installment_id integer
        references billing.installment,
    total          numeric,
    created_at     timestamp default now(),
    updated_at     timestamp default now()
);

alter table billing.monthly_installment
    owner to postgres;

create trigger update_monthly_installment
    before update
    on billing.monthly_installment
    for each row
execute procedure public.update_timestamp_function();

grant delete, insert, references, select, trigger, truncate, update on billing.monthly_installment to anon;

grant delete, insert, references, select, trigger, truncate, update on billing.monthly_installment to authenticated;

grant delete, insert, references, select, trigger, truncate, update on billing.monthly_installment to service_role;

-- tally the final values of sequences to match from the billing schema
SELECT setval('billing.resident_id_seq', (SELECT max(id) FROM billing.resident));
SELECT setval('billing.statement_id_seq', (SELECT max(id) FROM billing.statement));
SELECT setval('billing.installment_id_seq', (SELECT max(id) FROM billing.installment));
SELECT setval('billing.utility_id_seq', (SELECT max(id) FROM billing.utility));