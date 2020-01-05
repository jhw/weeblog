"""
- script to extract colours from bootstrap/bootswatch css files so they can be inserted into index.css
"""

import os, re, yaml

ShortNavbarMargin, MediumNavbarMargin, TallNavbarMargin = 90, 110, 130

MediumNavbars=yaml.load("""
- darkly
- flatly
- materia
- pulse
- simplex
""", Loader=yaml.FullLoader)

TallNavbars=yaml.load("""
- lux
""", Loader=yaml.FullLoader)

def margin_top(key):
    if key in TallNavbars:
        return TallNavbarMargin
    elif key in MediumNavbars:
        return MediumNavbarMargin
    else:
        return ShortNavbarMargin

def hex2rgb(h):
    if len(h) > 4:
        return list(int(h[i:i+2], 16) for i in (1, 3, 5))
    else:
        return list(int(h[i]+"0", 16) for i in (1, 2, 3))

def mean(X):
    return sum(X)/len(X)
    
def filter_bootstrap(root):
    bootstrap={}
    for filename in os.listdir(root):
        key=filename.split(".")[0]
        print (key)
        text=open("%s/%s" % (root, filename)).read()
        colours={k[2:]:{"hex": h,
                        "greyness": int(mean(hex2rgb(h)))}
                 for k, h in [re.split("\\:\\s*", tok)
                              for tok in re.split("\\{|\\}|\\;", text)
                              if tok.startswith("--")]
                 if h.startswith("#")}
        bootstrap[key]={"colours": colours,
                        "margin": {"top": margin_top(key)}}
    return bootstrap

if __name__=="__main__":
    bootstrap=filter_bootstrap("assets/css/lib/bootstrap")
    with open("tmp/bootstrap.yaml", 'w') as f:
        f.write(yaml.safe_dump(bootstrap,
                               default_flow_style=False))
