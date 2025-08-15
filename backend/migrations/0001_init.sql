create table if not exists users (
  id uuid primary key default gen_random_uuid(),
  email text unique,
  created_at timestamp default now()
);

create table if not exists personas (
  id uuid primary key,
  user_id uuid not null,
  display_name text not null,
  tone text not null,
  cadence text not null,
  emoji_policy text not null,
  boundaries text,
  goals text,
  disclosure boolean default false,
  created_at timestamp default now()
);

create table if not exists feedback (
  id bigserial primary key,
  user_id uuid not null,
  draft_text text not null,
  action text not null,
  edit_distance int,
  created_at timestamp default now()
);
