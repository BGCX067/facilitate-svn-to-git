#!/usr/bin/env python

import os.path

class tagHandler(object):
      def doHTML(bunch, text, env):
         """[[html] <text> ] - Emits <html> tags around the text."""
         return "<html>%s</html>" % text

      def doBODY(bunch, text, env):
         """[[body] <text> ] Emits <body> tags around the text."""
         return "<body>%s</body>" % text
      
      def doLINK(bunch, text, env):
         """[[link] link text] Emits an <a> hyperlink. (Looks buggy infact)"""
         return "<a href='%s'>%s</body>" % text

      def doPRE(bunch, text, env):
         """[[pre] <text> ] Wraps the supplied text in <pre> tags"""
         return "<pre>%s</pre>" % text

      def doTitle(bunch, text, env):
          """[[title] ]Emits the page name"""
          return env["pagename"]

      def doTT(bunch, text, env):
         """[[tt] <text>] - Takes the text and wraps it in <tt> tags"""
         return "<tt>%s</tt>" % text

      def doHref(bunch, text, env):
         """[[href][location=<url>] text ] Makes a hyperlink : <a href='<url>'> text </a>"""
         return "<a href='%s'>%s</a>" % (bunch["location"], text)

      def doAnchor(bunch, text, env):
         """[[anchor][name=<the anchor name>] ] Makes a named anchor. Text inside is ignored/removed."""
         return "<a name='%s'> </a>" % (bunch["name"], )

      def doGroup(bunch, text, env):
         "[[group] puts the text inside the box inside a table with no border ]"
         return "<table width='100%%' border='0'><tr><td>%s</td></tr></table>" % (text)

      def doBoxRight(bunch, text, env):
         """[[boxright] text ] - Create a nice box, and puts it on the right hand side. Everything inside this tag is inside the box"""
#         return "<table width='40%%' border='2' align='right'><tr><td>%s</td></tr></table>" % (text)
         return '</div> <div class="boxright">%s</div><div class="bodytext">' % (text)

      def doOldBoxRight(bunch, text, env):
         "[[oldboxright] <text> ] Puts text is a not so nice box (table, not div) and that goes on the right"
         return "<table width='40%%' border='2' align='right'><tr><td align='centre'>%s</td></tr></table>" % (text)
      
      def doSystemNote(bunch, text, env):
         "[[systemnote] <text> ] If there is a system wide note from the environment, this displays it + the text inside the tag"
         return env.get("systemnote","")+text


      def doImg(bunch, text, env):
         """[[img][align=<arg>][width=<size>][src=<url>] <text>] src is mandatory, rest are optional. Used to insert an image."""
         if bunch.get("align", None) is not None:
            align = " align='%s'" % bunch["align"]
         else:
            align = ""
         if bunch.get("width", None) is not None:
            width = " width='%s'" % bunch["width"]
         else:
            width = ""
         return "<img src='%s'%s%s>%s" % (bunch["src"], align, width,text)
     
      def doScriptUrl(bunch, text, env):
         """[[scripturl] <text>] Dumps out the script's base url + text"""
         return env.get("root", "")+text

      def doPagename(bunch, text, env):
         """[[discuss] ] - Spits out text + a link to a discussion version of the current page. Page -> PageDiscuss"""

         return "%s <a href='%s%s'> %s </a> %s " % (\
                                           "<b> Discussion </b> Please discuss this on",
                                           env.get("root", ""),
                                           env.get("pagename", "XXXXXX")+"Discuss",
                                           "the discussion page",
                                           "for this page")

      mapping = {
                 "group" : doGroup,
                 "img" : doImg,
                 "href": doHref,
                 "html": doHTML,
                 "body": doBODY,
                 "boxright" : doBoxRight,
                 "oldboxright" : doOldBoxRight,
                 "axon.interfacedef" : doBoxRight,
                 "pre" : doPRE,
                 "tt" : doTT,
                 "title" : doTitle,
                 "systemnote": doSystemNote,
                 "discuss" : doPagename,
                 "anchor" : doAnchor,
#                 "scripturl" : doScriptUrl,
      }
      
mapping = tagHandler.mapping

if __name__ == "__main__":
   print "TAG HANDLER", tagHandler
   print "MAPPING", tagHandler.mapping
   print "HMM", tagHandler.mapping["href"]({"location":"bingle"}, "hello world", {})
