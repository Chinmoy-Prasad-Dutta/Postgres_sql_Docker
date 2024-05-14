docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="project" \
    -v I:/2-Docker_sql_PROJECT/pgdb:/var/lib/postgresql/data \
    -p 5432:5432 \
    postgres:latest

-----------------------------------------
docker network create project-net

docker run -it \
    -e POSTGRES_USER="root" \
    -e POSTGRES_PASSWORD="root" \
    -e POSTGRES_DB="project" \
    -v I:/2-Docker_sql_PROJECT/pgdb:/var/lib/postgresql/data \
    -p 5432:5432 \
    --network=project-net \
    --name project-db \
    postgres:latest
    #image-name


docker run -it \
    -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
    -e PGADMIN_DEFAULT_PASSWORD="root" \
    -p 8080:80 \
    --network=project-net \
    --name project-pg-admin \
    dpage/pgadmin4:latest
    #image-name

-------------------------------------------
python ingest_data.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=project \
    --folder_path="I:\2-Docker_sql_PROJECT\DATA"

----------------------------------------

docker buildx build -t dfg:001 .

-------------------------------------------
https://www.howtogeek.com/devops/how-to-connect-to-localhost-within-a-docker-container/

docker run --network=host dfg:001 \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=project \
    --folder_path="DATA"


docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' project-db
