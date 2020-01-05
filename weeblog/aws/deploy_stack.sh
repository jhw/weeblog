#!/usr/bin/env bash

. app.props

aws cloudformation deploy --stack-name $AppName --template-file weeblog/config/stack.yaml --parameter-overrides AppName=$AppName --capabilities CAPABILITY_NAMED_IAM
