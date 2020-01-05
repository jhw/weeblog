#!/usr/bin/env python

import boto3, os, re

BucketName=re.findall("AppName=(.+)", open("app.props").read())[0]

S3=boto3.client("s3")

if __name__=="__main__":
    for item in S3.list_objects(Bucket=BucketName)["Contents"]:
        if not os.path.exists("site/%s" % item["Key"]):
            print (item["Key"])
            S3.delete_object(Bucket=BucketName,
                             Key=item["Key"])
