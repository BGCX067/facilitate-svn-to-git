#!/usr/bin/env python

import os.path
import Cerenity.CDML.Page

def get_cookie(thecookie, env):
    value = env["cookies"][thecookie].value
    return value

class tagHandler(object):
      def doShowRevision(bunch, text, env):
          "revisions"
          X = Cerenity.CDML.Page._pageVersions(env["pagename"])
          return text + str(X)

      def doShowVersions(bunch, text, env):
          "versions"
          result = []
          linktoself = os.environ.get("REQUEST_URI", "/BrokenLink")
          questionMark = linktoself.find("?")
          if questionMark != -1:
              baselink = linktoself[:linktoself.find("?")]
              result.append( '<a href="%s"> %s </a> ' % (baselink, "current") )
              linktoself = linktoself[:linktoself.find("?")] # linktoself +"?" #+ 
          else:
              result.append( '<a href="%s"> %s </a> ' % (linktoself, "current") )
          X = Cerenity.CDML.Page._pageVersions(env["docbase"], env["pagename"])
          for version in xrange(1, X+1):
              versionlink = "version=%s" % str(version)
              if "?" in linktoself:
                  versionlink = linktoself +"&" + versionlink
              else:
                  versionlink = linktoself +"?" + versionlink
#              raise versionlink
              result.append( '<a href="%s"> %s </a> ' % (versionlink, str(version)) )
          return text + ", ".join(result)

      def linkToVersion(bunch, text, env):
          "versionlink"
          linktoself = os.environ.get("REQUEST_URI", "/BrokenLink")
          version = bunch.get("version", "1")
          versionlink = linktoself + "?" + "version=%s" % str(version)
          return '<a href="%s"> %s </a> ' % (versionlink, text)

      def doLinkToSelf(bunch, text, env):
          "linktoself"
          linktoself = os.environ.get("REQUEST_URI", "/BrokenLink")
          return '<a href="%s"> %s </a> ' % (linktoself, text)

      def versionInfo(bunch, text, env):
          "linktoself"
          X = Cerenity.CDML.Page._pageVersions(env["pagename"])
          editor = Cerenity.CDML.Page._pageEditor(env["pagename"], env["pageversion"])
          userdetails = editor + "UNDEFINED AS YET..."


          raise "NEED TO STORE THE _SAVE/CGI_ DATA AS .txt.META, and add to it the editor name, the status what we know about them, their email and so on - this will mean we can find out lots of versionInformation"
      
          return "Version: " + str(X) + "Last editted by " + userdetails

      mapping = {
                 "revision" : doShowRevision,
                 "versions" : doShowVersions,
                 "linktoself" : doLinkToSelf,
                 "versionlink" : linkToVersion,
                 "versioninfo" : versionInfo,
      }

mapping = tagHandler.mapping

if __name__ == "__main__":
   print "TAG HANDLER", tagHandler
   print "MAPPING", tagHandler.mapping
