#!/bin/bash
eval "$(ssh-agent -s)" # Start ssh-agent cache
chmod 600 $TRAVIS_BUILD_DIR/.travis/travis_rsa # Allow read access to the private key
ssh-add $TRAVIS_BUILD_DIR/.travis/travis_rsa # Add the private key to SSH

ssh -o "StrictHostKeyChecking no" $USER@$IP 'cd $DEPLOY_DIR && git pull origin master'