@echo off

echo login: postgres
psql -Upostgres -f destroy_database.sql
