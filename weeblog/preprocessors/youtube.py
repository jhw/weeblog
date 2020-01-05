from blog.preprocessors import *

from lxml import html

"""
https://getbootstrap.com/docs/4.0/utilities/embed/
"""

Wrapper="""
<div class="embed-responsive embed-responsive-16by9 youtube">
  <iframe class="embed-responsive-item" %s></iframe>
</div>
"""

def preprocess(text):
    def handle_empty(fn):
        def wrapped(k, v):
            if v in ['', None]:
                return k
            return fn(k, v)
        return wrapped
    @handle_empty
    def format_attr(k, v):
        return "%s=\"%s\"" % (k, v)
    def filter_youtube(fn):
        def wrapped(row):
            if not ("iframe" in row and
                    "www.youtube.com/embed" in row):
                return row
            return fn(row)
        return wrapped
    @filter_youtube
    def process(row):
        iframe=html.fromstring(row)
        attrs={k:v for k, v in iframe.attrib.items()
               if k not in ["width", "height"]}
        attrlist=[format_attr(k, v)
                  for k, v in attrs.items()]
        return Wrapper % " ".join(attrlist)
    return "\n".join([process(row)
                      for row in text.split("\n")])

if __name__=="__main__":
    pass
