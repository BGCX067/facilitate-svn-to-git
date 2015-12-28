#!/usr/bin/env python

import os.path

class tagHandler(object):
      def doEnv(bunch, text, env):
         """[[env][var=<which var>][default=<default text] ] Insert the value of an environment variable. If the variable isn't set, return the default value"""
         try:
            variable = bunch["var"]
         except KeyError:
            return "WHICH VARIABLE?"

         try:
            return env[variable]
         except KeyError:
            if bunch.get("default", None) is None:
               return "variable not set"
            else:
               return bunch["default"]

      mapping = {
                 "env": doEnv,
      }
      
mapping = tagHandler.mapping

if __name__ == "__main__":
   print "TAG HANDLER", tagHandler
   print "MAPPING", tagHandler.mapping
   
