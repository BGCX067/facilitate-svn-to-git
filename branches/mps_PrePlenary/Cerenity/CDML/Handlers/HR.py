#!/usr/bin/env python

import os.path

class tagHandler(object):
      def doHr(bunch, text, env):
         "[[hr] ] - Insert a horizontal rule"
         return "<hr width='100%'>"

      mapping = {
                 "hr": doHr,
      }
      
mapping = tagHandler.mapping

if __name__ == "__main__":
   print "TAG HANDLER", tagHandler
   print "MAPPING", tagHandler.mapping
   
