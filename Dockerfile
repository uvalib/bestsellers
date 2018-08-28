FROM python:2.7.13-alpine

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

# Update permissions
RUN chown -R webservice $APP_HOME /home/webservice && chgrp -R webservice $APP_HOME /home/webservice

# Specify the user
USER webservice

# Define port and startup script
EXPOSE 8466
CMD scripts/entry.ksh

# Move in other assets
COPY data/container_bash_profile /home/webservice/.profile
