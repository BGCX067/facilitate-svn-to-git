#!/usr/bin/python

import os

from Lexer import parser
import CDML
import sys

def handleCDML(context, content):
    #
    # FIXME: the following (stub) handlers can become real
    # CDML handlers now. This requires passing in the context
    # obviously, but that's a relative detail.
    # 
    # Actually, the above is bunkum - content actually needs to
    # be evaluated in a *seperate* context - in much the same way
    # includes are. This can't happen right now because includes
    # work by luck, not by design. (It looked wierd as to why
    # it wasn't working, and then it became clear why it was
    # failing - it's a seperate thing altogether really, and
    # that's why it fails.
    #
    # Kinda wierd actually, I hadn't expected this conceptual split.
    # Have to think how this changes and improves things, and how to
    # make things back integrateable, and cleaner :)
    #
    content = content.replace("[[pagename]]", context.get("pagename", "()") )
    content = content.replace("[[userpagename]]", context.get("userpagename", "()") )

    # FIXME: THIS CAN BE SIMPLIFIED
    if context["mode"] != "edit":
        content = content.replace("[[content]]", context.get("content", "bingle"))
    else:
        content = content.replace("[[content]]", str(context["meta"]))

    content = content.replace("[[baseurl]]", context.get("fullurl", ""))
    content = content.replace("[[scripturl]]", context.get("root", ""))
    content = content.replace("[[scriptposturl]]", context.get("postroot", ""))

    # FIXME: THIS CAN BE SIMPLIFIED
    if context.get("page_is_defaultpage",False):
        content = content.replace("[[isdefault]]", "1")
        content = content.replace("[[userdefaultname]]",
             context.get("what_did_user_call_defaultpage",
                                         context["defaultpage"]))
    else:
        content = content.replace("[[isdefault]]", "0")
        content = content.replace("[[userdefaultname]]","n/a")

    try:
        username_from_cookie = context["cookies"]["name"].value
    except KeyError:
        username_from_cookie = "guest"

#    if "uest" not in username_from_cookie:
    if 1:
        content = content.replace("[[OKUSER]]", username_from_cookie)
#    else:
#        if context["mode"] == "edit":
#            return "sorry, editting not enabled for anonymous users at this time."

    referer = ""
    if os.environ.get("HTTP_REFERER","") != "":
       referer = '<a href="' +  os.environ.get("HTTP_REFERER","") + '"> back </a>'
    content = content.replace("[[referer]]", referer)
    meta = ""
    try:
        if 0 and context["meta"]:
            rowstart = "<tr><td><b>"
            divider = "</b>:</td><td>"
            rowend = "</td></tr>"
            result = ["<table>"]
            for key in [ x for x in context["meta"] if x != "__BODY__"]:
                result.append(rowstart)
                result.append(key)
                result.append(divider)
                result.append(context["meta"][key])
                result.append(rowend)
            result.append("</table>")
            raise repr(result[4])
            meta = "".join(result)
            if meta != "<table></table>":
                meta = "<hr>\n<b>Page metadata:</b>\n<ul>\n" + meta + "\n</ul>\n"

    except KeyError:
        pass
    content = content.replace("[[metadata]]", meta)

    if context["mode"] not in [ "view", "save" ]:
        return content

    context["context"] = context
    X = CDML.CDML(context) ### FIXME: also need to pass in the /context/ - handlers then have access to meta/etc
                               ### DON'T pass in a subset - more hassle than its worth

    tree = parser(content)
    content = "".join([x for x in X.evalTree(tree)])

    return content
