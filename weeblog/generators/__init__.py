from weeblog import *

import jinja2, os, shutil, yaml

TemplatesRoot="templates"

def load_yamlfile(filename):
    return yaml.load(open(filename).read(),
                     Loader=yaml.FullLoader)

def init_templates(root=TemplatesRoot):
    def template(filename):
        return jinja2.Template(open("%s/%s" % (root, filename)).read(),
                               undefined=jinja2.StrictUndefined)
    return {filename.split(".")[0]:template(filename)
            for filename in os.listdir(root)}

def makedirs(fn):
    def wrapped(self, *args, **kwargs):
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)
        return fn(self, *args, **kwargs)
    return wrapped
    
class Path(list):

    def __init__(self, path):
        list.__init__(self,
                      ["site"]+[tok for tok in path.split("/")
                                if tok!=''])

    @property
    def dirname(self):
        return "/".join([tok for tok in self[:-1]
                         if tok not in ['blog']])

    @property
    def filename(self):
        return "/".join([tok for tok in self
                         if tok not in ['blog']])

    @property
    def srcfilename(self):
        return "/".join(self[1:])
    
    @makedirs
    def dump(self, text):
        with open(self.filename, 'w') as f:
            f.write(text)

    @makedirs
    def copy(self):
        shutil.copyfile(self.srcfilename, self.filename)

