#!/usr/bin/env bash

export AWS_DEFAULT_OUTPUT=table
export AWS_PROFILE=default
export PYTHONPATH=.

if [ ! -L demo/weeblog ]; then    
    echo "creating demo/weeblog symlink"
    cd demo; ln -s ../weeblog weeblog
fi


