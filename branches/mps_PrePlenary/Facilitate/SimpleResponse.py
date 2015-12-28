#!/usr/bin/python
"""
This script handles user registrations
"""
import md5                          # for hexdigest
import random                       # for confirmation codes
import time                         # to check age
import pprint                       # for dumping errors

import CookieJar
import Cookie
from model.Record import EntitySet  # For access to the temporary DB
import Interstitials

def page_logic(json, **argd):
    if argd.get("action", "") == "submitresponse":
        response      = argd.get("response", None)
        response_type = argd.get("type", None)
        mission       = argd.get("mission", None)
        userid        = argd.get("userid", None)

        if response is None:
            return [
                      "error",
                      {
                        "message" : "You really ought to fill in a response to the form you know!",
                        "record" : "",
                        "problemfield" : "response",
                      }
                   ]
        if response_type is None:
            return [
                      "error",
                      {
                        "message" : "Response type not set, did something go wrong?",
                        "record" : "",
                        "problemfield" : "type",
                      }
                   ]

        if mission is None:
            return [
                      "error",
                      {
                        "message" : "Mission ID not set, did something go wrong?",
                        "record" : "",
                        "problemfield" : "mission",
                      }
                   ]

        if userid is None:
            return [
                      "error",
                      {
                        "message" : "User ID not set, did something go wrong?",
                        "record" : "",
                        "problemfield" : "userid",
                      }
                   ]

        rec = {
             "response": response,
             "response_type": response_type,
             "mission": mission,
             "userid": userid,
        }
        stored_rec = SimpleResponses.new_record(rec)

        return [ "responsestored",
                 { "message" : "Thanks for the response, it's been safely stored!"
                 }
               ]

    return [ 
             "__default__",  
             { "message" : "Hello World"+pprint.pformat(argd),
               "record" : {}
             }
           ]

def MakeHTML( structure ):
    if structure[0] == "__default__":
        return [], notdirect

    if structure[0] == "responsestored":
        return [], Interstitials.thankyou_template

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

SimpleResponses = EntitySet("simpleresponses", key="responseid")

if __name__ == "__main__":
     pass
