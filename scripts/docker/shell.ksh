if [ -z "$DOCKER_HOST" ]; then
   echo "ERROR: no DOCKER_HOST defined"
   exit 1
fi

# set the definitions
INSTANCE=bestsellers
NAMESPACE=uvadave

# mappable volumes
DATA_MAP="-v /lib_content22/bestsellers-staging/data:/bestsellers/static/data"
IMAGE_MAP="-v /lib_content22/bestsellers-staging/images:/bestsellers/static/images"

# DB environment
DB_ENV="-e BS_DB_HOST=$BS_DB_HOST -e BS_DB_NAME=$BS_DB_NAME -e BS_DB_USER=$BS_DB_USER -e BS_DB_PASS=$BS_DB_PASS"
echo "DB ENV: $DB_ENV"

docker run -p 8466:8466 $DATA_MAP $IMAGE_MAP $DB_ENV -t -i $NAMESPACE/$INSTANCE /bin/bash -l
