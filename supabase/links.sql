create table if not exists public.links(
  user_id uuid not null default auth.uid() references public.profiles(id) on delete cascade,
  task text not null,
  url text not null,
  updated_at timestamptz not null default now(),
  primary key (user_id, task)
);
alter table public.links enable row level security;
drop policy if exists l_sel on public.links;
drop policy if exists l_ins on public.links;
drop policy if exists l_upd on public.links;
create policy l_sel on public.links for select to authenticated using (user_id = auth.uid() or public.is_admin());
create policy l_ins on public.links for insert to authenticated with check (user_id = auth.uid());
create policy l_upd on public.links for update to authenticated using (user_id = auth.uid()) with check (user_id = auth.uid());
grant select, insert, update on public.links to authenticated;
notify pgrst, 'reload schema';
