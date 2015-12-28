#!/usr/bin/env python

import os.path


def get_cookie(thecookie, env):
    value = env["cookies"][thecookie].value
    return value

class tagHandler(object):
      def doShowCookie(bunch, text, env):
          "[[showcookie][cookie=<cookieid] ] Displays the value of a particular cookie, if set"
          thecookie = bunch["cookie"]
          try:
              return get_cookie(thecookie, env)
          except KeyError:
              return "cookie("+thecookie+": not set)"

      def doCookies(bunch, text, env):
         "[[cookies] ] - Displays all cookies the user supplied"
         if len(env["cookies"]) == 0:
             return "&lt;&lt;No cookies set, we need to set one!&gt;&gt;"
         result = []
         for cookie in env["cookies"]:
             value = env["cookies"][cookie].value
             result.append("Cookie - " + str(cookie) + " : " + str(value) )

         return "Cookies: <ul>" + ", ".join(result) + "</ul>"

      mapping = {
                 "showcookie" : doShowCookie,
                 "cookies" : doCookies,
      }

mapping = tagHandler.mapping

if __name__ == "__main__":
   print "TAG HANDLER", tagHandler
   print "MAPPING", tagHandler.mapping
