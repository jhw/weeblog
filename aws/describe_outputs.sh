#!/usr/bin/env bash

. config/app.props

aws cloudformation describe-stacks --stack-name $AppName --query 'Stacks[0].Outputs' --output table
