from blog.preprocessors import *

def postprocess(text):
    return re.sub("\\#post\\-img\"", "\" class=\"post-img img-fluid\"", text)

if __name__=="__main__":
    pass
