create or replace function public.overview()
returns table(user_id uuid, task text, status text, created_at timestamptz, id bigint)
language sql stable security definer set search_path = public as
$$ select user_id, task, status, created_at, id from public.submissions where auth.uid() is not null order by created_at, id $$;
revoke all on function public.overview() from public, anon;
grant execute on function public.overview() to authenticated;
