create table
  public.cart (
    cart_id bigint generated by default as identity,
    customer text not null,
    constraint cart_pkey primary key (cart_id),
    constraint cart_customer_key unique (customer)
  ) tablespace pg_default;

create table
  public.catalog (
    id bigint generated by default as identity,
    sku text not null,
    name text null,
    price integer not null default 50,
    potion_type integer[] null,
    priority integer null,
    constraint catalog_pkey primary key (id),
    constraint catalog_potion_type_key unique (potion_type),
    constraint catalog_priority_key unique (priority)
  ) tablespace pg_default;

create table
  public.cart_items (
    id bigint generated by default as identity,
    cart_id bigint not null,
    catalog_id bigint null,
    quantity integer null,
    constraint cart_items_pkey primary key (id),
    constraint cart_items_cart_id_fkey foreign key (cart_id) references cart (cart_id),
    constraint cart_items_catalog_id_fkey foreign key (catalog_id) references catalog (id)
  ) tablespace pg_default;


create table
  public.gold_transactions (
    id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    description text null,
    constraint gold_transactions_pkey primary key (id)
  ) tablespace pg_default;

  create table
  public.gold_ledger_entries (
    id bigint generated by default as identity,
    gold_transactions_id bigint null,
    change integer not null,
    constraint gold_ledger_entries_pkey primary key (id),
    constraint gold_ledger_entries_gold_transactions_id_fkey foreign key (gold_transactions_id) references gold_transactions (id)
  ) tablespace pg_default;

create table
  public.ml_transactions (
    id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    description text null,
    constraint ml_transactions_pkey primary key (id)
  ) tablespace pg_default;

create table
  public.ml_ledger_entries (
    id bigint generated by default as identity,
    ml_transactions_id bigint null,
    red_ml integer not null default 0,
    green_ml integer not null default 0,
    blue_ml integer not null default 0,
    dark_ml integer not null default 0,
    constraint ml_ledger_entries_pkey primary key (id),
    constraint ml_ledger_entries_ml_transactions_id_fkey foreign key (ml_transactions_id) references ml_transactions (id)
  ) tablespace pg_default;

create table
  public.potion_transactions (
    id bigint generated by default as identity,
    created_at timestamp with time zone not null default now(),
    description text null,
    constraint potion_transactions_pkey primary key (id)
  ) tablespace pg_default;


create table
  public.potion_ledger_entries (
    id bigint generated by default as identity,
    potion_id bigint not null,
    potion_transactions_id bigint null,
    inventory integer not null,
    constraint potion_ledger_entries_pkey primary key (id),
    constraint potion_ledger_entries_potion_id_fkey foreign key (potion_id) references catalog (id),
    constraint potion_ledger_entries_potion_transactions_id_fkey foreign key (potion_transactions_id) references potion_transactions (id)
  ) tablespace pg_default;

