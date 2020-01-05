from blog.preprocessors import *

Badge="<span class=\"badge badge-%s\">%%s</span>"

BadgeClass="warning"

Delimiter="`"

def preprocess(text,
               delimiter=Delimiter,
               klass=BadgeClass):
    def is_single_quote(text, match):
        i, j = match.span()
        lhs, rhs = True, True
        if i > 0:
            lhs&=text[i-1]!=delimiter
        if i < len(text)-1:
            rhs&=text[i+1]!=delimiter
        return lhs and rhs
    def filter_breakpoints(text):
        return [match.span()[0]
                for match in re.finditer(re.compile(delimiter), text)
                if is_single_quote(text, match)]
    def tokenize(text, breakpoints,
                 patterns=[Badge % klass, "%s"]):
        tokens=[]
        for k in range(1, len(breakpoints)):
            i, j = 1+breakpoints[k-1], breakpoints[k]
            token=patterns[k%2] % text[i:j]
            tokens.append(token)
        return tokens
    text="%s%s%s" % (delimiter, text, delimiter)
    breakpoints=filter_breakpoints(text)
    tokens=tokenize(text, breakpoints)
    return "".join(tokens)

class BacktickTest(unittest.TestCase):

    def test_emoji(self):
        for text, target in [("before `hello` after",
                              "before <span class=\"badge badge-warning\">hello</span> after"),
                             ("before ```hello``` after",
                              "before ```hello``` after")]:
            self.assertEqual(preprocess(text), target)
    
if __name__=="__main__":
    unittest.main()

