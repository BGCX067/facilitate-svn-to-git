#!/usr/bin/env python

import os.path

class tagHandler(object):
      def dowikilink(bunch, text, env):
         "w"
         name = text
         name = text.strip()
         tolink = name
         if bunch.get("here", False):
             tolink = bunch.get("here")
         words = tolink.split()
         capitalised_words = [x.capitalize() for x in words ] # Actually not quite right, really want ucfirst, not capitalize
         wikiword = "".join(capitalised_words)
         if not bunch.get("nolink", False):
             return "<a href='%s'>%s</a>" % (wikiword,name )
         else:
             return wikiword

      mapping = {
                 "w" : dowikilink,
      }
      
mapping = tagHandler.mapping

if __name__ == "__main__":
   print "TAG HANDLER", tagHandler
   print "MAPPING", tagHandler.mapping
   print "HMM", tagHandler.mapping["w"]({"location":"bingle"}, "hello world", {})
