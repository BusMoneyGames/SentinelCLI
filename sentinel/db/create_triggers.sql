create or replace function on_update()
returns trigger as
$$
begin
  new.updated_at = NOW();
  return new;
end;
$$
language plpgsql;
