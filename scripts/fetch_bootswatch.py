"""
- script to download and save all boostrap stylesheets from bootswatch.com
"""

from weeblog.utils import BrowserHeaders

import http.client, lxml.html, os, time

Endpoint="bootswatch.com:443"

def http_fetch(path):
    conn=http.client.HTTPSConnection(Endpoint)
    conn.request("GET", path, headers=BrowserHeaders)
    resp=conn.getresponse()
    if resp.status==200:
        return resp.read().decode("utf-8")
    elif resp.status==400:
        raise RuntimeError(resp.read())
    else:
        raise RuntimeError("Server returned HTTP %i" % resp.status)

def filter_links(doc):
    return sorted(list(set([str(a.attrib["href"])
                            for a in doc.xpath("//a")
                            if ("href" in a.attrib and
                                a.attrib["href"].endswith("/bootstrap.min.css"))])))
    
if __name__=="__main__":
    try:
        if not os.path.exists("tmp/bootstrap"):
            os.makedirs("tmp/bootstrap")
        doc=lxml.html.fromstring(http_fetch("/"))
        for href in filter_links(doc):
            themename=href.split("/")[1]
            print (themename)
            body=http_fetch("/"+href)
            filename="tmp/bootstrap/%s.min.css" % themename
            with open(filename, "w") as f:
                f.write(body)
            time.sleep(1)
    except RuntimeError as error:
        print ("Error: %s" % str(error))

