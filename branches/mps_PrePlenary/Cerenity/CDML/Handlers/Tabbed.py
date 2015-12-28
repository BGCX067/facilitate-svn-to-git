#!/usr/bin/env python

import os.path
import os
class tagHandler(object):

      def doTabs(bunch, text, env):
         """[[tabs] ... ] This is the most complex of the things inside
         cerenity. Please look at the source for the /Miniaxon tutorial
         to see how this works..."""
         tabs = {}
         tabstem = bunch.get("_tabstem", "tab")
         docbase = env["docbase"]
         for key in bunch:
             if key[:3] == tabstem and "_" not in key:
                tab_content = bunch[key]
                try:
                   tab_name = bunch[key+"_name"]
                except KeyError:
                   tab_name = tab_content[:-5]
                tabs[key] = (tab_content, tab_name)
         
         KEYS = str(tabs)
         KEYS = str(env)
         try:
             tabnumber = str(env["context"]["form"][tabstem].value)
         except KeyError:
             tabnumber = ""
#         raise repr(tabnumber)
         try:
            tab = tabs[tabstem+str(tabnumber)]
            tabID = tabstem+str(tabnumber)
         except KeyError:
            tab = tabs[tabstem+"1"]
            tabID = tabstem+"1"
            tabnumber = 1
         KEYS = str(tab)

         #
         # Read Current Tabfile
         #
         Filename  = tab[0]
         path = os.path.join(docbase,Filename)
         try:
            f = open(path)
         except IOError:
            return "Tab File: %s not found" % (Filename)
         else:
            lines = [x for x in f]
            f.close()
         lines = lines[1:-1]

         bodytext = "".join(lines)
         parseTree = parser(bodytext)
         includeTextGen = evalTree(parseTree)
         includeText = "".join([x for x in includeTextGen])
         bodytext = includeText


         header = ["<table width='100%'>"]
         tabkeys = tabs.keys()
         tabkeys.sort()
         for tab in tabkeys:
            tab_text = tabs[tab][1]
            tab_link = " %s " % ( tab )
            request_uri = os.environ["REQUEST_URI"]
            if tab != tabID:
               if tabstem+"="+str(tabnumber) in request_uri:
                  new_tabnumber = tab[3:]
                  request_uri = request_uri.replace(tabstem+"="+str(tabnumber),tabstem+"="+str(new_tabnumber))
               else:
                  if "?" not in request_uri:
                     request_uri = request_uri + "?"+tabstem+"=" + str(tab[3:])
                  else:
                     request_uri = request_uri + "&"+tabstem+"=" + str(tab[3:])
                
            tab_label = "<a href='%s'>%s</a>" % (request_uri, tab_text)
            
            BGCOLOR = bunch.get("inactivetab", "#AAAAAA")
            if tab == tabID: # Current Tab
               BGCOLOR = bunch.get("activetab","#FFFFAA")
            header_item = "<td bgcolor='%s' align='center'><b>%s</b></td>" % (BGCOLOR, tab_label)
            header.append(header_item)
         header.append("</table>")
         HEADER = "".join(header)
         
         if bunch.get("topntail", None) is not None:
            return HEADER + bodytext + HEADER
         
         return HEADER + bodytext

      mapping = {
                 "tabs": doTabs,
      }
      
mapping = tagHandler.mapping

if __name__ == "__main__":
   print "TAG HANDLER", tagHandler
   print "MAPPING", tagHandler.mapping
   
