#!/usr/bin/env python


import os.path
class tagHandler(object):
      def doInclude(bunch, text, env):
         """[[include][file=<filename relative to the root>][croptop=<numlines][cropbottom=<numlines>] text]
         Performs much the same function as a #include in C - literally pull in the text
         from another page (technical transcludes) the other page into this one.
         croptop & cropbottoms are partial hacks - they remove the top/bottom
         lines (as many as indicated).

         Included pages also get evaluated."""
#         print "Content-Type: text/plain\n\n"
#         print "BINGLE"
#         print "BINGLE"
#         return "INCLUDE"
         docbase = env["docbase"]
         filename = bunch["file"]
         failtext = bunch.get("failtext","")
         path = os.path.join(docbase,filename)
         try:
            f = open(path)
         except IOError:
            if "%" in failtext:
               pass
            return "File: %s not found" % (bunch["file"])
         else:
            lines = [x for x in f]
            f.close()
         try:
            croptop = bunch["croptop"]
            lines = lines[int(croptop):]
         except KeyError:
            pass
         try:
            cropbottom = bunch["cropbottom"]
            lines = lines[:-int(cropbottom)]
         except KeyError:
            pass

         file = "".join(lines)
         try:
             parseTree = parser(file) ### FIXME - misses out on context
             includeTextGen = evalTree(parseTree)
             includeText = "".join([x for x in includeTextGen])
         except:
             includeText = "ERROR DURING PARSING (" + str(filename)+")"+str(len(lines))
         return includeText + text

      mapping = {
                 "include": doInclude,
      }
      
mapping = tagHandler.mapping

if __name__ == "__main__":
   print "TAG HANDLER", tagHandler
   print "MAPPING", tagHandler.mapping
   
