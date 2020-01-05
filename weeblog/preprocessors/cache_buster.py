from weeblog.preprocessors import *

from lxml import html

import random

Wrapper="<script src=\"%s?_bust=%i\"></script>"

def preprocess(text):
    def filter_local(fn):
        def wrapped(row):
            if not ("script" in row and
                    "/assets/js/posts" in row):
                return row
            return fn(row)
        return wrapped
    @filter_local
    def process(row):
        doc=html.fromstring(row)
        script=doc.xpath("//script").pop()
        src=script.attrib["src"]
        bust=int(1e8*random.random())
        return Wrapper % (src, bust)
    return "\n".join([process(row)
                      for row in text.split("\n")])

if __name__=="__main__":
    pass
