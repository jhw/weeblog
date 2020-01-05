from weeblog.preprocessors import *

OpenBlockQuote="<blockquote class=\"twitter-tweet\">"

ModOpenBlockQuote="<blockquote class=\"twitter-tweet tw-align-center\">"

CloseBlockQuote="</blockquote>"

Wrapper="<div class=\"twitter\">%s</div>"

def preprocess(text):
    def filter_twitter(fn):
        def wrapped(row):
            if not (OpenBlockQuote in row and
                    CloseBlockQuote in row):
                return row
            return fn(row)
        return wrapped
    @filter_twitter
    def process(row):
        return Wrapper % row.replace(OpenBlockQuote, ModOpenBlockQuote)
    return "\n".join([process(row)
                      for row in text.split("\n")])

if __name__=="__main__":
    pass
