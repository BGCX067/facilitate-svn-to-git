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

hostdomain = "bicker"

def generate_confirmation_code():
    return md5.md5(str(random.randint(100000000000,1000000000000))).hexdigest()

def validate_record(rec):
    # Minimally validate email. (must not be null & check for "@")
    # email must not be null
    if rec["email"] == "":
        raise ValueError(rec, "email",
                         "%s must not be blank! (got: %s)" % ("email",repr(rec["email"]))
                        )

    # passwords typed must equal passwordtwo and not be ""
    if "@" not in rec["email"]:
        raise ValueError(rec, "email",
                         "Email looks wrong - doesn't contain a '@' symbol. (got: %s)" % repr(rec["email"]) )

    # Screenname must not be null
    if rec["screenname"] == "":
        raise ValueError(rec, "screenname",
                         "%s must not be blank! (got: %s)" % ("screenname",repr(rec["screenname"]))
                        )
    # Validate password
    # password typed must equal passwordtwo
    if rec["password"] != rec["passwordtwo"]:
        raise ValueError(rec, "password",
                         "Passwords provided do not match"
                        )
    # password must not be null
    if rec["password"] == "":
        raise ValueError(rec, "password",
                         "Passwords must not be blank!"
                        )

    # Email address must not match any other record in the database
    R = Registrations.read_database()
    uniquefield = "email"
    for r in R:
       if r[uniquefield] == rec[uniquefield]:
           raise ValueError(rec, uniquefield,
                            "Users are are identified as unique by %s - record already exists (got %s)" % (repr(uniquefield), repr(rec[uniquefield]))
                           )

    # Validate month
    if rec["dob.month"] not in [ "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December" ]:
        raise ValueError(rec, 
                         "dob.month",
                         "Month doesn't match options - should be full word, capitalised (got: %s)" % repr(rec["dob.month"])
                        ) 

    # year must not be null
    if rec["dob.year"] == "":
        raise ValueError(rec, "dob.year",
                         "%s must not be blank! (got: %s)" % ("dob.year",repr(rec["dob.year"]))
                        )

    try:
       year = int(rec["dob.year"])
    except ValueError:
        raise ValueError(rec, "dob.year",
                         "%s must parse as an integer! (got: %s)" % ("dob.year",repr(rec["dob.year"]))
                        )

    # Validate day is within range for given month
    m2d = {
         "January" : 31,
         "February" : 28,
         "March" : 31,
         "April": 30,
         "May" : 31,
         "June" : 30,
         "July" : 31,
         "August" : 31,
         "September" : 30,
         "October" : 31,
         "November" : 30,
         "December" : 31
    }
    days = m2d[rec["dob.month"]]
    if (int(rec["dob.year"]) % 4) == 0:
        if days == 28:
            days +=1
     
    # day must not be null
    if rec["dob.day"] == "":
        raise ValueError(rec, "dob.day",
                         "%s must not be blank! (got %s)" % ("dob.day", repr(rec["dob.day"]) )
                        )

    try:
       day = int(rec["dob.day"])
    except ValueError:
        raise ValueError(rec, "dob.day",
                         "%s must parse as an integer! (got: %s)" % ("dob.day",repr(rec["dob.day"]) )
                        )

    if (int(rec["dob.day"]) < 1) or int(rec["dob.day"]) > days:
        raise ValueError(rec,
                         "dob.day",
                         "Day in month falling on a day not in that month? (got: %s %s)" % (repr(rec["dob.day"]), repr(rec["dob.month"]))
                        )

                    
    # "yearage" >= 18
    # FIXME: This is actually excludes many 18 year olds...
    year_age = (time.localtime(time.time())[0] - int(rec["dob.year"]))
    min_age = 18

    if year_age < min_age: 
        raise ValueError(rec, "dob.year",
                         "Year age restriction not met. Must be minimum %d years. (Got: %d, %s)" % (min_age, year_age, repr(rec["dob.year"]))
                        )

    # Application logic validation
    if rec["side"] == "":
        raise ValueError(rec, "side",
                         "'side' is empty - you must pick sides! (Got: %s)" % repr(rec["side"])
                        )

    OKValues = ["eve", "isambard"]
    if rec["side"] not in OKValues:
        raise ValueError(rec, "side",
                         "'side' must be one of the valid values: %s. (Got: %s)" %
                            (repr(OKValues), repr(rec["side"]))
                        )

