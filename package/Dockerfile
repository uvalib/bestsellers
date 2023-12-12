FROM public.ecr.aws/docker/library/python:3.9.16-alpine3.18

# update the packages
RUN apk update && apk upgrade && apk add build-base bash tzdata mysql-dev libffi-dev && rm -fr /var/cache/apk/*

# Create the run user and group
RUN addgroup webservice && adduser webservice -G webservice -D

# set the timezone appropriatly
ENV TZ=UTC
RUN cp /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Specify home 
ENV APP_HOME /bestsellers
WORKDIR $APP_HOME

# install the application requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# install the application
ADD . $APP_HOME

# cleanup the scripts
RUN mv package/scripts $APP_HOME && rm $APP_HOME/scripts/build.ksh $APP_HOME/scripts/shell.ksh $APP_HOME/scripts/run.ksh

# Update permissions
RUN chown -R webservice $APP_HOME /home/webservice && chgrp -R webservice $APP_HOME /home/webservice

# Define port and startup script
EXPOSE 8080
CMD scripts/entry.ksh

# Move in other assets
COPY data/container_bash_profile /home/webservice/.profile

# Ensure permissions are correct
RUN chown webservice:webservice /home/webservice/.profile $APP_HOME/scripts/entry.ksh && chmod 755 /home/webservice/.profile $APP_HOME/scripts/entry.ksh

# Add the build tag
ARG BUILD_TAG
RUN test -n "$BUILD_TAG" && touch $APP_HOME/buildtag.build-$BUILD_TAG || touch $APP_HOME/buildtag.build-0

# Specify the user
USER webservice
