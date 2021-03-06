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

# environment
ENV="-e BS_PORT=$BS_PORT -e BS_DB_HOST=$BS_DB_HOST -e BS_DB_NAME=$BS_DB_NAME -e BS_DB_USER=$BS_DB_USER -e BS_DB_PASS=$BS_DB_PASS"
echo "ENV: $ENV"

# stop the running instance
docker stop $INSTANCE

# remove the instance
docker rm $INSTANCE

# remove the previously tagged version
docker rmi $NAMESPACE/$INSTANCE:current  

# tag the latest as the current
docker tag $NAMESPACE/$INSTANCE:latest $NAMESPACE/$INSTANCE:current

# run it
docker run -d -p 8466:8466 $DATA_MAP $IMAGE_MAP $ENV --log-opt tag=$INSTANCE --name $INSTANCE $NAMESPACE/$INSTANCE:latest