def reg_new(**argd):
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
    if argd.get("action", "") == "new":
        try:
            R = reg_new(**argd) # This internally validates the record before creating it. This thefore means a possible crash at this point
            return [ 
                     "new",  
                     { "message" : "Thank you for signing up. Just need to confirm your registration now!",
                       "record" : R,
                     }
                   ]

        except ValueError, e:
            try:
                (R, field, Reason) = e.args
            except ValueError:
                raise e
            return [ 
                     "error",  
                     { "message" : Reason,
                       "record" : R,
                       "problemfield" : field,
                     }
                   ]
        # end of action=new ------------------------------------------------------------------------

    if argd.get("action", "") == "dump":
        env = argd.get("__environ__")
        cookie = env["bbc.cookies"].get("sessioncookie",None)
        if cookie:
            try:
                userid = CookieJar.getUser(cookie)
            except CookieJar.NoSuchUser:
               return [ "error",
                 { "message" : "Can't find your registration associated with your cookie"+repr(cookie),
                   "record" : {},
                   "problemfield" : "regid",
                   "setcookies" : {"sessioncookie" : ";path=/"},
                  }
               ]

            try:
                R = Registrations.get_record(userid)
            except IOError: # probably means the db has been deleted/zapped
               CookieJar.wipePairing(cookie, userid)
               return [ "error",
                 { "message" : "Can't find your registration associated with your cookie - maybe it was deleted?",
                   "record" : {},
                   "problemfield" : "regid",
                   "setcookies" : {"sessioncookie" : ";path=/"},
                  }
               ]
                   
                 
        else:
            return [ "error",
                 { "message" : "Can't dump anything since you don't have a session cookie - please try registering :)",
                   "record" : {},
                   "problemfield" : "",                 
                   "setcookies" : {"sessioncookie" : ";path=/"},
                 }
                ]
            
        return [ "error",
                 { "message": "nearly implemented!",# + pprint.pformat(R),
                   "record" : R,
                   "problemfield" : ""
                 }
               ]

    if argd.get("action", "") == "confirmcode":
        if argd.get("regid",None) == None:
             return [ "error",
                      { "Message" : "Sorry, I can't confirm your registration without a registration id",
                        "record" : {},
                        "problemfield" : "regid",
                      }
                    ]

        if argd.get("confirmationcode",None) == None:
             return [ "error",
                      { "Message" : "Sorry, I can't confirm your registration without a confirmation code",
                        "record" : {},
                        "problemfield" : "confirmationcode",
                      }
                    ]
            
        registration = Registrations.get_record(argd.get("regid",""))
        if registration["confirmationcode"] == argd.get("confirmationcode",""):
             registration["confirmed"] = True
             Registrations.store_record(registration)
             cookie = CookieJar.getCookie(argd["regid"])
             
             return [ "confirmed",
                      { "message" : "Thank you for confirming your registration. Your account is now active.",
                        "sessioncookie" : cookie,
                        "record" : registration }
                    ]
        else:
             return [ "error",
                      { "Message" : "There's an error with the confirmation code you're using",
                      }
                    ]
             
        # end of action=confirmcode ------------------------------------------------------------------------

    return [ 
             "__default__",  
             { "message" : "Hello World"+pprint.pformat(argd),
               "record" : {}
             }
           ]

import MailConfirmCode

