"""
- script to download hjs themes
"""

import lxml.html, os, time, urllib.request

HJSVersion="9.15.10"

def filter_themes():
    doc=lxml.html.fromstring(urllib.request.urlopen("https://highlightjs.org/static/demo/").read())
    return sorted(list(set([link.attrib["href"].split("/")[1].split(".")[0]
                            for link in doc.xpath("//link")
                            if ("href" in link.attrib and
                                link.attrib["href"].startswith("styles"))])))

if __name__=="__main__":
    try:
        if not os.path.exists("tmp/highlightjs"):
            os.mkdir("tmp/highlightjs")
        themenames=filter_themes()
        for themename in themenames:
            print (themename)
            url="http://cdnjs.cloudflare.com/ajax/libs/highlight.js/%s/styles/%s.min.css" % (HJSVersion, themename)
            try:
                css=urllib.request.urlopen(url).read().decode("utf8")
            except:
                print ("Error downloading %s" % themename)
            with open("tmp/highlightjs/%s.min.css" % themename, 'w') as f:
                f.write(css)
            time.sleep(0.5)
    except RuntimeError as error:
        print ("Error: %s" % (str(error)))
    
