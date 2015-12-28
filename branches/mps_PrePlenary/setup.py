#!/usr/bin/env python

from distutils.core import setup

setup(name = "Facilitate",
      version = "0.1.0",
      description = "Facilitate Data Backend",
      author = "Michael Sparks",
      author_email = "ms_@users.sourceforge.net",
      url = "",
      license = "Copyright (c)2008 BBC ... License : ",
      packages = [\
                  "Cerenity",
                  "Cerenity.Apps",
                  "Cerenity.Apps.Participate",
                  "Cerenity.CDML",
                  "Cerenity.CDML.Handlers",
                  "Facilitate",
                  "Facilitate.model",
                  ""],
#      scripts = [ "App/somescript" ],

#      data_files=[ ('/etc', ['Config/facilitate.conf.dist']) ],

      long_description = """
""",
      )

