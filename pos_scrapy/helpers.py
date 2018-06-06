# -*- coding: utf-8 -*-

import re
import urlparse
import os
import datetime

whites_re = re.compile("[ \t\n\r]+", re.I | re.U | re.M)
jscript_re = re.compile(r"<script.*?</script>", re.I | re.U | re.M | re.S)
comment_re = re.compile(r"<!--.*?-->", re.I | re.U | re.M | re.S)
nondigits_re = re.compile("[^0-9]+", re.M | re.U)
nonsymbs_re = re.compile(r"[^\w|_\-,./?\\ \t\n\r!@#\$%\^\&\*\(\)\[\]\"\':;]+", re.M | re.U)


def eclipsed(s, l=50):
    try:
        if len(s) > l:
            return u"%s…%s" % (s[:int(l // 2)], s[-int(l // 2):])
        else:
            return s
    except:
        return u""


def int0(s, fb=0):
    try:
        return int(s)
    except:
        return fb


def float0(s, fb=0.0):
    try:
        return float(s)
    except:
        return fb


def ex0(xdoc, fb=None):
    if xdoc and len(xdoc) > 0:
        return xdoc[0].extract()
    else:
        return fb


def exN(xdoc, fb=None):
    if xdoc and len(xdoc) > 0:
        r = []
        for x in xdoc:
            r.append(x.extract())
        return r
    else:
        return fb


def complement_url(parent_url, url):
    # "https://docs.python.org/2/library/urlparse.html?q=0#2"
    # ['https', 'docs.python.org', '/2/library/urlparse.html', '', 'q=0', '2']
    url0p = list(urlparse.urlparse(parent_url))
    urlp = list(urlparse.urlparse(url))

    # copy scheme and hostname from the parent url if omitted
    if urlp[0] is None or urlp[0] == "":
        urlp[0] = url0p[0]
    if urlp[1] is None or urlp[1] == "":
        urlp[1] = url0p[1]
    if urlp[2] is None or not urlp[2].startswith("/"):
        urlp[2] = os.path.join(os.path.dirname(url0p[2]), urlp[2])

    return urlparse.urlunparse(urlp)


def unwhite(s):
    if s is None:
        return None

    s = whites_re.sub(" ", s)
    return s.strip()


def safe_date_parser(s, f, fb=datetime.datetime.now()):
    try:
        dt = datetime.datetime.strptime(s, f)
        return dt
    except:
        return fb


def godeep(d={}, keys=[], fb=None):
    if d is None:
        return fb

    dd = d

    try:
        for k in keys:
            if isinstance(dd, (list, tuple)):
                kk = int0(k)
                if len(dd) > kk:
                    dd = dd[kk]
                else:
                    return fb
            elif k in dd:
                dd = dd[k]
            else:
                return fb
    except:
        return fb

    return dd


USER_AGENTS = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.8.9 "
               "(KHTML, like Gecko) Version/7.1.8 Safari/537.85.17",

               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:40.0) Gecko/20100101 Firefox/40.0",

               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/600.8.9 "
               "(KHTML, like Gecko) Version/8.0.8 Safari/600.8.9",

               "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36",

               "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36",

               "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36",

               "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36",

               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36",

               "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/44.0.2403.125 Safari/537.36",

               "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/536.5 "
               "(KHTML, like Gecko) YaBrowser/1.0.1084.5402 Chrome/19.0.1084.5409 Safari/536.5",

               "Mozilla/5.0 (Windows NT 6.1; rv:40.0) Gecko/20100101 Firefox/40.0",
               "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0",

               "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
               "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",

               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
               "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",

               "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.15 "
               "(KHTML, like Gecko) Chrome/24.0.1295.0 Safari/537.15",

               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",

               "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36",

               "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36",

               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/31.0.1623.0 Safari/537.36",

               "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/34.0.1847.116 Safari/537.36",

               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36",

               "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 "
               "(KHTML, like Gecko) Chrome/40.0.2214.38 Safari/537.36",

               "Opera/9.80 (Windows NT 6.1; WOW64) Presto/2.12.388 Version/12.17", ]
