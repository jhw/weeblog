#!/usr/bin/env python

from weeblog.tools import *

from weeblog.utils import BrowserHeaders

import http.client, logging, lxml.html, os, urllib.request, urllib.parse

def crawl_site(path):
    def filter_links(doc):
        return set([str(a.attrib["href"])
                    for a in doc.xpath("//a")
                    if ("href" in a.attrib and
                        str(a.attrib["href"]) not in ["#", '', '/'])])
    def filter_images(doc):
        return set([str(img.attrib["src"])
                    for img in doc.xpath("//img")
                    if ("src" in img.attrib
                        and (str(img.attrib) not in ["#"]))])
    def filter_urls(doc):
        urls=set()
        for fn in [filter_links,
                   filter_images]:            
            urls.update(fn(doc))
        return list(urls)
    def outerfetch(path, cache):
        if os.path.isdir(path):
            innerfetch(path, cache)
        else:
            if path.endswith("html"):
                doc=lxml.html.fromstring(open(path).read())
                cache[path]=filter_urls(doc)
    def innerfetch(path, cache):
        for filename in os.listdir(path):
            newpath="%s/%s" % (path, filename)
            outerfetch(newpath, cache)
    def invert_cache(cache):
        modcache={}
        for path in cache:
            for url in cache[path]:
                modcache.setdefault(url, [])
                modcache[url].append(path)
        return modcache
    cache={}
    outerfetch(path, cache)
    return invert_cache(cache)

def http_fetch(url):
    uri=urllib.parse.urlparse(url)
    if uri.scheme=="https":
        conn=http.client.HTTPSConnection(uri.netloc)
    else:
        conn=http.client.HTTPConnection(uri.netloc)
    conn.request("GET", "%s?%s" % (uri.path, uri.query), headers=BrowserHeaders)
    return conn.getresponse()

if __name__=="__main__":
    try:
        from weeblog.utils.logger import init_info_logger
        init_info_logger()
        urls={url:refs
              for url, refs in crawl_site("site").items()
              if url.startswith("http")}
        for i, url in enumerate(sorted(urls.keys())):
            resp=http_fetch(url)
            logfn=logging.info if int(resp.status/100) in [2, 3] else logging.warning
            logfn("[%i/%i] [%i] %s" % (i+1, len(urls), resp.status, url))
    except RuntimeError as error:
        print ("Error: %s" % str(error))
