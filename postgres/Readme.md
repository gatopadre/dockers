## Comandos
docker run -p 5432:5432 -v /path/to/local/data:/var/lib/postgresql/data -v /path/to/local/logs:/var/log/postgresql my-postgres

-->
docker run --network="mynetwork" --ip="172.18.0.10" --add-host postgres:172.18.0.10 -p 5432:5432 my-postgres

-->
docker run -p 5433:5432 --network red_1 my_postgres_1