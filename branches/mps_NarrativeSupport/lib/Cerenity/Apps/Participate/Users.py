#!/usr/bin/env python5~

import os.path

import Facilitate.CookieJar as CookieJar
from Facilitate.Api import getRegistration, getAllUsers, getRegistrations, getContacts, initApi

initApi("/srv/www/sites/bicker.kamaelia.org/cgi/app/data")

def set_cookie(env, thecookie, value):
    env["context"]["newcookies"][thecookie] = value

loggedout = False

def loggedIn(env):
    if loggedout:
        return False

    cookies = env.get("cookies", None)
    if not cookies:
        return False

    sessioncookie_raw = cookies.get("sessioncookie", None)
    if not sessioncookie_raw:
        return False

    sessioncookie = sessioncookie_raw.value

    try:
        userid = CookieJar.getUser(sessioncookie)
    except CookieJar.NoSuchUser:
        return False

    user = getRegistration(userid)
    if user["confirmed"]:
        return userid
    else:
        return False


class tagHandler(object):

      def doTag(bunch, text, env):
          return """<div class='divide'></div>"""

      def doDumpProfile(bunch, text, env):
          userid = loggedIn(env)
          if userid:
              user = getRegistration(userid)
              return repr(user)
          else:
              return "No Profile"

      def douserid(bunch, text, env):
          userid = loggedIn(env)
          if userid:
              return userid
          else:
              return ""

      def doLoggedIn(bunch, text, env):
          if loggedIn(env):
              return text
          return ""

      def doLoggedOut(bunch, text, env):
          if not loggedIn(env):
             return text
          return ""

      def doscreenname(bunch, text, env):
          userid = loggedIn(env)
          if not userid:
              return "NOT LOGGED IN"
          user = getRegistration(userid)
          return user['screenname']

      def dodob(bunch, text, env):
          userid = loggedIn(env)
          if not userid:
              return ""
          user = getRegistration(userid)
          return user['dob.day']+" "+user['dob.month']+" "+user['dob.year']

      def doparticipateside(bunch, text, env):
          cap = bunch.get("capitalise", False)
          userid = loggedIn(env)
          if not userid:
              return ""
          user = getRegistration(userid)
          if cap:
              return user['side'].capitalize()
          else:
              return user['side']

      def doemail(bunch, text, env):
          userid = loggedIn(env)
          if not userid:
              return ""
          user = getRegistration(userid)
          return user['email']

      def dohandlelogout(bunch, text, env):
          import os
          
          if "logout" in os.environ["QUERY_STRING"]:
              global loggedout
              loggedout = True
              set_cookie(env, "sessioncookie", "")

          return ""

      def doparticipantlist(bunch, text, env):
          participants = getAllUsers()
          formatted_ps = ["<ul>"]

          if loggedIn(env):
              myid = loggedIn(env)
          else:
              myid = None

          for player in participants:
               p = dict(player)
               p["email"] = p["email"][p["email"].find("@")+1:]
               p["me"] = myid
               if myid:
                   if myid == p["regid"]:
                       continue # silly to be able to add self as a contact!
                   rec = "<li> <B>%(screenname)s</b> ( %(email)s ) <a href='/cgi-bin/app/contacts?action=addcontact&contact=%(regid)s&contactof=%(me)s'>Add as contact</a> " % p
               else:
                   rec = "<li> <B>%(screenname)s</b> ( %(email)s ) " % p

               formatted_ps.append( rec )
          formatted_ps.append( "</ul>" )
          player_list = "\n".join( formatted_ps )

          return player_list

      def dofriendslist(bunch, text, env):
          if loggedIn(env):
              myid = loggedIn(env)

              contacts = getContacts(myid)
              if not contacts:
                  return text

              users = ["<ul>"]
              for user in getRegistrations(contacts):
                  user["email"] = user["email"][user["email"].find("@")+1:]
                  users.append( "<li> <B>%(screenname)s</b> ( %(email)s )" % user )
              users.append("</ul>")
              
              return "\n".join(users)
          else:
              return "Sorry, in order to have a contact/friends list, you must be logged in!"


      mapping = {
           "dumpprofile" : doDumpProfile,
           "loggedin" : doLoggedIn,
           "loggedout" : doLoggedOut,
           "screenname" : doscreenname,
           "user.dob" : dodob,
           "user.email" : doemail,
           "participate.side" : doparticipateside,
           "handlelogout" : dohandlelogout,
           "participantlist" : doparticipantlist,
           "friendslist" : dofriendslist,
           "userid" : douserid,
      }

      
mapping = tagHandler.mapping

if __name__ == "__main__":
   print "TAG HANDLER", tagHandler
   print "MAPPING", tagHandler.mapping
   print "HMM", tagHandler.mapping["w"]({"location":"bingle"}, "hello world", {})
