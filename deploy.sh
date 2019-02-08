#!/bin/bash
eval "$(ssh-agent -s)" # Start ssh-agent cache
chmod 600 .travis/travis_rsa # Allow read access to the private key
ssh-add .travis/travis_rsa # Add the private key to SSH

ssh $USER@$IP <<EOF
  cd $DEPLOY_DIR
  git pull origin master
EOF