#!/usr/bin/python
"""
This script handles user registrations
"""

# import md5                          # for hexdigest
# import random                       # for confirmation codes
# import time                         # to check age
# import pprint                       # for dumping errors

import sys
import shutil
import pprint
import CookieJar

from model.Record import EntitySet  # For access to the temporary DB
import Interstitials
basedir = "/srv/www/sites/bicker"


def new_video(**argd):
    rec = {
      # --------------------------------------------------------- Required to create a new record
        "uploaded_file"     : argd.get("uploaded_file",""),
        "unique_name"       : argd.get("unique_name",""),
        "userid"            : argd.get("userid",""),
        "original_filename" : argd.get("original_filename",""),
        "trimmed_filename"  : argd.get("trimmed_filename",""),
    }

    # --------------------------------------------------------- Actual storage
    stored_rec = Videos.new_record(rec)
    return stored_rec

def page_logic(json, **argd):
    env = argd.get("__environ__")
    userid = None
    record = None

    if argd.get("action", "") == "":
        return [ "__default__",
          { "message" : "Sorry, this is not meant to be called directly",
            "record" : {},
            "problemfield" : "regid",
           }
        ]

    if argd.get("action", "") == "upload":
        cookie = env["bbc.cookies"].get("sessioncookie",None)
        if cookie:
            try:
                userid = CookieJar.getUser(cookie)
            except CookieJar.NoSuchUser:
               sys.stderr.write("line 41\n")
               return [ "error",
                 { "message" : "Can't identify you, so not accepting your submission, sorry - try logging out and in again"+repr(cookie),
                   "record" : {},
                   "problemfield" : "regid",
                   "setcookies" : {"sessioncookie" : ";path=/"},
                  }
               ]
        else:
            sys.stderr.write("line 51\n")
            return [ "error",
              { "message" : "Can't identify you, so not accepting your submission, sorry - try logging in or registering!",
                "record" : {},
                "problemfield" : "regid",
                "setcookies" : {"sessioncookie" : ";path=/"},
               }
            ]

        # We now have a valid userid.
        # OK, where's the uploaded data?
        video_file = argd.get("upload.filename.__filename", None)
        original_name = argd.get("upload.filename.__originalfilename", None)
        if (video_file == None) or (original_name == None):
            return [ "error",
              { "message" : "You need to upload a file for this method",
                "record" : argd,
                "problemfield" : "upload.filename",
               }
            ]

#        try:
#            import Video
#            Video.open(video_file)
#        except IOError:
#            return [ "error",
#              { "message" : "Sorry, but that doesn't seem to be an video",
#                "record" : {},
#                "problemfield" : "upload.filename",
#               }
#            ]

        # Data we have right now:
        #
        # We have a valid userid
        # video_file contains a valid filename
        # upload.filename.__originalfilename
        # We know it's not moderated.
        #    - Moderation is being handled by a file moving from a to b to c
        #    - we really ought to have the video filename without the directory name
        trimmed = video_file[video_file.rfind("/")+1:]
        unique = trimmed[:trimmed.rfind(".")]
        record = {
            "uploaded_file": video_file,
            "unique_name": unique,
            "userid" : userid,
            "original_filename" : original_name,
            "trimmed_filename" :  trimmed,
        }
#        try:
#           shutil.copytree(basedir + "/template/videos", 
#                           basedir + "/docs/videos/user/%(unique_name)s" % record )
#        except OSError:
#           pass
        record = new_video(**record)

    return [
             "video_uploadok",
             {
                "message": "Upload Successful",
                "user" : "",
             }
           ]


# import MailConfirmCode

def MakeHTML( structure ):

    sys.stderr.write(pprint.pformat(structure)+"\n")

    if structure[0] == "__default__":
        return [], Interstitials.notdirect

    if structure[0] == "video_uploadok":
        return [], Interstitials.video_uploadok

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

Videos        = EntitySet("videos",        key="videoid")
Registrations = EntitySet("registrations", key="regid")
Contacts      = EntitySet("contacts",      key="contactid")

if __name__ == "__main__":
     pass
