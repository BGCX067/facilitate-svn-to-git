#!/usr/bin/env python

import os.path


import sys ; sys.path.append("/srv/www/sites/bicker.kamaelia.org/cgi/app/Facilitate")
import CookieJar

from model.Record import EntitySet

EntitySet.data = "/srv/www/sites/bicker.kamaelia.org/cgi/app/data"

Registrations = EntitySet("registrations", key="regid")
Videos        = EntitySet("videos", key="imageid")

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
<form action="http://bicker.kamaelia.org/cgi-bin/app/videos" method="POST"
enctype="multipart/form-data">
<input type="hidden" name="action" value="upload" />

Upload file: <input type="file" name="upload.filename" value="" size="30"/>

<input type="submit" value="submit" />
</form><br>
<b> Please note - after you hit submit the amount of time taken to upload
may be significant - at least a few minutes, or maybe 15 minutes (or more)
for many video files. Please be patient!</b>
"""

playerscript = """\
<script type="text/javascript" src="/flvplayer/swfobject.js"></script>

<script type="text/javascript">
    var flashvars = {};
                // The following 3 things should change for the content
                flashvars.contentpath = "http://bicker.kamaelia.org/%(path_to_player)s";
                flashvars.video = "%(filename)s";
                flashvars.preview = "%(preview)s";

                // Following needs to change for other sites
                flashvars.playerpath = "http://bicker.kamaelia.org/flvplayer";

                // You could change these. I wouldn't, but you could.
                flashvars.skin = "skin-applestyle.swf";
                flashvars.skincolor = "0xaaddaa";
                flashvars.skinscalemaximum = "1";

                // If you change these, you'll need to change other things
                flashvars.autoscale = "false";
                flashvars.videowidth = "466";
                flashvars.videoheight = "350";

                var params = {};
                        params.scale = "noscale";
                        params.allowfullscreen = "true";
                        params.salign = "tl";

                var attributes = {};
                        attributes.align = "left";

        swfobject.embedSWF("/flvplayer/flvplayer.swf",
                           "videoPlayer",
                           "466", "380",
                           "9.0.28",
                           "/flvplayer/expressInstall.swf",
                           flashvars, params, attributes);
</script>
"""

player = """\
<div class="divide"></div>
        <div  class="column oneC"> &nbsp; </div>
        <div id="videoPlayer" class="column sixC">
            <p>This content requires the Adobe Flash Player.</p>
                <p><a href="http://www.adobe.com/go/getflashplayer"><img src="http://www.adobe.com/images/shared/download_buttons/get_flash_player.gif" alt="Get Adobe Flash player" /></a>
            </p>
        </div>
        <div  class="column oneC"> &nbsp; </div>
<div class="divide"></div>
"""

class tagHandler(object):

      def doUploadForm(bunch, text, env):
          return upload_form

      def doVideoPlayerScript(bunch, text, env):
          return env["context"].get("video.headeritems", "")
          
      def doUserVideos(bunch, text, env):

          userid = loggedIn(env)

          if userid:
              videos = Videos.read_database()
              user_videos = []
              for video in videos:
                  if video["userid"] == userid:
                      user_videos.append(video)
              Y = [ x["unique_name"] for x in user_videos]
              videos = ["<ul>"]
              import pprint
              for video in user_videos:
                  formatted_video = "<li><a href='/VideoPlayer?video=%(unique_name)s'> %(original_filename)s</a>\n" % video
                  videos.append(formatted_video)
              videos.append("</ul>")
              return "".join(videos)+ '<div class="divide"></div>'
          else:
              return "can't give you your videos - you're not logged in!"



      def doVideoPlayer(bunch, text, env):
          args = {
             "path_to_player" : "videos/user/",
             "filename" : bunch.get("video", text)+".flv",
             "preview" : "preview.jpg",
          }
          env["context"]["video.headeritems"] = playerscript % args
          return player

      mapping = {
           "videouploadone_form" : doUploadForm,
           "videoplayerscript" : doVideoPlayerScript,
           "videoplayer" : doVideoPlayer,
           "uservideos" : doUserVideos,
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
