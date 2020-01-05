from blog.preprocessors import *

import yaml

Emoji=yaml.load(open("blog/config/emoji.yaml").read(),
                Loader=yaml.FullLoader)

Img="<img src=\"%s/%s\" class=\"emoji\" />"

Root="/assets/img/emoji"

def preprocess(text):
    for emoji in Emoji.values():
        text=re.sub(emoji["pattern"],                            
                    Img % (Root, emoji["filename"]),
                    text)
    return text

class EmojiTest(unittest.TestCase):

    Target="before <img src=\"/assets/img/emoji/%s\" class=\"emoji\" /> after"
    
    def test_emoji(self):
        for text, img in [("before :-) after", "slightly-smiling.png"),
                          ("before :-( after", "confused.png"),
                          ("before :-| after", "neutral.png"),
                          ("before :-/ after", "thinking.png")]:
            self.assertEqual(preprocess(text), self.Target % img)
        
if __name__=="__main__":
    unittest.main()
