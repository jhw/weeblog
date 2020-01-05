from blog.utils import *

def pretty_format_date(date):    
    def suffix(day):
        if 4 <= day <= 20 or 24 <= day <= 30:
            return "th"
        else:
            return ["st", "nd", "rd"][day % 10 - 1]
    return "%i%s %s" % (date.day,
                        suffix(date.day),
                        date.strftime("%b %Y"))
