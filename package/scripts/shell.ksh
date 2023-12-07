# set the definitions
INSTANCE=bestsellers
NAMESPACE=uvadave

if [ -z "$DOCKER_HOST" ]; then
   DOCKER_TOOL=docker
else
   DOCKER_TOOL=docker-legacy
fi

# mappable volumes
#DATA_MAP="-v /lib_content22/bestsellers-staging/data:/bestsellers/static/data"
#IMAGE_MAP="-v /lib_content22/bestsellers-staging/images:/bestsellers/static/images"

# environment
#ENV="-e BS_PORT=$BS_PORT -e BS_DB_HOST=$BS_DB_HOST -e BS_DB_NAME=$BS_DB_NAME -e BS_DB_USER=$BS_DB_USER -e BS_DB_PASS=$BS_DB_PASS"
#echo "ENV: $ENV"

${DOCKER_TOOL} run -p 8466:8466 $DATA_MAP $IMAGE_MAP $ENV -t -i $NAMESPACE/$INSTANCE /bin/bash -l
