create table if not exists public.profiles(
  id uuid primary key references auth.users on delete cascade,
  name text not null,
  is_admin boolean not null default false
);
create or replace function public.is_admin() returns boolean
language sql stable security definer set search_path = public as
$$ select coalesce((select is_admin from public.profiles where id = auth.uid()), false) $$;

create table if not exists public.submissions(
  id bigint generated always as identity primary key,
  user_id uuid not null default auth.uid() references public.profiles(id) on delete cascade,
  task text not null,
  path text not null,
  note text,
  status text not null default 'new' check (status in ('new','ok','redo')),
  created_at timestamptz not null default now()
);
create table if not exists public.comments(
  id bigint generated always as identity primary key,
  submission_id bigint not null references public.submissions(id) on delete cascade,
  user_id uuid not null default auth.uid() references public.profiles(id) on delete cascade,
  body text not null,
  created_at timestamptz not null default now()
);

alter table public.profiles enable row level security;
alter table public.submissions enable row level security;
alter table public.comments enable row level security;

drop policy if exists p_sel on public.profiles;
create policy p_sel on public.profiles for select to authenticated using (true);

drop policy if exists s_sel on public.submissions;
drop policy if exists s_ins on public.submissions;
drop policy if exists s_upd on public.submissions;
drop policy if exists s_del on public.submissions;
create policy s_sel on public.submissions for select to authenticated using (user_id = auth.uid() or public.is_admin());
create policy s_ins on public.submissions for insert to authenticated with check (user_id = auth.uid());
create policy s_upd on public.submissions for update to authenticated using (public.is_admin());
create policy s_del on public.submissions for delete to authenticated using ((user_id = auth.uid() and status = 'new') or public.is_admin());

drop policy if exists c_sel on public.comments;
drop policy if exists c_ins on public.comments;
create policy c_sel on public.comments for select to authenticated using (
  exists (select 1 from public.submissions s where s.id = submission_id and (s.user_id = auth.uid() or public.is_admin())));
create policy c_ins on public.comments for insert to authenticated with check (
  user_id = auth.uid() and exists (select 1 from public.submissions s where s.id = submission_id and (s.user_id = auth.uid() or public.is_admin())));

grant select on public.profiles to authenticated;
grant select, insert, update, delete on public.submissions to authenticated;
grant select, insert on public.comments to authenticated;

insert into storage.buckets (id, name, public) values ('shots', 'shots', false) on conflict (id) do nothing;
drop policy if exists shots_ins on storage.objects;
drop policy if exists shots_sel on storage.objects;
drop policy if exists shots_del on storage.objects;
create policy shots_ins on storage.objects for insert to authenticated with check (
  bucket_id = 'shots' and (storage.foldername(name))[1] = auth.uid()::text);
create policy shots_sel on storage.objects for select to authenticated using (
  bucket_id = 'shots' and ((storage.foldername(name))[1] = auth.uid()::text or public.is_admin()));
create policy shots_del on storage.objects for delete to authenticated using (
  bucket_id = 'shots' and ((storage.foldername(name))[1] = auth.uid()::text or public.is_admin()));
