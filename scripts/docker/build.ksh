if [ -z "$DOCKER_HOST" ]; then
   echo "ERROR: no DOCKER_HOST defined"
   exit 1
fi

# set the definitions
INSTANCE=bestsellers
NAMESPACE=uvadave

echo "*****************************************"
echo "building on $DOCKER_HOST"
echo "*****************************************"

docker build -f package/Dockerfile -t $NAMESPACE/$INSTANCE .
