from weeblog.generators import *

from weeblog.generators.post import build_post

import copy

Components=yaml.load("""
- head
- navbar
- about
- pinned
- links
- paginator
""", Loader=yaml.FullLoader)

Ignore=yaml.load("""
- README.md
- index.css
""", Loader=yaml.FullLoader)

DraftFilterFn=lambda x: "draft" in x and x["draft"]
PinnedFilterFn=lambda x: ("pinned" in x and x["pinned"]) and not DraftFilterFn(x)

"""
- create drafts but don't link to them
"""

LinkFilterFns={
    "prod": lambda x: not DraftFilterFn(x) and not PinnedFilterFn(x),
    "dev": lambda x: not PinnedFilterFn(x)
}
# PostFilterFn=lambda x: not DraftFilterFn(x)
PostFilterFn=lambda x: True
PostPath="/%s/%s.html"

def timeit(msg):
    def decorator(fn):
        import time, logging
        def wrapped(*args, **kwargs):
            starttime=time.time()
            resp=fn(*args, **kwargs)
            endtime=time.time()
            buildtime=1000*(endtime-starttime)
            logging.info("%s [%i]" % (msg, buildtime))
            return resp
        return wrapped
    return decorator

def generate_posts(stage, config, themes, templates, root="posts"):
    @timeit("posts initialised")
    def init_posts(stage, config, root,
                   filterfn=PostFilterFn,
                   pattern=PostPath):
        posts=[]
        for dirname in os.listdir(root):
            for filename in os.listdir("%s/%s" % (root, dirname)):
                text=open("%s/%s/%s" % (root, dirname, filename)).read()
                post=build_post(stage, text)
                if not filterfn(post):
                    continue
                post["author"]=config["head"]["author"]
                post["path"]=pattern % (dirname,
                                        filename.split(".")[0])
                posts.append(post)
        return list(reversed(sorted(posts,
                                    key=lambda x: x["date"])))
    def filter_links(posts, filterfn):
        return {"links": [{"href": post["path"],
                           "draft": "draft" in post and post["draft"],
                           "text": post["title"]}
                          for post in reversed(sorted(posts,
                                                      key=lambda x: x["date"]))
                          if filterfn(post)]}
    def init_paginators(posts):
        def init_paginator(posts, i):
            if i==0:
                return {"next": posts[i+1]["path"]}
            elif i==len(posts)-1:
                return {"prev": posts[i-1]["path"]}            
            else:
                return {"prev": posts[i-1]["path"],
                        "next": posts[i+1]["path"]}
        return [init_paginator(posts, i)
                for i in range(len(posts))] if len(posts) > 1 else []
    def append_theme(fn):
        def wrapped(stage, config, *args, **kwargs):
            components=fn(stage, config, *args, **kwargs)
            themename=config["head"]["themes"]["bootstrap"]
            for component in components.values():
                if isinstance(component, dict):
                    component["theme"]=themes["bootstrap"][themename]
            return components
        return wrapped
    @append_theme
    def init_components(stage, config, themes, posts, post,
                        pinnedfn=PinnedFilterFn,
                        linkfns=LinkFilterFns):
        components={}
        for attr in ["head", "about", "navbar"]:
            components[attr]=copy.deepcopy(config[attr])
        """
        - title should be page- specific, not site- specific
        - base code uses (site) title from site.yaml as (page) title
        - this code overwrites (site) title with (page) title
        - note that src attribute contains site src
        """
        components["head"]["site"]=components["head"].pop("title")
        for attr in ["title",
                     "description",
                     "lang",
                     "img"]:
            if attr in post:
                components["head"][attr]=post[attr]
        pinned=filter_links(posts, pinnedfn)
        if pinned["links"]:
            components["pinned"]=pinned
        links=filter_links(posts, linkfns[stage])
        if links["links"]:
            components["links"]=links
        paginators=init_paginators(posts)
        if paginators:
            components["paginators"]=paginators
        return components
    def filter_components(components, i):
        struct=copy.deepcopy(components)
        if "paginators" in struct:
            paginators=struct.pop("paginators")
            struct["paginator"]=paginators[i]
        return struct
    def init_page(config, themes, templates, components, post, i):
        layout={key: templates[key].render(values)
                for key, values in filter_components(components,
                                                     i).items()}
        layout["post"]=templates["post"].render(post)
        themename=config["head"]["themes"]["bootstrap"]
        layout["theme"]=themes["bootstrap"][themename]
        return templates["layout"].render(layout)                             
    posts=init_posts(stage, config, root)
    for i, post in enumerate(posts):
        components=init_components(stage, config, themes, posts, post)
        post["page"]=init_page(config,
                               themes,
                               templates,
                               components,
                               post,
                               i)
    return posts

def build_site(stage, config, themes, templates):
    def validate_themes(config, themes):
        bsthemename=config["head"]["themes"]["bootstrap"]
        if bsthemename not in themes["bootstrap"]:
            raise RuntimeError("Bootstrap '%s' theme not found" % bsthemename)
        jsthemename=config["head"]["themes"]["highlightjs"]
        if jsthemename not in themes["highlightjs"]["themes"]:
            raise RuntimeError("HighlightJS '%s' theme not found" % jsthemename)
    def generate_css(config,
                     themes,
                     filename="weeblog/assets/css/index.css"):
        themename=config["head"]["themes"]["bootstrap"]
        template=jinja2.Template(open(filename).read(),
                                 undefined=jinja2.StrictUndefined)
        Path(filename).dump(template.render(themes["bootstrap"][themename]))
    @timeit("assets copied")
    def copy_assets(src, ignore=Ignore):
        def copy_assets(src):
            for filename in os.listdir(src):
                newsrc="%s/%s" % (src, filename)
                if (filename in ignore or
                    newsrc in ignore):
                    pass
                elif os.path.isdir(newsrc):
                    copy_assets(newsrc)
                else:
                    Path(newsrc).copy()
        copy_assets(src)
    def generate_index(posts):
        pinned=[post for post in posts
                if "pinned" in post and post["pinned"]]
        index=pinned[0] if pinned else posts[0]
        shutil.copyfile(Path(index["path"]).filename,
                        "site/index.html")
    def generate_error(config, templates):    
        layout={attr: templates[attr].render(config[attr])
                for attr in ["head", "navbar"]}
        page=templates["error"].render(layout)
        Path("error.html").dump(page)
    validate_themes(config, themes)
    posts=generate_posts(stage, config, themes, templates)
    for post in posts:
        Path(post["path"]).dump(post["page"])
    generate_css(config, themes)
    for src in ["weeblog/assets",
                "assets"]:
        if os.path.exists(src):
            copy_assets(src)
    generate_index(posts)
    generate_error(config, templates)
    
if __name__=="__main__":
    pass
