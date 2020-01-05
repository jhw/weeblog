"""
- script to filter highlightjs themes
"""

import os, yaml

def filter_highlightjs(root):
    themes=[]
    for filename in sorted(os.listdir(root)):
        key=filename.split(".")[0]
        themes.append(key)
    return {"themes": sorted(themes)}

if __name__=="__main__":
    highlightjs=filter_highlightjs("assets/css/lib/highlightjs")
    with open("tmp/highlightjs.yaml", 'w') as f:
        f.write(yaml.safe_dump(highlightjs,
                               default_flow_style=False))
