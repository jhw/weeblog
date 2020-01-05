#!/usr/bin/env bash

. config/app.props

aws s3 rm --recursive s3://$AppName/
aws cloudformation delete-stack --stack-name $AppName
