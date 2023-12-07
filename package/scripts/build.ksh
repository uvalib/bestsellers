# set the definitions
INSTANCE=bestsellers
NAMESPACE=uvadave

if [ -z "$DOCKER_HOST" ]; then
   DOCKER_TOOL=docker
else
   DOCKER_TOOL=docker-legacy
fi

echo "*****************************************"
echo "building on $DOCKER_HOST"
echo "*****************************************"

${DOCKER_TOOL} build -f package/Dockerfile -t $NAMESPACE/$INSTANCE .
