#!/usr/bin/python
"""
This script handles user registrations
"""
import md5                          # for hexdigest
import random                       # for confirmation codes
import time                         # to check age
import pprint                       # for dumping errors

import Interstitials
import CookieJar
import Cookie
from model.Record import EntitySet  # For access to the temporary DB

def page_logic(json, **argd):
    try:
        email = argd["email"]
        password = argd["password"]
    except KeyError:
        return [ 
                 "error",  
                 { "message" : "Need both email & password as parameters",
                   "record" : {},
                   "problemfield" : "",
                 }
               ]

    R = Registrations.read_database()
    for r in R:
       if r["email"] == email:
           break
    else:
        return [
                 "error",
                 { "message": "Sorry, could not log you in - please check your email & password",
                   "record" : {},
                   "problemfield" : "",
                 }
               ]
    if r["password"] != md5.md5(argd["password"]).hexdigest():
        return [
                 "error",
                 { "message": "Sorry, could not log you in - please check your email & password.",
                   "record" : {},
                   "problemfield" : "",
                 }
               ]

    if r["confirmed"]:
       cookie = CookieJar.getCookie(r["regid"])
       return [
                "loggedin",
                {
                   "message": "Login successful",
                   "user" : r["screenname"],
                   "sessioncookie" : cookie,
                }
              ]
    else:
        return [
                 "error",
                 { "message": "Sorry, you need to confirm your identity before you can login!",
                   "record" : {},
                   "problemfield" : "",
                 }
               ]

def MakeHTML( structure ):

    if structure[0] == "loggedin":

        sessioncookie = structure[1]["sessioncookie"]
        expirytime = time.gmtime(time.time()+31000000) # approx 1 year
        formatteddate = time.strftime("%a, %d-%b-%Y %H:%M:%S %Z", expirytime)

        headers = [("Set-Cookie", "sessioncookie=%s; path=/; expires=%s"  % ( sessioncookie, formatteddate))]

        return headers, Interstitials.loggedin_template

    if structure[0] == "error":
        structure[1]["record"] = pprint.pformat( structure[1]["record"] )
        page = Interstitials.error % structure[1]
        headers = []        
        if structure[1].get("setcookies", False):
            cookies = structure[1]["setcookies"]
            for cookie in cookies:
                headers.append( ("Set-Cookie", "%s=%s" % ( cookie, cookies[cookie]) ) )

        return headers, page

    return [], Interstitials.failback % { "body" : pprint.pformat(structure) }
    

def page_render_html(json, **argd):
    extra_headers, page = MakeHTML( page_logic(json, **argd) )
    status = "200 OK"
    headers = [('Content-type', "text/html")]
    return status, headers+extra_headers, page

Registrations = EntitySet("registrations", key="regid")

if __name__ == "__main__":

    print "Enter password for ms@cerenity.org"
    password = raw_input(">> ") # To avoid putting even a test password in the repository... :)

    loginbundle = {
                  'email' : 'ms@cerenity.org',
                  'password': password,
                  'submit': '+Login+',
               }
    result = page_logic(None, **loginbundle)
    print result
    result = page_render_html(None, **loginbundle)
    print result
