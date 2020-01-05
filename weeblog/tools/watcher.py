#!/usr/bin/env python

from weeblog.tools import *

from weeblog.generators import load_yamlfile, init_templates

from weeblog.generators.site import build_site, timeit

import logging, os

Paths=["posts", "assets", "config", "templates"]

# ValueFn=lambda path: len(open(path, 'rb').read())

ValueFn=lambda path: open(path, 'rb').read()

def diff(h0, h1):
    for k0 in h0.keys():
        if (k0 not in h1 or
            h0[k0]!=h1[k0]):
            return True
    return False

class Cache(dict):

    def __init__(self):
        dict.__init__(self)

    def diff(self, cache):
        return diff(self, cache) or diff(cache, self)

def init_cache(paths=Paths,
               valuefn=ValueFn):
    def update(path, cache):
        try:
            cache[path]=ValueFn(path)
        except FileNotFoundError:
            pass
    def outerfetch(path, cache):
        if os.path.isdir(path):
            innerfetch(path, cache)
        else:
            update(path, cache)            
    def innerfetch(path, cache):
        for filename in os.listdir(path):
            newpath="%s/%s" % (path, filename)
            outerfetch(newpath, cache)
    cache=Cache()
    for path in paths:
        outerfetch(path, cache)
    return cache

def loop(stage, wait=1):
    import time
    @timeit("site built")
    def build(*args, **kwargs):
        build_site(*args, **kwargs)
    cache=None
    while True:
        newcache=init_cache()
        if (not cache or
            (cache and
             cache.diff(newcache))):
            try:
                config=load_yamlfile("config/site.yaml")
                themes={"bootstrap": load_yamlfile("config/bootstrap.yaml"),
                        "highlightjs": load_yamlfile("config/highlightjs.yaml")}
                templates=init_templates()
                build(stage, config, themes, templates)
            except Exception as error:
                logging.error(str(error))                
        cache=newcache
        time.sleep(wait)
    
if __name__=="__main__":
    try:
        import sys
        if len(sys.argv) < 2:
            raise RuntimeError("Please enter stage")
        stage=sys.argv[1]
        if not stage in ["dev", "prod"]:
            raise RuntimeError("stage is invalid")
        from weeblog.utils.logger import init_info_logger
        init_info_logger()
        os.system("rm -rf site/*")
        loop(stage)
    except RuntimeError as error:
        print ("Error: %s" % str(error))
