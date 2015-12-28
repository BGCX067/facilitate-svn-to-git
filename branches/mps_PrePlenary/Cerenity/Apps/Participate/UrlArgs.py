#!/usr/bin/env python

# import os.path

import os
import cgi

import pprint

def get_url_args(env):
    url_args = env["context"].get("urlargs.urlargs",None)
    if url_args == None:
        qs = os.environ.get("QUERY_STRING", "")

        url_args = cgi.parse_qsl(qs)
        R = {}
        for key,value in url_args:
            R[key] = value

        url_args = R
        env["context"]["urlargs.urlargs"] = url_args

    return url_args


class tagHandler(object):
      def doUrlArgs(bunch, text, env):
          return repr(get_url_args(env))

      def doUrlArg(bunch, text, env):
          url_args = get_url_args(env)
          arg = bunch.get("arg", None)
          if arg == None:
             return "NO ARG REQUESTED"

          if url_args.get(bunch.get("arg", None), None):
              return url_args.get(bunch.get("arg", None), None)
          else:
              return text

      mapping = {
           "urlargs" : doUrlArgs,
           "urlarg" : doUrlArg,
      }

      
mapping = tagHandler.mapping

if __name__ == "__main__":
   print "TAG HANDLER", tagHandler
   print "MAPPING", tagHandler.mapping
   print "HMM", tagHandler.mapping["w"]({"location":"bingle"}, "hello world", {})

