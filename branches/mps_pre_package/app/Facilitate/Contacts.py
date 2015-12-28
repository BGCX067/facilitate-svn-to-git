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


def new_contacts(**argd):
    rec = {
      # --------------------------------------------------------- Required to create a new record
        'dob.day'          : argd.get("dob.day", ""),
        'dob.month'        : argd.get("dob.month", ""),
        'dob.year'         : argd.get("dob.year", ""),
        'email'            : argd.get("email", ""),
        'password'         : argd.get("password", ""),
        'passwordtwo'      : argd.get("passwordtwo", ""),
        'screenname'       : argd.get("screenname", ""),
        'side'             : argd.get("side", ""),
    }
    # --------------------------------------------------------- Sprinkle with default metadata
    rec["confirmed"] = False
    rec["confirmationcode"] = generate_confirmation_code()
    rec["personrecord"] = ""

    # -------------------------------------------- Validations... (lots of these)

    validate_record(rec) # Seperated out to a seperate function to make logic clearer

    # ---------------------------------------------------------  TRANSFORMS FOR STORAGE
    #    One way hash for security reasons before storage
    #    NOTE: This means we always check the digest, not the value
    #          This also means we can do a password reset, not a password reminder
    #
    if rec["password"] != "":
        rec["password"] = md5.md5(rec["password"]).hexdigest()

    if rec["passwordtwo"] != "":
        rec["passwordtwo"] = md5.md5(rec["passwordtwo"]).hexdigest()

    # --------------------------------------------------------- Actual storage
    stored_rec = Registrations.new_record(rec)
    return stored_rec


def page_logic(json, **argd):
    if argd.get("action", "") == "addcontact":
        contact   = argd.get("contact", None)
        contactof = argd.get("contactof", None)        
        if contact is None:
            return [
                      "error",
                      {
                        "message" : "Need to have contact to add to",
                        "record" : "",
                        "problemfield" : "contact",
                      }
                   ]

        if contactof is None:
            return [
                      "error",
                      {
                        "message" : "Need to know who to add this as a contact of...",
                        "record" : "",
                        "problemfield" : "contactof",
                      }
                   ]
        
        contacts = Contacts.read_database()
        for rec in contacts:
            if rec["contactof"] == contactof:
                break # Found the record
        else:
            rec = { "contactof" : contactof, "contacts" : [ ] }
            
        if contact not in rec["contacts"]:
            rec["contacts"].append( contact )
        else:
            return [
                      "error",
                      {
                        "message" : "You've already added this person as a contact! <a href='/BrowseParticipants'> more </a>",
                        "record" : "",
                        "problemfield" : "contactof",
                      }
                   ]


        if rec.get("contactid", None):
            stored_rec = Contacts.store_record(rec)
        else:
            stored_rec = Contacts.new_record(rec)

        return [ "contactadded",
                 { "message" : "Contact successfully added"
                 }
               ]

    return [ 
             "__default__",  
             { "message" : "Hello World"+pprint.pformat(argd),
               "record" : {}
             }
           ]

# import MailConfirmCode

def MakeHTML( structure ):

    if structure[0] == "__default__":
        return [], notdirect

    if structure[0] == "contactadded":
        return [], Interstitials.contact_added

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
Contacts      = EntitySet("contacts",      key="contactid")

if __name__ == "__main__":
     pass
