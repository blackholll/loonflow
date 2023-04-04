# remove init.sql after sql executed, since sql or shell in /docker-entrypoint-initdb.d will be executed as file name's order
rm -rf /docker-entrypoint-initdb.d/create_database.sql
rm -rf /docker-entrypoint-initdb.d/loonflow2.0.0_init.sql
