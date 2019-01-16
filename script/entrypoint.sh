#!/usr/bin/env bash

echo 'Creating application user and db'

mongo ${APP_MONGO_DB} \
        --host ${MONGO_HOST} \
        --port ${MONGO_PORT} \
        -u ${MONGO_ROOT_USER} \
        -p ${MONGO_ROOT_PASS} \
        --authenticationDatabase admin \
        --eval "db.createUser({user: '${APP_MONGO_USER}', pwd: '${APP_MONGO_PASS}', roles:[{role:'dbOwner', db: '${APP_MONGO_DB}'}, {role:'readWrite', db:'${APP_MONGO_DB}'}]});"