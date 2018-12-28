@echo off

echo login: postgres
psql -Upostgres -f create_database.sql
