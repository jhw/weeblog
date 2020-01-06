from weeblog.generators import *

from weeblog.preprocessors.backtick import preprocess as pp_backtick
from weeblog.preprocessors.cache_buster import preprocess as pp_cache_buster
from weeblog.preprocessors.emoji import preprocess as pp_emoji
from weeblog.preprocessors.twitter import preprocess as pp_twitter
from weeblog.preprocessors.youtube import preprocess as pp_youtube

from weeblog.postprocessors.post_icon import postprocess as pp_post_icon
from weeblog.postprocessors.post_img import postprocess as pp_post_img

from weeblog.utils.dateutils import pretty_format_date

import datetime, markdown, re

MetaConfig=yaml.load("""
- name: title
  type: str
- name: date
  type: date
- name: src
  type: link
  required: false
- name: pinned
  type: boolean
  required: false
- name: draft
  type: boolean
  required: false
""", Loader=yaml.FullLoader)

PreProcessors={
    "dev": [pp_backtick,
            pp_cache_buster,
            pp_emoji,
            pp_twitter,
            pp_youtube],
    "prod": [pp_backtick,
             pp_emoji,
             pp_twitter,
             pp_youtube]
}

Extensions=yaml.load("""
- meta
- fenced_code
- tables
""", Loader=yaml.FullLoader)

PostProcessors=[pp_post_icon,
                pp_post_img]
                
def parse_meta(meta, config=MetaConfig):
    def is_str(text):
        return True
    def is_boolean(text):
        return text.lower() in ["true", "false"]
    def is_date(text):
        return re.search("^\\d{4}\\-\\d{1,2}\\-\\d{1,2}$", text)!=None
    def is_link(text):
        return re.search("^https?\\:\\/\\/", text)!=None
    def is_list(text):
        return True
    def parse_str(text):
        return text
    def parse_boolean(text):
        return eval(text.lower().capitalize())
    def parse_date(text):
        return datetime.datetime.strptime(text, "%Y-%m-%d").date()
    def parse_link(text):
        return text
    def parse_list(text):
        return [tok
                for tok in re.split("\\s|\\,", text)
                if tok!='']        
    struct, errors = {}, []
    for item in config:
        if item["name"] not in meta:
            if not ("required" in item
                    and not item["required"]):
                errors.append(":%s not found" % item["name"])
        else:
            fn=eval("is_%s" % item["type"])
            value=meta[item["name"]].pop()
            if not fn(value):
                errors.append(":%s must be a %s" % (item["name"],
                                                    item["type"]))
            else:
                fn=eval("parse_%s" % item["type"])
                struct[item["name"]]=fn(value)
    return struct, errors

def build_post(stage, _post,
               preprocessors=PreProcessors,
               postprocessors=PostProcessors):
    def process(text, processors):
        for processor in processors:
            text=processor(text)
        return text
    def preprocess(text):
        return process(text, preprocessors[stage])
    def postprocess(text):
        return process(text, postprocessors)
    md=markdown.Markdown(extensions=Extensions)
    body=postprocess(md.convert(preprocess(_post)))
    post, errors = parse_meta(md.Meta)
    if errors!=[]:
        raise RuntimeError("; ".join(errors))
    post.update({"body": body,
                 "formatted_date": pretty_format_date(post["date"])})
    return post
        
if __name__=="__main__":
    pass

