#!/usr/bin/env python

import os.path
class tagHandler(object):
      def doSidebar(bunch, text, env):
         docbase = env["docbase"]
         try:
            filename = bunch["file"]
         except KeyError:
            includeText = "no sidebar"
         else:
             path = os.path.join(docbase,filename)
             f = open(path)
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
             parseTree = parser(file)
             includeTextGen = evalTree(parseTree)
             includeText = "".join([x for x in includeTextGen])
         if bunch.get("layout",None) == "ba":
            return """\
<table border=0>
<tr>
<td width="85%%" valign="top">
%s
</td>
<td valign="top">
%s
</td>
</tr>
</table>
""" % (text,includeText)
         return """\
<table border=0>
<tr>
<td valign="top">
%s
</td>
<td width="85%%" valign="top">
%s
</td>
</tr>
</table>
""" % (includeText, text)

      def _doSidebar(bunch, text, env):
         docbase = env["docbase"]
         try:
            filename = bunch["file"]
         except KeyError:
            includeText = "no sidebar"
         else:
             path = os.path.join(docbase,filename)
             f = open(path)
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
             parseTree = parser(file)
             includeTextGen = evalTree(parseTree)
             includeText = "".join([x for x in includeTextGen])
         if bunch.get("layout",None) == "ba":
            return """\
<div class="sidebar">
%s
</div>
<div class="bodytext">
%s
</div>
""" % (text,includeText)
         return """\
<div class="sidebar">
%s
</div>
<div class="bodytext">
%s
</div>
""" % (includeText, text)
      
      mapping = {
                 "sidebar": _doSidebar,
      }
      
mapping = tagHandler.mapping

if __name__ == "__main__":
   print "TAG HANDLER", tagHandler
   print "MAPPING", tagHandler.mapping
   
