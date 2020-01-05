from blog.preprocessors import *

def postprocess(text):
    return re.sub("\\#post\\-icon\"", "\" class=\"post-icon\"", text)

if __name__=="__main__":
    pass
