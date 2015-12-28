#!/usr/bin/env python

import os.path

import sys ; sys.path.append("/srv/www/sites/bicker.kamaelia.org/cgi/app/Facilitate")
import CookieJar

from model.Record import EntitySet

EntitySet.data = "/srv/www/sites/bicker.kamaelia.org/cgi/app/data"

Images        = EntitySet("images", key="imageid")
Registrations = EntitySet("registrations", key="regid")
Contacts      = EntitySet("contacts", key="contactid")

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

    user = Registrations.get_record(userid)
    if user["confirmed"]:
        return userid
    else:
        return False

upload_form = """\
<form action="http://bicker.kamaelia.org/cgi-bin/app/images" method="POST"
enctype="multipart/form-data">
<input type="hidden" name="action" value="upload" />

Upload file: <input type="file" name="upload.filename" value="" size="30"/>

<input type="submit" value="submit" />

</form><br>
<b> Please note - after you hit submit the amount of time taken to upload
may be significant - at least a few minutes. For very hi resoultion images,
it may be as much as 10-15 minutes. Please be patient!</b>


"""

class tagHandler(object):
      def doUploadForm(bunch, text, env):
          return upload_form

      def doAllUserImages(bunch, text, env):
          user_images = Images.read_database()
          images = []
          i = 0
          for image in user_images:
              i = i +1
              if i % 4 == 0:
                   image["extra"] = " last"
              else:
                   image["extra"] = ""
              image = """\
<div class='column twoC%(extra)s button'>
<a href="/Picture?image=%(unique_name)s">
<img border="0" src='/images/user/%(unique_name)s/thumb.jpg'>
</a></div>
""" % image
              if i % 4 == 0:
                  image += '<div class="divide"></div>'
              images.append(image)
          return "".join(images)+ '<div class="divide"></div>'

      def doUserImages(bunch, text, env):
          userid = loggedIn(env)
          if userid:
              images = Images.read_database()
              user_images = []
              for image in images:
                  if image["userid"] == userid:
                      user_images.append(image)

              if user_images == []:
                  return "You haven't uploaded any images yet! Why not?"

              Y = [ x["unique_name"] for x in user_images]
              images = []
              i = 0
              for image in user_images:
                  i = i +1
                  if i % 4 == 0:
                       image["extra"] = " last"
                  else:
                       image["extra"] = ""
                  image = """\
<div class='column twoC%(extra)s button'>
<a href="/Picture?image=%(unique_name)s">
<img border="0" src='/images/user/%(unique_name)s/thumb.jpg'>
</a></div>
""" % image
                  if i % 4 == 0:
                      image += '<div class="divide"></div>'
                  images.append(image)
              return "".join(images)+ '<div class="divide"></div>'
              return repr(Y)
          else:
              return "can't give you images, you're not logged in"


      def doFriendsImages(bunch, text, env):
          userid = loggedIn(env)
          if not userid:
              return "Can't show you your friends images - you're not logged in!"

          for rec in Contacts.read_database():
              if rec["contactof"] == userid:
                  break
          else:
              return "Sorry - I can't show you any images from your friends - maybe you haven't added any contacts?"

          # userid contains the user
          # rec["contacts"] contains the list of friend ids.

          images = Images.read_database()
          user_images = []
          for image in images:
              if image["userid"] in rec["contacts"]:
                  user_images.append(image)

          if user_images == []:
              return "Your friends haven't uploaded any images yet! Get them to do something!"
          images = []
          i = 0
          for image in user_images:
              i = i +1
              if i % 4 == 0:
                   image["extra"] = " last"
              else:
                   image["extra"] = ""
              image = """\
<div class='column twoC%(extra)s button'>
<a href="/Picture?image=%(unique_name)s">
<img border="0" src='/images/user/%(unique_name)s/thumb.jpg'>
</a></div>
""" % image
              if i % 4 == 0:
                  image += '<div class="divide"></div>'
              images.append(image)
          return "".join(images)+ '<div class="divide"></div>'

      def doOnePictureViewer(bunch, text, env):
          image = bunch.get("image", text)
          if ".." in "image":
              return ""
          return """\
<div class="divide"></div>
                <div class="column oneC">
                <p> &nbsp;
                </p></div>
                <div class="column sixC lightgrey">
<img src="http://bicker.kamaelia.org/images/user/%(image)s/normal.jpg">
                </div>
                <div class="column last oneC">
                <p> &nbsp;

                </p></div>
<div class="divide"></div>
""" % { "image" : image }

      mapping = {
           "onepictureviewer" : doOnePictureViewer,
           "uploadone_form" : doUploadForm,
           "userimages" : doUserImages,
           "alluserimages" : doAllUserImages,
           "friendsimages" : doFriendsImages,
      }

mapping = tagHandler.mapping

if __name__ == "__main__":
   print "TAG HANDLER", tagHandler
   print "MAPPING", tagHandler.mapping
   print "HMM", tagHandler.mapping["w"]({"location":"bingle"}, "hello world", {})

   if 0:
          if loggedIn(env):
              myid = loggedIn(env)
              for rec in Contacts.read_database():
                  if rec["contactof"] == myid:
                      break
              else:
                  return text

              users = ["<ul>"]
              for contactid in rec["contacts"]:
                  user = Registrations.get_record(contactid)
                  user["email"] = user["email"][user["email"].find("@")+1:]
                  users.append( "<li> <B>%(screenname)s</b> ( %(email)s )" % user )
              users.append("</ul>")
              
              return "\n".join(users)
          else:
              return "Sorry, in order to have a contact/friends list, you must be logged in!"
