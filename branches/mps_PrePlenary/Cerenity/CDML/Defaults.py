#!/usr/bin/python

import os
import cgi
from Cookie import SimpleCookie
from config import config

defaults = {
   "pagename": "FrontPage",
   "defaultpage" : "index",
   "mode" : "view",
   "missingpage" : "NewPageTemplate",
   "debuggable": 1,
   "alwaysdebug": 0,
   "content" : "",
   "template" : "<html><body>[[content]]</body>",
   "form" : cgi.FieldStorage(),
   "finalpage" : False,
   "user" : "guest",
   "username" : "",
   "userid" : "",
   "newcookies" : {},
   "headers" : {},
   "remember_preferences" : "on",
   "newuser" : False,
   "userstatefile" : "userstatefile.db",
   "user_email" : "",
   "handled_validation" : False,
   "validate_email" : "on",
   "name_validation" : "(not validated)",
   "email_validation" : "(not validated)",
   "systemnote" : "",
   "admin": "Michael",
   "logbase": "/tmp",

   "host":            "127.0.0.1",
   "fullurl" : "http://127.0.0.1/",
   "cgipath":                  "/cgi-bin/Wiki/wiki/",
   "cgipostpath" : "/cgi-bin/Workshop/wiki/",
   "root" :     "http://%(host)s%(cgipath)s",
   "postroot" : "http://%(host)s%(cgipostpath)s",
   "docbase": "Content",

}

#   "docbase": "/media/usbdisk/SF/cgi-bin/Workshop/Content",
context = {}
context.update(defaults)

# context["docbase"] = "/tmp/persistent/owiki/hotdocs"
# context["userstatefile"] = "/tmp/persistent/owiki/userstatefile.db"
# context["host"] = "owiki.sourceforge.net"

#context["host"] = "10.92.15.191"
#
#context["cgipath"] = "/cgi-bin/Workshop/wiki/"
#context["cgipath"] = "/"
#context["cgipostpath"] = "/cgi-bin/Workshop/wiki/"

context.update(config)

context["root"] = context["root"] % context
context["postroot"] = context["postroot"] % context
