-- script auto-generated via PyCharm Professional DB SQL Generator Tools
create schema if not exists sqa;

create table sqa.resident
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

alter table sqa.resident
    owner to postgres;

grant select, update, usage on sequence sqa.resident_id_seq to anon;

grant select, update, usage on sequence sqa.resident_id_seq to authenticated;

grant select, update, usage on sequence sqa.resident_id_seq to service_role;

create trigger update_resident
    before update
    on sqa.resident
    for each row
execute procedure public.update_timestamp_function();

grant delete, insert, references, select, trigger, truncate, update on sqa.resident to anon;

grant delete, insert, references, select, trigger, truncate, update on sqa.resident to authenticated;

grant delete, insert, references, select, trigger, truncate, update on sqa.resident to service_role;

create table sqa.installment
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
        references sqa.resident,
    start_date  date
);

alter table sqa.installment
    owner to postgres;

grant select, update, usage on sequence sqa.installment_id_seq to anon;

grant select, update, usage on sequence sqa.installment_id_seq to authenticated;

grant select, update, usage on sequence sqa.installment_id_seq to service_role;

create trigger update_installment
    before update
    on sqa.installment
    for each row
execute procedure public.update_timestamp_function();

grant delete, insert, references, select, trigger, truncate, update on sqa.installment to anon;

grant delete, insert, references, select, trigger, truncate, update on sqa.installment to authenticated;

grant delete, insert, references, select, trigger, truncate, update on sqa.installment to service_role;

create table sqa.utility
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

alter table sqa.utility
    owner to postgres;

grant select, update, usage on sequence sqa.utility_id_seq to anon;

grant select, update, usage on sequence sqa.utility_id_seq to authenticated;

grant select, update, usage on sequence sqa.utility_id_seq to service_role;

create trigger update_utility
    before update
    on sqa.utility
    for each row
execute procedure public.update_timestamp_function();

grant delete, insert, references, select, trigger, truncate, update on sqa.utility to anon;

grant delete, insert, references, select, trigger, truncate, update on sqa.utility to authenticated;

grant delete, insert, references, select, trigger, truncate, update on sqa.utility to service_role;

create table sqa.statement
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

alter table sqa.statement
    owner to postgres;

grant select, update, usage on sequence sqa.statement_id_seq to anon;

grant select, update, usage on sequence sqa.statement_id_seq to authenticated;

grant select, update, usage on sequence sqa.statement_id_seq to service_role;

create trigger update_statement
    before update
    on sqa.statement
    for each row
execute procedure public.update_timestamp_function();

grant delete, insert, references, select, trigger, truncate, update on sqa.statement to anon;

grant delete, insert, references, select, trigger, truncate, update on sqa.statement to authenticated;

grant delete, insert, references, select, trigger, truncate, update on sqa.statement to service_role;

create table sqa.monthly_utility
(
    statement_id integer
        references sqa.statement,
    utility_id   integer
        references sqa.utility,
    total        numeric,
    created_at   timestamp default now(),
    updated_at   timestamp default now()
);

alter table sqa.monthly_utility
    owner to postgres;

create trigger update_monthly_utility
    before update
    on sqa.monthly_utility
    for each row
execute procedure public.update_timestamp_function();

grant delete, insert, references, select, trigger, truncate, update on sqa.monthly_utility to anon;

grant delete, insert, references, select, trigger, truncate, update on sqa.monthly_utility to authenticated;

grant delete, insert, references, select, trigger, truncate, update on sqa.monthly_utility to service_role;

create table sqa.monthly_installment
(
    statement_id   integer
        references sqa.statement,
    installment_id integer
        references sqa.installment,
    total          numeric,
    created_at     timestamp default now(),
    updated_at     timestamp default now()
);

alter table sqa.monthly_installment
    owner to postgres;

create trigger update_monthly_installment
    before update
    on sqa.monthly_installment
    for each row
execute procedure public.update_timestamp_function();

grant delete, insert, references, select, trigger, truncate, update on sqa.monthly_installment to anon;

grant delete, insert, references, select, trigger, truncate, update on sqa.monthly_installment to authenticated;

grant delete, insert, references, select, trigger, truncate, update on sqa.monthly_installment to service_role;

-- tally the final values of sequences to match from the billing schema
SELECT setval('sqa.resident_id_seq', (SELECT max(id) FROM billing.resident));
SELECT setval('sqa.statement_id_seq', (SELECT max(id) FROM billing.statement));
SELECT setval('sqa.installment_id_seq', (SELECT max(id) FROM billing.installment));
SELECT setval('sqa.utility_id_seq', (SELECT max(id) FROM billing.utility));