def MakeHTML( structure ):
    structure[1]["record"]["password"] = "****"
    structure[1]["record"]["passwordtwo"] = "****"

    if structure[0] == "__default__":
        return [], Interstitials.notdirect

    if structure[0] == "new":
        app = "http://%(hostdomain)s/cgi-bin/app/register?action=confirmcode&" % { "hostdomain" : hostdomain }
        app_args =  "regid=%(regid)s&confirmationcode=%(confirmcode)s" % {
                                  "regid" : structure[1]["record"]["regid"],
                                  "confirmcode" : structure[1]["record"]["confirmationcode"],
                           }
        confirm_url = app + app_args

        MailConfirmCode.sendMail( structure[1]["record"]["screenname"],
                                  structure[1]["record"]["email"],
                                  confirm_url,
                                  "The Bicker Manor Team",
                                  "User registration confirmation for 'Bicker Manor'")

        page = Interstitials.registration_success % {
                       "body" : pprint.pformat(structure),
                       "confirmationcode" : structure[1]["record"]["confirmationcode"],
                       "regid"       : structure[1]["record"]["regid"],
                       "email"       : structure[1]["record"]["email"],
                       "screenname"  : structure[1]["record"]["screenname"],
                       "dob.day"     : structure[1]["record"]["dob.day"],
                       "dob.month"   : structure[1]["record"]["dob.month"],
                       "dob.year"    : structure[1]["record"]["dob.year"],
                       "side"        : structure[1]["record"]["side"],
                   }
        return [], page

    if structure[0] == "confirmed":

        sessioncookie = structure[1]["sessioncookie"]
        expirytime = time.gmtime(time.time()+31000000) # approx 1 year
        formatteddate = time.strftime("%a, %d-%b-%Y %H:%M:%S %Z", expirytime)

        headers = [("Set-Cookie", "sessioncookie=%s; path=/; expires=%s"  % ( sessioncookie, formatteddate))]

        return headers, Interstitials.confirmed_template

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
    if 0:
        print "WARNING, running this test will zap your local store"
        print "press return to continue, control-c to not continue"
        raw_input()
    Registrations.Zap("registrations","regid")
    testcases = [
             [ "new", 
                "should succeed",
               "Can create new record in new database",
               {
                  'action' : 'new',
                  'dob.day': '30',
                  'dob.month': 'June',
                  'dob.year': '1980',
                  'email': 'ms@cerenity.org',
                  'password': 'password',
                  'passwordtwo': 'password',
                  'screenname': 'Michael',
                  'side': 'eve',
               }],
             [ "error", 
               "email",
               "Can't recreate same record in existing database",
               {
                  'action' : 'new',
                  'dob.day': '30',
                  'dob.month': 'June',
                  'dob.year': '1980',
                  'email': 'ms@cerenity.org',
                  'password': 'password',
                  'passwordtwo': 'password',
                  'screenname': 'Michael',
                  'side': 'eve',
               }],
             [ "error", 
               "dob.day",
               "Can't create record with bogus day for month",
               {
                  'action' : 'new',
                  'dob.day': '31',
                  'dob.month': 'June',
                  'dob.year': '1980',
                  'email': 'ma@cerenity.org',
                  'password': 'password',
                  'passwordtwo': 'password',
                  'screenname': 'Michael',
                  'side': 'eve',
               }],
             [ "error", 
               "dob.month",
               "Can't create record with bogus month",
               {
                  'action' : 'new',
                  'dob.day': '30',
                  'dob.month': 'June...',
                  'dob.year': '1980',
                  'email': 'ma@cerenity.org',
                  'password': 'password',
                  'passwordtwo': 'password',
                  'screenname': 'Michael',
                  'side': 'eve',
               }],
             [ "error", 
               "dob.year",
               "Can't create user who is younger than 18",
               {
                  'action' : 'new',
                  'dob.day': '30',
                  'dob.month': 'June',
                  'dob.year': '2000',
                  'email': 'ma@cerenity.org',
                  'password': 'password',
                  'passwordtwo': 'password',
                  'screenname': 'Michael',
                  'side': 'eve',
               }],
             [ "error", 
               "email",
               "user's emails must contain an @ as a sanity check on the email",
               {
                  'action' : 'new',
                  'dob.day': '30',
                  'dob.month': 'June',
                  'dob.year': '2000',
                  'email': 'ms at cerenity.org',
                  'password': 'password',
                  'passwordtwo': 'password',
                  'screenname': 'Michael',
                  'side': 'eve',
               }],
             [ "error", 
               "password",
               "Passwords provided by the user must match",
               {
                  'action' : 'new',
                  'dob.day': '30',
                  'dob.month': 'June',
                  'dob.year': '1980',
                  'email': 'ma@cerenity.org',
                  'password': 'password',
                  'passwordtwo': 'passwordtwo',
                  'screenname': 'Michael',
                  'side': 'eve',
               }],
             [ "error", 
               "password",
               "Password must not be null",
               {
                  'action' : 'new',
                  'dob.day': '30',
                  'dob.month': 'June',
                  'dob.year': '1980',
                  'email': 'ma@cerenity.org',
                  'password': '',
                  'passwordtwo': '',
                  'screenname': 'Michael',
                  'side': 'eve',
               }],
             [ "error", 
               "side",
               "User must pick a side",
               {
                  'action' : 'new',
                  'dob.day': '30',
                  'dob.month': 'June',
                  'dob.year': '1980',
                  'email': 'ma@cerenity.org',
                  'password': 'password',
                  'passwordtwo': 'password',
                  'screenname': 'Michael',
                  'side': '',
               }],
             [ "error", 
               "side",
               "User must pick a side which is one of the permitted values",
               {
                  'action' : 'new',
                  'dob.day': '30',
                  'dob.month': 'June',
                  'dob.year': '1980',
                  'email': 'ma@cerenity.org',
                  'password': 'password',
                  'passwordtwo': 'password',
                  'screenname': 'Michael',
                  'side': 'not eve or isambard',
               }],
             [ "__default__", 
                "",
               "If called with a null action, just respond with default behaviour - echo input",
               {
                  'action' : '',
                  'dob.day': '30',
                  'dob.month': 'June',
                  'dob.year': '1980',
                  'email': 'ms@cerenity.org',
                  'password': 'password',
                  'passwordtwo': 'password',
                  'screenname': 'Michael',
                  'side': 'eve',
               }],
             [ "error", 
               "dob.day",
               "Day must not be null",
               {
                  'action' : 'new',
                  'dob.day': '',
                  'dob.month': 'June',
                  'dob.year': '1980',
                  'email': 'ma@cerenity.org',
                  'password': 'password',
                  'passwordtwo': 'password',
                  'screenname': 'Michael',
                  'side': 'eve',
               }],
             [ "error", 
               "dob.month",
               "month must not be null",
               {
                  'action' : 'new',
                  'dob.day': '30',
                  'dob.month': '',
                  'dob.year': '1980',
                  'email': 'ma@cerenity.org',
                  'password': 'password',
                  'passwordtwo': 'password',
                  'screenname': 'Michael',
                  'side': 'eve',
               }],
             [ "error", 
               "dob.year",
               "year must not be null",
               {
                  'action' : 'new',
                  'dob.day': '30',
                  'dob.month': 'June',
                  'dob.year': '',
                  'email': 'ma@cerenity.org',
                  'password': 'password',
                  'passwordtwo': 'password',
                  'screenname': 'Michael',
                  'side': 'eve',
               }],
             [ "error", 
               "dob.year",
               "year must not be a random string",
               {
                  'action' : 'new',
                  'dob.day': '30',
                  'dob.month': 'June',
                  'dob.year': 'hello',
                  'email': 'ma@cerenity.org',
                  'password': 'password',
                  'passwordtwo': 'password',
                  'screenname': 'Michael',
                  'side': 'eve',
               }],
             [ "error", 
               "dob.year",
               "year must be a string representing an integer, not a float",
               {
                  'action' : 'new',
                  'dob.day': '30',
                  'dob.month': 'June',
                  'dob.year': '2007.7',
                  'email': 'ma@cerenity.org',
                  'password': 'password',
                  'passwordtwo': 'password',
                  'screenname': 'Michael',
                  'side': 'eve',
               }],
             [ "error", 
               "dob.day",
               "day must not be a random string",
               {
                  'action' : 'new',
                  'dob.day': '30.3',
                  'dob.month': 'June',
                  'dob.year': '2007',
                  'email': 'ma@cerenity.org',
                  'password': 'password',
                  'passwordtwo': 'password',
                  'screenname': 'Michael',
                  'side': 'eve',
               }],
             [ "error", 
               "dob.day",
               "day must be a string representing an integer, not a float",
               {
                  'action' : 'new',
                  'dob.day': '30.3',
                  'dob.month': 'June',
                  'dob.year': '2007',
                  'email': 'ma@cerenity.org',
                  'password': 'password',
                  'passwordtwo': 'password',
                  'screenname': 'Michael',
                  'side': 'eve',
               }],
             [ "error", 
               "email",
               "email must not be null!",
               {
                  'action' : 'new',
                  'dob.day': '30',
                  'dob.month': 'June',
                  'dob.year': '1980',
                  'email': '',
                  'password': 'password',
                  'passwordtwo': 'password',
                  'screenname': 'Michael',
                  'side': 'eve',
               }],
             [ "error", 
               "screenname",
               "screenname must not be null!",
               {
                  'action' : 'new',
                  'dob.day': '30',
                  'dob.month': 'June',
                  'dob.year': '1980',
                  'email': 'ma@cerenity.org',
                  'password': 'password',
                  'passwordtwo': 'password',
                  'screenname': '',
                  'side': 'eve',
               }],
    ]
    if 0:
            print "RUNNING TEST SUITE"
            print "------------------"
            for testcase in testcases:
                testdata = testcase[-1]
                result = page_logic(None, **testdata)
                print testcase[2],"|",
                assert result[0] == testcase[0], ( "testcase return code mismatch %s != %s" % (repr(result[0]), repr(testcase[0])) )
                if result[0] == "error":
                    assert testcase[1] == result[1]["problemfield"], "Testcase return field mismatch %s %s" % (repr(result[1]["problemfield"]), repr(testcase[1]))
                    print result[1]["message"],"|",
                print "PASSED"

            print "CONFIRMCODE TEST"
            print "----------------"

    Registrations.Zap("registrations","regid")
    userinfo = {
                  'action' : 'new',
                  'dob.day': '30',
                  'dob.month': 'June',
                  'dob.year': '1980',
                  'email': 'ms@cerenity.org',
                  'password': 'password',
                  'passwordtwo': 'password',
                  'screenname': 'Michael',
                  'side': 'eve',
               }
    result = page_logic(None, **userinfo)
    assert result[0] == "new", "New user created"
#    pprint.pprint(result)
#    print MakeHTML(result)
    confirmbundle = {
            "action" :"confirmcode",
            "regid" : result[1]["record"]["regid"],
            "confirmationcode": result[1]["record"]["confirmationcode"],
    }
    print "sending..."
    pprint.pprint( confirmbundle )
    result = page_logic(None, **confirmbundle)
    print
    print "got back..."
    pprint.pprint(result)
    print
    print "Redoing it..."
    result = page_logic(None, **confirmbundle)
    assert result[0] == "confirmed", "Confirmation from the system of success"
    assert result[1]["record"]["confirmed"] , "Record updated to show success"
    assert result[1]["sessioncookie"], "Cookie set"
    print
    print "got back..."
    pprint.pprint(result)
