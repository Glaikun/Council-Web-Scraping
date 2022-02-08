import re


def regex_search(search, txt):

    return re.findall(r'%s' % search, txt)
