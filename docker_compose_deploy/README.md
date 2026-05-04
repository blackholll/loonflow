# docker compose deploy

## for local build testing
docker build -f docker_compose_deploy/loonflow-backend/Dockerfile -t blackholll/loonflow-backend:r3.2.0  .
docker build -f docker_compose_deploy/loonflow-ui/Dockerfile -t blackholll/loonflow-ui:r3.2.0  .