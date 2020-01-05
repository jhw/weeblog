#!/usr/bin/env python

import boto3, botocore, mimetypes, os, re

BucketName=re.findall("AppName=(.+)", open("app.props").read())[0]

S3=boto3.client("s3")

def guess_content_type(filename):
    if filename.endswith(".wasm"):
        return "application/wasm"
    else:
        contenttype=mimetypes.guess_type(filename)[0]
        if not contenttype:
            contenttype="application/octet-stream"
        return contenttype

def iterpush(root):
    def localsize(filename):
        return os.stat(abspath).st_size
    def remotesize(key):
        try:
            head=S3.head_object(Bucket=BucketName,
                                Key=key)
            return head["ContentLength"]
        except botocore.exceptions.ClientError:
            return None
    for path in os.listdir(root):
        abspath="%s/%s" % (root, path)
        if os.path.isdir(abspath):
            iterpush(abspath)
        else:
            key="/".join(abspath.split("/")[1:])
            localsz=localsize(abspath)
            remotesz=remotesize(key)
            if (localsz==remotesz and
                not key.endswith(".html")):
                continue
            contenttype=guess_content_type(abspath)
            print ("%s [%s]" % (key, contenttype))
            S3.put_object(Body=open(abspath, 'rb').read(),
                          Bucket=BucketName,
                          Key=key,
                          ContentType=contenttype)
            
if __name__=="__main__":
    iterpush("site")
