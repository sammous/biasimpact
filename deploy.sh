#!/bin/bash

ssh $USER@$IP <<EOF
  cd $DEPLOY_DIR
  git pull origin master
EOF