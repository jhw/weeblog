from weeblog.tools import *

from weeblog.generators.post import build_post

from spellchecker import SpellChecker

import lxml.html, re

Quote="QUOTE"

def filter_terms(path):
    def init_cleaner():
        from lxml.html.clean import Cleaner
        cleaner=Cleaner()
        cleaner.javascript=False
        cleaner.style=False
        cleaner.kill_tags=["pre", "code"]
        return cleaner
    def tokenize(text):
        return [re.sub(Quote, "'", tok)
                for tok in re.split("\\W", re.sub("'", Quote, text))
                if tok!='']
    cleaner=init_cleaner()
    post=build_post("dev", open(path).read())
    doc=cleaner.clean_html(lxml.html.fromstring(post["body"]))
    return set(tokenize(str(doc.text_content())))

if __name__=="__main__":
    try:        
        import sys, os
        if len(sys.argv) < 2:
            raise RuntimeError("Please enter filename")        
        filename=sys.argv[1]
        if not os.path.exists(filename):
            raise RuntimeError("File does not exist")
        if not filename.endswith(".md"):
            raise RuntimeError("File must be an md file")
        spell=SpellChecker()
        report=sorted(list(spell.unknown(filter_terms(filename))))
        import yaml
        print (yaml.safe_dump(report,
                              default_flow_style=False))
    except RuntimeError as error:
        print ("Error: %s" % str(error))
